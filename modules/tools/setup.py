import requests
import platform
import subprocess
import os
import sys
import zipfile
import yaml
from modules.tools import Logging, i18n, aria2, Config

class setup():
    def __init__(self):
        pass

    def check_maa_cli():
        """
        检查maa cli是否安装，默认获取最新版本的maa cli并安装到maa-cli目录下
        """
        if not os.path.exists("DATA/maa-cli") or len(os.listdir("DATA/maa-cli")) == 0:
        #下载maa cli
            Logging().info(i18n.file("maa.cli.not.install"))

            github_releases = requests.get("https://api.github.com/repos/MaaAssistantArknights/maa-cli/releases/latest").json()["assets"]
            for i in github_releases:
                #根据平台和架构选择合适的版本
                if platform.system().lower() in i["name"] and platform.machine().lower() in i["name"].lower():
                    Logging().info(i18n.file("maa.cli.download.start"))
                    if sys.platform == "win32":
                        aria2().download(Config.get("download.gh-proxy","https://v6.gh-proxy.com/")+i["browser_download_url"], "DATA/maa-cli/maa-cli.zip")
                    else:
                        aria2().download(Config.get("download.gh-proxy","https://v6.gh-proxy.com/")+i["browser_download_url"], "DATA/maa-cli/maa-cli.tar.gz")
                    break
            Logging().info(i18n.file("maa.cli.download.success"))
            #解压文件
            if sys.platform == "win32":
                with zipfile.ZipFile("DATA/maa-cli/maa-cli.zip", "r") as zip_ref:
                    zip_ref.extractall("DATA/maa-cli")
                os.remove("DATA/maa-cli/maa-cli.zip")
            else:
                import tarfile
                with tarfile.open("DATA/maa-cli/maa-cli.tar.gz", "r:gz") as tar_ref:
                    tar_ref.extractall("DATA/maa-cli")
                os.remove("DATA/maa-cli/maa-cli.tar.gz")
            #安装MAA Core
            Logging().info(i18n.file("maa.cli.install.core.start"))
            if sys.platform == "win32":
                subprocess.run(["DATA/maa-cli/maa.exe", "install"])
            else:
                subprocess.run(["DATA/maa-cli/maa", "install"])

    def maa_cli_update():
        subprocess.run(["DATA/maa-cli/maa", "update"])

    def check_aria2():
        if not os.path.exists("DATA/aria2") or len(os.listdir("DATA/aria2")) == 0:
            Logging().info(i18n.file("aria2.download.start"))
            # Aria2只提供了Windows的预编译版本
            if platform.machine() != "x86_64" or platform.system().lower() != "windows":
                raise Exception(i18n.file("aria2.not.support"))
            release = requests.get("https://api.github.com/repos/aria2/aria2/releases/latest").json()
            # 手动拼URL
            url = next((i["browser_download_url"] 
                        for i in release["assets"] if "win-64bit-build1" in i["name"] and i["name"].endswith(".zip")), 
                       "https://github.com/aria2/aria2/releases/download/release-1.37.0/aria2-1.37.0-win-64bit-build1.zip")
            try:
                open("DATA/aria2/aria2c.zip", "wb").write(requests.get(Config.get("download.gh-proxy","https://v6.gh-proxy.com/")+url).content)
                Logging().info(i18n.file("aria2.download.success"))
            except Exception as e:
                Logging().error(i18n.file("aria2.download.error") + str(e))
            Logging.info(i18n.file("aria2.install.start"))
            import zipfile
            with zipfile.ZipFile("DATA/aria2/aria2c.zip", "r") as zip_ref:
                zip_ref.extractall("DATA/aria2")
                with open(f"DATA/aria2/{url.split('/')[-1].replace('.zip',"")}/aria2c.exe", "wb") as f:
                    f.write(open("DATA/aria2/aria2c.exe", "rb").read())
            os.remove("DATA/aria2/aria2c.zip")
            for file in os.listdir("DATA/aria2"):
                if file.startswith("aria2") and file.endswith(".exe"):
                    os.rename(f"DATA/aria2/{file}", "DATA/aria2/aria2c.exe")
                    break
            for file in os.listdir(f"DATA/aria2/{url.split('/')[-1].replace('.zip',"")}"):
                os.remove(f"DATA/aria2/{url.split('/')[-1].replace('.zip',"")}/{file}")
            os.rmdir(f"DATA/aria2/{url.split('/')[-1].replace('.zip',"")}")
            Logging().info(i18n.file("aria2.install.success"))
            
    def config():
        #生成配置文件
        if os.path.exists("DATA/maa-cli/config") is False:
            os.makedirs("DATA/maa-cli/config")
        if os.path.exists("DATA/maa-cli/config/profiles") is False:
            os.makedirs("DATA/maa-cli/config/profiles")
        # 复制maa配置到config目录
        with open("config.yml", "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)
        if "maa" in config_data:
            with open("DATA/maa-cli/config/profiles/config.yml", "w", encoding="utf-8") as f:
                yaml.dump({"maa": config_data["maa"]["maa-core"]}, f, allow_unicode=True)
        