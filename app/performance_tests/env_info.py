import psutil
import platform
import socket

def get_env_info():
    print("📦 Environment Info")
    print("====================")
    print(f"System   : {platform.system()} {platform.release()}")
    print(f"Machine  : {platform.machine()}")
    print(f"CPU      : {psutil.cpu_count(logical=True)} cores")
    print(f"RAM      : {round(psutil.virtual_memory().total / (1024**3), 2)} GB")
    
    net_io = psutil.net_io_counters()
    print(f"Network  : Sent={round(net_io.bytes_sent / (1024**2), 2)} MB | Recv={round(net_io.bytes_recv / (1024**2), 2)} MB")

if __name__ == "__main__":
    get_env_info()
