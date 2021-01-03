# -*- coding: utf-8 -*-
# !/usr/bin/env python
import sys
file_path = __file__.replace('\\', '/')
abs_path = '%s/../' % file_path[:file_path.rfind('/')]
sys.path.append(abs_path)

from common import *
from common.download_quest import BookDownloadQuest, BookDownloadMession

global_var.set_var(
    DOWNLOAD_DIR='downloads/books/2021-01',
    XLSX_NAME='example.xlsx',
    XLSX_COLUMNS=['name', 'key', 'completed'],
    HTML_CODE='gbk',
    LOCAL_CODE='gbk',
    MAX_THREAD_NUM=1,
    DEBUG_MODE=0,
)
global_var.check()
# db_utils.XlsDB.read_column('name', 'key', default)
# db_utils.XlsDB.write_row('name', key='key', completed='completed')


class BookTxtDownloadQuest(BookDownloadQuest):
    def __init__(self, url):
        self.url = url

    def init(self):
        self.bs = utils.download_bs(self.url)
        self.name = self.get_name()
        self.set_write_handle()

    def set_write_handle(self, write_handle=utils.write_book):
        self.write_handle = write_handle

    def get_name(self):
        return self.bs.find('meta', property='og:title').attrs['content'].encode(global_var.LOCAL_CODE)

    def set_done(self, completed=1):
        db_utils.XlsDB.write_row(
            self.name, key=self.calc_key(), completed=completed)

    def has_done(self):
        key = self.calc_key()
        if key and db_utils.XlsDB.read_column(self.name, 'key', None) == key:
            return db_utils.XlsDB.read_column(self.name, 'completed', 0) == 1
        else:
            return False

    def calc_key(self):
        return self.bs.find('meta', property='og:novel:update_time').attrs['content'].encode(global_var.LOCAL_CODE)

    def gen_all_messions(self):
        messions = []
        div = list(self.bs.find_all('div', class_='box_con'))[1]
        dl = div.find('dl')
        dt_count = 0
        for node in dl:
            if type(node).__name__ != 'Tag':
                continue

            if node.name == 'dt':
                dt_count += 1

            if dt_count != 2 or node.name != 'dd':
                continue

            a = node.find('a')
            href = a.attrs['href']
            mession = BookTxtDownloadMession(utils.join_url_path(
                self.url, href), a.string.encode(global_var.LOCAL_CODE))
            messions.append(mession)

        messions = messions[:5]
        return messions

    def mark_do(self):
        print 'Doing Quest', self.name, self.url


class BookTxtDownloadMession(BookDownloadMession):
    SHOULD_JOIN = False

    def __init__(self, url, name):
        self.url = url
        self.name = name

    def mark_do(self):
        print 'Doing Mession', self.name, self.url

    def text(self):
        nodes = self.bs.find('div', id='content')
        content = '%s\n' % (self.name)
        for node in nodes:
            typeName = type(node).__name__
            if typeName == 'NavigableString':
                lineStr = utils.replace_blank(node.string)
                lineStr = lineStr.encode(global_var.LOCAL_CODE)
                if not lineStr.startswith('请记住本书首发域名') and lineStr.strip(' '):
                    lineStr = lineStr + '\n'
                    lineStr = lineStr.replace('        ', '  ')
                    content += lineStr

            elif typeName == 'Tag':
                if node.name == 'br':
                    pass
                pass
        content = content
        return content


print 'TEST BEGIN'
db_utils.XlsDB.init()
quest = BookTxtDownloadQuest('https://www.booktxt.net/7_7810/')
quest.init()
quest.set_done(0)
main_utils.main_multi_thread([
    BookTxtDownloadQuest('https://www.booktxt.net/7_7810/'),
    BookTxtDownloadQuest('https://www.booktxt.net/2_2096/'),
])
print 'TEST END'
