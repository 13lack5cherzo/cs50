-- list the names of all people who starred in a movie in which Kevin Bacon also starred
SELECT p2.name
FROM   people p2
WHERE  p2.id IN(SELECT DISTINCT s2.person_id
                FROM   stars s2
                WHERE  s2.movie_id IN (SELECT s1.movie_id
                                       FROM   stars s1
                                       WHERE  s1.person_id IN (SELECT p1.id
                                                               FROM   people p1
                                                               WHERE
                                              p1.name LIKE 'Kevin Bacon'
                                              AND p1.birth = 1958)))
       AND p2.name NOT LIKE 'Kevin Bacon';