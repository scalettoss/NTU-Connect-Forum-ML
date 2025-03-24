import streamlit as st
import pandas as pd
from scrape import scrape_website, clean_extracted_content, extract_specific_content, preprocess_text
import re

st.title("Crawl Data")
urls_input = st.text_area("Enter Website URLs (one per line):")

# Kiểm tra nếu session_state chưa có biến dom_content thì khởi tạo
if "dom_content" not in st.session_state:
    st.session_state.dom_content = []

if st.button("Start"):
    urls = urls_input.strip().split("\n")  # Chuyển đổi chuỗi thành danh sách URL
    st.write(f"Scraping {len(urls)} websites...")

    scraped_data = []
    for url in urls:
        st.write(f"Scraping {url}...")
        result = scrape_website(url.strip())  # Gọi hàm cào dữ liệu
        specific_content = extract_specific_content(result)
        clear_content = clean_extracted_content(specific_content)
        content = preprocess_text(clear_content)
        scraped_data.append(content)

    st.session_state.dom_content = scraped_data  # Lưu vào session_state để không bị mất dữ liệu
    with st.expander("View Extracted Content"):
        for idx, content in enumerate(scraped_data, start=1):
            st.text_area(f"Extracted Content {idx}", content, height=200)

if "dom_content" in st.session_state and st.session_state.dom_content:
    if st.button("Confirm Save to CSV"):
        cleaned_data = [line.strip() for content in st.session_state.dom_content for line in content.split("\n") if line.strip()]
        df = pd.DataFrame({"text": cleaned_data, "label": [0] * len(cleaned_data)})
        df.to_csv("new_raw_data.csv", index=False, header=False)
        st.success("Data saved to rawdata.csv")
