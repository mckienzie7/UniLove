DROP DATABASE IF EXISTS UniLove_db;
SHOW DATABASES;



CREATE  DATABASE IF NOT EXISTS UniLove_db;
CREATE USER IF NOT EXISTS 'ULAdmin'@'localhost';
SET PASSWORD FOR 'ULAdmin'@'localhost' = '12qwaszx@Q';
GRANT ALL ON UniLove_db.* TO 'ULAdmin'@'localhost';
GRANT SELECT ON performance_schema.* TO 'ULAdmin'@'localhost';
FLUSH PRIVILEGES;