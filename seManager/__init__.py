__author__ = 'ggentile'

from configparser import ConfigParser

from seManager.SeLogs import LogFileReader

test_file = '/home/ggentile/PycharmProjects/se-manager/SpaceEngineersDedicated_20140902_185151.log'

log_reader = LogFileReader(test_file)

print(
    log_reader.users_connections[0]['user'],
    log_reader.users_disconnections[0]['date'],
    log_reader.last_connected_user,
    log_reader.server_ready
)
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

    def uptime(self, server):
        pass

    def list_users(self, server):
        pass

    def purge_logs(self, server):
        pass

    def backup_server(self, server, path):
        pass

    def restore_server(self, server, path):
        pass

    def backup_config(self, server):
        pass

    def restore_config(self, server):
        pass

    def ban_player(self, server, player_name):
        pass

    def unban_player(self, server, player_name):
        pass

    def op_player(self, server, player_name):
        pass

    def deop_player(self, server, player_name):
        pass

    def add_mod(self, server, mod_id):
        pass

    def remove_mod(self, server, mod_id):
        pass

    def create_server(self, install, server_name):
        pass

    def remove_server(self, install, server_name):
        pass

    def list_servers(self, install=None):
        pass

    def update_install(self, install):
        pass

    def create_install(self, install_name, path):
        pass

    def remove_install(self, install):
        pass

    def list_installs(self):
        pass
