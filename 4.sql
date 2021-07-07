-- lists the names of any songs that have danceability, energy, and valence greater than 0.75.
SELECT DISTINCT name
FROM   songs
WHERE  ( danceability > 0.75 ) & ( energy > 0.75 ) & ( valence > 0.75 );