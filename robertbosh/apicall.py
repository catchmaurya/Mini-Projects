# To kick off the script, run the following from the python directory:
#   PYTHONPATH=`pwd` python apicall.py start
# path:/usr/share/apicall/apicall.py
#standard python libs
import logging
import time
import socket
import pwd
import os

#third party libs
from daemon import runner
import requests

class App():
    
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/null'
        self.stderr_path = '/dev/null'
        self.pidfile_path =  '/var/run/apicall.pid'
        self.pidfile_timeout = 5

    def call_url(self):
        hostname = socket.gethostname() 
        URL = 'https://database.company.com/devices/%s/allowedUsers' % hostname
        result = {}
        try:
           response = requests.get(URL)
        except Exception, e:
           logger.error("URL connection error = %s", str(e))
        else:
           result = response.json()
           
        return (hostname, result)

    def add_user(self):
        hostname, result =  self.call_url()
        #result = {'allowedUsers':['maurya', 'angita', 'aruna']}
        for each_user in result['allowedUsers']:
            try:
               user = pwd.getpwnam(each_user)
            except KeyError:
               logger.error('user does not exist %s' % each_user)
               #create new user
               os.system("sudo useradd %s" % each_user)
            else:
               logger.info("user present %s" % each_user)               

            self.sudo_add(each_user)

    def sudo_add(self, user):
        # check user has sudo privilege/in sudoers group, if yes do nothing, else add to sudoers group
        output = os.popen('id %s| grep \(sudo\) |wc -l' % user).read().split('\n')
        if output[0] == '1':
           #user in sudoers
           pass
        else:
           os.system('sudo adduser %s sudo' % user)      

    def run(self):
        while True:
            #Main code goes here ...
            #Note that logger level needs to be set to logging.DEBUG before this shows up in the logs
            self.add_user()
            time.sleep(10)

app = App()
logger = logging.getLogger("DaemonLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/var/log/apicall/apicall.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

daemon_runner = runner.DaemonRunner(app)
#This ensures that the logger file handle does not get closed during daemonization
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()

