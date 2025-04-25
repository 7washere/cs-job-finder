import re    # USE CHROME VERSION 135.0.7049.84
import os
import selenium 
import time 
import requests 
import random 
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import openai 
from selenium.webdriver.chrome.options import Options
import config 
import urllib.parse
from urllib.parse import quote,  urlparse, urlencode, parse_qsl


username = config.username
password = config.password
openai_api = config.openai_api
WEBHOOK = config.WEBHOOK
file_path = config.file_path
number = config.number 
global found_skills 

chrome_options = Options() # Assigns the options package to chrome_options for giving us our own settings for chrome 
chrome_options.add_experimental_option("detach", True) #Prevent chrome from closing after running ONLY FOR DEBUGGING 


service = Service(ChromeDriverManager().install()) # Chromedriver manager manages chrome
driver = webdriver.Chrome(service=service)


def send_discord_notif(message):  # Function to send a Discord notification via webhook
    data = {
        "content": message  # Creates a dictionary with the content and message values
    }
    try:  # Error handling. Any errors occur goes to the except block
        response = requests.post(WEBHOOK, json=data)
        response.raise_for_status()  # Checks if the request was successful
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Discord notification: {e}")  # Prints the error message in the console incase something goes wrong

send_discord_notif("🚀 Starting LinkedIn Job Application Bot...")  # Sends a notification to Discord when the bot starts
 

def skills_extract(file_path):  # Func to extract skills from a resume like python,java,django,c++ etc.
    with open(file_path, 'r+') as file: # Opens the resume file  
        content = file.read().lower()  # Makes characters lowercase

    known_skills = ["python", "java", "django", "c++", "javascript", "react", "angular", "vue", "ruby", "rails", "swift", "kotlin", "php", "mysql", "mongodb", "sql", "aws", "azure", "google cloud"]  # List of skills
    global found_skills # Makes the found_skills variable a global variable 
    found_skills = [skill for skill in known_skills if skill in content ]  # Finds the skills that are in the resume
     
    print("skills_extract2")
    print("Skills_extract")
    print(found_skills)
    
    return found_skills  # Now returns all the various skills found in the resume

skills_extract("resume.txt") # Calls the function to extract skills from the resume

def job_url_gen(found_skills):
    base = "https://www.linkedin.com/jobs/search/?keywords="
    urls = [] # List to store the generated URLs 
    file = open("job_urls.txt", "w")  # Open in 'w' mode to overwrite or create the file correctly

    for skill in found_skills:
        keyword = skill.replace(" ", "%20")  # Replace spaces with %20 for URL encoding
        url = base + keyword 
        urls.append(url)
        file.write(url + "\n")  # Write each URL to a new line in the file
        print(f"Generated URL for: {skill}") # More informative print statement


    file.close() # Close the file when done writing
    return urls 


 
def login_to_linkedin(driver, username, password):
    try:
        print("Driver:", driver)  # Prints the Selenium WebDriver instance.
        print("Current URL (before get):", driver.current_url)  # Prints the current URL before navigating to the login page.

        driver.get("https://www.linkedin.com/login") 

        print(driver.current_url) # Prints the current URL after navigating to the login page.

        email_element = WebDriverWait(driver, 20).until(  # Waits up to 20 seconds for the email input field to be present.
            EC.presence_of_element_located((By.ID, "username"))  # Locates the email input field by its ID.
        )
        password_element = WebDriverWait(driver, 20).until(  # Waits up to 20 seconds for the password input field to be present.
            EC.presence_of_element_located((By.ID, "password"))  # Locates the password input field by its ID.
        )

        email_element.clear()  # Clears any existing text in the email input field.
        email_element.send_keys(username)  # Enters the provided username into the email input field.
        time.sleep(random.uniform(5, 15))  # Pauses execution for a random time between 5 and 15 seconds

        password_element.clear()  # Clears any existing text in the password input field.
        password_element.send_keys(password)  # Enters the provided password into the password input field.
        time.sleep(random.uniform(5, 20))  # Pauses execution for a random time between 5 and 15 seconds

        password_element.send_keys(Keys.RETURN)  # Simulates pressing the Enter key to submit the login form.

        WebDriverWait(driver, 30).until(  # Waits up to 30 seconds for a specific element to be present, indicating successful login.
            EC.presence_of_element_located((By.ID, "profile-nav-item"))  # Locates an element that appears after successful login.
        )

        print("Login successful")  # Prints a success message to the console.
        send_discord_notif("✅ Logged into LinkedIn successfully.")  # Sends a Discord notification indicating successful login.
    except Exception as e:
        send_discord_notif(f"❌ Failed to log into LinkedIn: {e}")  # Sends a Discord notification indicating login failure.

login_to_linkedin(driver, username, password)
easy_apply_filter = driver.find_element(By.ID, "searchFilter_applyWithLinkedin") # Finds the easy apply filter and stores it in easy_apply_filter

