# -*- coding: utf-8 -*-
# !/usr/bin/env python
import sys
file_path = __file__.replace('\\', '/')
abs_path = '%s/../' % file_path[:file_path.rfind('/')]
sys.path.append(abs_path)

from common import global_var, utils, db_utils, main_utils
from common.download_quest import CommicDownloadQuest, CommicDownloadMession
from common.download_quest_factory import DownloadQuestUrls

global_var.set_var(
    DOWNLOAD_DIR='downloads/commic/2021-01',
    XLSX_NAME='example.xlsx',
    XLSX_COLUMNS=['name', 'key', 'completed', 'url'],
    HTML_CODE='utf-8',
    LOCAL_CODE='gb18030',
    MAX_THREAD_NUM=4,
    HTTP_TIMEOUT=10,
    DOWNLOAD_TICK=1,
    DEBUG_MODE=0,
)
global_var.check()


class CommicSomeDownloadQuest(CommicDownloadQuest):
    def __init__(self, url):
        self.url = url

    def get_name(self):
        # 读取name，并且做出一些需要的处理
        name = unicode(self.bs.find('title').string)
        if u'\xbb' in name:
            name = name[:name.find(u'\xbb') + len(u'\xbb') - 1]
            name = name.strip(u' ')
        while name[0] == '[':
            index = name.find(']')
            if index == -1:
                break

            name = u'%s(%s)' % (name[index + 1:], name[1:index])
            name = name.strip(u' ')
        return name.encode(global_var.LOCAL_CODE)

    def calc_key(self):
        # 类似用更新时间的东西做key
        return self.bs.find('xxxx', yyyy='zzzz').find('time').string.encode(global_var.LOCAL_CODE)

    def gen_all_messions(self):

        messions = []
        for div in self.bs.find_all('div', class_='thumb-container'):
            url = div.find('img').attrs['data-src']
            url = url.replace('xxxxxx', 'yyyyy')
            url = url.replace('t.jpg', '.jpg')
            url = url.replace('t.png', '.png')
            name = url[url.rfind('/') + 1:]
            # 这里的处理只是个示例，目的是拿到需要下载的漫画图片的url、name、希望下载后保存的本地路径
            messions.append(CommicSomeDownloadMession(url, name, '%s/%s' % (self.name, name.encode(global_var.LOCAL_CODE))))
        return messions


class CommicSomeDownloadMession(CommicDownloadMession):
    def __init__(self, url, name, path):
        self.url = url
        self.name = name
        self.path = path

    def do(self):
        self.mark_do()
        utils.download_file(self.url, self.path)


print 'TEST BEGIN'
db_utils.XlsDB.init()

# factroy = CommicSomeDownloadQuestFactory(CommicSomeDownloadQuest, 'https://xxxx/yyyy/zzzz/')
urs = [None for _ in xrange(1000)]

urs[0] = '''
'''

urs[1] = '''
'''

urs[2] = '''
'''

main_utils.main_multi_thread(DownloadQuestUrls(CommicSomeDownloadQuest, urs))

print 'TEST END'
