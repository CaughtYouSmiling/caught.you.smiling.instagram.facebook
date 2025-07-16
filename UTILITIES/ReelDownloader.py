from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import os
import shutil
import random
import time
from selenium_stealth import stealth
import pandas as pd

# initializing a list with two User Agents
useragentarray = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
]

def setup_stealth_browser(driver):
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)
    
    return driver

# Function to close Instagram login pop-up
def close_login_popup(driver):
    try:
        close_button = driver.find_element(By.XPATH, "//div[@role='button' and contains(@class, 'x1110hf1') and contains(@class, 'x972fbf') and contains(@class, 'xcfux61')]")
        close_button.click()
        print("Instagram login pop-up closed.")
    except Exception as e:
        print("No login pop-up found or could not close it:", e)

# Function to scroll and capture page sources
def scroll_and_capture_page_sources(url,driver, max_scrolls=10000):
    driver.get(url)
    page_sources = []
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    for _ in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(7)  # Increased wait time for content to load
        close_login_popup(driver)
        
        # Capture the page source
        page_source = driver.page_source
        page_sources.append(page_source)
        
        # Get new scroll height and check if it's the same as the last height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    return page_sources

# Function to extract Instagram reel links from a single page source
def extract_links_from_page_source(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    links = []
    
    for a_tag in soup.find_all('a', href=True):
        if '/reel/' in a_tag['href']:
            full_url = "https://www.instagram.com" + a_tag['href']
            links.append(full_url)
    
    return links

# # Setup Selenium WebDriver to use Brave with automatic download settings
# def setup_selenium(download_folder):
#     if not os.path.exists(download_folder):
#         os.makedirs(download_folder)

#     Chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"  # Update this path with your Brave installation path
#     options = webdriver.ChromeOptions()
#     options.binary_location = Chrome_path
    
#     prefs = {
#         "download.default_directory": os.path.abspath(download_folder),  # Set the download folder
#         "download.prompt_for_download": False,
#         "download.directory_upgrade": True,
#         "safebrowsing.enabled": True,
#     }
#     options.add_experimental_option("prefs", prefs)
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
#     options.add_argument("--disable-gpu")
#     options.add_argument("--disable-blink-features=AutomationControlled")
#     options.add_argument("--window-size=1920x1080")
#     options.add_argument("--ignore-certificate-errors")
#     options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
#     options.add_experimental_option("useAutomationExtension", False) 
#     driver = webdriver.Chrome(options=options)
#     return driver

# Setup Selenium WebDriver to use chrome with automatic download settings
def setup_selenium(download_folder):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    chrome_options = Options()
    
    prefs = {
        "download.default_directory": os.path.abspath(download_folder),  # Set the download folder
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    chrome_options.add_experimental_option("useAutomationExtension", False) 
    
    # Set up Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": random.choice(useragentarray)})
    print("driver = ",driver)
    
    return driver

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
        time.sleep(5)
        print("Logged in successfully.")
    except Exception as e:
        print("Failed to log in:", e)

# Function to get the next available serialized filename
def get_next_serialized_filename(download_folder):
    existing_files = [f for f in os.listdir(download_folder) if f.startswith('Video_') and f.endswith('.mp4')]
    if existing_files:
        last_file = max(existing_files, key=lambda x: int(x.split('_')[1].split('.')[0]))
        next_index = int(last_file.split('_')[1].split('.')[0]) + 1
    else:
        next_index = 1
    return f"Video_{next_index}.mp4"

# Function to check if the download is complete
def is_download_complete(download_folder):
    temp_files = [f for f in os.listdir(download_folder) if f.endswith('.crdownload') or f.endswith('.tmp')]
    return len(temp_files) == 0

# Function to handle file renaming after download
def rename_downloaded_file(download_folder, new_filename):
    # Wait until there are no active downloads
    while not is_download_complete(download_folder):
        time.sleep(5)  # Check every 5 seconds
    files = [f for f in os.listdir(download_folder) if f.endswith('.mp4')]
    
    if files:
        latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(download_folder, x)))
        latest_file_path = os.path.join(download_folder, latest_file)
        new_file_path = os.path.join(download_folder, new_filename)
        shutil.move(latest_file_path, new_file_path)
        print(f"File renamed to: {new_filename}")

