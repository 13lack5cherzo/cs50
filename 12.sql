-- list the titles of all movies in which both Johnny Depp and Helena Bonham Carter starred
SELECT m.title
FROM   movies m
WHERE  m.id IN (SELECT s.movie_id
                FROM   stars s
                WHERE  s.person_id IN (SELECT p.id
                                       FROM   people p
                                       WHERE  ( p.name LIKE 'Johnny Depp' )))
       AND m.id IN (SELECT s.movie_id
                    FROM   stars s
                    WHERE  s.person_id IN (SELECT p.id
                                           FROM   people p
                                           WHERE  ( p.name LIKE
                                                    'Helena Bonham Carter'
                                                  )));