SELECT cluster, AVG(syll), AVG(stress) FROM Node GROUP BY cluster;

SELECT *, COUNT (*) FROM Edge GROUP BY a ORDER BY a;