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
     
    
    print(found_skills)
    
    return found_skills  # Now returns all the various skills found in the resume



def job_url_gen():
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

        time.sleep(random.float(5.2, 15.2)) # Pauses execution for a random time between 5.2 and 15.2 seconds

        print("Login successful")  # Prints a success message to the console.
        send_discord_notif("✅ Logged into LinkedIn successfully.")  # Sends a Discord notification indicating successful login.
    except Exception as e:
        send_discord_notif(f"❌ Failed to log into LinkedIn: {e}")  # Sends a Discord notification indicating login failure.






def job_apply_all(jobs_per_skill=5):
    try:
        for skill in found_skills:
            print(f"🔍 Searching for {skill} jobs...")
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(random.uniform(6.23, 9.4))
            
            driver.get("https://www.linkedin.com/jobs/")
            time.sleep(random.uniform(3, 5))
            
            search_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "jobs-search-box-keyword-id-ember29"))
            )
            search_input.clear()
            search_input.send_keys(skill)
            search_input.send_keys(Keys.RETURN)
            
            time.sleep(random.uniform(3, 7))

            easy_apply_filter = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-tracking-control-name='public_jobs_f_LF']"))
            )
            easy_apply_filter.click()
            
            time.sleep(random.uniform(2, 5))
            
            print(f"\n📝 Ready to apply for {skill} jobs.")
            input("Press Enter after applying to move to the next job...")
            
            # Process job listings
            applied_count = 0
            while applied_count < jobs_per_skill:
                try:
                    job_cards = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card-container"))
                    )
                    
                    if not job_cards:
                        print(f"No more job listings found for {skill}")
                        break
                    
                    job_cards[0].click()
                    time.sleep(random.uniform(2, 4))
                    
                    print(f"\n📝 Please complete the application manually.")
                    input("Press Enter when you've finished this application...")
                    
                    applied_count += 1
                    print(f"✅ Moving to job {applied_count + 1} of {jobs_per_skill} for {skill}")
                    
                except Exception as e:
                    print(f"Error processing job: {e}")
                    input("Press Enter to try the next job or Ctrl+C to exit...")
                    continue
            
            print(f"Completed applications for {skill}. Moving to next skill...")
            time.sleep(random.uniform(5, 10))
            
    except Exception as e:
        print(f"Major error in job_apply_all: {e}")
        send_discord_notif(f"❌ Error in job application process: {e}")







    


input()