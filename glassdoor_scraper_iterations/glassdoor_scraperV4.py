from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import chromedriver_binary


def scrape_jobs(driver):
    try:
        job_cards = driver.find_elements(By.XPATH, "//div[@id='MainCol']//div[@data-test='jobListing']")
        jobs = []
        o = {}
        for index, card in enumerate(job_cards):
            # Scroll to the job card and click it
            ActionChains(driver).move_to_element(card).click(card).perform()
            time.sleep(3)  # Wait for the right column content to load

            # Click the "show more" button
            try:
                show_more_button = driver.find_element(By.XPATH, '//*[@id="app-navigation"]/div[3]/div[2]/div[2]/div/section/div[1]/div[2]/button')
                show_more_button.click()
                print("More shown")
            except NoSuchElementException:
                print("No 'show more' found")

            # Scrape data from the right column

            resp = driver.page_source
            soup = BeautifulSoup(resp, 'html.parser')

            o["name-of-company"] = soup.find("div",
                                            {"class": "EmployerProfile_employerInfo__GaPbq EmployerProfile_employerWithLogo__R_rOX"}).text if soup.find(
                "div", {"class": "EmployerProfile_employerInfo__GaPbq EmployerProfile_employerWithLogo__R_rOX"}) else None

            jobs.append(o)
            # Add your scraping logic here

            # Additional logic might be needed to handle dynamic content loading

    except NoSuchElementException:
        print("No job cards found")
    except StaleElementReferenceException:
        print("Stale element reference exception occurred")

    return jobs
    # resp = driver.page_source
    # soup = BeautifulSoup(resp, 'html.parser')
    # allJobsContainer = soup.find("ul", {"class": "JobsList_jobsList__Ey2Vo"})
    # jobs = []
    #
    # if allJobsContainer:
    #     allJobs = allJobsContainer.find_all("li")
    #     for job in allJobs:
    #         o = {}
    #         o["name-of-company"] = job.find("div", {"class": "EmployerProfile_profileContainer__d5rMb"}).text if job.find("div", {"class": "EmployerProfile_profileContainer__d5rMb"}) else None
    #         o["name-of-job"] = job.find("a", {"class": "JobCard_seoLink__WdqHZ"}).text if job.find("a", {"class": "JobCard_seoLink__WdqHZ"}) else None
    #         o["location"] = job.find("div", {"class": "JobCard_location__N_iYE"}).text if job.find("div", {"class": "JobCard_location__N_iYE"}) else None
    #         o["salary"] = job.find("div", {"class": "JobCard_salaryEstimate___m9kY"}).text if job.find("div", {"class": "JobCard_salaryEstimate___m9kY"}) else None
    #         jobs.append(o)
    # else:
    #     print("Job container not found")
    #
    # return jobs


def close_popup(driver):
    try:
        # Update the selector to match the close button of the pop-up
        close_button = driver.find_element(By.XPATH, '//button[contains(@class, "CloseButton")]')
        close_button.click()
        print("Pop-up closed")
    except NoSuchElementException:
        print("No pop-up found")


def scroller(driver):
    show_more_button = driver.find_element(By.CSS_SELECTOR,'.button_Button__meEg5.button-base_Button__9SPjH')  # Replace with the actual class or identifier of the "Show More" button
    driver.execute_script("arguments[0].scrollIntoView();", show_more_button)
    show_more_button.click()
    time.sleep(3)  # Wait for the page to load

    # Attempt to close pop-up after each "Show More" click
    close_popup(driver)


options = webdriver.ChromeOptions()
options.add_argument("window-size=1920,1080")

driver = webdriver.Chrome(options=options)
driver.get("https://www.glassdoor.com.au/Job/australia-data-jobs-SRCH_IL.0,9_IN16_KO10,14.htm")
time.sleep(5)

# Attempt to close any initial pop-up
close_popup(driver)

all_jobs = []
n = 3
try:
    while n > 0:  # Replace with a more specific condition if needed
        scroller(driver)
        all_jobs += scrape_jobs(driver)
        # show_more_button = driver.find_element(By.CSS_SELECTOR, '.button_Button__meEg5.button-base_Button__9SPjH') # Replace with the actual class or identifier of the "Show More" button
        # driver.execute_script("arguments[0].scrollIntoView();", show_more_button)
        # show_more_button.click()
        # time.sleep(5)  # Wait for the page to load

        n -= 1
except Exception as e:
    print("Finished scraping or an error occurred:", e)

driver.close()

# Process your scraped data in all_jobs
print(all_jobs)
