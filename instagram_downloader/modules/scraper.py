from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import os
import wget
from ..models import ScrapedInstagramImage

def scrape_instagram(username, password, hashtag):
    try:
                # Initialize WebDriver
                driver = webdriver.Firefox()

                # Open Instagram
                driver.get("http://www.instagram.com")

                # Fill in the username and password fields
                username_elem = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']"))
                )
                username_elem.clear()
                username_elem.send_keys(username)

                password_elem = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']"))
                )
                password_elem.clear()
                password_elem.send_keys(password)

                # Click the login button
                login_button = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
                )
                login_button.click()

                # Handle "Not Now" buttons (you may need to adjust this part)
                not_now_buttons = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), 'Not Now')]"))
                )
                for button in not_now_buttons:
                    try:
                        button.click()
                    except Exception as e:
                        print(f"Error clicking 'Not Now' button: {str(e)}")
                # Target the search input field
                searchbox = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']"))
                )
                searchbox.clear()

                # Search for the hashtag
                searchbox.send_keys(hashtag)
                time.sleep(5)
                searchbox.send_keys(Keys.ENTER)
                time.sleep(5)
                searchbox.send_keys(Keys.ENTER)
                time.sleep(5)

                # Scroll down to load more images
                driver.execute_script("window.scrollTo(0, 4000);")
                time.sleep(5)

                # Extract image URLs
                images = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, 'img'))
                )
                image_urls = [image.get_attribute('src') for image in images]

                # Create a directory to save images
                save_path = os.path.join(os.getcwd(), hashtag[1:] + "s")
                os.makedirs(save_path, exist_ok=True)

                # Download and save images
                for i, image_url in enumerate(image_urls):
                    try:
                        save_as = os.path.join(save_path, f"{hashtag[1:]}_{i}.jpg")
                        wget.download(image_url, save_as)

                        # Save the scraped image URL to the database
                        scraped_image = ScrapedInstagramImage(
                            hashtag=hashtag,
                            image_url=image_url
                        )
                        scraped_image.save()

                    except Exception as e:
                        print(f"Error downloading image {image_url}: {str(e)}")

                driver.quit()
                return True, "Instagram scraping completed successfully."

    except Exception as e:
                print(f"An error occurred: {str(e)}")
                driver.quit()
                return False, f"Error: {str(e)}"

def save_image_to_database(hashtag, image_url):
    scraped_image = ScrapedInstagramImage(
        hashtag=hashtag,
        image_url=image_url
    )
    scraped_image.save()
