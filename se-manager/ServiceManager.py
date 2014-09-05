from multiprocessing import connection
import os
import re
import subprocess
from pip.vendor.distlib._backport import shutil

__author__ = 'ggentile'

class User:
    def __init__(self, login, date_connection ):
        self.login = login
        self.date_connection = date_connection

class LogsManager:
    REGEX_USER_CONNECTED = r'World request received: (?P<login>.+)'
    REGEX_USER_ID = r'Server ValidateAuthTicketResponse (k_EAuthSessionResponseOK), owner: (?P<user_id>\d+)'
    REGEX_USER_DISCONNECTED = r'User left (?P<login>.+)'

    def purge_logs(self):
        for files in logs_dir:
            os.remove(files)

    def list_users(self):
        connected_users = []
        next_one_is_user_id = False
        for logLine in self.current_log_file:
            if next_one_is_user_id:
                result = re.search(self.REGEX_USER_ID, logLine.body)
                connected_users[-1].user_id = result.group('user_id')
            else:
                result = re.search(self.REGEX_USER_CONNECTED, logLine.body)
                if result:
                    connected_users.append(User(result.group('login'), logLine.date))
                    next_one_is_user_id = True
                else:
                    result = re.search(self.REGEX_USER_DISCONECTED, logLine.body)
                    if result and result.group('login') in connected_users:
                        for user in connected_users:
                            if user.login == result.group('login'):
                                connected_users.remove(user)
                                break

        return connected_users

    def backup_server(self, path):
        self.server.stop
        shutil.copytree(self.server.save_path, path)
        self.server.start

    def restore_server(self, path):
        self.server.stop
        shutil.copytree(path, self.server.save_path)
        self.server.start


class ServerStateManager:

    def __init__(self, instanceName):
        self.instanceName = instanceName

    def server_restart(self):
        self.server_stop()
        self.server_start()

class WindowsServerStateManager(ServerStateManager):

    def server_start(self):
        subprocess.call(['net', 'start', self.instanceName])

    def server_stop(self):
        subprocess.call(['net', 'stop', self.instanceName])

    def server_state(self):
        pass