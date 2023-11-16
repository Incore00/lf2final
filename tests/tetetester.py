import signal
import subprocess, os, sys
from threading import Thread
import time

leather_view = subprocess.Popen(["python", "SomeFile.py"], shell=True)
main_program = subprocess.Popen(["python", "main.py"], shell=True)
time.sleep(5)

leather_view.terminate()
main_program.terminate()
print('done')




