from configparser import ConfigParser
import os
import subprocess

__author__ = 'ggentile'

import re

LINE_REGEX = r'(?P<date_time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}) - Thread:   \d+ -> +(?P<body>\w.*)'

class LogLine:

    def __init__(self, date, body):
        self.date = date
        self.body = body

    def __str__(self):
        return self.body
test_file = '/home/ggentile/PycharmProjects/se-manager/SpaceEngineersDedicated_20140902_185151.log'

log_file = open(test_file, 'r')

for line in log_file:
    result = re.search(LINE_REGEX, line)
    if result:
        logLine = LogLine(result.group('date_time'), result.group('body'))
        print(logLine)

subprocess.call('pwd')

class SeManager:

    def __init__(self, config_path):
        self.installs = {}
        self.servers = {}
        self.config = ConfigParser()
        self.config.read(config_path)

    def start(self, server):
        pass

    def stop(self, server):
        pass

    def restart(self, server):
        pass

    def list_users(self, server):
        pass

    def purge_logs(self, server):
        pass

    def backup_server(self, server, path):
        pass

    def restore_server(self, server, path):
        pass

    def ban_player(self, server, player_name):
        pass

    def op_player(self, server, player_name):
        pass

    def add_mod(self, server, mod_id):
        pass

    def create_server(self, install, server_name):
        pass

    def remove_server(self, install, server_name):
        pass

    def update_install(self, install):
        pass

    def create_install(self, install_name, path):
        pass

    def remove_install(self, install):
        pass
