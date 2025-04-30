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
import testing as main

username = config.username
password = config.password
driver = main.driver

options = int(input("Enter what you want to do. 1 -> Apply to jobs. 2 -> Analyse resume  "))


if options == 1:
    main.send_discord_notif("🚀 Starting LinkedIn Job Application Bot...")
    print("🚀 Starting LinkedIn Job Application Bot...")

    main.skills_extract("resume.txt")
    main.send_discord_notif("Extracting Skills from Resume")
    print("Extracting Skills from Resume")

    main.job_url_gen()
    main.send_discord_notif("Generating Job URLs")
    print("Generating Job URLs")

    main.login_to_linkedin(driver, username, password)
    main.send_discord_notif("Logging into LinkedIn")
    print("Logging into linkedin")

    main.job_apply_all(jobs_per_skill=5)  
    main.send_discord_notif("Applying to jobs")
    print("Applying to jobs")



    input("Press Enter to close the browser...")  # Wait for user input before closing the browser

elif options == 2:
    print("WIP")
