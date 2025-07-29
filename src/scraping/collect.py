from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

service = Service(ChromeDriverManager().install())
options = Options()
options.add_argument("--disable-javascript")
# options.add_argument("--headless")

def openbrowser(locid, key):
    driver = webdriver.Chrome(service=service, options=options)
    driver.wait = WebDriverWait(driver, 1)
    driver.maximize_window()
    
    words = key.split()
    txt = ''    
    for w in words:
        txt += (w + '+')
    
    driver.get("https://www.glassdoor.co.in/Job/jobs.htm?suggestCount=0&suggestChosen=true&clickSource=searchBtn&typedKeyword={}&sc.keyword={}&locT=C&locId={}&jobType=fulltime&fromAge=1&radius=6&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0".format(txt[:-1], txt[:-1], locid))
    return driver

def geturl(driver):
    url = set()
    while True:
        if len(url) >= 20:
            break
        soup1 = BeautifulSoup(driver.page_source, "lxml")
        
        main = soup1.find_all("li", {"class": "JobsList_jobListItem__wjTHv"})
        
        for m in main:
            url.add('https://www.glassdoor.co.in{}'.format(m.find_all('a')[1]['href']))       
        try:
            next_element = soup1.find("li", {"class": "next"})
            try:
                next_exist = next_element.find('a')
            except AttributeError:
                driver.quit()
                break
            except NoSuchElementException:
                driver.quit()
                break
            if next_exist:
                driver.find_element(By.CLASS_NAME, "next").click()
                time.sleep(2)
            else:
                driver.quit()
                break
        except ElementClickInterceptedException:
            pass
        
    return list(url)

def fetch_job_urls(locid, key):
    driver = openbrowser(locid, key)
    job_urls = geturl(driver)
    driver.quit()
    return job_urls

locid_key_pairs = [
    (2940587, 'Cloud Solutions Architect'),
    (2940587, 'Data Scientist'),
    (2940587, 'Software Engineer'),
    (2940587, 'Full Stack Developer'),
]

def main():
    all_job_urls = []

    for locid, key in locid_key_pairs:
        print(f"Fetching URLs for locid {locid} with key '{key}'...")
        job_urls = fetch_job_urls(locid, key)
        all_job_urls.extend(job_urls)

    with open('jd_urls.json', 'w') as f:
        json.dump(all_job_urls, f, indent=4)
        print("File created with all job URLs.")

if __name__ == "__main__":
    main()