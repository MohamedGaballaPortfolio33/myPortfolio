/* UPDATING FOR NEW TEAMCOACHES FOR THE REMAINING TEAMS*/
UPDATE SPORTS_TEAM
SET TEAMCOACH = 'Pat Shurmur'
WHERE TEAMID = 4;

UPDATE SPORTS_TEAM
SET TEAMCOACH = 'Travis O Neil'
WHERE TEAMID = 5;

UPDATE SPORTS_TEAM
SET TEAMCOACH = 'Matthew Perez'
WHERE TEAMID = 6;

/*ADDING THE TEAMCOACHES TO THEIR PLAYERS*/
UPDATE PLAYER_DATA
SET TEAMCOACH = 'SCOTT RUSSEL'
WHERE TEAMID = 3;
UPDATE PLAYER_DATA
SET TEAMCOACH = 'Pat Shurmur'
WHERE TEAMID = 4;

UPDATE PLAYER_DATA
SET TEAMCOACH = 'Travis O Neil'
WHERE TEAMID = 5;

UPDATE PLAYER_DATA
SET TEAMCOACH = 'Matthew Perez'
WHERE TEAMID = 6;



