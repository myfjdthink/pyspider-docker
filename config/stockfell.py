#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-09-16 03:50:31
# Project: stockfeel

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
        'proxy': '10.10.21.2:1087'
    }

    @every(minutes=24 * 60)
    def on_start(self):
        items = {
            'fund':'https://www.stockfeel.com.tw/category/fund-knowledge/page/${page}/?tag=mutualfund-knowledge',
            'stock':'https://www.stockfeel.com.tw/category/stock-basic/page/${page}/?tag=stock-learning',
            'allocation':'https://www.stockfeel.com.tw/category/asset-allocation/page/${page}/'
        }
        for key, value in items.items(): 
            self.cat = key
            self.multi_page(value)
                
                
    @catch_status_code_error
    def multi_page(self, url):
        for i in range(2):
            page = url.replace('${page}', str(i+1))
            print('range', i, page)
            self.crawl(page, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        print('hello')
        for each in response.doc('div.prefix-post-category .row .post-info > a[href^="https"], div.prefix-post-category.row .post-info > a[href^="https"]').items():
            print(each('div.post-title').text())
            print(each.attr.href)
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        image = response.doc('body > div.wapper > div.container.single-content > div > div > div.sin-banner')
        image_url = image.attr('style').replace("background-image:url('", "").replace("');", "")
        title = response.doc('body > div.wapper > div.container.single-content > div > div > div.sin-content-wrapper > div > h1')
        content = response.doc('body > div.wapper > div.container.single-content > div > div > div.sin-content-wrapper > article > div')
        content.remove('span')
        content.remove('ul')
        
        category = response.doc('body > div.wapper > div.container.single-content > div > div > div.sin-content-wrapper > div > div > a > span').text()
        
        date = response.doc('body > div.wapper > div.container.single-content > div > div > div.sin-content-wrapper > div > p:nth-child(3)').text()
        date = '201' + date.replace(' ', '').split('201')[1]
        
        iamge_urls = []
        images = content('img')
        # images = response.doc('body > div.wapper > div.container.single-content > div > div > div.sin-content-wrapper > div > div > a > span > p > img')
        for each in images.items():
            iamge_urls.append(each.attr('src'))
            # print(each.attr('src'))
  
        return {
            "date":date,
            "category": category,
            "poster": image_url,
            "iamges": iamge_urls,
            "url": response.url,
            "title": title.text(),
            "content": content.outerHtml() 
        }

        
        
    
    
