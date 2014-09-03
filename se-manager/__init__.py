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
