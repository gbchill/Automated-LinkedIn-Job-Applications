from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time

# define your login credentials and phone number
account_email = "YOUR_LOGIN_EMAIL"
account_password = "YOUR_LOGIN_PASSWORD"
phone = "YOUR_PHONE_NUMBER"

def abort_application():
    # click close button in the modal
    close_modal_button = driver.find_element(by=By.CLASS_NAME, value="artdeco-modal__dismiss")
    close_modal_button.click()
    time.sleep(2)
    # click discard button in the modal
    discard_button = driver.find_elements(by=By.CLASS_NAME, value="artdeco-modal__confirm-dialog-btn")[1]
    discard_button.click()

# set the path to your ChromeDriver executable
chrome_driver_path = "YOUR_CHROME_DRIVER_PATH"

# optional - automatically update your ChromeDriver
from webdriver_manager.chrome import ChromeDriverManager
chrome_driver_path = ChromeDriverManager(path="YOUR_CHROME_DRIVER_FOLDER").install()

# optional - keep the browser open if the script crashes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

service = ChromeService(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# navigate to the LinkedIn job search page
driver.get("https://www.linkedin.com/jobs/search/?currentJobId=3586148395&f_LF=f_AL&geoId=101356765&"
           "keywords=python&location=London%2C%20England%2C%20United%20Kingdom&refresh=true")

# click "Reject Cookies" button
time.sleep(2)
reject_cookies_button = driver.find_element(by=By.CSS_SELECTOR, value='button[action-type="DENY"]')
reject_cookies_button.click()

# click "Sign in" button
time.sleep(2)
sign_in_button = driver.find_element(by=By.LINK_TEXT, value="Sign in")
sign_in_button.click()

# sign in
time.sleep(5)
email_field = driver.find_element(by=By.ID, value="username")
email_field.send_keys(account_email)
password_field = driver.find_element(by=By.ID, value="password")
password_field.send_keys(account_password)
password_field.send_keys(Keys.ENTER)

# CAPTCHA - solve the puzzle manually
input("Press Enter when you have solved the Captcha")

# get job listings
time.sleep(5)
all_job_listings = driver.find_elements(by=By.CSS_SELECTOR, value=".job-card-container--clickable")

# apply for jobs
for job_listing in all_job_listings:
    print("Opening job listing")
    job_listing.click()
    time.sleep(2)
    try:
        # click the "Apply" button
        apply_button = driver.find_element(by=By.CSS_SELECTOR, value=".jobs-s-apply button")
        apply_button.click()

        # insert your phone number
        time.sleep(5)
        phone_number_input = driver.find_element(by=By.CSS_SELECTOR, value="input[id*=phoneNumber]")
        if phone_number_input.text == "":
            phone_number_input.send_keys(phone)

        # check the "Submit" button
        submit_button = driver.find_element(by=By.CSS_SELECTOR, value="footer button")
        if submit_button.get_attribute("data-control-name") == "continue_unify":
            abort_application()
            print("Complex application, skipped.")
            continue
        else:
            # click the "Submit" button
            print("Submitting job application")
            submit_button.click()

        time.sleep(2)
        # click close button in the modal
        close_modal_button = driver.find_element(by=By.CLASS_NAME, value="artdeco-modal__dismiss")
        close_modal_button.click()

    except NoSuchElementException:
        abort_application()
        print("No application button, skipped.")
        continue

time.sleep(5)
driver.quit()