def job_apply_all(urls, jobs_per_url=5):
    for url in urls:
        try:
            driver.get(url)
            print(f"Navigated to job search URL: {url}")
            time.sleep(random.uniform(3, 7))

            # Apply Easy Apply filter (find it on each page)
            try:
                easy_apply_filter_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "searchFilter_applyWithLinkedin-1"))
                )
                easy_apply_filter_element.click()
                print("Applied 'Easy Apply' filter.")
                time.sleep(random.uniform(2, 5))
            except Exception as e:
                print(f"Could not find or click 'Easy Apply' filter: {e}")

            # Find all clickable job listings on the current page
            job_cards = WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card-container--clickable"))
            )

            applied_count = 0
            for i in range(min(jobs_per_url, len(job_cards))):
                # Re-find elements on each iteration to avoid StaleElementReferenceException
                job_cards = WebDriverWait(driver, 15).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card-container--clickable"))
                )
                if i >= len(job_cards):
                    break

                job_card = job_cards[i]
                job_number = i + 1
                print(f"Processing job listing number: {job_number}")

                try:
                    job_card.click()
                    print(f"Clicked on job listing number: {job_number}")
                    time.sleep(random.uniform(2, 5))

                    try:
                        easy_apply_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CLASS_NAME, "jobs-apply-button"))
                        )
                        easy_apply_button.click()
                        # send_discord_notif(f"📝 Easy Apply form opened for job {job_number} at {url}. Please fill it out manually.")
                        print(f"Easy Apply form opened for job {job_number}. Waiting for user input.")

                        input(f"Press Enter after you have filled out and submitted the form for job {job_number}...")
                        print("User indicated form submission.")
                        applied_count += 1
                        time.sleep(random.uniform(2, 5))

                        # Try to close any confirmation modal
                        try:
                            close_button = WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable((By.CLASS_NAME, "artdeco-modal__dismiss"))
                            )
                            close_button.click()
                            print("Closed confirmation modal (if any).")
                        except TimeoutException:
                            pass
                        except Exception as e:
                            print(f"Error closing modal: {e}")

                    except TimeoutException:
                        print(f"Could not find Easy Apply button for job {job_number}.")
                        try:
                            close_button = WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable((By.CLASS_NAME, "artdeco-modal__dismiss"))
                            )
                            close_button.click()
                        except TimeoutException:
                            pass
                        except Exception as e:
                            print(f"Error closing modal (no Easy Apply): {e}")

                except Exception as e:
                    print(f"Error processing job listing number {job_number}: {e}")

                if applied_count >= jobs_per_url:
                    print(f"Processed {jobs_per_url} job listings on this page.")
                    break

        except Exception as e:
            print(f"Error processing job search URL {url}: {e}")
            time.sleep(random.uniform(5, 10))


def job_apply_all():
    for skill in found_skills: 
        search_button = By.CSS_SELECTOR, "input.search-global-typeahead__input" # Finds the search button and stores it in search_button
        driver.click(search_button)
        time.sleep(random .uniform(9, 18.2)) # Pauses execution for a random time between 5 and 15 seconds
        search_button.send_keys(skill)
        driver.send_keys(Keys.RETURN) # Simulates pressing the Enter key to submit the search form.
        driver.click(easy_apply_filter) # Clicks on the easy apply filter

        return  


def fill_easy_form():
    try:
        phone_input = driver.find_element(By.CSS_SELECTOR, "input[aria-label='Phone number']") 
        if phone_input.get_attribute("value") == "":
            phone_input.send_keys(number)  # Replace with your number

        resume_upload = driver.find_element(By.CSS_SELECTOR, "input[type='file']") # Finds the resume upload field and stores it in resume_upload
        resume_upload.send_keys("resume.txt") # Uploads the resume from the current directory to the easy apply form

        while True:
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Continue to next step']") # Finds the next button and stores it in next_button
                if next_button.is_enabled(): # Checks if the next button is enabled
                    next_button.click() # Clicks on the next button 
                    prev_url = driver.current_url # Stores the current url 
                    WebDriverWait(driver, 10).until(EC.url_changes(prev_url)) # Waits for the next page to load
                else:
                    break
            except Exception as e:
                print(f"Error filling form: {e}")
                break

        submit_buttons = driver.find_elements(By.CSS_SELECTOR, "button") # Finds all the buttons on the page
        for button in submit_buttons: # Loops through all the buttons
            if "submit" in button.text.lower(): # Checks if the button text contains "submit" 
                button.click() # Clicks on the submit button
                print("Final submit button clicked.") # Notifies the user that the final submit button has been clicked in terminal 
                send_discord_notif("✅ Final form submitted.") # Notifies the user that the final submit button has been clicked in discord
                break 

    except Exception as e:
        print(f"Skipped optional fields or form already filled: {e}") # Notifies the user if any optional fields or form were skipped or already filled

    time.sleep(5) # Stops running the program for 5 seconds then resumes

input()

