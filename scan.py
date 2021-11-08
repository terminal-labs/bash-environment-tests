import configparser
import subprocess
from subprocess import check_output
import time, sys
import logging
import threading
import time
import os

def watch_progress(maxchecks):
    def update_progress(progress):
        barLength = 20
        status = ""
        if isinstance(progress, int):
            progress = float(progress)
        if not isinstance(progress, float):
            progress = 0
            status = "error: progress var must be float\r\n"
        if progress < 0:
            progress = 0
            status = "Halt...\r\n"
        if progress >= 1:
            progress = 1
            status = "Done...\r\n"
        block = int(round(barLength*progress))
        text = "\rPercent: [{0}] {1}".format( "#"*block + "-"*(barLength-block), status)
        sys.stdout.write(text)
        sys.stdout.flush()

    def count_progress_steps(searchfor):
        with open('log') as f:
            contents = f.read()
            count = 0
            for str in searchfor:
                if str in contents:
                    count = count + 1
        return count, len(searchfor)

    searchfor = ["Bringing machine 'default' up with 'virtualbox' provider", "test session starts"]

    i = 0
    while i < maxchecks:
        check = count_progress_steps(searchfor)
        update_progress(check[0]/check[1])
        if check[0] == check[1]:
            return
        time.sleep(1)
        i = i + 1


def test(dir,log,err):
    config = configparser.ConfigParser()
    config.read('tests/python/test.ini')
    out = subprocess.Popen(['sudo', 'make', 'vagrant.conda'], cwd="workspace/bash-environment-templates/samples/conda/python", universal_newlines=True, stdout=log, stderr=err)
    out.wait()

def scan_tests(dirs,log,err):
    for dir in dirs:
        if dir == "python":
            test(dir,log,err)

os.remove("log")
os.remove("err")
log = open("log", "w", 1)
err = open("err", "w", 1)

x = threading.Thread(target=watch_progress, args=(3600,))
x.start()

scan_tests(os.listdir('tests'),log,err)

x.join()

os.remove("log")
os.remove("err")
log = open("log", "w", 1)
err = open("err", "w", 1)

x = threading.Thread(target=watch_progress, args=(3600,))
x.start()

scan_tests(os.listdir('tests'),log,err)

x.join()
