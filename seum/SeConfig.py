"""Config file parser and editor"""

import shutil
import xml.etree.ElementTree as Et

__author__ = "Ewandor"
__copyright__ = "Copyright 2014-2015, Ewandor"
__credits__ = ["Ewandor"]
__maintainer__ = "Ewandor"
__license__ = "MIT"
__version__ = "0.1"
__email__ = "ewandor@dorfsvald.net"
__status__ = "Prototype"


class SeConfigReader:
    BACKUP_SUFFIX = '_save'

    def __init__(self, path):
        self.path = path
        self.tree = Et.parse(self.path)

    def add_op(self, user_id):
        op_list = self.tree.find('Administrators')
        Et.SubElement(op_list, 'op').text = user_id

    def remove_op(self, user_id):
        op_list = self.tree.find('Administrators')
        for op in op_list.children():
            if op.text == user_id:
                op_list.remove(op)

    def save(self):
        shutil.move(self.path, self.path + self.BACKUP_SUFFIX)
        self.tree.write(self.path)
