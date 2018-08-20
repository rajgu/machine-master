-- 
-- @table: stp_owners
-- 
-- Tabela przechowuje powiazanie o wlascicielach danej STP-y 
-- 

DROP TABLE IF EXISTS stp_owners;

CREATE TABLE stp_owners (
	stp_id INT NOT NULL,
	user_id INT NOT NULL
);
