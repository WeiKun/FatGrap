# -*- coding: utf-8 -*-
# !/usr/bin/env python
import os

# 声明公共变量，由使用者来具体定义
DEBUG_MODE = 0
DOWNLOAD_TICK = 0.5
DOWNLOAD_DIR = ''
HTML_CODE = 'utf-8'
LOCAL_CODE = 'utf-8',
HTTP_TIMEOUT = 5
XLSX_NAME = ''
XLSX_COLUMNS = []
MAX_THREAD_NUM = 20

# check函数保证不能有必填变量未定义


def check():
    assert DOWNLOAD_DIR, 'DOWNLOAD_DIR 未定义'
    assert XLSX_NAME, 'XLSX_NAME 未定义'


def set_var(**kw):
    vars = globals()
    vars.update(kw)
    dir_path = vars['DOWNLOAD_DIR']
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
