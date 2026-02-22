import sys
import subprocess

class aria2:
    def __init__(self,thread_num=16):
        self.aria2_path = "DATA/aria2/aria2c.exe" if sys.platform == "win32" else "DATA/aria2/aria2c"
        self.thread_num = thread_num
    
    def download(self, url, save_path):
        subprocess.run([self.aria2_path, "-x", str(self.thread_num), "-s", str(self.thread_num), "-o", save_path, url])