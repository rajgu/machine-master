-- 
-- @table: users
-- 
-- Tabela przechowuje informacje o uzytkownikach systemu 
-- 

DROP TABLE IF EXISTS users;

CREATE TABLE users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	signum TEXT NOT NULL UNIQUE,
	email TEXT
);
