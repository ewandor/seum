import re
import subprocess
from shutil import copytree

__author__ = "Ewandor"
__copyright__ = "Copyright 2014-2015, Ewandor"
__credits__ = ["Ewandor"]
__maintainer__ = "Ewandor"
__license__ = "MIT"
__version__ = "0.1"
__email__ = "ewandor@dorfsvald.net"
__status__ = "Prototype"


class ServerStateManager:

    def __init__(self, instance_name):
        self.instanceName = instance_name

    def server_restart(self):
        self.server_stop()
        self.server_start()


class WindowsServerStateManager(ServerStateManager):
    SERVICES_REGEX = r'STATE\s*: (?P<status>\d)'
    SERVICES_STATUS = {4: 'running'}

    def server_start(self):
        subprocess.call(['net', 'start', self.instanceName])

    def server_stop(self):
        subprocess.call(['net', 'stop', self.instanceName])

    def server_state(self):
        output = subprocess.check_output(['sc', 'query', self.instanceName]).decode('utf-8')
        result = re.search(self.SERVICES_REGEX, output)
        return result.group('status') == '4'

    def backup_server(self, path):
        self.server.stop
        copytree(self.server.save_path, path)
        self.server.start

    def restore_server(self, path):
        self.server.stop
        copytree(path, self.server.save_path)
        self.server.start