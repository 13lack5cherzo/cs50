-- returns the average energy of all the songs.
SELECT Sum(energy) / Count(energy) AS average_energy
FROM   songs;