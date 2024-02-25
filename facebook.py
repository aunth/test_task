import openpyxl
from bs4 import BeautifulSoup
import concurrent.futures
import requests
import re
from openpyxl import Workbook, load_workbook
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import os
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from selenium.webdriver.common.keys import Keys

def login_to_facebook(driver, email, password):
	login_url = "https://www.facebook.com/login.php"
	driver.get(login_url)
	
	# Find the email and password input fields and fill them with credentials
	email_input = driver.find_element(By.NAME, "email")
	email_input.send_keys(email)
	password_input = driver.find_element(By.NAME, "pass")
	password_input.send_keys(password)
	
	# Submit the form
	password_input.send_keys(Keys.RETURN)
	
	# Wait for the login to complete
	sleep(2)


def get_email_from_facebook(target_urls):

	driver = webdriver.Chrome()
	if not target_urls:
		print("THere is no target urls")
		return 

	for company, urls in target_urls.items():
		for url in urls:
			try:
				driver.get(url)
			except Exception as e:
				print(f"Error with get response from this URL: {url}")
				continue
			sleep(0.1)
			resp = driver.page_source
			soup = BeautifulSoup(resp, 'html.parser')
			login_required = soup.find('div', {'class': 'pam _9ay2 uiBoxYellow'})
			if login_required:
				login_to_facebook(driver, os.getenv("LOGIN"), os.getenv("PASSWORD"))
			items = soup.find_all('div', {'class': 'x9f619 x1n2onr6 x1ja2u2z x78zum5 x2lah0s x1qughib x1qjc9v5 xozqiw3 x1q0g3np x1pi30zi x1swvt13 xyamay9 xykv574 xbmpl8g x4cne27 xifccgj'})
			for item in items:
				allDetails = item.find_all("div", {"class": "x9f619 x1n2onr6 x1ja2u2z x78zum5 x2lah0s x1nhvcw1 x1qjc9v5 xozqiw3 x1q0g3np xyamay9 xykv574 xbmpl8g x4cne27 xifccgj"})
				for contact in allDetails:
					if '@' in contact.text:
						company.EMAIL = contact.text
						print(contact.text)
	
	driver.close()