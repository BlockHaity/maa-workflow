import sys
import os
from modules.tools import Logging, i18n, aria2

def check_maa_cli():
    """
    检查maa cli是否安装，默认获取最新版本的maa cli并安装到maa-cli目录下
    """
    import requests
    import platform
    import subprocess
    if not os.path.exists("DATA/maa-cli") or len(os.listdir("DATA/maa-cli")) == 0:
        #下载maa cli
        Logging().info(i18n.file("maa.cli.not.install"))

        github_releases = requests.get("https://api.github.com/repos/MaaAssistantArknights/maa-cli/releases/latest").json()["assets"]
        for i in github_releases:
            #根据平台和架构选择合适的版本
            if platform.system().lower() in i["name"] and platform.machine().lower() in i["name"].lower():
                Logging().info(i18n.file("maa.cli.download.start"))
                if sys.platform == "win32":
                    aria2().download("https://v6.gh-proxy.com/"+i["browser_download_url"], "DATA/maa-cli/maa-cli.zip")
                else:
                    aria2().download("https://v6.gh-proxy.com/"+i["browser_download_url"], "DATA/maa-cli/maa-cli.tar.gz")
                break
        Logging().info(i18n.file("maa.cli.download.success"))
        #解压文件
        if sys.platform == "win32":
            import zipfile
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
    import subprocess
    subprocess.run(["DATA/maa-cli/maa", "self", "update"])
    subprocess.run(["DATA/maa-cli/maa", "update"])
    
if __name__ == "__main__":
    check_maa_cli()
    maa_cli_update()
    if len(sys.argv) < 2:
        print("请指定运行模式:\n  python main.py webui - 启动Web界面\n  python main.py run [file] - 运行工作流")
        sys.exit(1)
    
    if sys.argv[1] == "webui":
        from modules.webui import main as webui_main
        webui_main()
    elif sys.argv[1] == "run":
        from modules.backend import main as workflow_main
        workflow_main()
    else:
        print(f"未知模式: {sys.argv[1]}\n可用模式: webui, run")
        sys.exit(1)