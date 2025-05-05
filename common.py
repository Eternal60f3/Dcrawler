import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlencode
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

experience_require = {
    "完全不限": "",
    "在校生": "108",
    "应届生": "102",
    "社招且经验不限": "101",
    "1年以下": "103",
    "1-3年": "104",
    "3-5年": "105",
    "5-10年": "106",
    "10年以上": "107",
}

citys = {
    # "全国": "100010000",
    "北京": "101010100",
    "上海": "101020100",
    "广州": "101280100",
    "深圳": "101280600",
    "杭州": "101210100",
    "成都": "101270100",
    "武汉": "101200100",
    "西安": "101110100",
    "南京": "101190100",
    "天津": "101030100",
    "重庆": "101040100",
    "郑州": "101180100",
    "厦门": "101230200",
    "长沙": "101250100",
}

init_url = "https://www.zhipin.com/web/geek/jobs"
init_params = {
    "city": "100010000",  # 全国
    "position": "100102",  # c++岗位
    "experience": experience_require["完全不限"],  # 经验要求
}