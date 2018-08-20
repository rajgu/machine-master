-- 
-- @table: TypesDuplexTypes
-- 
-- Tabela przechowuje typy dupleksu dla maszyn testowych 
-- 

DROP TABLE IF EXISTS TypesDuplexTypes;
CREATE TABLE TypesDuplexTypes (
	Type TEXT PRIMARY KEY
);

INSERT INTO TypesDuplexTypes(Type) VALUES ('');
INSERT INTO TypesDuplexTypes(Type) VALUES ('fdd');
INSERT INTO TypesDuplexTypes(Type) VALUES ('fdd,fdd_3cc');
INSERT INTO TypesDuplexTypes(Type) VALUES ('fdd,fdd_3cc,tdd,tdd_3cc');
INSERT INTO TypesDuplexTypes(Type) VALUES ('fdd,tdd');
INSERT INTO TypesDuplexTypes(Type) VALUES ('tdd');
