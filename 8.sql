-- lists the names of the songs that feature other artists
SELECT DISTINCT s.name
FROM   songs s
WHERE  name LIKE '%feat.%';