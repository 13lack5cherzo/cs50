-- list the names of all people who have directed a movie that received a rating of at least 9.0
SELECT DISTINCT p.name
FROM   people p
WHERE  p.id IN (SELECT d.person_id
                FROM   directors d
                WHERE  movie_id IN (SELECT r.movie_id
                                    FROM   ratings r
                                    WHERE  rating >= 9.0));