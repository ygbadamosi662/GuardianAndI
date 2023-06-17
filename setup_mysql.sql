-- Creates a MySQL server with:
--   Database gi_dev_db.
--   User gi_dev with password gandi in localhost.
--   Grants all privileges for gi_dev on gi_dev_db.
--   Grants SELECT privilege for gi_dev on performance_schema.

CREATE DATABASE IF NOT EXISTS gi_dev_db;
CREATE USER
    IF NOT EXISTS 'gi_dev'@'localhost'
    IDENTIFIED BY 'gandi';
GRANT ALL PRIVILEGES
   ON `gi_dev_db`.*
   TO 'gi_dev'@'localhost'
   IDENTIFIED BY 'gandi';
GRANT SELECT
   ON `performance_schema`.*
   TO 'gi_dev'@'localhost'
   IDENTIFIED BY 'gandi';
FLUSH PRIVILEGES;