-- list the names of all people who starred in Toy Story
SELECT p.name
FROM   people p
WHERE  p.id IN (SELECT s.person_id
                FROM   stars s
                WHERE  s.movie_id IN (SELECT m.id
                                      FROM   movies m
                                      WHERE  m.title LIKE 'TOY STORY'));

