from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup
import time
import math

options = webdriver.ChromeOptions()
options.add_argument("window-size=1920,1080")

driver = webdriver.Chrome(options=options)
driver.get("https://www.glassdoor.com.au/Job/melbourne-australia-data-analyst-manager-jobs-SRCH_IL.0,19_IC2264754_KO20,40.htm")
wait = WebDriverWait(driver, 10)

# Log-in delay. 20 seconds to enter sign in details manually. Sorts some of the page loading issues with
# the show more button
time.sleep(20)

def scrape_job_details(driver):
    # Wait for the job details to load
    time.sleep(2)
    # Scrape data here, modify according to what you need to scrape
    # Example:
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    job_title = soup.find("h1", {"class": "jobTitle"}).text if soup.find("h1", {"class": "jobTitle"}) else None
    # Add more scraping logic as needed
    print(job_title)


# def close_popup(driver):
#     try:
#         # Update the selector to match the close button of the pop-up
#         close_button = driver.find_element(By.XPATH, '//button[contains(@class, "CloseButton")]')
#         close_button.click()
#         print("Pop-up closed")
#     except NoSuchElementException:
#         print("No pop-up found")


def scroller():
    try:
        time.sleep(3)  # Wait for any dynamic content
        # scrolling_element = driver.find_element(By.XPATH, '//*[@id="left-column"]/div[2]/ul')
        # driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrolling_element)
        show_more_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.button_Button__meEg5.button-base_Button__9SPjH')))

        # Scroll using ActionChains
        # ActionChains(driver).move_to_element(show_more_button).perform()

        # Alternative: Scroll using JavaScript
        # driver.execute_script("arguments[0].scrollIntoView(true);", show_more_button)

        #time.sleep(2)  # Give time for any lazy-loaded elements
        show_more_button.click()
        time.sleep(3)  # Wait for content to load

    except TimeoutException:
        print("No 'Show More Jobs' button found")


# Calculate the number of pages and round up
number_of_jobs = 203
jobs_per_page = 30
number_of_pages = math.ceil(number_of_jobs / jobs_per_page)

while number_of_pages > 0:
    scroller()
    number_of_pages -= 1
    print(f"{number_of_pages} pages to be loaded")

# Find all job listing elements
job_listings = driver.find_elements(By.XPATH, "//li[contains(@class, 'JobsList_jobListItem__JBBUV')]")

all_job_data = []

for job in job_listings:
    try:
        # Scroll to the job element and click it
        ActionChains(driver).move_to_element(job).click(job).perform()
        job_data = scrape_job_details(driver)
        all_job_data.append(job_data)

        # Navigate back if necessary
        # driver.back()
        # time.sleep(2)

    except Exception as e:
        print("Error occurred:", e)
        continue

driver.quit()

# Process or print all scraped job data
print(all_job_data)

# if soup.find_all("div", {"class": "JobDetails_overviewItemValue__5TqNi"}):
#     company_overview = soup.find_all("div", {"class": "JobDetails_overviewItemValue__5TqNi"})
#     o["company_size"] = company_overview[0].text
#     o["company_founded"] = company_overview[1].text
#     o["company_type"] = company_overview[2].text
#     o["company_industry"] = company_overview[3].text
#     o["company_sector"] = company_overview[4].text
#     o["company_revenue"] = company_overview[5].text
# else:
#     o["company_size"] = None
#     o["company_founded"] = None
#     o["company_type"] = None
#     o["company_industry"] = None
#     o["company_sector"] = None
#     o["company_revenue"] = None