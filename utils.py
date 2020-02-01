# -*- coding:utf-8 -*-
'''
@project: SecKillWeb
@file: utils.py
@author: kael
@contact: https://github.com/kaelsunkiller
@time: 2020-01-31(星期五) 19:17
@Copyright © 2020. All rights reserved.
'''
import sys
import os
import time
import logging
import ctypes
import inspect
import subprocess
from pathlib import Path


def create_logger(loggername:str='logger', levelname:str='DEBUG', console_levelname='INFO'):
    levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    logger = logging.getLogger(loggername)
    logger.setLevel(levels[levelname])

    logger_format = logging.Formatter("[%(asctime)s][%(levelname)s][%(filename)s][%(funcName)s][%(lineno)03s]: %(message)s")
    console_format = logging.Formatter("[%(levelname)s] %(message)s")

    handler_console = logging.StreamHandler()
    handler_console.setFormatter(console_format)
    handler_console.setLevel(levels[console_levelname])

    path = Path(__file__).parent/'logs' # 日志目录
    path.mkdir(parents=True, exist_ok=True)
    today = time.strftime("%Y-%m-%d")     # 日志文件名
    common_filename = path / f'{today}.log'
    handler_common = logging.FileHandler(common_filename , mode='a+', encoding='utf-8')
    handler_common.setLevel(levels[levelname])
    handler_common.setFormatter(logger_format)

    logger.addHandler(handler_console)
    logger.addHandler(handler_common)

    return logger


def open_file_os(file_path):
    platform = sys.platform
    if platform.startswith('win'):
        os.startfile(file_path)
    elif platform.startswith('linux'):
        subprocess.call(['xdg-open', file_path])
    elif platform.startswith('darwin'):
        subprocess.call(['open', file_path])
