# -*- coding:utf8 -*-

# 写个小脚本就搞定了！
import re

import pymysql

import time
from selenium import webdriver
from lxml import etree
import datetime
import requests
from requests.exceptions import RequestException


#请求

def get_first_page(url):


    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None



    # driver.set_window_size(1200, 1200)  # 设置窗口大小
    # driver.get(url)
    # html = driver.page_source
    # driver.quit()
    #
    # return html










# 用遍历打开网页59次来处理

    # print(html)  #正则还是有问题，选择了一个动态变动的颜色标记是不好的 最近浏览不是每次都有的！所以用数字的颜色取判断吧

def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    selector = etree.HTML(html)
    big_list = []
    # 首页的解析
    # title = selector.xpath('/html/body/section/div/div/article/header/h2/a/text()')
    # link = selector.xpath('/html/body/section/div/div/article/header/h2/a/@href')

    # 剩下的页数
    title = selector.xpath('/html/body/section/div/div/article/header/h2/a/text()')
    link = selector.xpath('/html/body/section/div/div/article/header/h2/a/@href')
    for i1,i2 in zip(title,link):
        big_list.append((i1,i2))


    return big_list



#存储到MySQL中

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='centos',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into linux_Yunwei (title,link) values (%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration :
        pass

if __name__ == '__main__':
    for item in range(2,513):

        url = 'https://www.centos.bz/page/'+str(item)+'/'
        html = get_first_page(url)

        content = parse_html(html)
        insertDB(content)
        print(url)


# #
# create table linux_Yunwei(
# id int not null primary key auto_increment,
# title varchar(88),
# link text
# ) engine=InnoDB  charset=utf8;


#  drop table linux_Yunwei;