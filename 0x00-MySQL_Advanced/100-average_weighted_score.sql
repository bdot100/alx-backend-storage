-- Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.
-- Requirements:
-- Procedure ComputeAverageScoreForUser is taking 1 input:
-- user_id, a users.id value (you can assume user_id is linked to an existing users)

DELIMITER //
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    IN user_id INT
)
BEGIN
  UPDATE users AS U, 
    (SELECT U.id, SUM(score * weight) / SUM(weight) AS weight_avg 
    FROM users AS U
    JOIN corrections as C ON U.id=C.user_id 
    JOIN projects AS P ON C.project_id=P.id 
    GROUP BY U.id)
  AS WA
  SET U.average_score = WA.w_avg 
  WHERE U.id=WA.id;
END;
//
DELIMITER ;
