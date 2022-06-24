# libraries 
import requests
import json
from bs4 import BeautifulSoup 

# Get user URL 
url = str(input("Enter Amazon URL: "))

# Headers sent with request to not trigger CAPTCHA
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

# Scraping HTML
print("Sending Page Request")
page = requests.get(url, headers=headers) 
print("Parsing page data")
page = BeautifulSoup(page.content, "html.parser")
print("Page data parsed")

### * * FUNCTIONS HANDLING DIFFERENT IDS * * ###

# *function handles table type of listing; th is the heading for the product info and td is the value.  
def handle_table(id):
    prod_info = (page.find(id=id).find_all('tr'))
    prod_info_dict = {}
    for info in prod_info:
        prod_info_dict[(info.find('th').text.strip())] = (info.find('td').text.strip().replace('\u200e', '').replace('\n',''))
    return prod_info_dict

# *function handles the alternate table-listing where only td tags are used and no th tags are used 
def handle_alt_table(id):
    prod_info = (page.find(id=id).find_all('tr'))
    prod_info_dict = {}
    # because both tags are the same (td), use .contents to have a list of the child tags. The tags are seperated by \n so use [1] and [3] instead of [0], [1].
    for info in prod_info:
        (prod_info_dict[info.contents[1].text.strip()]) = (info.contents[3].text.strip())
    return prod_info_dict

# * function handles list type listing (<ul>)
def handle_list(id):
    # there are two divs with the same id, in order to select the right one find_all then select the second in array.
    prod_info = page.find(id=id).find_all('ul')[0].find_all('li')
    prod_info_dict = {}
    for info in prod_info:
        prod_info_dict[(info.span.contents[1].text.replace(':','').replace('\n', '').replace('\u200f', '').replace('\u200e','').strip())] = (info.span.contents[3].text.strip())
    return prod_info_dict
    


# List of possible ID values containing product info
ids = ['prodDetails', 'tech', 'detailBullets_feature_div']

# scrape product information into a dictionary
def get_info(ids=ids):
    for id in ids:
        print(f"checking {id} ID")
        match id:
            case 'prodDetails':
                try:
                    data = handle_table(id)
                except AttributeError:
                    print("ID not prodDetails")
                else:
                    return data
            case 'tech':
                try:
                    data = handle_alt_table(id)
                except AttributeError:
                    print("ID not tech")
                else:
                    return data
            case 'detailBullets_feature_div':
                try:
                    data = handle_list(id)
                except AttributeError:
                    print("ID not detailBullets_feature_div")
                else:
                    return data
            case _:
                return "Invalid product"

# product information       
prod_info_dict = get_info(ids)

# Serializing JSON
json_object = json.dumps(prod_info_dict, indent = 4)

# Writing to JSON 
with open("./product.json", "w") as outfile:
    outfile.write(json_object)

print("Finished writing to products.json")
