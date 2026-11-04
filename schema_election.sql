-- ============================================================
-- STUDENT ELECTION - SIMPLE CRUD
-- File 1 of 4 : schema_election.sql
--
-- UNSAON PAG-IMPORT:
--   1. Ablihi ang XAMPP Control Panel
--   2. Pindota ang Start tapad sa MySQL (dapat green)
--   3. Adto sa http://localhost/phpmyadmin
--   4. Pindota ang Import tab
--   5. Pilia kini nga file (schema_election.sql)
--   6. Pindota ang Go
--
-- HUMAN SA IMPORT, makita nimo:
--   Database : school_election_db
--   Table    : candidates
-- ============================================================

-- 1) Mohimo sa database
CREATE DATABASE IF NOT EXISTS retchie;
USE retchie;

-- 2) Papasa sa daan nga table (para fresh ang testing)
DROP TABLE IF EXISTS candidates;

-- 3) Mohimo sa table
CREATE TABLE candidates (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    position_name VARCHAR(50)  NOT NULL
);

-- 4) Sample data (para naay makita sa [2] View)
INSERT INTO candidates (name, position_name) VALUES
('Juan Dela Cruz', 'President'),
('Maria Santos',   'Vice President'),
('Pedro Reyes',    'Secretary');

-- 5) Check kung sakto ang na-import
SHOW TABLES;
SELECT * FROM candidates;

-- ============================================================
-- EXPLANATION SA TABLE
-- ------------------------------------------------------------
-- id            = auto number (1, 2, 3...) -> primary key
-- name          = pangalan sa kandidato
-- position_name = posisyon (President, Vice President, ...)
--
-- ANG CRUD NAA SA PYTHON FILES:
--   Create -> db_election.add_candidate()
--   Read   -> db_election.get_candidates()
--   Update -> db_election.update_candidate()
--   Delete -> db_election.delete_candidate()
-- ============================================================
