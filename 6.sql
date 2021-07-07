-- determine the average rating of all movies released in 2012
SELECT Sum(r.rating) / Count(r.rating)
FROM   ratings r
WHERE  movie_id IN (SELECT m.id
                    FROM   movies m
                    WHERE  m.year = 2012);