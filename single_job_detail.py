from common import *

import hashlib
import re

def get_job_detail(url):
    # 设置无头模式
    boss = webdriver.Chrome()
    boss.get(url)

    wait = WebDriverWait(boss, 10)  # 等待页面加载完成
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.job-detail")))
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.sider-company")))

    job_info = {}

    html_text = boss.page_source
    with open("job_detail.html", "w", encoding="utf-8") as f:
        f.write(html_text)

    soup = BeautifulSoup(html_text, "html.parser")
    
    if soup.select_one("div.sider-company") is None:
        return None

    # TODO job.status 获取，用于判断是否已失效
    try: 
        info_primary = soup.select_one("div.info-primary")
        job_info["title"] = info_primary.select_one("h1").text.strip()
        job_info["salary"] = info_primary.select_one("span.salary").text.strip()
        job_info["position"] = info_primary.select_one("a.text-desc.text-city").text.strip()
        job_info["experience"] = info_primary.select_one(
            "span.text-desc.text-experiece"
        ).text.strip()
        job_info["degree"] = info_primary.select_one("span.text-desc.text-degree").text.strip()

        job_box = soup.select_one("#main > div.job-box > div > div.job-detail")
        job_tags = job_box.select_one("ul.job-keyword-list")
        job_info["tags"] = ",".join([
            tag.text.strip() for tag in job_tags.select("li") if tag.text.strip() != ""
        ])
        job_info["describe"] = job_box.select_one("div.job-sec-text").text.strip()

        job_boss = soup.select_one("div.sider-company")
        job_info["company_name"] = job_boss.select_one("div > a:nth-child(2)").text.strip() # TODO 更改定位方式，而不是使用固定索引
        # job_info["scale"] = job_boss.select_one("p:nth-child(4)").text.strip()

        p_tags = job_boss.find_all("p")
        for p_tag in p_tags:
            if "人" in p_tag.text:
                job_info["scale"] = p_tag.text.strip()
                break
        else:
            job_info["scale"] = "未找到规模信息"

        job_info["industry"] = soup.select_one("a[ka='job-detail-brandindustry']").text.strip()

        combined_string = job_info["title"] + job_info["describe"] + job_info["company_name"] + job_info["tags"]
        job_info["Idx"] = hashlib.md5(combined_string.encode('utf-8')).hexdigest()

    except AttributeError as e:
        print(f"Error parsing job details: {e}")
        return job_info

    print(job_info)

    boss.quit()
    return job_info
