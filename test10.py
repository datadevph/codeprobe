import streamlit as st
from bs4 import BeautifulSoup
from Wappalyzer import Wappalyzer, WebPage
import requests
import jsbeautifier
import re

def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return str(soup)

def extract_css_from_html(html_code):
    styles = set()
    soup = BeautifulSoup(html_code, 'html.parser')
    style_tags = soup.find_all('style')

    for style_tag in style_tags:
        css_content = style_tag.get_text()
        extracted_styles = re.findall(r'{(.*?)}', css_content, re.DOTALL)
        styles.update(extracted_styles)

    return styles

def extract_js_from_html(html_code):
    scripts = set()
    soup = BeautifulSoup(html_code, 'html.parser')
    script_tags = soup.find_all('script')

    for script_tag in script_tags:
        js_content = script_tag.get_text()
        scripts.add(js_content)

    return scripts

def beautify_js(js_code):
    beautified_code = jsbeautifier.beautify(js_code)
    return beautified_code

def detect_technologies(url):
    wappalyzer = Wappalyzer.latest()
    webpage = WebPage.new_from_url(url)
    analysis_result = wappalyzer.analyze(webpage)
    technologies = analysis_result.technologies if hasattr(analysis_result, 'technologies') else set()
    return technologies

def learn_links(technology):
    learning_links = {
        "HTML": "https://developer.mozilla.org/en-US/docs/Web/HTML",
        "CSS": "https://developer.mozilla.org/en-US/docs/Web/CSS",
        "JavaScript": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
        # Add more technologies and corresponding learning links as needed
    }

    return learning_links.get(technology, "No learning link available.")

def main():
    st.title("CodeProbe SEO Analyzer")

    # Ask user for URL
    url = st.text_input("Enter website URL:")
    if url == "Enter website URL:":
        url = ""

    if st.button("Analyze"):
        try:
            # Scrape website and detect technologies
            html_code = scrape_website(url)
            css_code = extract_css_from_html(html_code)
            js_code = extract_js_from_html(html_code)
            technologies = detect_technologies(url)

            # Display in expandable sections
            with st.expander("HTML Code", expanded=False):
                st.code(html_code[:5000], language='html')  # Truncate to first 5000 characters

            with st.expander("CSS Code", expanded=False):
                for style in css_code:
                    st.code(style, language='css')

            with st.expander("JavaScript Code", expanded=False):
                for js in js_code:
                    beautified_js = beautify_js(js)
                    st.code(beautified_js, language='javascript')

            # Learn tab
            with st.expander("Learn"):
                st.write("Free Learning Resources:")
                for tech in ["HTML", "CSS", "JavaScript"]:
                    learn_link = learn_links(tech)
                    st.write(f"- Learn {tech}: {learn_link}")

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
