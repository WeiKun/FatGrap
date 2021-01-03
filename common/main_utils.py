# -*- coding: utf-8 -*-
# !/usr/bin/env python
import utils
import global_var
import threading
import traceback


def do_single_quest(quest):
    ret = None
    stack = ''
    try:
        ret = quest.do()
    except:
        stack = traceback.format_exc()
    return ret, stack


def main_single_thread_for_test(factory):
    for quest in factory:
        _, stack = do_single_quest(quest)

        if stack:
            quest.mark_fail()
            print stack
            return
        else:
            quest.mark_succ()


def main_single_thread(factory):
    for quest in factory:
        _, stack = do_single_quest(quest)
        if stack:
            quest.mark_fail()
            print stack
        else:
            quest.mark_succ()


class thread_quest(object):
    """"""

    def __init__(self, quest):
        self.ret = None
        self.stack = ''
        self.quest = quest
        self.done = 0
        self.thread = None

    def has_done(self):
        return self.done == 1

    def set_done(self, done=1):
        self.done = done
        self.set_thread(None)

    def set_thread(self, thread=None):
        self.thread = thread

    def do(self):
        try:
            self._do()
        except Exception as exception:
            traceback.print_exc()
            self.set_done()
            raise exception

    def _do(self):
        if self.has_done():
            return

        self.ret, self.stack = do_single_quest(self.quest)

        self.set_done()

    def colloct(self):
        if self.stack:
            self.quest.mark_fail()
            print self.stack
        else:
            self.quest.mark_succ()


def main_multi_thread(factory):
    thread_handle_list = []
    for quest in factory:
        while len(thread_handle_list) >= global_var.MAX_THREAD_NUM:
            for quest_handle in thread_handle_list:
                if quest_handle.has_done():
                    quest_handle.colloct()
            thread_handle_list = [
                quest_handle for quest_handle in thread_handle_list if not quest_handle.has_done()]
            utils.wait()
            continue

        quest_handle = thread_quest(quest)
        thread = threading.Thread(target=quest_handle.do, args=())
        thread.start()
        quest_handle.set_thread(thread)
        thread_handle_list.append(quest_handle)
        utils.wait()

    while thread_handle_list:
        utils.wait()
        for quest_handle in thread_handle_list:
            if quest_handle.has_done():
                quest_handle.colloct()
        thread_handle_list = [
            quest_handle for quest_handle in thread_handle_list if not quest_handle.has_done()]
