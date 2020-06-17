from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import os

chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1280x1696')
chrome_options.add_argument('--user-data-dir=/tmp/user-data')
chrome_options.add_argument('--hide-scrollbars')
chrome_options.add_argument('--enable-logging')
chrome_options.add_argument('--log-level=0')
chrome_options.add_argument('--v=99')
chrome_options.add_argument('--single-process')
chrome_options.add_argument('--data-path=/tmp/data-path')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--homedir=/tmp')
chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
chrome_options.binary_location = os.getcwd() + "/bin/headless-chromium"


def get_lawn_status():
    # Start driver
    driver = webdriver.Chrome(chrome_options = chrome_options)

    # Load Page
    driver.get("http://www.bryantpark.org")
    assert "Bryant" in driver.title

    # Define xpaths
    status_xpath = "//*[@id=\"react-home\"]/section/section/div[1]/div/div[2]/div[2]/section/div/h4"
    open_at_xpath = "//*[@id=\"react-home\"]/section/section/div[1]/div/div[2]/div[2]/section/div/p/span"

    # Check for stuff
    try:
        myElem = WebDriverWait(driver,
                               2).until(EC.presence_of_element_located((By.XPATH,
                                                                        status_xpath)))
    except TimeoutException:
        print ("Loading took too much time!")

    # Grab the intels
    try:
        lawn_status_string = str(driver.find_element_by_xpath(status_xpath).text)
        open_time_string = str(driver.find_element_by_xpath(open_at_xpath).text)
    except NoSuchElementException:
        print('No such element')
        return ('','')

    # Shutdown driver
    driver.close()
    driver.quit()

    return lawn_status_string, open_time_string
