# time: 7 18:30start

from common import *
from database import *
from single_job_detail import *

import json

def add_cookies(driver):
    with open('cookies.json', 'r') as f:
        cookies = json.load(f)

    # 添加 cookies 到浏览器
    for cookie in cookies:
        driver.add_cookie(cookie)


def scroll(driver, element, wait):
    # 滚动到页面底部
    # while True:
    # 记录当前高度
        # prev_height = driver.execute_script("return arguments[0].scrollHeight", element)
        # # 滑动到底部
        # driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element)
        # # 等待加载
        # # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.job-list-container")))
        # time.sleep(10)
        # # 检查新高度
        # new_height = driver.execute_script("return arguments[0].scrollHeight", element)
        # # 如果高度不再变化，退出循环
        # if new_height == prev_height:
        #     break

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)", element)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.job-list-container")))

if __name__ == "__main__":
    job_data_manager = JobDataManager()

    # while True:
    while True:
        try:
            for city, code in citys.items():
                driver = get_clean_driver()

                init_params['city'] = code
                driver.get(init_url + "?" + urlencode(init_params))
                # add_cookies(driver)

                wait = WebDriverWait(driver, 100)  # 等待页面加载完成
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.job-list-container")))

                # 滚动获取全部职位信息
                # job_list_container = driver.find_element(By.CSS_SELECTOR, "ul.rec-job-list")
                # scroll(driver, job_list_container, wait)

                html_text = driver.page_source

                soup = BeautifulSoup(html_text, "html.parser")

                jobs = soup.select("div.card-area")
                print(f"找到 {len(jobs)} 个职位")
                cnt = 0
                for job in jobs:
                    cnt += 1
                    print(f"正在处理第 {cnt} 个职位")
                    # 获取每个职位的链接
                    # job_link = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                    try: 
                        job_link = job.select_one("a").get("href")
                        # print(job_link)
                        # 获取职位详情
                        job_link = "https://www.zhipin.com" + job_link
                        ob_info = get_job_detail(job_link)
                        if ob_info:
                            job_data_manager.add_job(ob_info)
                    except Exception as e:
                        print(f"Error processing job: {e}")
                        # job_data_manager.save()

                # job_data_manager.save()
                driver.quit()

            time.sleep(1000) 
        except Exception as e:
            continue