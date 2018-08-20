-- 
-- @table: TypesSites
-- 
-- Tabela przechowuje typy dupleksu dla maszyn testowych 
-- 

DROP TABLE IF EXISTS TypesSites;
CREATE TABLE TypesSites (
	Type TEXT PRIMARY KEY
);

INSERT INTO TypesSites(Type) VALUES ('Bj');
INSERT INTO TypesSites(Type) VALUES ('Ki');
INSERT INTO TypesSites(Type) VALUES ('Ld');
INSERT INTO TypesSites(Type) VALUES ('Li');
INSERT INTO TypesSites(Type) VALUES ('Ot');
INSERT INTO TypesSites(Type) VALUES ('Ln');
INSERT INTO TypesSites(Type) VALUES ('Vu');
