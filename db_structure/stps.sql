-- 
-- @table: stps
-- 
-- Tabela przechowuje informacje o maszynach testowych 
-- 

DROP TABLE IF EXISTS stps;

CREATE TABLE stps (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL UNIQUE,
	board_type TEXT NOT NULL REFERENCES TypesBoardTypes(Type),
	duplex_type TEXT REFERENCES TypesDuplexTypes(Type),
	site TEXT REFERENCES TypesSites(Type),
	worker TEXT,
	customer_organization REFERENCES TypesOrganizations(Type),
	last_update TEXT,
	eris_url TEXT,
	worker_log TEXT,
	type TEXT,
	site_lan_ip TEXT,
	status TEXT
);
