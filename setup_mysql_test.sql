-- This script prepares a MySQL server for the project


-- Check if the database hbnb_test_db exists
SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'hbnb_test_db';

-- If the database doesn't exist, create it
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Check if the user hbnb_test exists
SELECT User FROM mysql.user WHERE User = 'hbnb_test' AND Host = 'localhost';

-- If the user doesn't exist, create it and grant privileges
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant all privileges on hbnb_test_db to hbnb_test
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- Grant SELECT privilege on performance_schema to hbnb_test
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
