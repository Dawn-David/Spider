# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 01:56:29 2020

@author: Dawn
"""

import requests
from bs4 import BeautifulSoup
import  pandas  as pd


def getHTMLText(url):
    # 使用requeats函数发送和接收响应
    # 设置header和url
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
		       'Cookie':'TY_SESSION_ID=e5b5e6fe-dc4b-45be-9a72-9ce52a79e2cd; select_city=330100; lianjia_uuid=d8087fc7-e0fb-4a89-891a-2ab83ab9db2b; _smt_uid=5e242ed9.4ccd3555; sajssdk_2015_cross_new_user=1; _ga=GA1.2.2128468659.1579429597; _gid=GA1.2.802829246.1579429597; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1579429625; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216fbd57042925-0230b87022a6e-c383f64-921600-16fbd57042c5e%22%2C%22%24device_id%22%3A%2216fbd57042925-0230b87022a6e-c383f64-921600-16fbd57042c5e%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; User-Realip=117.153.2.23; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1579444564; lianjia_ssid=d5035848-7c29-04e9-8d45-9833598d7806'
		      }
    r = requests.get(url,headers=headers)
    # 设置编码格式
    r.encoding = 'utf-8'
    
    # 使用BeautifulSoup解析HTML文档
    bs = BeautifulSoup(r.text,'lxml')
    # 用find_all函数搜索文档
    prices = bs.find_all('div',{'class':'totalPrice'})
    # 如果无参考价格，则置为0
    if len(prices) != 0:
        for price in prices:
            # tag的 .contents 属性可以将tag的子节点以列表的方式输出
            a = price.find('span').contents[0]
            if a.isdigit():
                jiage = float(a)
                print(jiage)
            else:
                jiage = 0
            break    # 以查询的第一个价格为准
    else:
        jiage = 0
    return jiage
 
if __name__ == '__main__':	
    xiaoqu = pd.read_excel('最终结果/小区_gaode.xlsx')
    price = [[]for row in range(100)]
    for index , row in xiaoqu.iterrows():
        url='https://hz.lianjia.com/xiaoqu/rs'+row['name']
        price[index] = getHTMLText(url)
    xiaoqu['price'] = price
    xiaoqu.to_excel('最终结果/小区_gaode.xlsx')

