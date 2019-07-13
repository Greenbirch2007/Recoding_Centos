
# -*- coding:utf8 -*-

# 写个小脚本就搞定了！
import re

import pymysql

import time
from requests.exceptions import ConnectionError
from selenium import webdriver
from lxml import etree
import datetime

import pyautogui





def next_page():
    for i in range(1,457):  # selenium 循环翻页成功！
        driver.find_element_by_xpath('//*[@id="pages"]/a[last()]').click()
        time.sleep(1)
        html = driver.page_source
        return html




#存储到MySQL中

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='centos',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into us_stock (name,code,industry,market_value) values (%s,%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration :
        pass

if __name__ == '__main__':

    big_list = []

    url = 'https://www.centoschina.cn/command'  # 直接到登录界面！
    driver = webdriver.Firefox()
    driver.get(url)

    while True:

        time.sleep(2)  # 每三秒往下翻一页
        pyautogui.keyDown("down")  # 下翻页成功！
        html = driver.page_source
        selector = etree.HTML(html)
        big_list = []
        title = selector.xpath('//*[@id="scroll"]/section/ul/li/article/h2/a/text()')
        link = selector.xpath('//*[@id="scroll"]/section/ul/li/article/h2/a/@href')

        long_tuple = (i for i in zip(title, link))
        for i in long_tuple:
            big_list.append(i)
        #
        # connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456',
        #                              db='centos',
        #                              charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        # cursor = connection.cursor()
        # cursor.executemany('insert into Mingling (tite,link) values (%s,%s)', big_list)
        # connection.commit()
        # connection.close()
        # print('向MySQL中添加数据成功！')
        print(big_list)





# #
# create table Mingling(
# id int not null primary key auto_increment,
# title varchar(88),
# link text
# ) engine=InnoDB  charset=utf8;


#  drop table us_stock;