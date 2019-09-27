#!/usr/bin/env python3
# coding=utf-8

import re
msg = '[2、霸王别姬 9.6](https://movie.douban.com/subject/1291546/)——风华绝代。'
output = re.findall('\[.+\]', msg)
print(output[0].replace('[', '').replace(']', ''))
