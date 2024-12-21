from selenium.webdriver import Chrome, ChromeOptions
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os


def scrape_website(website):
    
    print("Scraping Website...")
    with Chrome(options=ChromeOptions()) as driver:
        driver.get(website)
        driver.implicitly_wait(10)
        html = driver.page_source
        return html

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    print('HTML soup made...')
    return str(body_content) if body_content else ""

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

def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
