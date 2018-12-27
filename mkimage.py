#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Copyright (C) 2015-2018 Shenzhen Auto-link world Information Technology Co., Ltd.
  All Rights Reserved

  Name: mkimage.py
  Purpose:

  Created By:    Clive Lau <liuxusheng@auto-link.com.cn>
  Created Date:  2018-12-25

  Changelog:
  Date         Desc
  2018-12-25   Created by Clive Lau
"""

# Builtin libraries
import os
import sys

# Third-party libraries
import paramiko

# Customized libraries


HOSTNAME = '192.168.3.249'
HOSTPORT = 22
USERNAME = 'wangyixin'
PASSWORD = '156524'

COMMON_DEST_PATH_PREFIX = '/home/wangyixin'

PUT_SRC_FILE = os.path.abspath('rear_view_camera.bin')
PUT_DEST_FILE = COMMON_DEST_PATH_PREFIX + '/imx-mkimage/iMX8QX/CM4.bin'

GET_SRC_FILE = os.path.abspath('flash.bin')
GET_DEST_FILE = COMMON_DEST_PATH_PREFIX + '/imx-mkimage/iMX8QX/flash.bin'


def usage(tips):
    print('Usage: ' + tips + ' <xxx.bin>')


class TinySsh(object):
    def __init__(self, host, port, user, pwd):
        self.hostname = host
        self.port = port
        self.username = user
        self.password = pwd
        self.ssh = None

    def connect(self):
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(
                self.hostname,
                self.port,
                self.username,
                self.password,
                allow_agent=False,
                look_for_keys=False)
            print("连接已建立")
        except Exception as e:
            print("未能连接到主机")

    def cmd(self, s):
        stdin, stdout, stderr = self.ssh.exec_command(s)
        print(stdout.read())

    def put(self, abs_local, abs_remote):
        sftp = self.ssh.open_sftp()
        sftp.put(abs_local, abs_remote)

    def get(self, abs_local, abs_remote):
        sftp = self.ssh.open_sftp()
        sftp.get(abs_remote, abs_local)

    def close(self):
        self.ssh.close()
        print("连接关闭")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage(sys.argv[0])
        exit(255)

    PUT_SRC_FILE = os.path.abspath(sys.argv[1])

    # 初始化TinySsh
    remote = TinySsh(HOSTNAME, HOSTPORT, USERNAME, PASSWORD)
    # 连接
    remote.connect()
    # 上传文件
    remote.put(PUT_SRC_FILE, PUT_DEST_FILE)
    # 执行编译
    remote.cmd('cd ' + COMMON_DEST_PATH_PREFIX + '/imx-mkimage/iMX8QX/ ; '
               './../mkimage_imx8 -soc QX -rev B0 -append mx8qx-ahab-container.img -c -scfw scfw_tcm.bin -ap u-boot-atf.bin a35 0x80000000 -data tee.bin 0x84000000 -m4 CM4.bin 0 0x34FE0000 -out flash.bin')
    # 下载文件
    remote.get(GET_SRC_FILE, GET_DEST_FILE)
    # 断开
    remote.close()
