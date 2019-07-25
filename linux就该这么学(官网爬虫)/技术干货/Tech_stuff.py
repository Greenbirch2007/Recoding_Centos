# -*- coding:utf8 -*-

# 写个小脚本就搞定了！
import re

import pymysql
from selenium import webdriver
from lxml import etree
import datetime
from selenium import webdriver
from lxml import etree
import datetime
driver = webdriver.Chrome()

#请求

def get_first_page(url):
    driver.set_window_size(1200, 1200)  # 设置窗口大小
    driver.get(url)
    # time.sleep(3)
    html = driver.page_source
    # time.sleep(3)
    return html


def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    selector = etree.HTML(html)
    big_list = []
    # 首页
    title = selector.xpath('//*[@id="article-list"]/div/section[1]/center/div/h1/a/span/text()')
    link = selector.xpath('//*[@id="article-list"]/div/section[1]/center/div/h1/a/@href')


    for i1,i2 in zip(title,link):
        big_list.append((i1,i2))

    return big_list



#存储到MySQL中

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='centos',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into Tech_stuff (title,link) values (%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration :
        pass



if __name__ == '__main__':
    for item in range(1,146):
        url ='https://www.linuxprobe.com/thread/page/'+str(item)
        html = get_first_page(url)
        content = parse_html(html)
        insertDB(content)
        print(datetime.datetime.now())
#
# create table Tech_stuff(
# id int not null primary key auto_increment,
# title text,
#  link text
# ) engine=InnoDB  charset=utf8;


#  drop table Tech_stuff;