#!/usr/bin/env python2
import logging

from src.db.DBJobs import DBJobs
from src.db.DBJobsToolsVersions import DBJobsToolsVersions
from src.db.DBJobsTargets import DBJobsTargets
from src.db.DBJobsMetaData import DBJobsMetaData
from src.db.DBJobsSuites import DBJobsSuites
from src.db.DBJobsLinks import DBJobsLinks
from src.db.DBUsers import DBUsers
from src.helpers.DateHelper import DateHelper


class Job:

    _jobProperties = ['up', 'ip_version', 'criteria', 'priority', 'stp', 'owner', 'use_stp', 'force_install']

    def __init__(self, db):
        self.db                  = db
        self.DBJobs              = DBJobs(db)
        self.DBJobsToolsVersions = DBJobsToolsVersions(db)
        self.DBJobsTargets       = DBJobsTargets(db)
        self.DBJobsMetaData      = DBJobsMetaData(db)
        self.DBJobsSuites        = DBJobsSuites(db)
        self.DBJobsLinks         = DBJobsLinks(db)
        self.DBUsers             = DBUsers(db)
        self.DateHelper          = DateHelper()


    def save(self, jobData):

        if not jobData:
            raise Exception ("No job Data to save")
        if not 'id' in jobData:
            raise Exception ("Trying to save JOB without id")

        oldCommit = self.db.getAutocommit()
        self.db.setAutocommit(False)

        jobId = jobData['id']

        existingJob = self.DBJobs.read({'id' : jobData['id']})

        if existingJob:
            self.DBJobsToolsVersions.delete({'job_id' : jobId})
            self.DBJobsTargets.delete({'job_id' : jobId})
            self.DBJobsMetaData.delete({'job_id' : jobId})
            self.DBJobsSuites.delete({'job_id' : jobId})
            self.DBJobsLinks.delete({'job_id' : jobId})

            self.DBJobs.update({
                'id'               : jobData['id'].strip(),
                'event'            : jobData['event'].strip(),
                'du'               : jobData['du'].strip(),
                'duplex'           : jobData['duplex'].strip(),
                'up'               : jobData['up'].strip(),
                'time_test'        : jobData['time_test'].strip() if 'time_test' in  jobData else '',
                'time_prep'        : jobData['time_prep'].strip() if 'time_prep' in  jobData else '',
                'time_utilization' : jobData['time_utilization'].strip() if 'time_utilization' in  jobData else '',
                'type'             : jobData['type'].strip(),
                'inst_type'        : jobData['inst_type'].strip(),
                'date_created'     : jobData['date_created'].strip() if 'date_created' in  jobData else '',
                'date_finished'    : jobData['date_finished'].strip() if 'date_finished' in  jobData else '',
                'date_rcm_install' : jobData['date_rcm_install'].strip() if 'date_rcm_install' in  jobData else '',
                'date_started'     : jobData['date_started'].strip() if 'date_started' in jobData else '',

                'prop_up'          : jobData['job_properties']['up'].strip() if 'up' in jobData['job_properties'] else '',
                'ip_version'       : jobData['job_properties']['ip_version'].strip() if 'ip_version' in jobData['job_properties'] else '',
                'criteria'         : jobData['job_properties']['criteria'].strip() if 'criteria' in jobData['job_properties'] else '',
                'priority'         : jobData['job_properties']['priority'].strip() if 'priority' in jobData['job_properties'] else '',
                'stp'              : jobData['job_properties']['stp'].strip() if 'stp' in jobData['job_properties'] else '',
                'owner'            : jobData['job_properties']['owner'].strip() if 'owner' in jobData['job_properties'] else '',
                'use_stp'          : jobData['job_properties']['use_stp'].strip() if 'use_stp' in jobData['job_properties'] else '',
                'force_install'    : jobData['job_properties']['force_install'].strip() if 'force_install' in jobData['job_properties'] else '',
            }, {'id' : jobId})

        else:

            self.DBJobs.create({
                'id'               : jobData['id'].strip(),
                'event'            : jobData['event'].strip(),
                'du'               : jobData['du'].strip(),
                'duplex'           : jobData['duplex'].strip(),
                'up'               : jobData['up'].strip(),
                'time_test'        : jobData['time_test'].strip() if 'time_test' in  jobData else '',
                'time_prep'        : jobData['time_prep'].strip() if 'time_prep' in  jobData else '',
                'time_utilization' : jobData['time_utilization'].strip() if 'time_utilization' in  jobData else '',
                'type'             : jobData['type'].strip(),
                'inst_type'        : jobData['inst_type'].strip(),
                'date_created'     : jobData['date_created'].strip() if 'date_created' in  jobData else '',
                'date_finished'    : jobData['date_finished'].strip() if 'date_finished' in  jobData else '',
                'date_rcm_install' : jobData['date_rcm_install'].strip() if 'date_rcm_install' in  jobData else '',
                'date_started'     : jobData['date_started'].strip() if 'date_started' in jobData else '',

                'prop_up'          : jobData['job_properties']['up'].strip() if 'up' in jobData['job_properties'] else '',
                'ip_version'       : jobData['job_properties']['ip_version'].strip() if 'ip_version' in jobData['job_properties'] else '',
                'criteria'         : jobData['job_properties']['criteria'].strip() if 'criteria' in jobData['job_properties'] else '',
                'priority'         : jobData['job_properties']['priority'].strip() if 'priority' in jobData['job_properties'] else '',
                'stp'              : jobData['job_properties']['stp'].strip() if 'stp' in jobData['job_properties'] else '',
                'owner'            : jobData['job_properties']['owner'].strip() if 'owner' in jobData['job_properties'] else '',
                'use_stp'          : jobData['job_properties']['use_stp'].strip() if 'use_stp' in jobData['job_properties'] else '',
                'force_install'    : jobData['job_properties']['force_install'].strip() if 'force_install' in jobData['job_properties'] else '',
            })

        if 'suites' in jobData and jobData['suites'] and len(jobData['suites']) > 0:
            suites = jobData['suites']
            for index in range(len(suites)):
                suites[index]['job_id'] = jobId
            self.DBJobsSuites.create(suites)

        if 'job_tools_versions' in jobData and jobData['job_tools_versions']:
            job_tools_versions = jobData['job_tools_versions']
            job_tools_versions['job_id'] = jobId
            self.DBJobsToolsVersions.create(job_tools_versions)

        if 'job_target' in jobData and jobData['job_target']:
            job_target = jobData['job_target']
            job_target['job_id'] = jobId
            self.DBJobsTargets.create(job_target)

        if 'meta_data' in jobData and jobData['meta_data']:
            meta_data = jobData['meta_data']
            meta_data['job_id'] = jobId
            self.DBJobsMetaData.create(meta_data)

        if 'links' in jobData and jobData['links']:
            links = jobData['links']
            links['job_id'] = jobId
            self.DBJobsLinks.create(links)

        # Dodajemy uzytkownika, jako wlasciciela JOB-a, jezeli musimy
        if 'job_properties' in jobData and 'owner' in jobData['job_properties'] and jobData['job_properties']['owner'] != '':
            users = self.DBUsers.read({'signum' : jobData['job_properties']['owner']})
            if len(users) == 0:
                self.DBUsers.create({'signum' : jobData['job_properties']['owner']})

        if oldCommit:
            self.db.commit()

        self.db.setAutocommit(oldCommit)


    def load(self, jobSearchData):

        jobData = False
        if 'id' in jobSearchData:
            jobData = self.DBJobs.read({'id' : jobSearchData['id']})

        if not jobData:
            return False

        jobData = jobData[0]
        jobId = jobData['id']

        tool_versions = self.DBJobsToolsVersions.read({'job_id' : jobId})
        if tool_versions:
            del tool_versions[0]['job_id']
            jobData['tool_versions'] = tool_versions[0]

        job_targets = self.DBJobsTargets.read({'job_id' : jobId})
        if job_targets:
            del job_targets[0]['job_id']
            jobData['job_targets'] = job_targets[0]

        meta_data = self.DBJobsMetaData.read({'job_id' : jobId})
        if meta_data:
            del meta_data[0]['job_id']
            jobData['meta_data'] = meta_data[0]

        suites = self.DBJobsSuites.read({'job_id' : jobId})
        if suites:
            for i in range(len(suites)):
                del suites[i]['job_id']
            jobData['suites'] = suites

        job_links = self.DBJobsLinks.read({'job_id' : jobId})
        if job_links:
            del job_links[0]['job_id']
            jobData['job_links'] = job_links[0]

        return jobData



    def remove(self, jobSearchData):

        jobData = False
        if 'id' in jobSearchData:
            jobData = self.DBJobs.read({'id' : jobSearchData['name']})

        if not jobData:
            raise Exception("Could not find job to deletion, search data: {0}".format(jobSearchData))

        oldCommit = self.db.getAutocommit()
        self.db.setAutocommit(False)

        jobId = jobData[0]['id']

        self.DBJobs.delete({'id' : jobId})
        self.DBJobsToolsVersions.delete({'id' : jobId})
        self.DBJobsTargets.delete({'id' : jobId})
        self.DBJobsMetaData.delete({'id' : jobId})
        self.DBJobsSuites.delete({'id' : jobId})
        self.DBJobsLinks.delete({'id' : jobId})

        if oldCommit:
            self.db.commit()

        self.db.setAutocommit(oldCommit)

