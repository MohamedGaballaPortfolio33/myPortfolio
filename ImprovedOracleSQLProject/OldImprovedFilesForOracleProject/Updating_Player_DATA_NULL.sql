/*Updating PLAYER_DATA Only if the social is null to 'No Social on File'*/
UPDATE PLAYER_DATA
SET social = 'No Social on File'
WHERE social IS NULL;