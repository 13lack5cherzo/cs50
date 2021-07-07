-- list the names of the top 5 longest songs, in descending order of length
SELECT DISTINCT name
FROM   songs
ORDER  BY duration_ms DESC
LIMIT  5;