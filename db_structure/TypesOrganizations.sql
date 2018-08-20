-- 
-- @table: TypesOrganizations
-- 
-- Tabela przechowuje nazwy wszystkich dostepnych organizacji 
-- 

DROP TABLE IF EXISTS TypesOrganizations;
CREATE TABLE TypesOrganizations (
	Type TEXT PRIMARY KEY
);

INSERT INTO TypesOrganizations(Type) VALUES ('');
INSERT INTO TypesOrganizations(Type) VALUES ('bbi');
INSERT INTO TypesOrganizations(Type) VALUES ('bid');
INSERT INTO TypesOrganizations(Type) VALUES ('capacity');
INSERT INTO TypesOrganizations(Type) VALUES ('dt');
INSERT INTO TypesOrganizations(Type) VALUES ('eliot');
INSERT INTO TypesOrganizations(Type) VALUES ('fasttrack_dc');
INSERT INTO TypesOrganizations(Type) VALUES ('g2_grat');
INSERT INTO TypesOrganizations(Type) VALUES ('g2_lrat');
INSERT INTO TypesOrganizations(Type) VALUES ('g2_nodeci');
INSERT INTO TypesOrganizations(Type) VALUES ('g2_tcu');
INSERT INTO TypesOrganizations(Type) VALUES ('g2_wrat');
INSERT INTO TypesOrganizations(Type) VALUES ('itte');
INSERT INTO TypesOrganizations(Type) VALUES ('l1_ebt');
INSERT INTO TypesOrganizations(Type) VALUES ('l2_ebt');
INSERT INTO TypesOrganizations(Type) VALUES ('lnedc');
INSERT INTO TypesOrganizations(Type) VALUES ('lrat_ci');
INSERT INTO TypesOrganizations(Type) VALUES ('lte_sim');
INSERT INTO TypesOrganizations(Type) VALUES ('mbb');
INSERT INTO TypesOrganizations(Type) VALUES ('mct');
INSERT INTO TypesOrganizations(Type) VALUES ('pd_cat');
INSERT INTO TypesOrganizations(Type) VALUES ('pd_radio');
INSERT INTO TypesOrganizations(Type) VALUES ('pd_tc');
INSERT INTO TypesOrganizations(Type) VALUES ('performance');
INSERT INTO TypesOrganizations(Type) VALUES ('pir_saci');
INSERT INTO TypesOrganizations(Type) VALUES ('plm');
INSERT INTO TypesOrganizations(Type) VALUES ('qa_func');
INSERT INTO TypesOrganizations(Type) VALUES ('rcs_mw');
INSERT INTO TypesOrganizations(Type) VALUES ('robustness_ms');
INSERT INTO TypesOrganizations(Type) VALUES ('sa_ci');
INSERT INTO TypesOrganizations(Type) VALUES ('stability');
INSERT INTO TypesOrganizations(Type) VALUES ('sv_capacity');
INSERT INTO TypesOrganizations(Type) VALUES ('sv_eup');
INSERT INTO TypesOrganizations(Type) VALUES ('sv_oam');
INSERT INTO TypesOrganizations(Type) VALUES ('sv_stab');
INSERT INTO TypesOrganizations(Type) VALUES ('svupgrade');
INSERT INTO TypesOrganizations(Type) VALUES ('tem');
INSERT INTO TypesOrganizations(Type) VALUES ('unknown');
INSERT INTO TypesOrganizations(Type) VALUES ('upcul_ebt');
INSERT INTO TypesOrganizations(Type) VALUES ('xft_AI');
