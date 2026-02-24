import sys
from modules.cli import setup

if __name__ == "__main__":
    setup.check_aria2()
    setup.check_maa_cli()
    setup.maa_cli_update()
    if len(sys.argv) < 2:
        print("请指定运行模式:\n  python main.py webui - 启动Web界面\n  python main.py run [file] - 运行工作流")
        sys.exit(1)
    
    if sys.argv[1] == "webui":
        from modules.web import main as webui_main
        webui_main()
        
    elif sys.argv[1] == "run":
        from modules.cli import main as workflow_main
        workflow_main()
    
    else:
        print(f"未知模式: {sys.argv[1]}\n可用模式: webui, run")
        sys.exit(1)