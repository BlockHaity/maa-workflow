import sys
import subprocess
from modules.tools import Config, i18n

class aria2:
    def __init__(self):
        self.aria2_path = "DATA/aria2/aria2c.exe" if sys.platform == "win32" else "DATA/aria2/aria2c"
        self.thread_num = Config.get("download.aria2.threads", 16)
    
    def download(self, url, save_path):
        session = subprocess.run([self.aria2_path, "-x", str(self.thread_num), "-s", str(self.thread_num), "-o", save_path, url])
        if session.returncode != 0:
            raise Exception(i18n.file("aria2.download.error"))