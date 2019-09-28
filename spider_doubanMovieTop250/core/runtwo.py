#!/usr/bin/env python3
# coding=utf-8

"""
@File：runtwo.py
@Author：seeker0720
@Date：2019/9/28 19:05
@Instructions: 异步爬虫，用时10s左右
"""
from gevent import monkey
monkey.patch_all()
# 用于添加程序中所有的io操作!!!
import requests
from bs4 import BeautifulSoup
import os, sys
import gevent
import time


def download_movie_info(url):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)
    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text, 'lxml')
    rank_value_list = soup.select('div.pic > em')
    movie_tile_list = soup.select('div.hd > a')
    rating_num_list = soup.select('span.rating_num')
    quote_list = soup.select('span.inq')
    img_src_list = soup.select('img[width="100"]')
    for rank_value, movie_tile, rating_num, quote, img_src in zip(rank_value_list,
                                                                  movie_tile_list,
                                                                  rating_num_list,
                                                                  quote_list,
                                                                  img_src_list):
        rank_value = rank_value.get_text()
        movie_name = list(movie_tile.stripped_strings)[0]
        rating_num = rating_num.get_text()
        movie_url = movie_tile.get('href')
        quote = quote.get_text()

        img_url = img_src.get('src')


        movie_info = f'[{rank_value}.{movie_name} {rating_num}]({movie_url}) ——{quote}'
        info = f'{movie_info}\n\n![]({img_url})\n\n'
        # with open(f'{BASE_DIR}\docs\豆瓣电影top250.md', 'w+', encoding='utf8') as f:
        #     f.write(info)
        img_title = f'{rank_value}.{movie_name}.jpg'
        # print(info)
        img = requests.get(img_url)
        with open(f'{BASE_DIR}\download\pictures\{img_title}', 'wb') as f:
            f.write(img.content)
            print(f'{img_title} ...')
        # print(img_url)


if __name__ == '__main__':
    start_time = time.time()
    gevent.joinall([
        gevent.spawn(download_movie_info,
                     f'https://movie.douban.com/top250?start={str(i)}&filter') for i in range(0, 250, 25)])
    end_time = time.time()
    cost_time = end_time - start_time
    print(f'用时：{cost_time}')

