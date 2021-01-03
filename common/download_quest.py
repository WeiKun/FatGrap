# -*- coding: utf-8 -*-
# !/usr/bin/env python
import os
import utils
import global_var
import db_utils

# Quest是一个独立完成任务节点，拥有独立的done标记，除了初始的url，不需要配置任何信息，name也是独立从url提取
# Quest之前没有关系


class DownloadQuestImp(object):
    def __init__(self, url):
        pass

    def init(self):
        pass

    def has_inited(self):
        pass

    def get_name(self):
        pass

    def set_done(self):
        pass

    def has_done(self):
        pass

    def mark_do(self):
        print 'Doing Quest', self.name, self.url

    def mark_succ(self):
        print '**Done Quest %s succ!' % (self.name, )

    def mark_fail(self):
        print '**Done Quest %s fail!' % (self.url, )

    def do(self):
        pass

# Mession是非独立的任务节点，其没有独立的done标记，url只是必备的参数，也可以加入name等参数
# 互相之间的组织关系可以有父子关系跟兄弟关系以及其他任何需要的形式


class DownloadMessionImp(object):
    def __init__(self, url):
        pass

    def init(self):
        pass

    def mark_do(self):
        print 'Doing Mession', self.name, self.url

    def children(self):
        return []

    def next_brother(self):
        return None

    def do(self):
        pass


class CommicDownloadQuest(DownloadQuestImp):
    def __init__(self, url):
        self.url = url

    def init(self):
        self.bs = utils.download_bs(self.url)
        self.name = self.get_name()

    def has_inited(self):
        return hasattr(self, 'name')

    def get_name(self):
        return self.url

    def set_done(self, completed=1):
        db_utils.XlsDB.write_row(
            self.name, key=self.calc_key(), completed=completed)

    def has_done(self):
        key = self.calc_key()
        if key and db_utils.XlsDB.read_column(self.name, 'key', None) == key:
            return db_utils.XlsDB.read_column(self.name, 'completed', 0) == db_utils.XlsDB.format(1)
        else:
            return False

    def do(self):
        if not self.has_inited():
            self.init()

        if self.has_done():
            return

        if not os.path.exists(utils.join_file_path(self.name)):
            os.makedirs(utils.join_file_path(self.name).decode(global_var.LOCAL_CODE))

        self.mark_do()
        for mession in self.gen_all_messions():
            mession.do()

        self.set_done()
        self.bs = None


class CommicDownloadMession(DownloadMessionImp):
    def __init__(self, url):
        self.url = url

    def do(self):
        self.mark_do()
        pass


class BookDownloadQuest(DownloadQuestImp):
    def __init__(self, url):
        self.url = url

    def init(self):
        self.bs = utils.download_bs(self.url)
        self.name = self.get_name()
        self.set_write_handle()

    def set_write_handle(self, write_handle=utils.write_book):
        self.write_handle = write_handle

    def has_inited(self):
        return hasattr(self, 'name')

    def get_name(self):
        return self.url

    def set_done(self, completed=1):
        db_utils.XlsDB.write_row(
            self.name, key=self.calc_key(), completed=completed, name=self.name)

    def has_done(self):
        key = self.calc_key()
        if key and db_utils.XlsDB.read_column(self.name, 'key', None) == key:
            return db_utils.XlsDB.read_column(self.name, 'completed', 0) == db_utils.XlsDB.format(1)
        else:
            return False

    def do(self):
        if not self.has_inited():
            self.init()

        print 'has done', self.name, self.has_done()
        if self.has_done():
            return

        self.mark_do()
        strings = [self.name]
        for mession in self.gen_all_messions():
            strings += mession.do()

        self.write_handle(self.name, strings)
        self.set_done()
        self.bs = None


class BookDownloadMession(DownloadMessionImp):
    SHOULD_JOIN = False

    def __init__(self, url, name):
        self.url = url
        self.name = name

    def text(self):
        return ''

    def do(self):
        self.mark_do()
        self.bs = utils.download_bs(self.url)
        string = self.text()
        strings = [string]
        for mession in self.children():
            strings_ = mession.do()
            strings += strings_

        current_ = self.next_brother()
        while current_:
            strings_ = current_.do()
            strings += strings_
            current_ = current_.next_brother()

        if self.SHOULD_JOIN:
            strings = ['\n'.join(strings)]

        self.bs = None
        return strings
