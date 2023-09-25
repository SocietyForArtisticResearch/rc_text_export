import lxml
import cchardet
import requests
from bs4 import BeautifulSoup
import subprocess

url = "https://www.researchcatalogue.net/view/2293686/2293687"


def is_sub_page(expositionUrl, url):
    "check if the page is in the exposition"
    try:
        base = getExpositionUrl(url)
        if base == expositionUrl:
            return True
        else:
            return False
    except:
        return False


def find_submenu_hrefs(parsed_soup):
    "find all hyperlinks in the contents menu"
    navigation_ul = parsed_soup.find('ul', class_='submenu')

    # Initialize a list to store the href values
    hrefs = []
    # Check if the navigation_ul is found
    if navigation_ul:
        # Find all <a> elements within the navigation_ul
        a_elements = navigation_ul.find_all('a')

        # Extract and store the href attribute values
        hrefs = [a.get('href') for a in a_elements]
    return hrefs


def make_soup(url):
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'lxml')

        return soup
    else:
        raise Exception(
            f"Failed to fetch URL. Status code: {response.status_code}")


def get_text_spans(soup):
    "find all text content in both simple-text and html tools"
    span_elements = soup.find_all(
        'span', class_='html-text-editor-content')
    span_elements = span_elements + \
        soup.find_all('span', class_='simple-text-editor-content')
    return span_elements


def as_html(span_elements):
    "render all elements as HTML"
    html_content = ''
    for span in span_elements:
        html_content += span.prettify()
    return html_content


def as_text(span_elements):
    "make into plain text"
    just_text = ''

    for span in span_elements:
        just_text += span.get_text()
    return just_text


def pandoc_html_to_word(html_str):
    "this turns html into a word document using pandoc"
    output_file = 'output.docx'
    pandoc_command = ["pandoc", "--from=html",
                      "--to=docx", "--output=" + output_file]
    process = subprocess.Popen(pandoc_command, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate(input=html_str)

    if process.returncode == 0:
        print(f"HTML successfully converted to {output_file}")
    else:
        print(f"Conversion failed. Error: {stderr}")


def main():
    soup = make_soup(url)
    print(find_submenu_hrefs(soup))
    elements = get_text_spans(soup)
    html = as_html(elements)
    pandoc_html_to_word(html)


main()
