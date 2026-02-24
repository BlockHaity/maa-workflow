import subprocess
import os
from unittest import result

from modules.tools import i18n

def subprocess_run(command=list(), Shell=False, Async=False, **kwargs):
    """对subprocess的二次封装

    Args:
        command (_type_, optional): _description_. Defaults to list().
    """
    # 合并环境变量
    env = None
    env_vars = {
        "MAA_CONFIG_DIR": os.path.abspath("DATA/maa-cli/config"),  
        }
    env = os.environ.copy()
    env.update(env_vars)
    
    if Async:
        result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=Shell, env=env, **kwargs)
        return result
    else:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=Shell, env=env, **kwargs)
        if result.returncode != 0:
            raise Exception(i18n.file("maa.task.run.error") + result.stderr.decode("utf-8"))
        return result

class maa():
    """
    对MAA CLI的python封装
    """
    def __init__(self):
        self.maa_path = "DATA/maa-cli/maa"  # 默认MAA CLI命令路径
    
    # https://docs.maa.plus/zh-cn/manual/cli/usage.html#%E9%A2%84%E5%AE%9A%E4%B9%89%E4%BB%BB%E5%8A%A1
    def startup(self, client=""):
        """启动游戏并进入主界面

        Args:
            client (str): 是客户端类型，如果留空则不会启动游戏客户端
        """
        subprocess_run([self.maa_path, "startup", client])