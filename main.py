import re      # USE CHROME VERSION 135.0.7049.84
import os
import selenium 
import time 

from selenium import webdriver 
from selenium.webdriver.common.by import  by
from selenium.webdriver.common.keys import keys

driver = webdriver.Chrome(executable_path="./chromedriver-linux64") # checks whether chromedriver for selenium is in the same file as the rest of the code. 

def skills_extract(file_path):         # Func to extract skills from a resume like python,java,django,c++ etc.
     file_path = "resume.txt" # Path to the resume file
     with open(file_path, 'r') as file:
        content = file.read().lower() # Makes chracters lowercase


         known_skills = ["python", "java", "c++", "html", "css", "javascript", "git",
        "github", "machine learning", "deep learning", "nlp", 
        "data structures", "algorithms", "linux", "sql", "django", 
        "flask", "react", "node.js", "c", "data science", "computer vision", "php"]     # List of skills that are most well known in the CS job field

        found_skills = [skill for skill in known_skills if skill in content] # Finds the skills that are in the resume

        return found_skills # Now returns all the various skills found in the resume 


def job_url_gen(skills): # A func to give us job urls 
    base = "https://www.linkedin.com/jobs/search/?keywords=" # Every linkedin job search starts with this 
    urls = [] # The generated urls will be stored here
    for skill in skills:    # Creates a loop with each skill in the list skills
        keyword = skill.replace(" ", "+") # Replaces the blank area with each keyword
        url = base + keyword # Adds the keywords to the base url
        urls.append(url) # Changes the urls list adding new job urls

def login_to_linkedin(username, password):       # Creates a function to login to linkedin using a username and password that is given 
    driver.get("https://www.linkedin.com/login")
    time.sleep(5)


     email_element = driver.find_element(BY.ID, "username") # Finds the place on linkedin website to input username via using an id attribute called username and stores it in email_element 
     password_element = driver.find_element(BY.ID, "password") # Finds the place on linkedin's web to input password via identifying it with an id attribute called password and stores it in password_element

     email_element.send_keys(username) # Takes the username and inputs in the username field identified above 
     password_element.send_keys(password) # Takes the password and inputs it in the password field identified above 

     password_element.send_keys(keys.return) # Press the enter key while in the password field on linkedin
     time.sleep(5) # Stops running the program for 5 seconds then resumes 

     login_to_linkedin("your_email@example.com", "your_password") # ENTER YOUR LINKEDIN EMAIL AND PASSWORD HERE

def job_apply_all(urls): # A function to apply to all job urls in the list urls
     for url in urls:
        job_appply(url) # Opens each job url in a new tab
        time.sleep(5) # Stops running the program for 5 seconds then resumes
        