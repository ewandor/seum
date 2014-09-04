import subprocess

__author__ = 'ggentile'


class WindowsServerStateManager:

    def __init__(self, instanceName):
        self.instanceName = instanceName

    def server_start(self):
        subprocess.call(['net', 'start', self.instanceName])

    def server_stop(self):
        subprocess.call(['net', 'stop', self.instanceName])

    def server_state(self):
        pass