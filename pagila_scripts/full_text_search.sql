-- Create tsv (Tabbed Separated Values) for description, this will be used for full text search
-- There are GIN and GiST, GIN is better for full text search, Gist is better for spatial search, like Maps

-- Create tsv column desciption_tsv from existing column description
ALTER TABLE film ADD COLUMN description_tsv tsvector;
UPDATE film SET description_tsv = to_tsvector(description);

-- Look for film with description having "This is a gem", actually using separated words
SELECT 
    * 
FROM film 
WHERE description_tsv @@ to_tsquery('This | gem');

-- For literally phases
SELECT * 
FROM film
WHERE tsv @@ plainto_tsquery('is the feedback');

SELECT * 
FROM film
WHERE description_tsv @@ plainto_tsquery('\"This is a gem\"');

-- What if we combine two above?
SELECT * 
FROM film
WHERE 
    description_tsv @@ to_tsquery('This | gem')
    AND
    tsv @@ plainto_tsquery('is the feedback');


