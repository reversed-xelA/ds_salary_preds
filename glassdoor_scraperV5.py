from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
import math
import pandas as pd

# The glassdoor URL with keyword and location already entered on site.
URL = "https://www.glassdoor.com.au/Job/western-australia-australia-data-analyst-jobs-SRCH_IL.0,27_IS3698_KO28,40.htm"

# Enter the number of jobs your search contains. This is used to calculate the number of pages to load.
NUMBER_OF_JOBS = 76

# Log-in delay. Number of seconds to enter sign in details manually. Logging in resolves some of the
# page loading issues with the show more button.
LOG_IN_DELAY = 20

# Setting up the webdriver
options = webdriver.ChromeOptions()
options.add_argument("window-size=1920,1080")

driver = webdriver.Chrome(options=options)
driver.get(URL)
wait = WebDriverWait(driver, 10)

time.sleep(LOG_IN_DELAY)


# Uses the webdriver to scroll down the page and click the "show more jobs" button.
def scroller():
    try:
        time.sleep(3)  # Wait for any dynamic content
        show_more_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Show more jobs')]]")))
        show_more_button.click()
        time.sleep(3)  # Wait for content to load
    except TimeoutException:
        print("No 'Show More Jobs' button found")


def scrape_job_details(driver):
    # Wait for the right column content to load
    time.sleep(3)

    # Scrape data from the right column
    resp = driver.page_source
    soup = BeautifulSoup(resp, 'html.parser')
    o = {}

    # Scraping the job title, company name, Location, Salary, Job description, Company size, Company type,
    # Company Sector, Company founded, Company industry, Company revenue and Company rating.

    if soup.find_all("div", {"class": "EmployerProfile_employerInfo__GaPbq"}):
        company_div_tags = soup.find_all("div", {"class": "EmployerProfile_employerInfo__GaPbq"})
        o["company"] = company_div_tags[-1].text
    else:
        o["company"] = None
    o["job_title"] = soup.find("div", {"class": "JobDetails_jobTitle__Rw_gn"}).text if soup.find(
        "div", {"class": "JobDetails_jobTitle__Rw_gn"}) else None
    o["location"] = soup.find("div", {"class": "JobDetails_location__MbnUM"}).text if soup.find(
        "div", {"class": "JobDetails_location__MbnUM"}) else None
    o["salary"] = soup.find("div", {"class": "SalaryEstimate_averageEstimate__xF_7h"}).text if soup.find(
        "div", {"class": "SalaryEstimate_averageEstimate__xF_7h"}) else None

    company_overview = soup.find_all("div", {"class": "JobDetails_overviewItemValue__5TqNi"})
    # A list of keys corresponding to the company details
    keys = ["company_size", "company_founded", "company_type", "company_industry", "company_sector", "company_revenue"]

    # Update the dictionary with the text from each element, or None if not available
    for i, key in enumerate(keys):
        o[key] = company_overview[i].text if i < len(company_overview) else None

    o["job_description"] = (
        soup.find("div", {"class": "JobDetails_jobDescriptionWrapper__BTDTA"}).text) \
        if soup.find("div", {"class": "JobDetails_jobDescriptionWrapper__BTDTA"}) else None

    return o


# Math to figure out the number of clicks on the show more jobs button
jobs_per_page = 30
number_of_pages = math.ceil(NUMBER_OF_JOBS / jobs_per_page)

# Loading all the job pages
while number_of_pages > 0:
    scroller()
    number_of_pages -= 1
    print(f"{number_of_pages} pages to be loaded")

# Find all job listing elements
job_listings = driver.find_elements(By.XPATH, "//li[contains(@class, 'JobsList_jobListItem__JBBUV')]")

all_job_data = []

# Iterate through the jobs and scrape data from each
for job in job_listings:
    try:
        # Scroll to the job element and click it
        ActionChains(driver).move_to_element(job).click(job).perform()
        job_data = scrape_job_details(driver)
        all_job_data.append(job_data)
    except Exception as e:
        print("Error occurred:", e)
        continue

driver.quit()

# Process and save all scraped job data
df = pd.DataFrame(all_job_data)

df['job_description'] = df['job_description'].str.replace('\n', ' ', regex=False)

df.to_csv('job_data_data_analyst_WA.csv', index=False)
