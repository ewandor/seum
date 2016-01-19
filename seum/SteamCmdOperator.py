import subprocess

__author__ = "Ewandor"
__copyright__ = "Copyright 2014-2015, Ewandor"
__credits__ = ["Ewandor"]
__maintainer__ = "Ewandor"
__license__ = "MIT"
__version__ = "0.1"
__email__ = "ewandor@dorfsvald.net"
__status__ = "Prototype"

SteamAppIds = {
    "SpaceEngineers": '244850'
}


class SteamCmdOperator:

    STEAM_CMD_PATH = '/cygdrive/c/steamcmd/steamcmd.exe'
    INSTALL_DIR = 'c:\SE\\'

    def __init__(self, steam_user_login, steam_user_pass):
        self.steamUserLogin = steam_user_login
        self.steamUserPass = steam_user_pass

    def _send_command(self, commands):
        subprocess.call([self.STEAM_CMD_PATH, '+login', self.steamUserLogin, self.steamUserPass] + commands + ['+quit'])

    def update_app(self):
        self._send_command(['+force_install_dir', self.INSTALL_DIR, '+app_update', SteamAppIds['SpaceEngineers']])
