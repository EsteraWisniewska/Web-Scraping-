
#### web scraping - IRISH WHISKY

# followed steps from https://www.youtube.com/watch?v=nCuPv3tf2Hg&t=50s
# changed : used different source,
#           pulled additional data,
#           data saved into 2 files with additional updates,
#           mergeing Excel files to update Main file,



############## PART 1 ##############

# importing libraries

import openpyxl 
import requests
from bs4 import BeautifulSoup 
import pandas as pd
from datetime import date


# Get your own User-Agent from https://httpbin.org/get
headers = { "User-Agent": "  ", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
baseurl = 'https://www.thewhiskyexchange.com/'
today = date.today() 


productlinks = []
for x in range(1,10):
    r = requests.get(f'https://www.thewhiskyexchange.com/c/32/irish-whiskey?pg={x}')
    soup = BeautifulSoup(r.content, 'lxml')
    productlist = soup.find_all('li', class_='product-grid__item')
    for item in productlist:
        for link in item.find_all('a', href = True):
            productlinks.append(baseurl + link['href'])
              

# pulling data from a webpage
whiskylist = []
for link in productlinks:
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    
    # finding line where is the 'name' of product, removing unwanted characters behind name
    name = soup.find('h1', class_ = 'product-main__name').text.strip()
    name = name.replace('\n',"")
    
    price = soup.find('p', class_ = "product-action__price").text.strip()
    
    # pulling ratings, if there is none write - 'no ratings'
    try:
        ratings = soup.find('span', class_ = "review-overview__rating star-rating star-rating--50").text.strip()
    except:
        ratings = 'no ratings'
    v= soup.find('p', class_ ='product-main__data').text.strip()
    v = v.split()
    volume = v[0]
    volume3 = v[2]

    # creating a dictionary to save data
    whisky = {
        'Date': today,
        'Name' : name,
        'Ratings': float(ratings),
        'Volume': volume,
        'Alcohol': float(volume3),
        'Price': float(price)}
    whiskylist.append(whisky)
    print(whisky)

# transforming dictionary into DF
df = pd.DataFrame(whiskylist)
print(df.head(10))


# create before Excel file where you want to save pulled data
# save data to that file
df.to_excel(r' filepath 1', index=False, header=True)





############################################

##  UPDATING FILE



import openpyxl 
import requests
from bs4 import BeautifulSoup 
import pandas as pd
from datetime import date



headers = { "User-Agent": " your user-agent ", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
baseurl = 'https://www.thewhiskyexchange.com/'
today = date.today() 


productlinks = []
for x in range(1,10):
    r = requests.get(f'https://www.thewhiskyexchange.com/c/32/irish-whiskey?pg={x}')
    soup = BeautifulSoup(r.content, 'lxml')
    productlist = soup.find_all('li', class_='product-grid__item')
    for item in productlist:
        for link in item.find_all('a', href = True):
            productlinks.append(baseurl + link['href'])
              

# pulling data from a webpage
whiskylist = []
for link in productlinks:
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    
    # finding line where is the 'name' of product, removing unwanted characters behind name
    name = soup.find('h1', class_ = 'product-main__name').text.strip()
    name = name.replace('\n',"")
    price = soup.find('p', class_ = "product-action__price").text.strip()
    price = price.strip('£')
    
    try:
        ratings = soup.find('span', class_ = "review-overview__rating star-rating star-rating--50").text.strip()
    except:
        ratings = 'NaN'
    
    v= soup.find('p', class_ ='product-main__data').text.strip()
    v = v.split()
    volume = v[0]
    volume3 = v[2].strip('%')

      # creating a dictionary to save data
    whisky = {
      'Date': today,
      'Name' : name,
      'Ratings': float(ratings),
      'Volume': volume,
      'Alcohol': float(volume3),
      'Price': float(price)}
    whiskylist.append(whisky)
    print(whisky)


# transforming dictionary into DF
df = pd.DataFrame(whiskylist)
print(df.head(10))


# create before Excel file where you want to put updated data
df.to_excel(r' filepath - update.xlsx', index=False, header=True)



df1 = pd.read_excel('filepath 1')
df2 = pd.read_excel('filepath - update.xlsx')

df3 = pd.concat([df1,df2])
df3.to_excel('filepath 1',index=False)


#################################
