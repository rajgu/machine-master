-- 
-- @table: stp_organization_history
-- 
-- Tabela przechowuje informacje o organizacjach, do ktorych nalezala dana STP-a 
-- 

DROP TABLE IF EXISTS stp_organization_history;

CREATE TABLE stp_organization_history (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	stp_id INT NOT NULL,
	organization TEXT REFERENCES TypesOrganizations(Type),
	date TEXT NOT NULL
);
