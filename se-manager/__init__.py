__author__ = 'ggentile'

import re


class LogLine:
    LINE_REGEX = r'(?P<date_time>\d{4}-\d{2}-\{2} \d{2}:\d{2}:\d{2}.\d{3}) - Thread:   \d+ -> +(?P:<body>\w.*)'

    def __init__(self, line):
        result = re.search(self.LINE_REGEX, line)
        self.date = result.match('date_time')
        self.body = result.match('body')

test_file = '/home/ggentile/PycharmProjects/se-manager/SpaceEngineersDedicated_20140902_185151.log'

log_file = open(test_file, 'r')

for line in log_file:
    logLine = LogLine(line)
