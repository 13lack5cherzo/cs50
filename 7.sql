-- returns the average energy of songs that are by Drake.
SELECT Sum(energy) / Count(energy) AS average_energy
FROM   songs s
WHERE  s.artist_id IN (SELECT a.id
                       FROM   artists a
                       WHERE  a.name LIKE '%DRAKE%');