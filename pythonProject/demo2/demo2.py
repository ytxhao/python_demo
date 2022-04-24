# coding=utf-8
# This is a sample Python script.
from __future__ import print_function
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import sys

if sys.version > '3':
    import queue as Queue
else:
    import Queue
import commands
import operator
import copy
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
import threading
import time

CMAKE_VERSION = "3.23.1"
NINJA_VERSION = "1.10.2"
SCRIPT_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
SRC_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, 'test_dir', 'src'))
TOOLS_DIR = os.path.normpath(os.path.join(SRC_DIR, 'tools'))
NINJA_ROOT_DIR = os.path.normpath(os.path.join(TOOLS_DIR, platform.system(), 'ninja'))
CMAKE_SOURCE_DIR = os.path.normpath(os.path.join(TOOLS_DIR, 'cmake', 'source'))
CMAKE_ROOT_DIR = os.path.normpath(os.path.join(CMAKE_SOURCE_DIR))

CMAKE_BUILD_SCRIPT = os.path.normpath(os.path.join(CMAKE_SOURCE_DIR, 'cmake-3.23.1', 'bootstrap'))


def run_test(q, tarf):
    print("run_test===")
    while not q.empty():
        tarinfo = q.get()
        try:
            # tarf.extract(name_, path=os.path.join(CMAKE_SOURCE_DIR))
            if tarinfo.isdir():
                # Extract directories with a safe mode.
                # directories.append(tarinfo)
                tarinfo = copy.copy(tarinfo)
                tarinfo.mode = 0700
            tarf.extract(tarinfo, CMAKE_SOURCE_DIR)
        except Exception as e:
            pass
        q.task_done()  # 处理完成


# 显示进度 （当前，总数）
def progressbar(nowprogress, toyal):
    print("==progressbar", nowprogress, toyal)
    # get_progress = int((nowprogress + 1) * (50 / toyal))  # 显示多少>
    # get_pro = int(50-get_progress)  # 显示多少-
    # percent = (nowprogress + 1) * (100 / toyal)
    # if percent > 100:
    #     percent = 100
    # print("\r"+"["+">"*get_progress+"-"*get_pro+']'+"%.2f" %
    #       percent + "%", end="")


def show_test(q, q_len):
    print("show_test===")
    while not q.empty():
        time.sleep(0.5)
        progressbar(q_len - q.unfinished_tasks, q_len)
    progressbar(q_len, q_len)


def show_test2(count, len):
    # num = count.cnt()
    # print("show_test2===num:", num)
    while True:
        num = count.cnt()
        if num != 0:
            time.sleep(0.5)
            progressbar(len - num, len)
        else:
            break
    progressbar(len, len)


def mult_thread_test():
    shutil.rmtree(os.path.normpath(os.path.join(CMAKE_SOURCE_DIR, 'cmake-3.23.1')), True)
    cmake_tar_file = os.path.join(CMAKE_SOURCE_DIR, 'cmake-3.23.1.tar.gz')
    q = Queue.Queue()  # 不传MaxSize
    q_len = 0  # 记录队列长度
    tarf = tarfile.open(cmake_tar_file)
    names = tarf.getnames()
    numbers = tarf.getmembers()
    threadlist = []
    for name in numbers:
        q.put(name)
        q_len += 1
    # def __init__(self, group=None, target=None, name=None,
    #              args=(), kwargs=None, verbose=None):
    # 处理线程
    # lock = threading.Lock()
    # for x in range(0, 8):
    #     th = threading.Thread(target=run_test, args=(q, tarf,))
    #     th.setDaemon(True)
    #     threadlist.append(th)
    th = threading.Thread(target=extract_test, args=(q, tarf,))
    th.setDaemon(True)
    threadlist.append(th)

    # 进度线程
    threadlist.append(threading.Thread(target=show_test, args=(q, q_len,)))

    # 运行并加入等待运行完成
    for t in threadlist:
        t.start()
    for t in threadlist:
        t.join()


def single_thread():
    shutil.rmtree(os.path.normpath(os.path.join(CMAKE_SOURCE_DIR, 'cmake-3.23.1')), True)
    cmake_tar_file = os.path.join(CMAKE_SOURCE_DIR, 'cmake-3.23.1.tar.gz')
    tar = tarfile.open(cmake_tar_file)
    # names = tar.getnames()
    # for name in names:
    #     # print(name)
    #     tar.extract(name, path=os.path.join(CMAKE_ROOT_DIR, 'source'))
    tar.extractall(CMAKE_SOURCE_DIR)
    tar.close()


