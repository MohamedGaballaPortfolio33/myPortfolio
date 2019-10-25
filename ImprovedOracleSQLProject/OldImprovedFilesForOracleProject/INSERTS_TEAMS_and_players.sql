/*ISERTING TEAMS DATA INFORMATION USING INSERT INTO COMMAND FOR TABLE SPORTS_TEAM*/
INSERT INTO SPORTS_TEAM(Teamid, City,  TeamName)
VALUES (1, 'Pittsburgh', 'Penguins');

INSERT INTO SPORTS_TEAM(Teamid, City, TeamName)
VALUES(2, 'Miami', 'Dolphins');

INSERT INTO SPORTS_TEAM(Teamid, City, teamName)
VALUES(3, 'San Jose', 'Sharks');

/* PLAYER DATA INFORMATION USING INSERT INTO COMMAND FOR PLAYER_DATA*/

INSERT INTO PLAYER_DATA
(Playerid,firstname,lastname,Teamid,dateofbirth,social)
VALUES (1,'Mike','Schaub',2, TO_DATE('07/05/1978', 'MM/DD/YYYY'),'134-00-9872');

INSERT INTO PLAYER_DATA
(Playerid,firstname,lastname,Teamid,dateofbirth,social)
VALUES (2,'Marci','Rogan',2, TO_DATE('01/09/1985', 'MM/DD/YYYY'),'143-09-6793');

INSERT INTO PLAYER_DATA
(Playerid,firstname,lastname,Teamid,dateofbirth,social)
VALUES (3,'Carl','Fenzila',2,TO_DATE('04/25/1968', 'MM/DD/YYYY'),'009-87-2365');

INSERT INTO PLAYER_DATA
(Playerid,firstname,lastname,Teamid,dateofbirth,social)
VALUES (4,'John','Pomeraina',3, TO_DATE('04/25/1968', 'MM/DD/YYYY'),'128-09-6874');

INSERT INTO PLAYER_DATA
(Playerid,firstname,lastname,Teamid,dateofbirth,social)
VALUES (5,'Anton','Orlovsky',3, TO_DATE('09/10/2001', 'MM/DD/YYYY'),'234-09-9087');

INSERT INTO PLAYER_DATA
(Playerid,firstname,lastname,Teamid,dateofbirth,social)
VALUES (6,'Brian','Portis',1, TO_DATE('07/02/1973', 'MM/DD/YYYY'),'125-09-9988');

INSERT INTO PLAYER_DATA
(Playerid,firstname,lastname,Teamid,dateofbirth)
VALUES (7,'Andrew','Jackson',1, TO_DATE('06/27/2001', 'MM/DD/YYYY'));

