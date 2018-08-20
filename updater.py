#!/usr/bin/env python
import os, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/modules/')

from lib.parsers import tgwParser
from lib.parsers import tgrParser
from lib.parsers import alarmParser
from src import Alarm
from src import Stp
from src import Job
from src import Config
from src import DBConnection
from src.db import DBStps
from src.db.DBJobs import DBJobs
from src.helpers import IpExtractor
from src.helpers import Mosheller


config      = Config.Config()
db          = DBConnection.DBConnection(config).connect()

ipExtractor = IpExtractor.IpExtractor(db, config.get('repositories.stp_cfg'))
tgwParse    = tgwParser.tgwParser()
tgrParse    = tgrParser.tgrParser()
alarmParse  = alarmParser.alarmParser()
alarmObj    = Alarm.Alarm(db)
stpObj      = Stp.Stp(db)
jobObj      = Job.Job(db)
DBJobs      = DBJobs(db)
mosheller   = Mosheller.Mosheller(config.get('moshell.command'), config.get('moshell.directory'))

if len(sys.argv) >= 2:
	if sys.argv[1] == 'get_stp_list':
		stpList = tgwParse.getStps('sa_ci')
		for stp in stpList:
			print stp['name']

	else:
		stpName = sys.argv[1]
		print "Adding STP: {0}".format(stpName)
		stpData = tgwParse.getStp(stpName)
		stpData['site_lan_ip'] = ipExtractor.extract(stpData)
		stpObj.save(stpData)
		jobsList = tgrParse.getJobs(stpName, 100)
		jobsIds = map(lambda x: x['id'], jobsList)
		searchedJobs = DBJobs.read({'id' : jobsIds})
		searchedIds = map(lambda x: x['id'], searchedJobs)
		for job in jobsList:
			if int(job['id']) in searchedIds:
				print "Skipping job: {0}".format(job['id'])
				continue
			print "Adding job: {0}".format(job['id'])
			jobData = tgrParse.getJob(job['id'])
			jobObj.save(jobData)

		if stpData['site_lan_ip'] != '':
			print 'Gather moshell data for: {0}'.format(stpData['site_lan_ip'])
			connStatus = mosheller.connect(stpData['site_lan_ip'])
			print "Conn status: {0}".format(connStatus)
			if connStatus:
				alarmData = alarmParse.parse(connStatus)
				if alarmData != type(False):
					alarmObj.save(stpData['name'], alarmData)
