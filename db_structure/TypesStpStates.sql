-- 
-- @table: TypesStpStates
-- 
-- Tabela przechowuje statusu, w ktorych moze znajdowac sie STP-a 
-- 

DROP TABLE IF EXISTS TypesStpStates;
CREATE TABLE TypesStpStates (
	Type TEXT PRIMARY KEY
);

INSERT INTO TypesStpStates(Type) VALUES ('');
INSERT INTO TypesStpStates(Type) VALUES ('disabled');
INSERT INTO TypesStpStates(Type) VALUES ('disconnected');
INSERT INTO TypesStpStates(Type) VALUES ('offline');
INSERT INTO TypesStpStates(Type) VALUES ('online');
INSERT INTO TypesStpStates(Type) VALUES ('starting');
