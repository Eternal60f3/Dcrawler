# time: 7 18:30start

from common import *
from database import *
from single_job_detail import *
from ip_switch import *

import json


if __name__ == "__main__":
    job_data_manager = JobDataManager()
    node_idx = 0

    with open("info.html", "r", encoding="utf-8") as f:
        html_text = f.read()

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
            ob_info = get_job_detail(job_link)
            if ob_info:
                job_data_manager.add_job(ob_info)
        except Exception as e:
            print(f"Error processing job: {e}")