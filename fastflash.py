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
import re
import sys
import time
import platform
import commands
import subprocess

# Third-party libraries
import serial

# Customized libraries


SERIAL_PORT_WINDOWS = 'COM5'
SERIAL_PORT_UNIX = '/dev/ttyUSB0'
SERIAL_BAUDRATE = 115200


def is_windows_os():
    return platform.system() == 'Windows'


def get_status_output(cmd):
    output = ''
    if is_windows_os():
        try:
            status = subprocess.call(cmd)
            if not status:
                output = subprocess.check_output(cmd)
        except WindowsError:
            status = 255
            output = ''
    else:
        try:
            (status, output) = commands.getstatusoutput(cmd)
        except Exception:
            status = 255
            output = ''
    return status, output


def reboot_by_uart(port, baudrate):
    ser = serial.Serial(port, baudrate)
    while True:
        ser.write('\n')
        line = ser.readline()
        print(line)
        if re.search(b'=>', line):
            ser.write('fastboot 0\n')
            break
        elif re.search(b'console:/', line):
            ser.write('reboot bootloader\n')
            break
        time.sleep(1)
        ser.flush()
    ser.close()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        if is_windows_os():
            SERIAL_PORT = SERIAL_PORT_WINDOWNS
        else:
            SERIAL_PORT = SERIAL_PORT_UNIX
    else:
        SERIAL_PORT = sys.argv[1]

    reboot_by_uart(SERIAL_PORT, SERIAL_BAUDRATE)

    status, output = get_status_output('fastboot flash bootloader0 flash.bin')
    print(output)

    status, output = get_status_output('fastboot reboot')
    print(output)
