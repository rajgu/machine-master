-- 
-- @table: stp_hardware
-- 
-- Tabela przechowuje informacje o sprzecie danej STP-y 
-- 

DROP TABLE IF EXISTS stp_hardware;

CREATE TABLE stp_hardware (
	stp_id INT NOT NULL,
	type TEXT REFERENCES TypesHardwareType(Type),
	name TEXT NOT NULL,
	serial_number TEXT NOT NULL,
	location TEXT NOT NULL
);
