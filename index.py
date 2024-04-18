import os
import json
import time
import multiprocessing
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from PIL import Image

start_time = time.time()

desktop_user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4644.188 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
]

mobile_user_agents = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Mobile/15E148 Safari/604.1"
]

def main(urls):
    # Create directory for saving screenshots if it doesn't exist
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
        os.makedirs("screenshots/Desktop")
        os.makedirs("screenshots/Mobile")

     # Create a multiprocessing Queue
    queue = multiprocessing.Queue()

    # Populate the queue with indices
    for index in range(1, len(urls) + 1):
        queue.put(index)

    # Create multiprocessing pool for capturing screenshots concurrently
    with multiprocessing.Pool() as pool:
        # Determine the number of processes to run concurrently
        num_processes = 5
        # Calculate the number of tasks per chunk
        chunksize = len(urls) // num_processes + (len(urls) % num_processes > 0)
        # Map the function to capture screenshots to the list of URLs
        pool.starmap(capture_screenshot, [(url, index) for index, url in enumerate(urls, start=1)], chunksize=chunksize)

        
def capture_screenshot(url, screenshot_index):
    if(check_url_in_all_used(url)):
        print(f"{url} already used. Skipping screenshot")
        return

    # if(not check_filtered_value(f"{screenshot_index:05d}.jpeg")):
    #     print(f"{url} - {screenshot_index:05d}.jpeg EXISTS! skipping.")
    #     return

    # if(not check_filtered_value_by_failed(f"{screenshot_index:05d}.jpeg")):
    #     print(f"{url} - {screenshot_index:05d}.jpeg not in failed - skipping.")
    #     return

    # Set up Chrome options
    desktop_user_agent = random.choice(desktop_user_agents)
    mobile_user_agent = random.choice(mobile_user_agents)

    print(f"Using user agents: {desktop_user_agent}, {mobile_user_agent}")

    # Set up common options
    common_options = Options()
    # common_options.add_argument("--headless")  # Run Chrome in headless mode
    common_options.add_argument("--start-maximized")
    common_options.add_argument("--disable-infobars")
    common_options.add_argument("--disable-extensions")
    common_options.add_argument("--disable-dev-shm-usage")
    common_options.add_argument("--no-sandbox")
    common_options.add_argument("--disable-browser-side-navigation")
    common_options.add_argument("--disable-gpu")

    # Adding argument to disable the AutomationControlled flag 
    common_options.add_argument("--disable-blink-features=AutomationControlled") 

    # Set browser language
    common_options.add_argument("--lang=en")
    
    # Exclude the collection of enable-automation switches 
    common_options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    
    # Turn-off userAutomationExtension 
    common_options.add_experimental_option("useAutomationExtension", False) 

    # Create web driver instance
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=common_options)

    # Changing the property of the navigator value for webdriver to undefined 
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 

    try:
        # Navigate to the URL in both desktop and mobile drivers
        driver.get(url)

        time.sleep(25)
        
        # Dequeue an index from the queue

        print(f"Accessing URL: {url} - {screenshot_index}")

         # Wait until DOMContentLoaded event fires
        def dom_content_loaded(driver):
            return driver.execute_script("return document.readyState") == "complete"
        
        WebDriverWait(driver, 10).until(dom_content_loaded)


        # Save screenshots for desktop and mobile versions
        desktop_screenshot_path = f"screenshots/Desktop/{screenshot_index:05d}.jpeg"
        mobile_screenshot_path = f"screenshots/Mobile/{screenshot_index:05d}.jpeg"
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {'userAgent': desktop_user_agent})
        driver.set_window_size(1920, 1080)  # Set window size for mobile

        driver.save_screenshot(desktop_screenshot_path)

        time.sleep(5)
        # Set up user agent and window size for mobile
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {'userAgent': mobile_user_agent})
        driver.set_window_size(375, 1200)  # Set window size for mobile


        driver.save_screenshot(mobile_screenshot_path)

        verify_all_used_json(f"{screenshot_index:05d}.jpeg", url)
        print(f"Screenshots taken successfully - {screenshot_index}")

        # Increment counter for naming screenshots

    except TimeoutException:
        print(f"Timeout occurred while loading {url}. Skipping...")
        update_failed_json(f"{screenshot_index:05d}.jpeg", url)
        # Capture black screen screenshot
        black_screen = Image.new('RGB', (375, 812), (0, 0, 0))
        black_screen.save(f"screenshots/Desktop/{screenshot_index:05d}.jpeg")
        black_screen.save(f"screenshots/Mobile/{screenshot_index:05d}.jpeg")

    except Exception as e:
        print(f"Error occurred while capturing screenshot of {url}: {e}")
        update_failed_json(f"{screenshot_index:05d}.jpeg", url)
        # Capture black screen screenshot
        black_screen = Image.new('RGB', (375, 812), (0, 0, 0))
        black_screen.save(f"screenshots/Desktop/{screenshot_index:05d}.jpeg")
        black_screen.save(f"screenshots/Mobile/{screenshot_index:05d}.jpeg")

    finally:
        print("Ended")
        driver.quit()
        driver.quit()


def update_failed_json(filename, url):
    failed_screenshots = []

    # Check if the JSON file exists
    if os.path.exists("failed.json"):
        # Load existing data
        with open("failed.json", "r") as json_file:
            failed_screenshots = json.load(json_file)["failed"]

    # Append new failed screenshot
    failed_screenshots.append({"name": filename, "url": url})

    # Write updated data to JSON file
    with open("failed.json", "w") as json_file:
        json.dump({"failed": failed_screenshots}, json_file, indent=4)

def verify_all_used_json(filename, url):
    # Initialize all_used list
    all_used = []

    # Check if the JSON file exists
    if os.path.exists("all_used.json"):
        # Load existing data
        with open("all_used.json", "r") as json_file:
            all_used = json.load(json_file)

    # Add the object to the list
    all_used.append({"name": filename, "url": url})

    # Write updated data to JSON file
    with open("all_used.json", "w") as json_file:
        json.dump(all_used, json_file, indent=4)

def check_url_in_all_used(url):
    if os.path.exists("all_used.json"):
        # Load data from all_used.json
        with open("all_used.json", "r") as all_used_file:
            all_used_data = json.load(all_used_file)

        # Extract used urls from all_used.json
        used_urls = [item["url"] for item in all_used_data]

        # Check if the provided URL is in used_urls
        if url in used_urls:
            return True
        else:
            return False

def check_filtered_value(filteredValue):
    # Read contents from "not_created.json"
    with open("not_created.json", "r") as f:
        not_created_data = json.load(f)

    # Check if filteredValue exists in not_created array
    if filteredValue in not_created_data.get("not_created", []):
        return True
    else:
        return False
    
def check_filtered_value_by_failed(filteredValue):
    # Read contents from "failed.json"
    with open("failed.json", "r") as f:
        failed_data = json.load(f)

    # Check if filteredValue exists in "name" property of objects in "failed" array
    for item in failed_data.get("failed", []):
        if item.get("name") == filteredValue:
            return True
        
    return False

# Initialize an empty list to store the URLs
urls = []

# Load URLs from the JSON file
with open('urls.json', 'r') as file:
    data = json.load(file)
    urls = data['urls']

if __name__ == '__main__':
    main(urls)

end_time = time.time()

# Calculate the duration
duration = end_time - start_time

print(f"Script took {duration} seconds to run.")
