"""Gathers and returns job postings from SimplyHired as a dataframe."""

# Import libraries
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

# Get job postings (number of jobs to collect) and return dataframe.
def get_posting(num_jobs, verbose=0):
    
    """Gathers and returns job postings from SimplyHired. as a dataframe."""
    
    # Initialize chrome driver.
    driver = webdriver.Chrome(
        executable_path=
        "C:/Users/malex/Desktop/data-science-jobs/scraping/chromedriver.exe")
    
    # Pop-up window size.
    driver.set_window_size(1120, 1000)

    # URL to begin scraping from.
    url ='https://www.simplyhired.com/search?q=data+scientist&l=california&mi=exact&job=yg9uNGLrfFPinxyBzXi--B5GxVAlHYGQXqXiadHKUI2S7PqufaQxpQ'
    
    # Open URL in window.
    driver.get(url)    
    
    # Wait 10 seconds for browser to open and page to load.
    time.sleep(10)
    
    # Initialize jobs list.
    jobs = []
    
    # Initialize page count (used for first four pages).
    page = 1
    
    # While number of jobs collected are less than or equal to the number of
    # jobs specified.
    while len(jobs) <= num_jobs:
        
        # Loops over number of jobs on the current page.
        for i in range(len(driver.find_elements_by_xpath('//*[@id="job-list"]/li'))):
            
            # Click on the ith job posting.
            driver.find_element_by_xpath(
                '//*[@id="job-list"]/li[{}]/article/div/div[1]/h3/a'.format(
                    i+1)).click()
            
            # Wait 3 seconds.
            time.sleep(3)
            
            # Initialize title, company, location, and salary lists.
            title = []
            company = []
            location = []
            salary = []
            
            # Try to collect title, company, location, and salary, and if
            # exception to any then don't collect and go to next.
            try:
                title = driver.find_element_by_xpath(
                    '//*[@id="job-list"]/li[{}]/article/div/div[1]/h3/a'.format(
                        i+1)).text
            except NoSuchElementException:
                pass
            try:
                company = driver.find_element_by_xpath(
                    '//*[@id="content"]/div[2]/div/div/div[2]/div/div/aside/header/div/div[2]/div[1]/div[1]'
                    ).text
            except NoSuchElementException:
                pass
            try:
                location = driver.find_element_by_xpath(
                    '//*[@id="content"]/div[2]/div/div/div[2]/div/div/aside/header/div/div[2]/div[1]/div[2]'
                    ).text
            except NoSuchElementException:
                pass
            try:
                salary = driver.find_element_by_xpath(
                    '//*[@id="job-list"]/li[{}]/article/div/div[4]/div[1]/div[1]'.format(
                        i+1)).text
            except NoSuchElementException:
                pass
            
            # Initialize benefits/qualification lists and description.
            benefits_qual1 = []
            benefits_qual2 = []
            description = []
            
            # Try to collect benefits and qualifications and if exception to
            # any then don't collect and go to next.
            try:
                for j in range(len(driver.find_elements_by_xpath(
                        '//*[@id="content"]/div[2]/div/div/div[2]/div/div/aside/div/div[3]/ul/li'))):
                    benefits_qual1.append(driver.find_element_by_xpath(
                        '/html/body/main/div[2]/div/div/div[2]/div/div/aside/div/div[3]/ul/li[{}]'.format(
                            j+1)).text)
            except NoSuchElementException:
                pass
            
            try:
                for k in range(len(driver.find_elements_by_xpath(
                        '//*[@id="content"]/div[2]/div/div/div[2]/div/div/aside/div/div[4]/ul/li'))):
                    benefits_qual2.append(
                        driver.find_element_by_xpath(
                            '/html/body/main/div[2]/div/div/div[2]/div/div/aside/div/div[4]/ul/li[{}]'.format(
                                k+1)).text)
            except NoSuchElementException:
                pass
            
            # The location depends on whether both benefits/qualifications have
            # been collected. if both benefits and qualifications were
            # collected, try collecting description from specified location. if
            # exception to any then don't collect and go to next.
            if benefits_qual1 and benefits_qual2:
                try:
                    description = driver.find_element_by_xpath(
                        '//*[@id="content"]/div[2]/div/div/div[2]/div/div/aside/div/div[6]/div/div[2]'
                        ).text
                except NoSuchElementException:
                    pass
            # If either one or no benefits or qualifications were collected,
            #try collecting description from specified location. If exception
            # to any then don't collect and go to next
            else:
                try:
                    description = driver.find_element_by_xpath(
                        '//*[@id="content"]/div[2]/div/div/div[2]/div/div/aside/div/div[5]/div/div[2]'
                        ).text
                except NoSuchElementException:
                    pass 
    
            # Append collected job posting information to jobs list as
            # dictionary
            jobs.append(
                {'title': title, 'company': company, 'location': location,
                 'salary': salary, 'benefits_qual1': benefits_qual1,
                 'benefits_qual2': benefits_qual2, 'description': description})
            
            # Check to see if number of jobs specified by user have been
            # collected. If so then break.
            if len(jobs) >= num_jobs:
                break
        
        # Check to see if number of jobs specified by user have been collected.
        # If so then break.
        if len(jobs) >= num_jobs:
            break
        
        # The next button is located in different places for the first four
        # pages, so page is kept current until page=5 then the next button
        # has the same location. Then the else statement is entered for the
        # remainder of pages. If no page button is found then break and return
        # dataframe.
        if page == 1:
            driver.find_element_by_xpath(
                '//*[@id="content"]/div[2]/div/div/div[3]/nav/ul/li[6]/a'
                ).click()
            time.sleep(5)
            page += 1  
        if page == 2:
            driver.find_element_by_xpath(
                '//*[@id="content"]/div[2]/div/div/div[3]/nav/ul/li[7]/a'
                ).click()
            time.sleep(5)
            page += 1
        if page == 3:
           driver.find_element_by_xpath(
               '//*[@id="content"]/div[2]/div/div/div[3]/nav/ul/li[7]/a'
               ).click()
           time.sleep(5)
           page += 1 
        if page == 4:
            driver.find_element_by_xpath(
                '//*[@id="content"]/div[2]/div/div/div[3]/nav/ul/li[8]/a'
                ).click()
            time.sleep(5)
            page += 1
        else:
            try:
                driver.find_element_by_xpath(
                    '//*[@id="content"]/div[2]/div/div/div[3]/nav/ul/li[9]/a'
                    ).click()
                time.sleep(5)
            except NoSuchElementException:
                break
        
    return pd.DataFrame(jobs)
