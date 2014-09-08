import shutil

__author__ = 'ggentile'

import xml.etree.ElementTree as et


class SeConfigReader:
    BACKUP_SUFFIX = '_save'

    def __init__(self, path):
        self.path = path
        self.tree = et.parse(self.path)

    def add_op(self, user_id):
        op_list = self.tree.find('Administrators')
        et.SubElement(op_list, 'op').text = user_id

    def remove_op(self, user_id):
        op_list = self.tree.find('Administrators')
        for op in op_list.children():
            if op.text == user_id:
                op_list.remove(op)

    def save(self):
        shutil.move(self.path, self.path + self.BACKUP_SUFFIX)
        self.tree.write(self.path)
