#!/usr/bin/env python3
# coding=utf-8

"""
@File：test_download_movie_info.py
@Author：seeker0720
@Date：2019/9/28 23:02
@Instructions:
"""
from unittest import TestCase
from spider_doubanMovieTop250.core import run
import os


class TestDownload_movie_info(TestCase):
    def test_download_movie_info(self):
        urls = ['https://movie.douban.com/top250?start=' + str(i) +
                '&filter' for i in range(0, 250, 25)]
        s = run.download_movie_info(urls=urls)
        os.system('cd ..&cd download&cd pictures&del *.jpg')
        os.system('cd ..&cd docs&del 豆瓣电影top250.md')

    def test_demo(self):
        self.fail()
