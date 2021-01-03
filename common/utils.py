# -*- coding: utf-8 -*-
# !/usr/bin/env python
import os
import time
import math
import urlparse2
from bs4 import BeautifulSoup
import requests
import global_var


def wait():
    time.sleep(global_var.DOWNLOAD_TICK)


def join_file_path(file_path):
    if global_var.DOWNLOAD_DIR.endswith('/'):
        return '%s%s' % (global_var.DOWNLOAD_DIR, file_path)
    else:
        return '%s/%s' % (global_var.DOWNLOAD_DIR, file_path)


def join_url_path(url, relative_url):
    return urlparse2.urljoin(url, relative_url)


def replace_blank(content):
    if isinstance(content, unicode):
        content = unicode(content)
        content = content.replace(u'\xa0', u' ')
        content = content.replace(u'\u3000', u' ')
        content = content.replace(u'\u0020', u' ')
        content = content.replace(u'\u00A0', u' ')
    return content


def fliter_urls(urls):
    urls_ = []
    for url in urls:
        if url and url not in urls_:
            urls_.append(url)
    return urls_


def download_file(url, file_path):
    file_path = join_file_path(file_path)
    print file_path, os.path.exists(file_path)
    if os.path.exists(file_path):
        return True

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'
    }
    try:
        response = requests.get(
            url, timeout=global_var.HTTP_TIMEOUT, headers=headers)
    except:
        # ERROR
        return False

    if response.status_code != 200 or not response.content:
        return False

    with open(file_path, 'wb') as f:
        f.write(response.content)

    return True


def download_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'}
    try:
        response = requests.get(
            url, timeout=global_var.HTTP_TIMEOUT, headers=headers)
    except:
        # ERROR
        return False

    if response.status_code != 200 or not response.content:
        return None

    content = response.content
    if not content:
        return content

    # .encode(global_var.LOCAL_CODE)
    return content.decode(global_var.HTML_CODE, 'ignore')


def download_bs(url, times=4):
    for _ in xrange(times):
        content = download_html(url)
        if not content:
            continue
        return BeautifulSoup(content, 'html.parser')

    return None


def write_book(book_name, strings):
    len_per_book = 300000
    content_len = sum([len(string.decode(global_var.LOCAL_CODE))
                       for string in strings])
    if not strings:
        return

    if content_len > len_per_book:
        book_count = math.ceil(float(content_len) / len_per_book)
        book_template = book_name + '%0' + \
            str(math.ceil(math.log(book_count, 10))) + 'd.txt'
        book_index, book_content_len, book_content_strings, write_tasks = 1, 0, [], []
        for string in strings:
            book_content_len += len(string.decode(global_var.LOCAL_CODE))
            book_content_strings.append(string)
            if book_content_len > len_per_book:
                write_tasks.append(
                    (join_file_path(book_template % book_index), book_content_strings))
                book_index += 1
                book_content_len, book_content_strings = 0, []
        else:
            write_tasks.append(
                (join_file_path(book_template % book_index), book_content_strings))

        for path, book_content_strings in write_tasks:
            with open(path, 'wb') as f:
                text = '\n'.join(book_content_strings)
                f.write(text)

    else:
        path = join_file_path('%s.txt' % book_name)
        with open(path, 'wb') as f:
            text = '\n'.join(strings)
            f.write(text)
