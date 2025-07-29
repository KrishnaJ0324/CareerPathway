import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
service = Service(ChromeDriverManager().install())

options = Options()
options.add_argument("--disable-javascript")
# options.add_argument("--headless")

# Initialize the driver with the options
driver = webdriver.Chrome(service=service, options=options)

with open('jd_urls.json', 'r') as f:
    url = json.load(f)

data = {}
i = 1
jd_df = pd.DataFrame()

for u in tqdm(url):
    driver.wait = WebDriverWait(driver, 2)
    driver.maximize_window()
    driver.get(u)
    soup = BeautifulSoup(driver.page_source, "lxml")
    try:
        position = soup.find('h1').text
        company = soup.find('h4').text
        location = soup.find('div', {'data-test': 'location'}).text
        sections = soup.find_all('section')
        second_section = sections[1] if len(sections) > 1 else None
        # header = soup.find("div", {"class": "header cell info"})
        # company = driver.find_element(By.XPATH, "//span[@class='strong ib']").text
        # location = driver.find_element(By.XPATH, "//span[@class='subtle ib']").text
        # jd_temp = driver.find_element(By.TAG_NAME, 'JobDescriptionContainer')
        jd = second_section.text
        data[i] = {
            'url': u,
            'Position': position,
            'Company': company,
            'Location': location,
            'Job_Description': jd
        }
    except IndexError:
        print(f'IndexError at URL: {u}')
    except NoSuchElementException:
        print(f'NoSuchElementException at URL: {u}')
    except Exception as e:
        print(f'Error at URL: {u}, Error: {e}')
    i += 1

job_list = [job for job in data.values()]

jd_df = pd.DataFrame(data)
jd_df.transpose().to_csv(r'C:\Users\Naghul\Documents\Semester6\FOSS\hackathon\src\scraping\jd_unstructured_data.csv')

print('File created')
driver.quit()