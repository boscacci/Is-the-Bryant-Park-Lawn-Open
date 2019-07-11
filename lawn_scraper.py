from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options


import os

def get_lawn_status():
    # Start driver
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(executable_path = os.getcwd() + '/geckodriver',options=options)

    # Load Page
    driver.get("http://www.bryantpark.org")
    assert "Bryant" in driver.title

    # Define xpaths
    status_xpath = "/html/body/div/div[1]/section/section/div[1]/div/div[2]/div[2]/section/div/h4"
    open_at_xpath = "/html/body/div/div[1]/section/section/div[1]/div/div[2]/div[2]/section/div/p/span"

    # Check for stuff
    try:
        myElem = WebDriverWait(driver,
                               2).until(EC.presence_of_element_located((By.XPATH,
                                                                        status_xpath)))
    except TimeoutException:
        print ("Loading took too much time!")

    # Grab the intels
    lawn_status_string = str(driver.find_element_by_xpath(status_xpath).text)
    open_time_string = str(driver.find_element_by_xpath(open_at_xpath).text)

    # Shutdown driver
    driver.close()
    driver.quit()

    return lawn_status_string, open_time_string
