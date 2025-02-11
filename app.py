from flask import Flask, request, jsonify, Response
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class Scrapping:
    def __init__(self, data):
        # self.base_url = "https://online.immi.gov.au"
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Uncomment for headless browsing
        options.add_argument('--disable-gpu')
        options.add_argument('--incognito')
        self.driver = webdriver.Chrome(options=options)
        self.data = data

    def visaHolderEnquiryForm(self):
        try:
            form_url = self.data.get('video_url')
            self.driver.get(form_url)

            # Wait for the page to load
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            # Fetch price
            try:
                price_element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.index-price--hHzq8 span'))
                )
                price = price_element.text if price_element else None
            except:
                price = None  # If price element is not found

            # Fetch description
            try:
                description_element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.index-text--cRhk2'))
                )
                description = description_element.text if description_element else None
            except:
                description = None  # If description element is not found

            # Find all images on the page
            try:
                images = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, 'img'))
                )
                image_urls = [
                    img.get_attribute('src') for img in images if img.get_attribute('src') and not img.get_attribute('src').startswith("data:image")
                ]
            except:
                image_urls = []
            result = {
                "price": price,
                "description": description,
                "image_urls": image_urls
            }
            return result

        finally:
            self.driver.quit()  # Ensure the browser is always closed


app = Flask(__name__)

@app.route('/')
def index():  # put application's code here
    return 'API /search method POST'


@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.json
        required_variables = ['video_url']
        for variable in required_variables:
            if variable not in data:
                raise ValueError(f"'{variable}' is missing in the JSON data")

        # Initialize the Scrapping class with the received data
        scraping = Scrapping(data)
        
        # Call the scraping method to get the images
        result = scraping.visaHolderEnquiryForm()

        # Return the results in JSON format
        response = {
            "status": "success",
            "message": "Search successful",
            "results": result
        }
        return jsonify(response)

    except Exception as e:
        error_response = {
            "status": "error",
            "message": "An error occurred",
            "error_details": str(e)
        }
        return jsonify(error_response), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