# Function to download Instagram reels using sssinstagram.net
def download_instagram_reels_sssinstagram(reel_url, download_folder):
    driver = setup_selenium(download_folder)
    driver = setup_stealth_browser(driver)
    # Navigate to sssinstagram's Instagram Reel Downloader
    driver.get("https://sssinstagram.com/reels-downloader")
    time.sleep(10)
    try:
        # Find the input box and paste the reel URL
        input_box = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='input']"))
        )
        input_box.send_keys(reel_url)
        
        # Click the Download button to submit the URL
        download_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
        )
        download_button.click()
        time.sleep(10)

    
        # Wait for either of the "Download Video" buttons to appear and get the href
        download_video_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='button button--filled button__download']"))
        )

        # Extract the href link for the video
        video_download_link = download_video_button.get_attribute("href")
        print(f"Download link: {video_download_link}")
        
        # Download the video manually using the extracted href link
        driver.get(video_download_link)
        time.sleep(10)  # Give time for the download to start
        
        # Generate a serialized filename
        serialized_filename = get_next_serialized_filename(download_folder)

        # Rename the file after download
        rename_downloaded_file(download_folder, serialized_filename)

        # print(f"Download attempt finished for: {reel_url}")
        driver.quit() 
        return 1
        
    except Exception as e:
        print(f"Error clicking the download button or fetching video link: {str(e)}")
        driver.quit() 
        return 0
    
# Add this function to handle retries
def download_with_retry(reel_url, download_folder, max_retries=7):
    attempt = 0
    success = False

    while attempt < max_retries and not success:
        print("attempt Reel= ",attempt)
        number = download_instagram_reels_sssinstagram(reel_url, download_folder)
        if number == 1:
            success = True
            break
        else:
            attempt += 1
            time.sleep(5)  # Wait for a few seconds before retrying
            
    if not success:
        print(f"Failed to download reel after {max_retries} attempts: {reel_url}")
        
# # Function to get the next available serialized filename
# def get_next_serialized_filename_thumbnail(download_folder):
#     existing_files = [f for f in os.listdir(download_folder) if f.startswith('thumb_') and f.endswith('.jpg')]
#     if existing_files:
#         last_file = max(existing_files, key=lambda x: int(x.split('_')[1].split('.')[0]))
#         next_index = int(last_file.split('_')[1].split('.')[0]) + 1
#     else:
#         next_index = 1
#     return f"thumb_{next_index}.jpg"

# # Function to check if the download is complete
# def is_download_complete_thumbnail(download_folder):
#     temp_files = [f for f in os.listdir(download_folder) if f.endswith('.crdownload') or f.endswith('.tmp')]
#     return len(temp_files) == 0

# # Function to handle file renaming after download
# def rename_downloaded_file_thumbnail(download_folder, new_filename):
#     # Wait until there are no active downloads
#     while not is_download_complete_thumbnail(download_folder):
#         time.sleep(5)  # Check every 5 seconds
#     files = [f for f in os.listdir(download_folder) if f.endswith('.jpg')]
    
#     if files:
#         latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(download_folder, x)))
#         latest_file_path = os.path.join(download_folder, latest_file)
#         new_file_path = os.path.join(download_folder, new_filename)
#         shutil.move(latest_file_path, new_file_path)
#         print(f"File renamed to: {new_filename}")
        
# Function to download Instagram reels using sssinstagram.net
# def download_instagram_reels_sssinstagram_thumbnails(reel_url, download_folder):
#     driver = setup_selenium(download_folder)
#     driver = setup_stealth_browser(driver)

#     # Navigate to sssinstagram's Instagram Reel Downloader
#     driver.get("https://sssinstagram.net/photo")
#     time.sleep(2)
#     try:
#         # Find the input box and paste the reel URL
#         # input_box = driver.find_element(By.XPATH, "//input[@name='url']")
#         input_box = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, "//input[@name='url']"))
#         )
#         input_box.send_keys(reel_url)
        
#         # Click the Download button to submit the URL
#         # download_button = driver.find_element(By.XPATH, "//button[@type='submit']")
#         download_button = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
#         )
#         download_button.click()
#         time.sleep(3)

    
#         # Wait for either of the "Download Video" buttons to appear and get the href
#         download_video_button = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, "//body//div//main"))
#         )

#         # Extract the href link for the video
#         video_download_link = download_video_button.get_attribute("href")
#         print(f"Download link: {video_download_link}")
        
#         # Download the video manually using the extracted href link
#         driver.get(video_download_link)
#         time.sleep(5)  # Give time for the download to start

#         # Generate a serialized filename
#         serialized_filename = get_next_serialized_filename_thumbnail(download_folder)

#         # Rename the file after download
#         rename_downloaded_file_thumbnail(download_folder, serialized_filename)

#         print(f"Download attempt finished for: {reel_url}")
#         return 1
        
