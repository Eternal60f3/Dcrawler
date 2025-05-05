# time: 2.5 + 1.5
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
import json
import re
from urllib.parse import urlencode
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from common import *

driver = webdriver.Chrome()
driver.get(init_url + "?" + urlencode(init_params))
input("请登录后按回车键继续...")
driver.get(init_url + "?" + urlencode(init_params))
input("已重定向，待回车继续")

cookies = driver.get_cookies()
cookies_dict = {cookie["name"]: cookie["value"] for cookie in cookies}
cookies_json = json.dumps(cookies, indent=4)
with open('cookies.json', 'w') as f:
    f.write(cookies_json)

print("cookies.json文件已保存")