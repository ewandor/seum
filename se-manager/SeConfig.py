__author__ = 'ggentile'

import xml.etree.ElementTree as et


class SeConfigReader:
    def __init__(self, path):
        self.path = path
        self.tree = et.parse(self.path)

    def get_value(self, node):
        pass

    def set_value(self, node, value):
        pass
