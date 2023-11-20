# Glassdoor Scraper

## Overview
This program is designed to scrape job listings from Glassdoor for a specific search query. It automatically navigates through the job listings pages, extracts relevant job details, and saves the data in a CSV file.

## Prerequisites
- Python 3.x
- Selenium WebDriver
- BeautifulSoup4
- ChromeDriver (or any other compatible driver for the browser of your choice)
- Pandas

## Installation
To run this scraper, you need to install the required Python libraries. You can install them using pip:

```bash
pip install selenium beautifulsoup4 pandas
```

Ensure that you have the appropriate WebDriver installed for your browser and added to your system's PATH.

## Usage
- Max 570 jobs scrape-able
- Set the `URL` variable to the Glassdoor search results page URL.
- Enter the total number of jobs in `NUMBER_OF_JOBS` for pagination.
- Set `LOG_IN_DELAY` to provide yourself time to manually log in to Glassdoor, if necessary.

Run the script with Python:

```bash
python glassdoor_scraper.py
```

## Functions
- `scroller()`: Scrolls through the pages and clicks the "Show more jobs" button.
- `scrape_job_details(driver)`: Scrapes job details from the current page.

## Output
The script will save the job listings in a file named job_data_data_analyst_WA.csv with relevant details like job title, company name, location, salary, and more.


