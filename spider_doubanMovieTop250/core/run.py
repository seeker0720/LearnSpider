#!/usr/bin/env python3
# coding=utf-8

"""
@Author：seeker0720
@File：run.py
@Date：2019/9/28 0:30
"""
import requests
from bs4 import BeautifulSoup
import os, sys
import re


def get_movie_info_tags(urls):
    title_list = []
    rating_num_list = []
    img_src_list = []
    quote_list = []

    for url in urls:
        # 发送请求，获得网页
        web_data = requests.get(url)
        # 解析网页
        soup = BeautifulSoup(web_data.text, 'lxml')
        # 将所需要的信息提取到列表中
        title_list.extend((soup.select('div.hd > a')))
        rating_num_list.extend(soup.select('span.rating_num'))
        img_src_list.extend(soup.select('img[width="100"]'))
        quote_list.extend(soup.select('span.inq'))
    return title_list, rating_num_list, img_src_list, quote_list


def get_movie_info(urls):
    title_list, rating_num_list, img_src_list, quote_list = get_movie_info_tags(urls)
    movie_info_list = []
    img_url_list = []
    rank_value = 0
    for title, rating_num, img_src, quote in zip(title_list,
                                                 rating_num_list,
                                                 img_src_list,
                                                 quote_list):
        rank_value += 1
        movie_title = list(title.stripped_strings)
        rate_num = rating_num.get_text()
        img_url = img_src.get('src')
        quote = quote.get_text()
        movie_url = title.get('href')

        movie_info = f'[{rank_value}、{movie_title[0]} {rate_num}]({movie_url})——{quote}'

        movie_info_list.append(movie_info)
        img_url_list.append(img_url)
    return movie_info_list, img_url_list


def output_movie_info_file(urls):
    # 输出含有电影信息的markdown文件
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)

    fi = open(f'{BASE_DIR}\docs\豆瓣电影top250URL.md', 'w', encoding='utf8')

    movie_info_list, img_url_list = get_movie_info(urls)
    for movie_info, img_url in zip(movie_info_list, img_url_list):
        info = f'{movie_info}\n\n![]({img_url})\n\n'
        fi.write(info)


def download_img(urls):
    # 下载电影的海报
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)
    movie_info_list, img_url_list = get_movie_info(urls)
    for movie_info, img_url in zip(movie_info_list, img_url_list):
        img_title = re.findall('\[.*\]', movie_info)[0].replace('[', '').replace(']', '')
        img = requests.get(img_url)
        with open(f'{BASE_DIR}\download\pictures\\{img_title}.jpg', 'wb') as f:
            f.write(img.content)
        print(f'{img_title} is ok...')


if __name__ == '__main__':
    url_list = ['https://movie.douban.com/top250?start=' + str(i) +
                '&filter' for i in range(0, 250, 25)]
    print('Please wait a minutes...')
    output_movie_info_file(urls=url_list)
    print('Ok')
    download_img(urls=url_list)

