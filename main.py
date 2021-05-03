import csv
import json
import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
    with open('temp.csv', 'a', encoding='utf-8-sig') as temp_file:
        for link in links:
            chrome_options = Options()
            chrome_options.add_argument("--incognito")
            driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='driver/chromedriver.exe')
            driver.get(link)
            time.sleep(1)
            # get the image source
            page_source = BeautifulSoup(driver.page_source, 'lxml')
            # items = page_source.find_all('')
            # html = page_source.prettify('utf-8')
            for price in page_source.findAll("i", class_="iconSave"):
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


if __name__ == '__main__':
    crawler()
