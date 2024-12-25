from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import argparse

parser = argparse.ArgumentParser(description='Linkedin Scraper')

driver = webdriver.Chrome()
parser.add_argument('-u', '--username', type=str, required=True, help='Linkedin Username')
parser.add_argument('-p', '--password', type=str, required=True, help='Linkedin Password')
parser.add_argument('-f', '--filename', type=str, required=True, help='File containing Linkedin links')
args = parser.parse_args()
user=args.username
password=args.password
filename=args.filename

def waitTillElement(driver, element):
    try:
        element_present = EC.presence_of_element_located((By.ID, element))
        WebDriverWait(driver, 5).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    sleep(2)
def loginLinkedIn(driver,username, password):
    driver.get("https://www.linkedin.com/login")
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, ".btn__primary--large").click()
    waitTillElement(driver,"ember424")


loginLinkedIn(driver,user,password)


def getProfile(driver, id):
    driver.get("https://www.linkedin.com/in/"+id)
    waitTillElement(driver, "profile-content")
    try:
        name = driver.find_element(By.CSS_SELECTOR, ".XcqMGBrLgSDsfiaCuMsRfEqqGQIKDfI").text 
    except:
        name = "Not Found"
    try:
        JobTitle = driver.find_element(By.CSS_SELECTOR, ".text-body-medium").text
    except:
        JobTitle = "Not Found"
    try:
        location = driver.find_element(By.CSS_SELECTOR, ".text-body-small.inline.t-black--light.break-words").text
    except:
        location = "Not Found"
    try:
        driver.find_element(By.CSS_SELECTOR, ".inline-show-more-text__button").click()
    except:
        pass
    try:
        for i in driver.find_elements(By.TAG_NAME,"section"):
            if  "About" in i.text:
                about = i
                break
        about = about.find_element(By.CSS_SELECTOR, ".aMzyYNDgIKUOyCZrTaSqHAmnsrpHAuwdZss").text
    except:
        about = "Not Found"
    return {
        "name": name,
        "JobTitle": JobTitle,
        "location": location,
        "about": about
    }



def getCompany(driver,id):
    driver.get("https://www.linkedin.com/company/"+id+"/home")
    try:
        name = driver.find_element(By.CSS_SELECTOR, ".org-top-card-summary__title").text
    except:
        name = "Not Found"
    try:
        Industry = driver.find_element(By.CSS_SELECTOR, ".org-top-card-summary-info-list")
        Industry = Industry.find_elements(By.CSS_SELECTOR, ".org-top-card-summary-info-list__info-item")[0].text
    except:
        Industry = "Not Found"
    try:
        Headquaters = driver.find_element(By.CSS_SELECTOR, ".org-top-card-summary-info-list")
        Headquaters = Headquaters.find_elements(By.CSS_SELECTOR, ".org-top-card-summary-info-list__info-item")[1].text
    except:
        Headquaters = "Not Found"
    try:
        for i in driver.find_elements(By.TAG_NAME,"section"):
            if  "Overview" in i.text:
                for j in i.find_elements(By.TAG_NAME,"a"):
                    if "see more" in j.text:
                        j.click()
                        break
    except:
        pass
    try:
        for i in driver.find_elements(By.TAG_NAME,"section"):
            if  "Overview" in i.text:
                about = i
                break
        Overview = about.find_element(By.CSS_SELECTOR, ".lt-line-clamp__raw-line").text
    except Exception as e:
        Overview = "Not Found"
        print(e)
    return {
        "name": name,
        "Industry": Industry,
        "Headquaters": Headquaters,
        "Overview": Overview
    }


with open(filename, "r") as f:
    links = [line.strip() for line in f.readlines()]

profiles = []
companies = []

for link in links:
    if "linkedin.com/in/" in link:
        profile_id = link.split("linkedin.com/in/")[-1].strip("/")
        print(f"Fetching profile: {profile_id}")
        profiles.append(getProfile(driver, profile_id))
    elif "linkedin.com/company/" in link:
        company_id = link.split("linkedin.com/company/")[-1].strip("/")
        company_id = company_id.split("/")[0].strip("/")
        print(f"Fetching company: {company_id}")
        companies.append(getCompany(driver, company_id))

driver.quit()

# Saving the results to JSON files
import json

with open("profiles.json", "w") as profile_file:
    json.dump(profiles, profile_file, indent=4)

with open("companies.json", "w") as company_file:
    json.dump(companies, company_file, indent=4)

print("Data saved to profiles.json and companies.json")
