import pexpect
import logging


class Mosheller:


    def __init__(self, moCommand, moDir):
        self.moCommand = moCommand
        self.moDir     = moDir
        return None


    def connect(self, ip):

        try:
            logFile =  '{0}/{1}.log'.format(self.moDir, ip)

            child = pexpect.spawn('{0} {1}'.format(self.moCommand, ip))
            child.logfile = open(logFile, "w")
            child.expect('^.*>')
            child.sendline('lt all')
            child.expect('Please enter Username')
            child.sendline('expert')
            child.expect('Node Password')
            child.sendline('expert')
            child.expect('^.*>')
            child.sendline('ala')
            child.expect('^.*>')
            child.sendline('exit')

        except Exception as e:
            logging.fatal("Exception: {0}".format(e))
            return False


        return logFile
