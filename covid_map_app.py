import requests
from bs4 import BeautifulSoup
import numpy as np
link=requests.get("https://www.worldometers.info/coronavirus/?fbclid=IwAR2cvtDz4w1I7jJn6y0tzl-rN8yxr6-dEvkEPQ8uZrxWPLPZVk3t0RSKRpQ")

date=link.text

soup=BeautifulSoup(date,"lxml")

#download country
country_array=[]
for country in soup.find_all("a",{"class":"mt_a"}):
    tmp_country=country.get_text()
    country_array.append(tmp_country)
print(country_array)

#download total cases
totalCases_array=[]
tmp =soup.find_all("tr")
# od 9 do 223

for i in range(9,223):
    totalCases_array.append((tmp[i].find_all("td",{"style":"font-weight: bold; text-align:right"})))
for i in range(0,213):
    print(totalCases_array[i][0].text)

#for i in range(0,2123):
#    print(i+1," Panistwo ",country_array[i]," Liczba zarazen ", totalCases_array[i][0].text)




            