def extract_test(q, q_len):
    shutil.rmtree(os.path.normpath(os.path.join(CMAKE_SOURCE_DIR, 'cmake-3.23.1')), True)
    cmake_tar_file = os.path.join(CMAKE_SOURCE_DIR, 'cmake-3.23.1.tar.gz')
    tar = tarfile.open(cmake_tar_file)

    directories = []

    # if members is None:
    members = tar.getmembers()
    path = CMAKE_SOURCE_DIR
    for tarinfo in members:
        if tarinfo.isdir():
            # Extract directories with a safe mode.
            directories.append(tarinfo)
            tarinfo = copy.copy(tarinfo)
            tarinfo.mode = 0700
        tar.extract(tarinfo, path)
        # q.task_done()  # 处理完成

    # Reverse sort directories.
    directories.sort(key=operator.attrgetter('name'))
    directories.reverse()

    # Set correct owner, mtime and filemode on directories.
    # for tarinfo in directories:
    #     dirpath = os.path.join(path, tarinfo.name)
    #     try:
    #         self.chown(tarinfo, dirpath)
    #         self.utime(tarinfo, dirpath)
    #         self.chmod(tarinfo, dirpath)
    #     except ExtractError, e:
    #         if self.errorlevel > 1:
    #             raise
    #         else:
    #             self._dbg(1, "tarfile: %s" % e)


def extract_test3():
    shutil.rmtree(os.path.normpath(os.path.join(CMAKE_SOURCE_DIR, 'cmake-3.23.1')), True)
    cmake_tar_file = os.path.join(CMAKE_SOURCE_DIR, 'cmake-3.23.1.tar.gz')
    tar = tarfile.open(cmake_tar_file)
    tar.extractall(CMAKE_SOURCE_DIR)
    tar.close()


def extract_test2(count):
    shutil.rmtree(os.path.normpath(os.path.join(CMAKE_SOURCE_DIR, 'cmake-3.23.1')), True)
    cmake_tar_file = os.path.join(CMAKE_SOURCE_DIR, 'cmake-3.23.1.tar.gz')
    tar = tarfile.open(cmake_tar_file)

    directories = []

    # if members is None:
    members = tar.getmembers()
    # members.count()
    count.set(len(members))

    th = threading.Thread(target=show_test2, args=(count, len(members),))
    th.start()

    path = CMAKE_SOURCE_DIR
    for tarinfo in members:
        if tarinfo.isdir():
            # Extract directories with a safe mode.
            directories.append(tarinfo)
            tarinfo = copy.copy(tarinfo)
            tarinfo.mode = 0700
        tar.extract(tarinfo, path)
        count.sub()


    # Reverse sort directories.
    directories.sort(key=operator.attrgetter('name'))
    directories.reverse()

    # Set correct owner, mtime and filemode on directories.
    # for tarinfo in directories:
    #     dirpath = os.path.join(path, tarinfo.name)
    #     try:
    #         self.chown(tarinfo, dirpath)
    #         self.utime(tarinfo, dirpath)
    #         self.chmod(tarinfo, dirpath)
    #     except ExtractError, e:
    #         if self.errorlevel > 1:
    #             raise
    #         else:
    #             self._dbg(1, "tarfile: %s" % e)
    th.join()


class Count:

    def __init__(self):
        self.num = 0
        # self.lock = threading.Lock()

    def add(self):
        # with self.lock:
        self.num = self.num + 1

    def sub(self):
        # with self.lock:
        self.num = self.num - 1

    def set(self, cnt):
        # with self.lock:
        self.num = cnt

    def cnt(self):
        # with self.lock:
        return self.num


if __name__ == '__main__':
    start_sec = time.time()
    print("==============CMAKE_SOURCE_DIR:" + CMAKE_SOURCE_DIR)
    # extract_test2()
    # extract_test()
    count = Count()
    extract_test2(count)
    # single_thread()
    # mult_thread_test()
    end_sec = time.time()
    consume_sec = end_sec - start_sec
    # print("==============main end")
    print("\033[32m\nDone! Consumed " + str(round(consume_sec, 2)) + " seconds.\n\033[0m")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
