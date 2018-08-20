-- 
-- @table: jobs_suites
-- 
-- Tabela przechowuje informacje o suitach przypisanych do danego zadania 
-- 

DROP TABLE IF EXISTS jobs_suites;

CREATE TABLE jobs_suites (
	job_id INTEGER,
	suite TEXT,
	ok INT,
	nok INT,
	skip INT
);
