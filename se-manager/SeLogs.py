import os
import re

__author__ = 'ggentile'

class User:
    def __init__(self, login, date_connection):
        self.login = login
        self.date_connection = date_connection


class LogLine:

    def __init__(self, date, body):
        self.date = date
        self.body = body

    def __str__(self):
        return self.body


class LogFileReader:
    REGEX_LOG_LINE = r'(?P<date_time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}) - Thread:   \d+ -> +(?P<body>\w.*)'
    REGEX_USER_CONNECTED = r'World request received: (?P<login>.+)'
    REGEX_USER_ID = r'Server ValidateAuthTicketResponse (k_EAuthSessionResponseOK), owner: (?P<user_id>\d+)'
    REGEX_USER_DISCONNECTED = r'User left (?P<login>.+)'
    REGEX_SERVER_INITIALIZED = r'Game ready... Press Ctrl\+C to exit'

    def __init__(self, path):
        self.path = path
        self.file = open(self.path, 'r')
        self.lines = []
        self.parse_file()

    def parse_file(self):
        for line in self.file:
            result = re.search(self.REGEX_LOG_LINE, line)
            if result:
                self.lines.append(LogLine(result.group('date_time'), result.group('body')))

    def list_users(self):
        connected_users = []
        next_one_is_user_id = False
        for logLine in self.lines:
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
                    if result:
                        self.remove_user_from_list(connected_users, result.group('login'))
        return connected_users

    @staticmethod
    def remove_user_from_list(user_list, user_name):
        for user in user_list:
            if user.login == user_name:
                user_list.remove(user)
                break

    def get_start_time(self):
        for logLine in self.lines:
            if re.search(self.REGEX_SERVER_INITIALIZED, logLine.body):
                return logLine.date


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
                if result and result.group('date') > current_log_file['date'] \
                        or result.group('date') == current_log_file['date'] \
                        and result.group('time') > current_log_file['time']:
                    current_log_file = {
                        'filename': entry,
                        'date': result.group('date'),
                        'time': result.group('time')
                    }
            return current_log_file
        else:
            return None

    def purge_logs(self):
        for file_name in os.listdir(self.log_dir):
            if self.current_log_file is None or file_name != self.current_log_file['filename']:
                os.remove(file_name)
