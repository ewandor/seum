import os
import subprocess

__author__ = 'ggentile'

SteamAppIds = {
    "SpaceEngineers": '244850'
}

class SteamCmdOperator:

    STEAM_CMD_PATH = '/cygdrive/c/steamcmd/steamcmd.exe'
    INSTALL_DIR = 'c:\SE\\'

    def __init__(self, steamUserLogin, steamUserPass):
        self.steamUserLogin = steamUserLogin
        self.steamUserPass = steamUserPass

    def _sendCommand(self, commands):
        subprocess.call([self.STEAM_CMD_PATH, '+login', self.steamUserLogin, self.steamUserPass] + commands + ['+quit'])

    def updateApp(self):
        self._sendCommand(['+force_install_dir', self.INSTALL_DIR, '+app_update', SteamAppIds['SpaceEngineers']])
