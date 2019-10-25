/* Selecting all null values from PLAYER_DATA*/
SELECT Playerid, firstname, lastname, Teamid, dateofbirth, social
FROM PLAYER_DATA 
WHERE social is NULL;