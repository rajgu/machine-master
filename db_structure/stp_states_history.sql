-- 
-- @table: stp_states_history
-- 
-- Tabela przechowuje informacje o stanach danej STP-y 
-- 

DROP TABLE IF EXISTS stp_states_history;

CREATE TABLE stp_states_history (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	stp_id INT NOT NULL,
	new_state TEXT REFERENCES TypesStpStates(Type),
	locker_id INT DEFAULT NULL,
	date TEXT NOT NULL
);
