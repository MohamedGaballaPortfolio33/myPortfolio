/*This will select and retrieve only the columns of firstname,lastname, and teamname players*/
SELECT p.firstname, p.lastname, t.teamname
FROM PLAYER_DATA p
INNER JOIN 
SPORTS_TEAM t
ON(T.Teamid = p.Teamid);
