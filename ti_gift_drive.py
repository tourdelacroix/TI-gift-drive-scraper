import urllib.request
import pandas as pd
from bs4 import BeautifulSoup
import datetime
import re 

# add in timestamp

partner_urls = {
    'boys and girls club':'https://www.amazon.com/hz/wishlist/printview/1IWYXCJKPFD71',
    'childrens health':'https://www.amazon.com/hz/wishlist/printview/1T5IP5W3ER6H6',
    'hopes door':'https://www.amazon.com/hz/wishlist/printview/33XYXFSSTPOYU'
    
    }

df_list = []

for partner, url in partner_urls.items():
    

    html_table = pd.read_html(url)
    html_table_as_df = html_table[0]
    html_table_as_df['partner'] = partner
    
    df_list.append(html_table_as_df)



# CPD 



response = urllib.request.urlopen('https://helpcpdkids.org/toyota/toyota.html')
page_source = response.read()

soup = BeautifulSoup(page_source)
mydivs = soup.findAll("div", {"class": "catalog-item__content"})

pattern = '\s([\$€¥₹]\d+([\.,]\d{2}?))|(\d+([\.,]\d{2}?)[\$€¥₹])\s?'

for div in mydivs:
    
    div_info = div.find("div", {"class": "catalog-item-number"})
    
    wish_number = div_info.text
    
    
    div_desc = div.find("div", {"class": "catalog-item-description"})
    description = div_desc.text
    
    try:
        price = div.findAll("div", {"class": "item-option-quantity-unit-price"})[0].text
        #x = re.findall('/d+',price.text)
    except:
        price = None
    
    if price is not None:
        price_value = re.findall(pattern,price)[0][0]
    else:
        price_value = None

    data_dictionary= {
        'id':wish_number,
        'Title':description,
        'Price':price_value,
        'Quantity':1,
        'Has': 0,
        'partner':'CPD'
        }
    
    cpd_df = pd.DataFrame(data_dictionary,index=[0])
    df_list.append(cpd_df)
    
    

df_to_output = pd.concat(df_list,sort=False)
df_to_output['pull_timestamp'] = datetime.datetime.now()