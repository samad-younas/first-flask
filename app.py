from flask import Flask, request, jsonify
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
        # options.add_argument('--headless')  # Uncomment for headless browsing
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
