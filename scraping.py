from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class Scrapping:
    def __init__(self, data):
        self.base_url = "https://online.immi.gov.au"
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--incognito')
        self.driver = webdriver.Chrome(options=options)
        self.data = data

    def visaHolderEnquiryForm(self):

        form_url = self.data.get('video_url')
        self.driver.get(form_url)
        time.sleep(3)  # Let the page load

        # Find all images on the page
        images = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'img'))
        )

        image_urls = []
        for image in images:
            src = image.get_attribute('src')  # Get the image source URL
            if src:
                image_urls.append(src)

        # Close the browser
        self.driver.quit()

        return image_urls
        