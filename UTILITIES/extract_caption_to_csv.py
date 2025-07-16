import time
import csv
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup logging
logging.basicConfig(
    filename="caption_extraction.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Setup Selenium WebDriver to use Brave with automatic download settings
def setup_selenium():

    Chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"  # Update this path with your Brave installation path
    options = webdriver.ChromeOptions()
    options.binary_location = Chrome_path
    
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--ignore-certificate-errors")
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    options.add_experimental_option("useAutomationExtension", False) 
    driver = webdriver.Chrome(options=options)
    return driver

def extract_caption(driver,link):
    """Extract caption from an Instagram reel link."""
    logging.info(f"Processing link: {link}")
    driver.get(link)
    time.sleep(5)  # Adjust delay based on network speed

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    caption_element = soup.select_one("article div[role='button'] div[class='_a9zr'] h1")

    if caption_element:
        raw_html = str(caption_element)
        formatted_caption = raw_html.replace("<br/>", "\n").replace("<br>", "\n")
        clean_caption = BeautifulSoup(formatted_caption, "html.parser").get_text()
        logging.info(f"Caption extracted successfully for link: {link}")
        return clean_caption
    else:
        logging.warning(f"Caption not found for link: {link}. Retrying...")
        return None  # Retry once if caption is not found

# Function to log in to Instagram
def login_to_instagram(driver, username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        username_input = driver.find_element(By.NAME, "username")
        username_input.send_keys(username)
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(10)
        print("Logged in successfully.")
    except Exception as e:
        print("Failed to log in:", e)
def process_links(input_file, output_file):
    """Read links from input file, extract captions, and save to CSV."""
    logging.info("Starting the extraction process.")
    
    with open(input_file, "r") as file:
        links = [line.strip() for line in file.readlines() if line.strip()]
    
    username = "jhonybhai_5"  # Replace with your Instagram username
    password = "jhonybhai@#@#19996"  # Replace with your Instagram password
    driver = setup_selenium()
    login_to_instagram(driver, username, password)
    results = []
    for idx, link in enumerate(links, start=1):
        print("Number = {} Reel Link = {}".format(idx,link))
        caption = extract_caption(driver,link)
        results.append([idx, link, caption])

    # Save results to CSV
    with open(output_file, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["No", "Link", "Caption"])
        writer.writerows(results)
    
    driver.quit()
    logging.info("Extraction process completed. CSV file generated successfully.")

# Run the script
input_file = "UTILITIES/LINKS.TXT"  # Text file with Instagram reel links
output_file = "UTILITIES/captions_output.csv"  # Output CSV file
process_links(input_file, output_file)