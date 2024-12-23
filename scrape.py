from selenium.webdriver import Chrome, ChromeOptions
from selenium_driverless.sync import webdriver as sync_webdriver
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os


def scrape_website(website):
    
    print("Scraping Website...")
    with sync_webdriver.Chrome() as driver:
        driver.get(website)
        html = driver.page_source
        return html

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    print('HTML soup made...')
    return str(body_content) if body_content else ""

def extract_target_data_dom(body_content, target_tag_css):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    
    # Extract only the DOM of element that has the target data
    target_data_dom = soup.select_one(target_tag_css)
    return target_data_dom

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content

def split_dom_content(dom_content, max_length=20_000):
    
    if not isinstance(dom_content, str):
        dom_content = str(dom_content)

    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]