from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup

def openresume(file_path):
    # Use the ChromeDriverManager to install the correct version
    service = Service(ChromeDriverManager().install())

    options = Options()
    options.add_argument("--disable-javascript")
    options.add_argument("--headless")

    # Initialize the driver with the options
    driver = webdriver.Chrome(service=service, options=options)

    # Open the resume parser page
    url = "http://localhost:3000/resume-parser"
    driver.get(url)

    # Step 1: Find the file input inside the label element
    file_input = driver.find_element(By.CSS_SELECTOR, 'label input[type="file"]')

    # Step 2: Send the file path to the input element
    # file_path = r'C:\Users\Naghul\Downloads\Job-Recommendation-System-main\Job-Recommendation-System-main\src\notebook\Resume - Internshaala.pdf'  # Adjust to your file path
    file_input.send_keys(file_path)

    # Step 3: Wait for the server to process the file and load the result
    time.sleep(3)  # Wait for the processing to finish (adjust the time if necessary)

    # Step 4: Get the page source after file is processed
    page_source = driver.page_source

    # Step 5: Parse the page content using BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Step 6: Find the last table element in the page
    tables = soup.find_all('table')
    if tables:
        last_table = tables[0]  # Get the last table element
        # last_table = tables[-4]  # Get the last table element

        # Step 7: Extract the text content of each row in the last table
        rows = last_table.find_all('tr')
        table_data = []

        for row in rows:
            columns = row.find_all('td')  # Find all columns in the row
            row_data = [column.get_text(strip=True) for column in columns]  # Get text from each column
            table_data.append(row_data)
        
        driver.quit()

        # Step 8: Print the extracted table data
        text_data = ""
        for row in table_data:
            try:
                text_data += " " + row[0]
            except Exception as e:
                ...
        
        return text_data
    else:
        return 0

if __name__ == "__main__":
    print(openresume(r"C:\Users\Naghul\Downloads\Job-Recommendation-System-main\Job-Recommendation-System-main\src\notebook\Resume - Internshaala.pdf"))
