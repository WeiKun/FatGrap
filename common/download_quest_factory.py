# -*- coding: utf-8 -*-
# !/usr/bin/env python

# 最基础的QuestFactory就是List of Quest，但是对于比较复杂的情况，不能在初始阶段就拿到所有Quest，此时需要一个特殊的迭代器Factory
# 例如：
#     想下载一个小说网站的所有小说的时候，这时候第一页是看不到所有的小说链接的，需要一页一页地拿，并且应该先将第一页的拿到并且开始执行
# 再去拉下一页的小说
# 再例如：
#     对于长篇漫画，不能单个漫画作为一个Quest(因为有上千集)，这时候需要根据漫画总地址找到每一集的地址，然后创建成任务
class DownloadQuestFactoryImp(object):
    def __init__(self, quest_class):
        self.quest_class = quest_class

    def __iter__(self):
        return self.__call__()

    def __call__(self):
        current_ = self
        while current_:
            for quest_args in current_.children():
                if not quest_args:
                    continue

                yield self.quest_class(quest_args)

            current_ = current_.next_brother()

    def next_brother(self):
        return None

    def children(self):
        return []


class DownloadQuestList(DownloadQuestFactoryImp):
    def __init__(self, quest_class, urls):
        self.quest_class = quest_class
        self.urls = urls

    def __iter__(self):
        return self.__call__()

    def next_brother(self):
        return None

    def children(self):
        return self.urls
