-- 
-- @table: TypesToolsVersions
-- 
-- Tabela przechowuje typy dopuszczalne do uzycia jako wersje narzedzi
-- 

DROP TABLE IF EXISTS TypesToolsVersions;
CREATE TABLE TypesToolsVersions (
	Type TEXT PRIMARY KEY NOT NULL
);

INSERT INTO TypesToolsVersions(Type) VALUES ('prep-ctx');
INSERT INTO TypesToolsVersions(Type) VALUES ('prep-stp_cfg');
INSERT INTO TypesToolsVersions(Type) VALUES ('prep-rcm');
INSERT INTO TypesToolsVersions(Type) VALUES ('prep-test_bundle');
INSERT INTO TypesToolsVersions(Type) VALUES ('prep-gte');
INSERT INTO TypesToolsVersions(Type) VALUES ('prep-user_defined_gte');
INSERT INTO TypesToolsVersions(Type) VALUES ('prep-uctool');
INSERT INTO TypesToolsVersions(Type) VALUES ('prep-ltesim');
INSERT INTO TypesToolsVersions(Type) VALUES ('test-gte');
INSERT INTO TypesToolsVersions(Type) VALUES ('test-test_bundle');
INSERT INTO TypesToolsVersions(Type) VALUES ('test-stp_cfg');
INSERT INTO TypesToolsVersions(Type) VALUES ('test-testjar');
INSERT INTO TypesToolsVersions(Type) VALUES ('test-user_defined_gte');
INSERT INTO TypesToolsVersions(Type) VALUES ('test-uctool');
INSERT INTO TypesToolsVersions(Type) VALUES ('test-ltesim');
INSERT INTO TypesToolsVersions(Type) VALUES ('vm_cfg-tgf');
