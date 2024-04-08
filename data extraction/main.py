from urllib.parse import urljoin
import requests, json, os, random, time
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent

start_time = time.time()

# Global Variables
status = 0 # Instance of an item
num_pages = 0 # Pages Parsed
page_data = [] # Data Extracted

# Choosing the Currency which is on the Amazon Page
# CURRENCY = "CAD"
# CURRENCY = "INR"
CURRENCY = "USD"

# Setting the Uni-Code symbol and Converstion Rate into Canadian Dollar
if CURRENCY == "INR":
    curr_uni_code = "\u20b9"
    conversion_rate = 0.016
    extenstion = "in"

elif CURRENCY == "USD":
    curr_uni_code = "\u0024"
    conversion_rate = 1.36
    extension = "com"

elif CURRENCY == "CAD":
    curr_uni_code = "\u0024"
    conversion_rate = 1
    extension = "ca"

# ⬆ Add more currencies, symbols and their conversion rate. ⬆

# Initialize UserAgent object
ua = UserAgent()

agent_list = []

# Using only PC Agents
for i in ua.data_browsers:
    if i["type"] in ["mobile", "tablet"]:
        pass
    else:
        agent_list.append(i['useragent'])

# Function to get a random user agent
def get_random_user_agent():
    return random.choice(agent_list)

def get_headers():
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': f'https://www.amazon.{extension}/'  # amazon.com / .ca / .in
    }
    return headers

# Creating file for the dataset
filename = f"laptops_amazon_{CURRENCY}.json"
if not os.path.exists(filename):
    open(filename, 'w').close()


def connect(url):
    while True:
        custom_headers = get_headers()  # Get custom headers
        response = requests.get(url, headers=custom_headers)  # Make a request

        if response.status_code == 200:
            return response


def extract_product_info(url):
    """
    Extracts product information from a given URL.

    Args:
        url (str): The URL of the product page.
        custom_headers (dict): Custom headers to be used in the HTTP request.

    Returns:
        str: A JSON-formatted string containing the extracted product information.

    Note:
        This function extracts information such as technical specifications and price from the product page.
        
    """

    data = {}

    response = connect(url)

    # Reading the page
    soup_page = BeautifulSoup(response.text, "lxml")

    # Selecting the Product Specifications Table after the product description
    content_element_1 = soup_page.select_one('#productDetails_techSpec_section_1')
    if CURRENCY == "USD":
        content_element_2 = soup_page.select_one('#productDetails_techSpec_section_2')
        if content_element_1 and content_element_2:
            content_1 = content_element_1.prettify()
            content_2 = content_element_2.prettify()
            content = content_1 + content_2
        else:
            return ""
    else:
        if content_element_1:
            content = content_element_1.prettify()
        else:
            return ""

    # Parsing through the Technical Specifications
    soup_content = BeautifulSoup(content, 'html.parser')  

    # Extracting th and td elements
    # th - Table Headings ( Features )
    # tr - Table Rows ( Information )
    th_elements = soup_content.find_all('th', class_='a-color-secondary a-size-base prodDetSectionEntry')
    td_elements = soup_content.find_all('td', class_='a-size-base prodDetAttrValue')

    # Tapping into the price section
    price_element = soup_page.select_one("span.a-price")
    if price_element:
        # Extracting the price
        price_offscreen = price_element.select_one("span.a-offscreen")
        if price_offscreen:
            # Formating the price extracted
            price = price_offscreen.text.strip()
            price = price.replace(curr_uni_code, '') # Remove the Currency symbol
            price = price.replace(',', '') # Remove comma
            # If needed change the currency
            if price:
                price = float(price) * conversion_rate
        else:
            price = pd.NA
    else:
        price = pd.NA

    # Adding Price to the Dictionary
    data["Price"] = price

    # Adding product title
    title = soup_page.select_one('#productTitle')
    if title:
        data["Title"] = title.text.strip()

    # Extracting text content and creating dictionary
    for th, td in zip(th_elements, td_elements):
        key = th.get_text(strip=True)
        value = td.get_text(strip=True)
        data[key] = value

    # 'u200e' refers to reading of left to right direction
    cleaned_data = {key: str(value).replace('\u200e', '') for key, value in data.items()}
    pretty_data = json.dumps(cleaned_data, indent=4)

    return pretty_data

def parse_listing(listing_url):
    """
    Parses product listings from a given URL.

    Args:
        listing_url (str): The URL of the product listing page.
        custom_headers (dict): Custom headers to be used in the HTTP request.

    Returns:
        None

    Note:
        This function iterates through product links in a listing page, extracts product information,
        and stores it in a global variable.

    """

    # Getting the response from the listing URL
    response = connect(listing_url)

    # Parsing the HTML content
    soup_search = BeautifulSoup(response.text, "lxml")
    
    # Selecting all product link elements
    link_elements = soup_search.select("[data-asin] h2 a")
    
    global status, num_pages, page_data
    for link in link_elements:
         # Constructing the full URL of the product page
        full_url = urljoin(listing_url, link.attrs.get("href"))

        # Extracting product information from the product page and appending it to global variable
        product_info = extract_product_info(full_url)
        page_data.append(product_info)

        # Tracking Progress and updating on the same line
        status += 1
        elapsed_time = time.time() - start_time
        print(f"\rStatus: {status} | Pages Processed: {num_pages} | Elapsed Time: {int(elapsed_time)} sec", end='', flush=True)

    # If there is a next page link, continue parsing recursively
    next_page_el = soup_search.select_one('a:-soup-contains("NEXT")')
    if next_page_el:
        next_page_url = next_page_el.attrs.get('href')
        next_page_url = urljoin(listing_url, next_page_url)


def main():
    global num_pages, link

    # Program Executes
    print("Initialized")
    
    # Starting range would be the first page
    # Ending Range value is the last - 1 page
    for i in range(1, 151):
        # amazon.in
        # link = f"https://www.amazon.in/s?i=computers&rh=n%3A1375424031&fs=true&page={i}&qid=1712214652&ref=sr_pg_{i}"
        
        # amazon.ca
        # link = f"https://www.amazon.ca/s?i=electronics&rh=n%3A677252011&fs=true&page={i}&qid=1712521323&ref=sr_pg_{i}"

        # amazon.com
        link = f"https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page={i}&qid=1712528131&ref=sr_pg_{i}"

        parse_listing(link)
        num_pages += 1 

    filtered_data = [json.loads(item) for item in page_data if item.strip()]

# Open the file in write mode to dump the extracted data
    with open(filename, 'w') as f:
        json.dump(filtered_data, f, indent=4)

# Executes as the final line of the program
    print(f"\rStatus: {status} | Pages Processed: {num_pages}\nSuccessfully Converted Into JSON", flush=True)

if __name__ == "__main__":
    main()