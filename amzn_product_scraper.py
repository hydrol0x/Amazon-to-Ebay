# libraries 
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


### * * FUNCTIONS HANDLING DIFFERENT IDS * * ###

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
    prod_info = (page.find(id=id).find_all('tr'))
    prod_info_dict = {}
    # because both tags are the same (td), use .contents to have a list of the child tags. The tags are seperated by \n so use [1] and [3] instead of [0], [1].
    for info in prod_info:
        (prod_info_dict[info.contents[1].text.strip()]) = (info.contents[3].text.strip())
    return prod_info_dict

# function handles list type listing (<ul>)
def handle_list(id):
    prod_info = (page.find(id=id).find_all('li'))
    prod_info_dict = {}
    for info in prod_info:
        prod_info_dict[(info.span.contents[1].text.replace(':','').replace('\n', '').replace('\u200f', '').replace('\u200e','').strip())] = (info.span.contents[3].text.strip())
    return prod_info_dict


# List of possible ID values containing product info
ids = ['prodDetails', 'tech', 'detailBullets_feature_div']

# TODO try except
# scrape product information into a dictionary
# prod details : tableli, tech: altli, detailBulletsWrapper_feature_div : listli <-- which function to use
def get_info(ids=ids):
    for id in ids:
        match id:
            case 'prodDetails':
                try:
                    data = handle_table(id)
                except AttributeError:
                    pass
                else:
                    return data
            case 'tech':
                try:
                    data = handle_alt_table(id)
                except AttributeError:
                    pass
                else:
                    return data
            case 'detailBullets_feature_div':
                try:
                    data = handle_list(id)
                except AttributeError:
                    pass
                else:
                    return data
            case _:
                return "Invalid product"
       

with open('product.txt', 'w') as json_file:
  json.dump(get_info(ids), json_file)
print(get_info(ids))