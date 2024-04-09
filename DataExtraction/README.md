# Amazon Laptop Data Extractor

This Python script extracts laptop product information from Amazon's website, utilizing web scraping techniques. The extracted data includes specifications like brand, processor, RAM, etc., and prices converted to Canadian Dollars (CAD) from Indian Rupees (INR) or US Dollars (USD). The extracted data is stored in a JSON file for further analysis.

## Installation

To run the script, you need to install the required libraries. You can install them using pip and the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Approach

- **Initial Setup**: The code was initially designed to extract data for a single product by parsing the structured data provided by Amazon in a table format.

- **Expanding to Category Pages**: Later, the script was modified to extract product links from category pages, allowing for the extraction of multiple laptop products.

## Optimization

- **Parallel Execution**: To save time, you can execute multiple instances of the script simultaneously in different terminal windows. This allows you to scrape different categories or Amazon domains concurrently

## Challenges

- **Currency Symbol Handling**: The script needed to handle different currency symbols. To streamline the process, separate data files were created for each currency (INR, USD, CAD).

- **Uni-Code Handling**: The uni-code character `\u200e` indicating the text should be read from left to right was removed during data extraction.

## Currency Conversion

- Prices were converted to Canadian Dollars using conversion rates for INR and USD.
- Conversion rates used:
  - 1 INR = 0.016 CAD
  - 1 USD = 1.36 CAD

## Overcoming Anti-Scraping Measures on Amazon

- Amazon's anti-scraping defenses were addressed by utilizing the fake-useragent library. This enabled the generation of headers closely resembling those of real users, thereby enhancing the scraping success rate.

- Since Amazon's website structure changes for different devices, we stuck to PC user agents.

- To ensure access and data extraction, we set up a loop to keep rotating the headers until we got what we needed.

## Quality of Life Improvements

- **Real-time Status Updates**: The script provides real-time updates on the extraction progress, displaying the number of products processed and pages scraped.

- **Elegant Status Display**: Status updates overwrite the previous value, providing a cleaner and more readable output.


## Future Improvements

- **Incremental Data Storage**: Instead of writing the entire extracted data at once, a more efficient approach would be to append records iteratively as each page is processed.

---

*Reference Links:*
- [amazon.ca - laptops](https://www.amazon.ca/s?rh=n%3A677252011&fs=true&ref=lp_677252011_sar)
- [amazon.in - laptops](https://www.amazon.in/s?i=computers&rh=n%3A1375424031&fs=true&qid=1712521207&ref=sr_pg_1)
- [amazon.us - laptops](https://www.amazon.com/s?rh=n%3A565108&fs=true&ref=lp_565108_sar)
- [Scraping Amazon With Python: Step-By-Step Guide](https://youtu.be/w3XcMfyUGxY?si=HZtDA8PKuGocGb2L)
- [Web Scraping Ethics](https://towardsdatascience.com/ethics-in-web-scraping-b96b18136f01)
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Documentation](https://docs.python-requests.org/en/latest/)
- [Unicode Currency Symbols](https://www.unicode.org/charts/PDF/U20A0.pdf)
- [Currency Symbols (Unicode block)](https://en.wikipedia.org/wiki/Currency_Symbols_(Unicode_block))
