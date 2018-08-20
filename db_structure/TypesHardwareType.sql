-- 
-- @table: TypesHardwareType
-- 
-- Tabela przechowuje typy sprzetu podlaczonego do STP 
-- 

DROP TABLE IF EXISTS TypesHardwareType;
CREATE TABLE TypesHardwareType (
	Type TEXT PRIMARY KEY
);

INSERT INTO TypesHardwareType(Type) VALUES ('ctx');
INSERT INTO TypesHardwareType(Type) VALUES ('du');
INSERT INTO TypesHardwareType(Type) VALUES ('duw');
INSERT INTO TypesHardwareType(Type) VALUES ('ru');
INSERT INTO TypesHardwareType(Type) VALUES ('xmu');
