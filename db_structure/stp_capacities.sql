-- 
-- @table: stp_capacities
-- 
-- Tabela przechowuje informacje o parametrach sprzetowej danej STP-y
-- 

DROP TABLE IF EXISTS stp_capacities;

CREATE TABLE stp_capacities (
	stp_id INT NOT NULL,
	key TEXT REFERENCES TypesStpCapacity(Type),
	value TEXT NOT NULL
);
