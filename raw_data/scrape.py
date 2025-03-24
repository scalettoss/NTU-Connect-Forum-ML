from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
import re

AUTH = 'brd-customer-hl_48ad7741-zone-scraping_browser1:fyqdt7e1b101'
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'

tag = "div" # chọn thẻ cần cào
tag_class = "structItem-title" # class or id

def scrape_website(webUrl):
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Đang cào dữ liệu')
        driver.get(webUrl)
        html = driver.page_source
        return html
    
def extract_specific_content(html):
    soup = BeautifulSoup(html, "html.parser")
    titles = soup.find_all(tag, class_=tag_class)
    return "\n".join(str(title) for title in titles)

def clean_extracted_content(content):
    soup = BeautifulSoup(content, "html.parser")
    return "\n".join(title.get_text(strip=True) for title in soup.find_all(tag, class_=tag_class))

def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', text)  # Loại bỏ dấu câu
    text = text.lower().strip()  # Chuyển thành chữ thường và loại bỏ khoảng trắng thừa
    return text




