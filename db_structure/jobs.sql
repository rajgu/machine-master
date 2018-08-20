-- 
-- @table: jobs
-- 
-- Tabela przechowuje informacje o zadaniach 
-- 

DROP TABLE IF EXISTS jobs;

CREATE TABLE jobs (
	id INTEGER PRIMARY KEY,
	event TEXT,
	du TEXT,
	duplex TEXT,
	up TEXT,
	time_test TEXT,
	time_prep TEXT,
	time_utilization TEXT,
	type TEXT,
	inst_type TEXT,
	date_created TEXT,
	date_finished TEXT,
	date_rcm_install TEXT,
	date_started TEXT,
-- JOBS PROPERTIES:
	prop_up TEXT,
	ip_version TEXT REFERENCES TypesIpVersion(Type),
	criteria TEXT,
	priority INT,
	stp TEXT,
	owner INT,
	use_stp TEXT,
	force_install INT
);
