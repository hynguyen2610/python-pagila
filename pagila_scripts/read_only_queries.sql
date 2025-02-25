-- Query full name from pagila db
EXPLAIN ANALYZE 
SELECT DISTINCT CONCAT(first_name, ' ', last_name) AS full_name
FROM actor;

EXPLAIN ANALYZE
SELECT CONCAT(a.first_name, ' ', a.last_name) AS full_name from actor a
GROUP BY full_name

-- Query full_name but in a loop, and don't care about reading result
DO $$ 
DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    total_time INTERVAL := '0s';
    avg_time INTERVAL;
    i INTEGER;
BEGIN
    FOR i IN 1..10 LOOP
        start_time := clock_timestamp();
        
        -- Your query goes here
        PERFORM CONCAT(first_name, ' ', last_name) FROM actor;
        
        end_time := clock_timestamp();
        total_time := total_time + (end_time - start_time);
    END LOOP;
    
    avg_time := total_time / 10;
    
    RAISE NOTICE 'Average execution time: %', avg_time;
END $$;

-- Query not repeated last name
SELECT 
	a.last_name, COUNT(a.last_name)
FROM actor a
WHERE
	a.last_name = ''
GROUP BY
	a.last_name
HAVING COUNT(a.last_name) < 2	

SELECT 
	a.last_name, COUNT(a.last_name)
FROM actor a
WHERE
	a.last_name = ''
GROUP BY
	a.last_name
HAVING COUNT(a.last_name) < 2	

-- Quey by firt_name Orphan
SELECT * FROM actor WHERE first_name = 'Orphan'
SELECT * FROM actor WHERE last_name = ''
SELECT * FROM actor WHERE last_name = null

--Query for repeated ( > 1) last_name, subquery is less efficiency
SELECT 
	a.last_name, COUNT(a.last_name)
FROM actor a
WHERE a.last_name NOT IN (

	SELECT 
		a.last_name, COUNT(a.last_name)
	FROM actor a
	GROUP BY a.last_name
	HAVING COUNT(a.last_name) > 1
-- Query actors who have NO movies
--1. Use sub query
SELECT * FROM actor a
WHERE a.actor_id NOT IN (
SELECT 
	actor_id 
FROM
	film_actor)

--2. Use JOIN
SELECT a.actor_id, fa.film_id 
FROM 
	actor a
	LEFT JOIN
	film_actor fa
	ON
		a.actor_id = fa.actor_id
GROUP BY
	a.actor_id, fa.film_id
HAVING
	fa.film_id IS NULL
		
EXPLAIN ANALYZE
SELECT a.actor_id, a.first_name, a.last_name, fa.film_id
FROM actor a
LEFT JOIN film_actor fa
ON a.actor_id = fa.actor_id
WHERE fa.actor_id IS NULL;

-- select actors who joined a film X
SELECT a.actor_id, a.first_name, a.last_name, fa.film_id
FROM actor a
 JOIN film_actor fa
ON a.actor_id = fa.actor_id
WHERE fa.film_id = 1

-- select actors who DID NOT joined a film X
SELECT a.actor_id, a.first_name, a.last_name, fa.film_id
FROM 
	actor a
	LEFT JOIN 
	film_actor fa
	ON a.actor_id = fa.actor_id
WHERE a.actor_id > 5000

		
select * from film_actor WHERE film_id = 612

select * from actor where actor_id > 333

select count(*) from film_actor

select * from film f  join inventory i
ON f.film_id = i.film_id

SELECT * FROM inventory WHERE film_id IS NULL;
SELECT * FROM film WHERE film_id IS NULL;

SELECT f.*, i.*
FROM film f
INNER JOIN inventory i ON f.film_id = i.film_id;

-- List columns of the film table
SELECT column_name FROM information_schema.columns WHERE table_name = 'film';

-- List columns of the inventory table
SELECT column_name FROM information_schema.columns WHERE table_name = 'inventory';

-- Average runtime of films by category
SELECT c.category_id, c.name, AVG(f.rental_rate)
FROM
	film f
	JOIN
	film_category fc
	ON
	fc.film_id = f.film_id
	JOIN
	category c
	ON
	fc.category_id = c.category_id
GROUP BY
	c.category_id
HAVING
	2.5 < AVG(f.rental_rate) AND AVG(f.rental_rate) < 3


SELECT c.category_id, c.name, AVG(f.rental_rate)
FROM
	film f
	JOIN
	film_category fc
	ON
	fc.film_id = f.film_id
	JOIN
	category c
	ON
	fc.category_id = c.category_id
GROUP BY
	c.category_id
HAVING
	2.5 < AVG(f.rental_rate) AND AVG(f.rental_rate) < 3
