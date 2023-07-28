# import libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from flask import Flask, render_template, request
import urllib.parse

app = Flask(__name__, template_folder='Template')

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/automation", methods = ['GET', 'POST'])
def run_automation():
    if request.method == 'POST' : 
        search_key = request.form.get('search_key')
        response = selenium_code(search_key)
        return response


def selenium_code(search_key):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
    driver = webdriver.Chrome(options=chrome_options)

    # prod = input()
    # Define the URL
    url = "https://www.smartprix.com/products/?q=" + urllib.parse.quote("iphone 14") #todo search_key
    print(url)
    # load the web page
    driver.get(url)

    # set maximum time to load the web page in seconds
    driver.implicitly_wait(10)

    # collect data that are withing the id of contents
    # contents = driver.find_element(By.CLASS_NAME, "sm-products")

    elements = driver.find_elements(By.CLASS_NAME, "sm-product")

    obj = {
        "img" : elements[1].find_element(By.XPATH, "./div/img").get_attribute("src"),
        "name" : elements[1].find_element(By.XPATH, "./a/h2").text,
        "price" : elements[1].find_element(By.XPATH, "./span[@class='price']").text,
        "rating" : elements[1].find_element(By.XPATH, "./div[@class='rating']/span").get_attribute("style"),
        "redirect" : elements[1].find_element(By.XPATH, "./a").get_attribute("href")
    }

    for i in obj.values() : print(i)

    specsList = elements[1].find_elements(By.XPATH, "./ul")
    specs = []
    for spec in specsList :
        specs.append(spec.text)

    for i in specs : print(i)

    driver.quit()
    return obj