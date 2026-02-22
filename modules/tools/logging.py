import time

class Logging():
    def __init__(self):
        self.log_list = []
        pass
    
    def info(self,log_str):
        log_time = time.strftime("%H:%M:%S", time.localtime())
        print(f"\033[92m[{log_time}][INFO]\033[0m {log_str}")
        self.log_list.append(f"[{log_time}][INFO] {log_str}")

    def error(self,log_str):
        log_time = time.strftime("%H:%M:%S", time.localtime())
        print(f"\033[91m[{log_time}][ERROR]\033[0m {log_str}")
        self.log_list.append(f"[{log_time}][ERROR] {log_str}")

    def warn(self,log_str):
        log_time = time.strftime("%H:%M:%S", time.localtime())
        print(f"\033[93m[{log_time}][WARN]\033[0m {log_str}")
        self.log_list.append(f"[{log_time}][WARN] {log_str}")
    
    def debug(self,log_str):
        log_time = time.strftime("%H:%M:%S", time.localtime())
        print(f"\033[94m[{log_time}][DEBUG]\033[0m {log_str}")
        self.log_list.append(f"[{log_time}][DEBUG] {log_str}")
    
    def save_log(self,path):
        with open(path, "w") as f:
            for log in self.log_list:
                f.write(log + "\n")
