SELECT cluster, COUNT (*) AS count FROM Node GROUP BY cluster ORDER BY count DESC;

SELECT *, COUNT (*) AS count FROM Edge GROUP BY a ORDER BY count DESC;

