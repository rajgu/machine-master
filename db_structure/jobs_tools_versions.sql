-- 
-- @table: tools_versions
-- 
-- Tabela przechowuje informacje o wersjach srodowiska (repozytorium/instalatora) uzytych do uruchomienia testu 
-- 

DROP TABLE IF EXISTS jobs_tools_versions;

CREATE TABLE jobs_tools_versions (
	job_id INTEGER NOT NULL,
	key TEXT REFERENCES TypesToolsVersions(Type),
	value TEXT NOT NULL
);
