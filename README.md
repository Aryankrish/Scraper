# LinkedIn Scraper

## Description
This script automates the process of scraping profile and company information from LinkedIn using Selenium. It fetches data for provided LinkedIn profiles and companies and saves the results in JSON format.

---

## Features
- Logs into LinkedIn with provided credentials.
- Fetches details of individual profiles, including:
  - Name
  - Job Title
  - Location
  - About section
- Fetches details of companies, including:
  - Name
  - Industry
  - Headquarters
  - Overview section
- Saves the scraped data into `profiles.json` and `companies.json`.

---

## Requirements
- Python 3.x
- Selenium
- Google Chrome
- ChromeDriver

---

## Installation

1. Install the required Python libraries:
   ```bash
   pip install selenium
   ```

2. Download and install [Google Chrome](https://www.google.com/chrome/).

3. Download the compatible version of [ChromeDriver](https://chromedriver.chromium.org/downloads) and add it to your system PATH.

---

## Usage

### Command Line Arguments
- `-u` or `--username`: LinkedIn username (email)
- `-p` or `--password`: LinkedIn password
- `-f` or `--filename`: Path to the file containing LinkedIn links (one link per line)

### Running the Script
1. Create a text file with the LinkedIn profile and company links, e.g., `links.txt`:
   ```text
   https://www.linkedin.com/in/example-profile
   https://www.linkedin.com/company/example-company
   ```

2. Run the script:
   ```bash
   python scraper.py -u your_email -p your_password -f links.txt
   ```

3. Output files `profiles.json` and `companies.json` will be created with the scraped data.

---
