-- 
-- @table: jobs_targets
-- 
-- Tabela przechowuje informacje o wymaganiach odpalonego testu 
-- 

DROP TABLE IF EXISTS jobs_targets;

CREATE TABLE jobs_targets (
	job_id INTEGER NOT NULL,
	key TEXT REFERENCES TypesJobTargets(Type),
	value TEXT NOT NULL
);
