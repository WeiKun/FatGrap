# -*- coding: utf-8 -*-
# !/usr/bin/env python
import sys
file_path = __file__.replace('\\', '/')
abs_path = '%s/../' % file_path[:file_path.rfind('/')]
sys.path.append(abs_path)

from common import *
from common.download_quest import BookDownloadQuest, BookDownloadMession
from common.download_quest_factory import DownloadQuestUrls

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
    def get_name(self):
        return self.bs.find('meta', property='og:title').attrs['content'].encode(global_var.LOCAL_CODE)

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
        # 测试时可以只取前几个mession，早点发现错误
        return messions


class BookTxtDownloadMession(BookDownloadMession):
    SHOULD_JOIN = False

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
urs = [None for _ in xrange(1000)]

urs[0] = '''
https://www.booktxt.net/7_7810/
'''

urs[1] = '''
https://www.booktxt.net/2_2096/
'''

urs[2] = '''
'''

main_utils.main_multi_thread(DownloadQuestUrls(BookTxtDownloadQuest, urs))

print 'TEST END'