#     except Exception as e:
#         print(f"Error clicking the download button or fetching video link: {str(e)}")
#         return 0

#     driver.quit()  # Close the browser once done
        
# # Add this function to handle retries
# def download_with_retry_thumbnails(reel_url, download_folder, max_retries=5):
#     attempt = 0
#     success = False

#     while attempt < max_retries and not success:
#         print("attempt Thumbnail= ",attempt)
#         number = download_instagram_reels_sssinstagram_thumbnails(reel_url, download_folder)
#         if number == 1:
#             success = True
#             break;
#         else:
#             attempt += 1
#             time.sleep(5)  # Wait for a few seconds before retrying
            
#     if not success:
#         print(f"Failed to download reel after {max_retries} attempts: {reel_url}")
        
def extract_reel_date(driver, url):
    # Open the reel link
    driver.get(url)
    time.sleep(10)  # Wait for the page to fully load (adjust the time as necessary)

    try:
        # Find the date element in the HTML structure
        date_element = driver.find_element(By.XPATH, "//time[@class='x1p4m5qa']")
        date_text = date_element.get_attribute('datetime')  # Extract the date value from 'datetime' attribute
        return date_text
    except Exception as e:
        print(f"Error extracting date from {url}: {e}")
        return None

def ordering_reels(driver, input_file):
    
    # Set up Selenium WebDriver (Make sure to provide the correct path to your WebDriver)
    # Chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"  # Update this path with your Chrome installation path
    # options = webdriver.ChromeOptions()
    # options.binary_location = Chrome_path

    # options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    # # driver = webdriver.Chrome(options=options)
    # Read reel links from the .txt file
    with open(input_file, 'r') as file:
        reel_links = [line.strip() for line in file.readlines()]

    # List to store extracted data
    data = []
    
    count = 1
    # Loop through each reel link and extract the date
    for reel_link in reel_links:
        print("Reel link = {} , Reel Number = {}".format(count,reel_link))
        date = extract_reel_date(driver, reel_link)
        if date:
            data.append([reel_link, date])
        count+=1

    # Close the WebDriver
    driver.quit()

    # Create a DataFrame and sort it by date
    df = pd.DataFrame(data, columns=['Reel Link', 'Date'])
    df['Date'] = pd.to_datetime(df['Date'])  # Convert date strings to datetime objects for sorting
    df = df.sort_values(by='Date')  # Set ascending=False for reverse order

    # Save to CSV
    df.to_csv('reel_dates.csv', index=False)

    # Save ordered reel links to .txt file
    with open('ordered_reel_links.txt', 'w') as file:
        for link in df['Reel Link']:
            file.write(link + '\n')
            
# Main function to automate the process
def main():
    
    # STEP 1
    
    # username = "johnmorgan1259"  # Replace with your Instagram username
    # password = "1991-=-=ar"  # Replace with your Instagram password
    # website_url = 'https://www.instagram.com/pageonthingsbeingmade/reels/'  # Replace with actual website URL
    download_folder = "VIDEOS"  # Set this to your desired download folder
    # # thumbnail_download_folder = "DegaDiosReelsThumbnails"

    # driver = setup_selenium(download_folder)

    # login_to_instagram(driver, username, password)

    # # Scroll down and capture page sources
    # page_sources = scroll_and_capture_page_sources(website_url,driver)

    # # Extract reel links from each page source
    # all_reel_links = []
    
    # for page_source in page_sources:
    #     reel_links = extract_links_from_page_source(page_source)
    #     all_reel_links.extend(reel_links)

    # # Remove duplicates
    # all_reel_links = list(set(all_reel_links))
    
    # # Save all reel links to .txt file
    # with open('all_reel_links.txt', 'w') as file:
    #     for link in all_reel_links:
    #         file.write(link + '\n')
    
    # driver.quit()
    
    # STEP 2
    
    # ordering_reels(driver, input_file="all_reel_links.txt")

    # STEP 3
    
    # Read reel links from the .txt file
    with open('ordered_reel_links.txt', 'r') as file:
        reel_links = [line.strip() for line in file.readlines()]
        for reel_link in reel_links:
            download_with_retry(reel_link, download_folder)
            
    # # STEP 4
    # # Read reel links from the .txt file
    # with open('ordered_reel_links.txt', 'r') as file:
    #     reel_links = [line.strip() for line in file.readlines()]
    #     for reel_link in reel_links:
    #         download_with_retry_thumbnails(reel_link, thumbnail_download_folder)

if __name__ == "__main__":
    main()
