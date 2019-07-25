# -*- coding:utf8 -*-

# 写个小脚本就搞定了！
import re

import pymysql
import datetime
from selenium import webdriver
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


def parse_html(html):  #必须要用正则
    big_list=[]
    patt = re.compile('<a rel="bookmark" href="(.*?)">(.*?)</a>',re.S)
    items = re.findall(patt,html)
    for item in items:
        big_list.append(item)

    return big_list





#存储到MySQL中

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='centos',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into AllOrders (link,title) values (%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration :
        pass



if __name__ == '__main__':
    # url = 'https://www.linuxcool.com/category/device'

    for item in range(1,3):

        url ='https://www.linuxcool.com/category/other/page/'+str(item)
        html = get_first_page(url)
        content = parse_html(html)
        insertDB(content)
        print(datetime.datetime.now())



# create table AllOrders(
# id int not null primary key auto_increment,
# link text,
# title text
# ) engine=InnoDB  charset=utf8;


#  drop table AllOrders;

