-- 
-- @table: jobs_meta_data
-- 
-- Tabela przechowuje metadane o zadaniach 
-- 

DROP TABLE IF EXISTS jobs_meta_data;

CREATE TABLE jobs_meta_data (
	job_id INTEGER NOT NULL,
	key TEXT NOT NULL,
	value TEXT NOT NULL
);
