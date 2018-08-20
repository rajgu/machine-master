-- 
-- @table: jobs_links
-- 
-- Tabela przechowuje informacje o linkach powiązanych z danym JOB-em 
-- 

DROP TABLE IF EXISTS jobs_links;

CREATE TABLE jobs_links (
	job_id INTEGER NOT NULL,
	key TEXT NOT NULL,
	value TEXT NOT NULL
);
