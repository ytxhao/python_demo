# coding=utf-8
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import commands
import os
import sys
import tarfile
import time
import datetime  # 导入datetime模块
import threading
import logging
import subprocess
import platform
import shutil
import commands

CMAKE_VERSION = "3.23.1"
NINJA_VERSION = "1.10.2"
# SCRIPT_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
SRC_DIR = "/Volumes/kingston/shared_vagrant_v2/msl-core-v3/src"
TOOLS_DIR = os.path.normpath(os.path.join(SRC_DIR, 'tools'))
NINJA_ROOT_DIR = os.path.normpath(os.path.join(TOOLS_DIR, platform.system(), 'ninja'))
CMAKE_ROOT_DIR = os.path.normpath(os.path.join(TOOLS_DIR, platform.system(), 'cmake'))
CMAKE_SOURCE_DIR = os.path.normpath(os.path.join(TOOLS_DIR, 'cmake', 'source'))
CMAKE_BUILD_SCRIPT = os.path.normpath(os.path.join(CMAKE_SOURCE_DIR, 'cmake-3.23.1', 'bootstrap'))


# threading.Timer


class SimpleTimer(threading.Thread):
    def __init__(self, interval, function, args=[], kwargs={}):
        threading.Thread.__init__(self)
        if args is None:
            args = []
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.finished = threading.Event()

    def cancel(self):
        self.finished.set()

    def canceled(self):
        self.finished.is_set()

    def run(self):
        while not self.finished.is_set():
            self.finished.wait(self.interval)
            self.function(*self.args, **self.kwargs)
        self.finished.set()


def thread_fun(num):
    print("======num:", num)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print("Hi, {0}".format(name))  # Press ⌘F8 to toggle the breakpoint.
    # cmake_version_status = commands.getstatusoutput("cmake ---version")
    # print("{0} \r\ncode:{1}".format(cmake_version_status[1], cmake_version_status[0]))
    src_ninja_file = os.path.normpath(os.path.join(NINJA_ROOT_DIR, NINJA_VERSION, 'bin', 'ninja'))
    dist_ninja_file = os.path.normpath(os.path.join(CMAKE_ROOT_DIR, CMAKE_VERSION, 'bin', 'ninja'))
    shutil.copyfile(src_ninja_file, dist_ninja_file)
    shutil.copymode(src_ninja_file, dist_ninja_file)

    simpleTimer = SimpleTimer(1, thread_fun, (1,))
    simpleTimer.start()
    # simpleTimer.join()
    print("=========end")
    time.sleep(5)
    simpleTimer.cancel()
    simpleTimer.join()
    print("=========end2")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
