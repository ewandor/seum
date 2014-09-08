import shutil

__author__ = 'ggentile'

import xml.etree.ElementTree as et


class SeConfigReader:
    BACKUP_SUFFIX = '_save'

    def __init__(self, path):
        self.path = path
        self.tree = et.parse(self.path)

    def get_value(self, node):
        pass

    def set_value(self, node, value):
        pass

    def save(self):
        shutil.move(self.path, self.path + self.BACKUP_SUFFIX)
        self.tree.write(self.path)
