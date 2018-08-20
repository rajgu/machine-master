-- 
-- @table: stp_misc
-- 
-- Tabela przechowuje dodatkowe informacje o STP-ach
-- 

DROP TABLE IF EXISTS stp_misc;

CREATE TABLE stp_misc (
	stp_id INT NOT NULL,
	key TEXT NOT NULL,
	value TEXT NOT NULL
);
