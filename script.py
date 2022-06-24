import requests
from bs4 import BeautifulSoup 

url = str(input("Enter Amazon URL: "))
# url = "https://www.athMove-Fastfold-Removal/dp/B01BLQW5L8/ref=sxin_15_cpf_saw-CPFPecos-dsk-lmlk-asin?content-id=amzn1.sym.703e7930-fafd-47ae-8c40-75457dde32d7%3Aamzn1.sym.703e7930-fafd-47ae-8c40-75457dde32d7&crid=27FRVNFHJLDEV&cv_ct_cx=box&keywords=box&pd_rd_i=B01BLQW5L8&pd_rd_r=65515bf0-e6dd-4f12-8603-29687d46b578&pd_rd_w=G7WcH&pd_rd_wg=bl6P2&pf_rd_p=703e7930-fafd-47ae-8c40-75457dde32d7&pf_rd_r=ACX916SX2RKG1AV484ND&qid=1656021093&sprefix=box%2Caps%2C156&sr=1-1-67f35b41-5700-4945-9201-4d897d32b16c&th=1"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}



page = requests.get(url, headers=headers) 
soup = BeautifulSoup(page.content, "html.parser")
tech_details = (soup.find(id='productDetails_techSpec_section_1').find_all('tr'))

prod_info = {}
for info in tech_details:
    prod_info[(info.find('th').text.strip())] = (info.find('td').text.strip().replace('\u200e', ''))

print(prod_info)

