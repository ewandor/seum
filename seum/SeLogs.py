"""Log file parser"""

import os
import re

from datetime import datetime

__author__ = "Ewandor"
__copyright__ = "Copyright 2014-2015, Ewandor"
__credits__ = ["Ewandor"]
__maintainer__ = "Ewandor"
__license__ = "MIT"
__version__ = "0.1"
__email__ = "ewandor@dorfsvald.net"
__status__ = "Prototype"


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.login = ''

    def __str__(self):
        return '%s (%s)' % (self.user_id, self.login)

    def __repr__(self):
        return '<SeLogs.User: %s (%s)>' % (self.user_id, self.login)


class UserFactory:

    users = {}

    @classmethod
    def get_user_by_login(cls, login):
        for user in cls.users.values():
            if login == user.login:
                return user

    @classmethod
    def get_user_by_id(cls, user_id):
        if not user_id in cls.users:
            cls.users[user_id] = User(user_id)
        return cls.users[user_id]


class LogLine:

    def __init__(self, date, body):
        self.date = date
        self.body = body

    def __str__(self):
        return self.body


class LogFileReader:
    REGEX_LOG_LINE = r'(?P<date_time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}) - Thread:   \d+ -> +(?P<body>\w.*)'
    REGEX_USER_LOGIN = r'World request received: (?P<login>\S+)'
    REGEX_USER_CONNECTED = r'Server ValidateAuthTicketResponse \(k_EAuthSessionResponseOK\), owner: (?P<user_id>\d+)'
    REGEX_USER_DISCONNECTED = r'User left (?P<login>.+)'
    REGEX_SERVER_INITIALIZED = r'Game ready... Press Ctrl\+C to exit'

    def __init__(self, path):
        self.path = path
        self.file = open(self.path, 'r')
        self.__init_server_states()

        self.line_parsers = ['user_connected', 'user_login', 'user_disconnected', 'server_ready']
        self.parse_file()

    def __init_server_states(self):
        self.users_connections = []
        self.users_disconnections = []
        self.last_connected_user = False
        self.server_ready = False

    def parse_file(self):
        for line in self.file:
            result = re.search(self.REGEX_LOG_LINE, line)
            if result:
                line_date = datetime.strptime(result.group('date_time'), '%Y-%m-%d %H:%M:%S.%f')
                line_body = result.group('body')
                for parser_name in self.line_parsers:
                    if self.call_parser(parser_name, line_body, line_date):
                        break

    def call_parser(self, parser_name, line_body, line_date):
        parser = getattr(self, 'parse_' + parser_name)
        return parser(line_body, line_date)

    def parse_user_connected(self, body, date):
        result = re.search(self.REGEX_USER_CONNECTED, body)
        if result:
            user = UserFactory.get_user_by_id(result.group('user_id'))
            self.users_connections.append({'date': date, 'user': user})
            self.last_connected_user = user
            return True

    def parse_user_login(self, body, date):
        if self.last_connected_user:
            result = re.search(self.REGEX_USER_LOGIN, body)
            if result:
                self.last_connected_user.login = result.group('login')
                self.last_connected_user = False
                return True

    def parse_user_disconnected(self, body, date):
        result = re.search(self.REGEX_USER_DISCONNECTED, body)
        if result:
            user = UserFactory.get_user_by_login(result.group('login'))
            self.users_disconnections.append({'date': date, 'user': user})
            return True

    def parse_server_ready(self, body, date):
        if re.search(self.REGEX_SERVER_INITIALIZED, body):
            self.server_ready = date


class LogFilesManager:
    REGEX_LOGFILE_NAME_FORMAT = r"SpaceEngineersDedicated_(?P<date>\d{8})_(?P<time>)\d{6}.log"

    def __init__(self, server):
        self.server = server
        self.log_dir = server.log_dir
        self.current_log_file = self.find_current_log_file()

    def find_current_log_file(self):
        current_log_file = {'filename': '', 'date': '0', 'time': '0'}
        if self.server.state == 'running':
            for entry in os.listdir(self.log_dir):
                result = re.search(self.REGEX_LOGFILE_NAME_FORMAT, entry)
                if result:
                    file_date = datetime.strptime(result.group('date') + result.group('time'), '%Y%m%d%H%M%S')
                    if file_date > current_log_file['datetime']:
                        current_log_file = {
                            'filename': entry,
                            'datetime': file_date,
                        }
            return current_log_file
        else:
            return None

    def purge_logs(self):
        for file_name in os.listdir(self.log_dir):
            if self.current_log_file is None or file_name != self.current_log_file['filename']:
                os.remove(file_name)
