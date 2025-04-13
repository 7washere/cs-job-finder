import re      # USE CHROME VERSION 135.0.7049.84
import os
import selenium 
import time 
import requests 
import random 
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WEBHOOK = "YOUR_WEBHOOK_URL" # Replace with your actual webhook URL (DISCORD WEBHOOK)
    def send_discord_notif(message):  # Function to send a Discord notification via webhook 
        def send_discord_notification(message):
    data = {
        "content": message  # Creates a dictionary with the content and message values 
    }
    try:  # Error handling. Any errors occur goes to the except block 
        response = requests.post(WEBHOOK, json=data)
        response.raise_for_status() # Checks if the request was successful
    except requests.exceptions.RequestException as e: 
        print(f"Failed to send Discord notification: {e}") # Prints the error message in the console incase something goes wrong 

driver = webdriver.Chrome(executable_path="./chromedriver-linux64") # checks whether chromedriver for selenium is in the same file as the rest of the code. 

def skills_extract(file_path):  # Func to extract skills from a resume like python,java,django,c++ etc.
    with open(file_path, 'r') as file: # Opens the resume file  
        content = file.read().lower()  # Makes characters lowercase

    known_skills = ["python", "java", "django", "c++", "javascript", "react", "angular", "vue", "ruby", "rails", "swift", "kotlin", "php", "mysql", "mongodb", "sql", "aws", "azure", "google cloud"]  # List of skills
    found_skills = [skill for skill in known_skills if skill in content]  # Finds the skills that are in the resume
    return found_skills  # Now returns all the various skills found in the resume

def job_url_gen(skills): # A func to give us job urls 
    base = "https://www.linkedin.com/jobs/search/?keywords=" # Every linkedin job search starts with this 
    urls = [] # The generated urls will be stored here
    for skill in skills:    # Creates a loop with each skill in the list skills
        keyword = skill.replace(" ", "+") # Replaces the blank area with each keyword
        url = base + keyword # Adds the keywords to the base url
        urls.append(url) # Changes the urls list adding new job urls

    return urls

def login_to_linkedin(username, password):
    driver.get("https://www.linkedin.com/login") # Opens the linkedin login page 

    email_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "username")))
    password_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "password")))

    email_element.clear()
    email_element.send_keys(username)

    password_element.clear()
    password_element.send_keys(password)

    password_element.send_keys(Keys.RETURN)

    # Wait for the login to complete
    WebDriverWait(driver, 10).until(EC.title_contains("LinkedIn"))

    # Check if the login was successful
    if driver.title == "LinkedIn":
        print("Login successful")
    else:
        print("Login failed")

def job_apply_all(urls): # A function to apply to all job urls in the list urls
    for url in urls:
        driver.get(url) # Opens each job url in the current tab
        time.sleep(5) # Stops running the program for 5 seconds then resumes
        try:
            easy_apply_button = WebDriverWait(driver, 10).until( # makes selenium wait for 10 seconds 
                EC.element_to_be_clickable((By.CLASS_NAME, "jobs-apply-button")) # Waits for the apply button to be clickable
            )
            easy_apply_button.click() # Clicks the apply button
            time.sleep(random.uniform(1.8, 6.4)) # Wait for the apply form to open

            submit_button = WebDriverWait(driver, 10).until( # Makes selenium wait for 10 seconds 
                EC.element_to_be_clickable((By.CLASS_NAME, "artdeco-button--primary")) #   waits for the submit button to be clickable
            )
            submit_button.click() # Clicks on the submit button
            time.sleep(2) # Stops program for 2 seconds then resumes 
            
            send_discord_notif("Job applied successfully!") # Notifies the user that the job has been applied in discord
            print(f"Job applied successfully to {url}") # Notifies the user that the job has been applied in terminal

        except Exception as e:
            print(f"Error applying to job {url}: {e}") # Notifies the user if any error occurred while applying to a job giving the job url
            send_discord_notif(f"Error applying to job {url}: {e}")
            
        time.sleep(5) # Stops running the program for 5 seconds then resumes
        fill_easy_form() # Calls the function to fill the easy apply form
      
def fill_easy_form():
    try:
        phone_input = driver.find_element(By.CSS_SELECTOR, "input[aria-label='Phone number']") 
        if phone_input.get_attribute("value") == "":
            phone_input.send_keys("1234567890")  # Replace with your number

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
                print("Final submit button clicked.")
                break 

    except Exception as e:
        print(f"Skipped optional fields or form already filled: {e}") # Notifies the user if any optional fields or form were skipped or already filled

    time.sleep(5) # Stops running the program for 5 seconds then resumes


