import requests
import json
from bs4 import BeautifulSoup 

# Get user URL 
url = str(input("Enter Amazon URL: "))

# Headers sent with request to not trigger CAPTCHA
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

# Scraping HTML
page = requests.get(url, headers=headers) 
page = BeautifulSoup(page.content, "html.parser")

### FUNCTIONS HANDLING DIFFERENT IDS ###

# function handles table type of listing; th is the heading for the product info and td is the value.  
def handle_table(id):
    prod_info = (page.find(id=id).find_all('tr'))
    prod_info_dict = {}
    for info in prod_info:
        prod_info_dict[(info.find('th').text.strip())] = (info.find('td').text.strip().replace('\u200e', '').replace('\n',''))
    return prod_info_dict

# function handles the alternate table-listing where only td tags are used and no th tags are used 
# TODO differentiate between first td tag and second for key/value, use <em> tags on heading
def handle_alt_table(id):
    pass

# function handles list type listing (<ul>)
# def handle_list(id):


# List of possible ID values containing product info
ids = ['prodDetails', 'tech', 'detailBulletsWrapper_feature_div']

# TODO try except
# scrape product information into a dictionary
# prod details : tableli, tech: altli, detailBulletsWrapper_feature_div : listli <-- which function to use
def get_info(ids, page):
    for id in ids:
        match id:
            case 'prodDetails':
                return handle_table(id)
            case 'tech':
                return handle_alt_table(id)
        # case 'detailBulletsWrapper_feature_div'

with open('product.txt', 'w') as json_file:
  json.dump(get_info(ids, page), json_file)
print(get_info(ids, page))