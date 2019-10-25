/*This is to select the number of players from the PLAYER_DATA*/
SELECT T.teamname, count(*) AS "number of players"
FROM PLAYER_DATA P, SPORTS_TEAM T
WHERE T.teamid = p.teamid
GROUP BY T.teamname having  count(*)>2;
