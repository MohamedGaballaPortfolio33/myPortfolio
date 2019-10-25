/*This statement is to let the server to add a new user to the database and set the session to be true*/
alter session set "_ORACLE_SCRIPT"=true;  

/*This query will let the user to be create to the username Leaarning_User2019 and identify by the password learning1234*/
CREATE USER Learner_User2019  IDENTIFIED BY learning1234;

/* GRANT CONNECT will let the user to connect to the username that was created.*/
GRANT CONNECT TO Learner_User2019;

/*Connect the user to the resources and the database*/
GRANT CONNECT,RESOURCE,DBA TO Learner_User2019;

/*Creating a session to grant any privilege to the user*/
GRANT CREATE SESSION,GRANT ANY PRIVILEGE TO Learner_User2019;

/* Let the user to have any tablespace which will let them to have diskspaces.*/
GRANT UNLIMITED TABLESPACE TO Learner_User2019;


