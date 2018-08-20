-- 
-- @table: alarms
-- 
-- Tabela przechowuje informacje o alarmach 
-- 

DROP TABLE IF EXISTS alarms;

CREATE TABLE alarms (
	id INTEGER PRIMARY KEY,
	stp_id INTEGER,
	date_notice_start TEXT,
	date_notice_end TEXT,
	alarm_id INT,
	event_time TEXT,
	perceived_severity TEXT,
	managed_object_class TEXT,
	managed_object_instance TEXT,
	specific_problem TEXT,
	probable_cause TEXT,
	additional_text TEXT,
	acknowledged_by TEXT,
	acknowledgement_time TEXT,
	acknowledgement_state TEXT,
	system_dn TEXT,
	notification_id INTEGER,
	additional_info TEXT
);
