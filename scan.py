import configparser
import subprocess
import threading
import logging
import time
import time
import sys
import os

from pathlib import Path

_poll_time = 1
_poll_max = 3600
_barlength = 20

class Person:
  def __init__(self):
    self.name = "name"
    self.age = "age"

  def myfunc(self):
    print("Hello my name is " + self.name)

p1 = Person()

def watch_progress(maxchecks, searchfor):
    def update_progress(progress):
        barLength = _barlength
        prefix = "Testing"
        working = ""
        done = "Done...\r\n"
        status = "python - vagrant.conda"
        if isinstance(progress, int):
            progress = float(progress)
        if progress >= 1:
            progress = 1
            status = done
        block = int(round(barLength*progress))
        text = "\r{0}: [{1}] {2}".format(prefix, "#"*block + "-"*(barLength-block), status)
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

    i = 0
    while i < maxchecks:
        check = count_progress_steps(searchfor)
        update_progress(check[0]/check[1])
        if check[0] == check[1]:
            return
        time.sleep(_poll_time)
        i = i + 1

def init_progress_bar():
    clear_logs()
    #print(get_commands("python"))
    searchfor = ["Bringing machine 'default' up with 'virtualbox' provider", "test session starts"]
    x = threading.Thread(target=watch_progress, args=(_poll_max, searchfor))
    x.start()
    return x

def clear_logs():
    def remove_file(path):
        path = Path(path)
        if path.is_file():
            os.remove(path)

    remove_file("log")
    remove_file("err")
    log = open("log", "w")
    err = open("err", "w")
    return log,err

def get_commands(type):
    out = subprocess.Popen(
        ['sudo', 'make', 'help'],
        cwd="workspace/bash-environment-templates/samples/conda/python",
        universal_newlines=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    log, err = out.communicate()
    commands = log.split("\n")
    commands.remove("")
    return commands

def test(dir):
    log, err = clear_logs()
    config = configparser.ConfigParser()
    config.read('tests/python/test.ini')
    out = subprocess.Popen(
        ['sudo', 'make', 'vagrant.conda'],
        cwd="workspace/bash-environment-templates/samples/conda/python",
        universal_newlines=True,
        stdout=log,
        stderr=err
    )
    out.wait()

def queue_tests(dirs):
    for dir in dirs:
        if dir == "python":
            progress_bar_thread = init_progress_bar()
            test(dir)
            progress_bar_thread.join()

if __name__ == '__main__':
    queue_tests(os.listdir('tests'))
    queue_tests(os.listdir('tests'))
