from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import chromedriver_binary

l = []
o = {}

target_url = "https://www.glassdoor.com.au/Job/australia-data-jobs-SRCH_IL.0,9_IN16_KO10,14.htm"

options = webdriver.ChromeOptions()
options.add_argument("window-size=1920,1080")

driver = webdriver.Chrome(options=options)

driver.get(target_url)

driver.maximize_window()
time.sleep(5)

resp = driver.page_source

driver.close()

# Create a BeautifulSoup object with the page source
soup = BeautifulSoup(resp, 'html.parser')

# Now use the soup object to find elements
allJobsContainer = soup.find("ul", {"class": "JobsList_jobsList__Ey2Vo"})

# Check if the container is found and then find all list items
if allJobsContainer:
    allJobs = allJobsContainer.find_all("li")
else:
    allJobs = []
    print("Job container not found")

for job in allJobs:
    try:
        o["name-of-company"] = job.find("div", {"class": "EmployerProfile_profileContainer__d5rMb"}).text
    except:
        o["name-of-company"] = None

    try:
        o["name-of-job"] = job.find("a", {"class": "JobCard_seoLink__WdqHZ"}).text
    except:
        o["name-of-job"] = None

    try:
        o["location"] = job.find("div", {"class": "JobCard_location__N_iYE"}).text
    except:
        o["location"] = None

    try:
        o["salary"] = job.find("div", {"class": "JobCard_salaryEstimate___m9kY"}).text
    except:
        o["salary"] = None

    l.append(o)
    o = {}

print(l)