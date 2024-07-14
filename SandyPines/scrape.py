import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

# Function to scrape detailed information from a property's detailed page
def scrape_property_details(property_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(property_url, headers=headers)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    if response.status_code == 200:
        print(f"Scraping detailed information from {property_url}")

        #if soup.find('ul', 'overview_stats wpp_property_stats list') is not None:


            # Extract detailed information
            
            # list location
        try:
            address = soup.find('li', class_='property_location wpp_stat_plain_list_location').find('span', class_='value').text.strip()
        except AttributeError:
            address = 'N/A'
        # list phase
        try:
            phase = soup.find('li', class_='property_phase wpp_stat_plain_list_phase alt').find('span', class_='value').text.strip()
        except AttributeError:
            phase = 'N/A'
        # list site number
        try:
            site_number = soup.find('li', class_='property_site_number wpp_stat_plain_list_site_number').find('span', class_='value').text.strip()
        except AttributeError:
            site_number = 'N/A'
        # list price
        try:
            price = soup.find('li', class_='property_price wpp_stat_plain_list_price alt').find('span', class_='value').text.strip()
        except AttributeError:
            price = 'N/A'
        # list year
        try:
            year = soup.find('li', class_='property_deposit wpp_stat_plain_list_deposit').find('span', class_='value').text.strip()
        except AttributeError:
            year = 'N/A'

        try:
            make = soup.find('li', class_='property_area wpp_stat_plain_list_area alt').find('span', class_='value').text.strip()
        except AttributeError:
            make = 'N/A'


        # Return detailed information as a dictionary
        return {
            'Address': address,
            'Phase': phase,
            'Site Number': site_number,
            'Price': price,
            'Year': year,
            'Make': make,
        }
    else:
        print(f'Failed to retrieve property details. Status code: {response.status_code}')
        return None

# Function to scrape all listings from the listings page
def scrape_all_listings(listings_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(listings_url, headers=headers)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all property listings
        listings = soup.find_all('div', class_='property_div property')

        # List to store all scraped property data
        all_properties = []

        # Process each listing
        for listing in listings:
            try:
                # Extract basic information
                property_title = listing.find('li', class_='property_title').text.strip()
                property_link = listing.find('li', class_='property_title').find('a', href=True, )['href']
                property_url = urljoin(listings_url, property_link)

                # Scrape detailed information from the property's detailed page
                detailed_info = scrape_property_details(property_url)

                # Combine summary and detailed information into a single dictionary
                property_data = {
                    'Property Title': property_title,
                    'Address': detailed_info.get('Address', ''),
                    'Phase': detailed_info.get('Phase', ''),
                    'Site Number': detailed_info.get('Site Number', ''),
                    'Price': detailed_info.get('Price', ''),
                    'Year': detailed_info.get('Year', ''),
                    'Make': detailed_info.get('Make', ''),
                }



                # Append property data to the list
                all_properties.append(property_data)

            except Exception as e:
                print(f'Error processing listing: {e}')

        return all_properties
    else:
        print(f'Failed to retrieve listings page. Status code: {response.status_code}')
        return None

# Main function to demonstrate scraping all listings
def main():
    listings_url = 'https://sandypines.com/listings/'

    df = pd.DataFrame(columns=['Property Title', 'Address', 'Phase', 'Site Number', 'Price', 'Year', 'Make'])
    
    # Scrape all listings from the listings page
    all_properties = scrape_all_listings(listings_url)

    if all_properties:
        print(f"Scraped {len(all_properties)} listings successfully:")
        for idx, property_data in enumerate(all_properties, start=1):
            print(f"Listing {idx}:")
            for key, value in property_data.items():
                print(f"{key}: {value}")
            print("------------------")
    else:
        print("Failed to scrape listings.")

    df = df._append(all_properties, ignore_index=True)
    
    df.to_csv('sandypines.csv', index=False)

if __name__ == "__main__":
    main()