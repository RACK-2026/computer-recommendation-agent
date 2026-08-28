"""一键重启"""
import subprocess, sys, os

script = os.path.join(os.path.dirname(__file__), "run.py")
subprocess.run([sys.executable, script])

