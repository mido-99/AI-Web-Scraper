import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
    extract_target_data_dom,
)
from parse import parse_with_ollama

# Streamlit UI
st.title("AI Web Scraper")
url = st.text_input("Enter Website URL")
target_tag_css = st.text_input('CSS selctor for HTML tag that contains target data (makes process faster)')

# Step 1: Scrape the Website
if st.button("Scrape Website") and url:
    st.write("Scraping the website...")

    # Scrape the website
    dom_content = scrape_website(url)
    body_content = extract_body_content(dom_content)
    cleaned_content = clean_body_content(body_content)
    if target_tag_css:
        target_data_dom = extract_target_data_dom(body_content, target_tag_css)
        st.session_state.target_data_dom = target_data_dom

    # Store the DOM content in Streamlit session state
    st.session_state.dom_content = cleaned_content

    # Display the DOM content in an expandable text box
    with st.expander("View DOM Content"):
        st.text_area("DOM Content", cleaned_content, height=300)


# Step 2: Ask Questions About the DOM Content
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content") and parse_description:
        st.write("Parsing the content...")

        # Parse the content with Ollama
        if 'target_data_dom' in st.session_state:
            dom_chunks = split_dom_content(st.session_state.target_data_dom)
        else:
            dom_chunks = split_dom_content(st.session_state.dom_content)

        parsed_result = parse_with_ollama(dom_chunks, parse_description)
        st.write(parsed_result)

#* Prompt: Can you extract each product info (name, price, monthly price, link, image url) and prepare them for me in a table?