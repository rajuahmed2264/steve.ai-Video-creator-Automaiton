
import os
import subprocess
import sys

sys.setrecursionlimit(999999999)
running= True

pidtotext = os.getpid()
pidtextfile = open("temppid.file", "r+")
pidtextfile.seek(0)
pidtextfile.truncate()
pidtextfile.close()
pidtextfile = open("temppid.file", "w")
pidtextfile.writelines(str(pidtotext))
pidtextfile.close()

def run_program():
    global running

    subprocess.call('process.exe')
    #os.startfile('gmailwithedge.exe')
    running = True
while running:
    run_program()