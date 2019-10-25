/* Selecting columns from the PLAYER_DATA using inner join*/
SELECT p.firstname, p.lastname, t.city, t.teamname
FROM PLAYER_DATA p
INNER JOIN 
SPORTS_TEAM t
ON(T.Teamid = p.Teamid);

