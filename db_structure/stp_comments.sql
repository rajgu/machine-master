-- 
-- @table: stp_comments
-- 
-- Tabela przechowuje komentarze dla STP 
-- 

DROP TABLE IF EXISTS stp_comments;

CREATE TABLE stp_comments (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	stp_id INT NOT NULL,
	text TEXT NOT NULL,
	ticket TEXT,
	date TEXT NOT NULL
);
