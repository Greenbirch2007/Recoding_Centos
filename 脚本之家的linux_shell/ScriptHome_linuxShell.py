# -*- coding:utf8 -*-

# 写个小脚本就搞定了！
import re

import pymysql
import requests
from requests.exceptions import RequestException
import time
from selenium import webdriver
from lxml import etree
import datetime


#请求

def get_first_page(url):

    req= requests.get(url)
      #  requests 中文编码的终极办法！
    if req.encoding == 'ISO-8859-1':
        encodings = requests.utils.get_encodings_from_content(req.text)
        if encodings:
            encoding = encodings[0]
        else:
            encoding = req.apparent_encoding

        # encode_content = req.content.decode(encoding, 'replace').encode('utf-8', 'replace')
        global encode_content
        encode_content = req.content.decode(encoding, 'replace')  # 如果设置为replace，则会用?取代非法字符；
        return  encode_content



def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    selector = etree.HTML(html)
    big_list = []
    # 首页
    title = selector.xpath('//*[@id="contents"]/div[2]/div[1]/div/div[3]/dl/dt/a/text()')
    link = selector.xpath('//*[@id="contents"]/div[2]/div[1]/div/div[3]/dl/dt/a/@href')



    #
    # title = selector.xpath('//*[@id="contents"]/div[2]/div[1]/div/div[2]/dl/dt/a/text()')
    # link = selector.xpath('//*[@id="contents"]/div[2]/div[1]/div/div[2]/dl/dt/a/@href')

    for i1,i2 in zip(title,link):
        big_list.append((i1,'https://www.jb51.net'+i2))

    return big_list



#存储到MySQL中

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='centos',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into ScriptHome_linuxShell (title,link) values (%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration :
        pass

if __name__ == '__main__':
    for item in range(1,2):
        url = 'https://www.jb51.net/list/list_235_'+str(item)+'.htm'
        html = get_first_page(url)
        content = parse_html(html)
        insertDB(content)
        print(url)

#
# create table ScriptHome_linuxShell(
# id int not null primary key auto_increment,
# title text,
#  link text
# ) engine=InnoDB  charset=utf8;


#  drop table ScriptHome_linuxShell;