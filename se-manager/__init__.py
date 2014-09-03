__author__ = 'ggentile'

import re

test_file = '/home/ggentile/PycharmProjects/se-manager/SpaceEngineersDedicated_20140902_185151.log'

log_file = open(test_file, 'r')

for line in log_file:
    print(line)


class LogLine:
    LINE_REGEX = r''

    def __init__(self, line):
        pass
