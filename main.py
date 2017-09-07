#!/usr/bin/python3
"""
    info:一个基于关键字的google图片下载脚本
    author:qh
    date:2017/09/07
"""

import time
import os
import urllib.request
import imghdr
from PIL import Image

search_keywords = ['Raichu']
header = {}
header['User-Agent'] = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0"


# downloading the webPage by url
def download_page(url):
    req = urllib.request.Request(url, headers = header)
    response = urllib.request.urlopen(req)
    resData = str(response.read())
    return resData

# Finding 'Next Image' from the given raw page
def _images_get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:    #If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"',start_line+1)
        end_content = s.find(',"ow"',start_content+1)
        content_raw = str(s[start_content+6:end_content-1])
        return content_raw, end_content


# Getting all links with the help of '_images_get_next_image'
def _images_get_all_items(page):
    items = []
    while True:
        item, end_content = _images_get_next_item(page)
        if item == "no_links":
            break
        else:
            items.append(item)      #Append all the links in the list named 'Links'
            time.sleep(0.1)        #Timer could be used to slow down the request for image downloads
            page = page[end_content:]
    return items

# download single pic
def _images_download_items(search_keyword, index, item):
    try:
        req = urllib.request.Request(item, headers = header)
        response = urllib.request.urlopen(req)
        data = response.read()
        file_name = search_keyword + "/" + str(index + 1) + ".png"
        output_file = open(file_name, 'wb')
        output_file.write(data)
        response.close()
        output_file.close()
        
        if imghdr.what(file_name) != "png":
            new_name = search_keyword + "/" + str(index + 1) + "." + imghdr.what(file_name)
            os.rename(file_name, new_name)
            im = Image.open(new_name)
            im.save(file_name)
            os.remove(new_name)

        print("complete ======>" + str(index + 1))
        return 1
    except:
        return 0


# main function
if __name__ == '__main__':
    # start  计时器
    t0 = time.time()
    i = 0
    while i < len(search_keywords):
        items = []
        search_keyword = search_keywords[i]
        iteration = "Item no.:" + str(i+1) + " -->" + " Item name = " + str(search_keyword)
        print(iteration)
        print("Evaluating...")

        # 空格转url码(' ' - > %20)
        search = search_keyword.replace(' ', '%20')

        # create dir for search_keyword
        try:
            os.makedirs(search_keyword)
        except:
            pass

        # combine the true url address 
        url = 'https://www.google.com/search?q=' + search + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
        raw_html = download_page(url)
        time.sleep(0.1)
        items = items + (_images_get_all_items(raw_html))
        print("Total pic number : " + str(len(items)))

        count = 0
        for index,item in enumerate(items):
            if count >= 50:
                break
            count = count + _images_download_items(search_keyword, index, item)
            
        i = i + 1


