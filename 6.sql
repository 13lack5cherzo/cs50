-- lists the names of songs that are by Post Malone.
SELECT DISTINCT s.name
FROM   songs s
WHERE  s.artist_id IN (SELECT a.id
                       FROM   artists a
                       WHERE  a.name LIKE '%POST MALONE%');