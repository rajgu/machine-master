-- 
-- @table: TypesJobTargets
-- 
-- Tabela przechowuje typy dopuszczalne do uzycia jako wymagania dla tabeli jobs_targets 
-- 

DROP TABLE IF EXISTS TypesJobTargets;
CREATE TABLE TypesJobTargets (
	Type TEXT PRIMARY KEY NOT NULL
);

INSERT INTO TypesJobTargets(Type) VALUES ('apc_pool');
INSERT INTO TypesJobTargets(Type) VALUES ('bait');
INSERT INTO TypesJobTargets(Type) VALUES ('band');
INSERT INTO TypesJobTargets(Type) VALUES ('cascaded');
INSERT INTO TypesJobTargets(Type) VALUES ('cells');
INSERT INTO TypesJobTargets(Type) VALUES ('cloud');
INSERT INTO TypesJobTargets(Type) VALUES ('config');
INSERT INTO TypesJobTargets(Type) VALUES ('ct10');
INSERT INTO TypesJobTargets(Type) VALUES ('du');
INSERT INTO TypesJobTargets(Type) VALUES ('duplex');
INSERT INTO TypesJobTargets(Type) VALUES ('enm');
INSERT INTO TypesJobTargets(Type) VALUES ('equipment');
INSERT INTO TypesJobTargets(Type) VALUES ('feature');
INSERT INTO TypesJobTargets(Type) VALUES ('flow');
INSERT INTO TypesJobTargets(Type) VALUES ('ngr');
INSERT INTO TypesJobTargets(Type) VALUES ('noofenb');
INSERT INTO TypesJobTargets(Type) VALUES ('org');
INSERT INTO TypesJobTargets(Type) VALUES ('oss');
INSERT INTO TypesJobTargets(Type) VALUES ('owner');
INSERT INTO TypesJobTargets(Type) VALUES ('pool');
INSERT INTO TypesJobTargets(Type) VALUES ('psu');
INSERT INTO TypesJobTargets(Type) VALUES ('radiodots');
INSERT INTO TypesJobTargets(Type) VALUES ('rru');
INSERT INTO TypesJobTargets(Type) VALUES ('ru');
INSERT INTO TypesJobTargets(Type) VALUES ('scenario');
INSERT INTO TypesJobTargets(Type) VALUES ('site');
INSERT INTO TypesJobTargets(Type) VALUES ('solution');
INSERT INTO TypesJobTargets(Type) VALUES ('standard');
INSERT INTO TypesJobTargets(Type) VALUES ('stpname');
INSERT INTO TypesJobTargets(Type) VALUES ('testspec');
INSERT INTO TypesJobTargets(Type) VALUES ('tma');
INSERT INTO TypesJobTargets(Type) VALUES ('trust_anchor');
INSERT INTO TypesJobTargets(Type) VALUES ('trx');
INSERT INTO TypesJobTargets(Type) VALUES ('ue');
INSERT INTO TypesJobTargets(Type) VALUES ('up');
INSERT INTO TypesJobTargets(Type) VALUES ('upgrade');
INSERT INTO TypesJobTargets(Type) VALUES ('xmu03');
