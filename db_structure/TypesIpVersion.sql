-- 
-- @table: TypesIpVersion
-- 
-- Tabela przechowuje typy dopuszczalne do uzycia jako typy dostepnych protokolow IP 
-- 

DROP TABLE IF EXISTS TypesIpVersion;
CREATE TABLE TypesIpVersion (
	Type CHAR(1) PRIMARY KEY NOT NULL
);

INSERT INTO TypesIpVersion(Type) VALUES ('4');
INSERT INTO TypesIpVersion(Type) VALUES ('6');
