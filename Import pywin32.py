import subprocess
import sys

try:
    import win32api
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"])
    import win32api
