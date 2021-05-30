import csv
import json
import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
# Declare constant file csv
RESULT_FILE = 'result.csv'
LINK_FILE = 'links.csv'


def get_urls():
    with open(LINK_FILE, 'r') as link_file:
        links = link_file.readlines()
    links = [link.split(',')[0] for link in links[1:]]  # remove first line and value after ','
    return links


def write_csv(data):
    fields = ['price', 'area', 'location', 'title', 'image', 'content', 'up_time', 'contact_name', 'contact_phone']
    with open(RESULT_FILE, 'w', encoding="utf-8-sig") as write_file:
        cw = csv.DictWriter(write_file, fields, delimiter=',')
        cw.writeheader()
        cw.writerows(data)

def crawler():
    links = get_urls()
    all_items = []

    if sys.platform.startswith('win'):
        executable_path = "driver/chromedriver.exe"
        with open('temp.csv', 'a', encoding='utf-8-sig') as temp_file:
            for link in links:
                chrome_options = Options()
                chrome_options.add_argument("--incognito")
                driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=executable_path)
                driver.get(link)
                time.sleep(1)
                # get the image source
                page_source = BeautifulSoup(driver.page_source, 'lxml')
                # items = page_source.find_all('')
                # html = page_source.prettify('utf-8')
                print(page_source)
                for price in page_source.findAll("i", class_="iconSave"):
                    print(price)
                    property_json = {
                        'price': price['data-price'],
                        'area': price['data-area'],
                        'location': price['data-address'],
                        'title': price['data-title'],
                        'image': price['data-avatarwap'],
                        'content': price['data-description'],
                        'up_time': price['data-updatedtime'],
                        'contact_name': price['data-contactname'],
                        'contact_phone': price['data-contactmobile']
                    }
                    writer = csv.writer(temp_file)
                    writer.writerow(property_json.values())
                    all_items.append(property_json)
                driver.close()
                time.sleep(random.randint(1, 3))
        print(all_items)
        print(len(all_items))
        write_csv(all_items)
    else:
        executable_path = "driver/chromedriver"
        with open('temp.csv', 'a', encoding='utf-8-sig') as temp_file:
            for link in links:
                chrome_options = Options()
                chrome_options.add_argument("--incognito")
                driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=executable_path)
                driver.get(link)
                time.sleep(1)
                # get the image source
                page_source = BeautifulSoup(driver.page_source, 'lxml')
                # items = page_source.find_all('')
                # html = page_source.prettify('utf-8')
                # print(page_source)
                for price in page_source.findAll("div", class_="product-item"):
                    area = price.find("span", class_="area")
                    phone = price.find("span", class_="hidden-mobile m-on-title")
                    img = price.find("img", class_="product-avatar-img")
                    contact_name = price.find("span", class_="contact_name")
                    property_json = {
                        'price': price.find("span", class_="price").text,
                        'area': area.text if area else None,
                        'location': price.find("span", class_="location").text,
                        'title': price.find("span", class_="pr-title").text,
                        'image': img['data-img'] if img else None,
                        'content': price.find("div", class_="product-content").text,
                        'up_time': price.find("span", class_="tooltip-time").text,
                        'contact_name': contact_name.text if contact_name else None,
                        'contact_phone': phone['raw'] if phone else None
                    }
                    writer = csv.writer(temp_file)
                    writer.writerow(property_json.values())
                    all_items.append(property_json)
                driver.close()
                time.sleep(random.randint(1, 3))
        print(all_items)
        print(len(all_items))
        write_csv(all_items)



if __name__ == '__main__':
    crawler()
