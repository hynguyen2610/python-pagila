-- Select from actor where profile has email contains a
-- Using classicand slow LIKE
SELECT * FROM actor WHERE profile->>'email' LIKE '%a%';

-- Better idea is to create GIN index for profile's email
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX idx_profile_email ON actor USING gin ( (profile->>'email') gin_trgm_ops );
DROP INDEX idx_profile_email;

-- Select from actor where profile has email contains a
-- Using GIN index
SELECT * FROM actor
WHERE profile->>'email' = 'dgarcia@example.net';