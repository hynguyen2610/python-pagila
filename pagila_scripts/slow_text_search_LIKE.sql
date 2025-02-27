-- using LIKE is the classic way, but no optimized
EXPLAIN ANALYZE
SELECT 
    film_id, title 
FROM film 
WHERE title LIKE '%This is a gem%';