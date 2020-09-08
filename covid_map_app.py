import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
link=requests.get("https://www.worldometers.info/coronavirus/?fbclid=IwAR2cvtDz4w1I7jJn6y0tzl-rN8yxr6-dEvkEPQ8uZrxWPLPZVk3t0RSKRpQ")

date=link.text

soup=BeautifulSoup(date,"lxml")

#download country
country_array=[]
for country in soup.find_all("a",{"class":"mt_a"}):
    tmp_country=country.get_text()
    country_array.append(tmp_country)


#download total cases
totalCases_array=[]
tmp =soup.find_all("tr")
# od 9 do 223

for i in range(9,223):
    totalCases_array.append((tmp[i].find_all("td",{"style":"font-weight: bold; text-align:right"})))
#print(totalCases_array[1])

#download total deaths
totalDeaths_array=[]

for i in range(8,223):
    totalDeaths_array.append((tmp[i].find_all("td")))
#print(totalDeaths_array[2][4])
#for i in range(1,215):
#    print(totalDeaths_array[i][4].text)

#for i in range(0,212):
#    print(i+1," Country ",country_array[i]," Total Cases ", totalCases_array[i][0].text," Total Deaths ",totalDeaths_array[i+1][4].text)

mainArray=[]
for i in range(0,212):
    tmp_array=[(country_array[i],totalCases_array[i][0].text,totalDeaths_array[i+1][4].text)]
    mainArray.append(tmp_array)


labels=["Country","Total Cases","Total Deaths"]
covid=pd.DataFrame.from_records(mainArray)     
print(covid)       
covid.to_csv ("covid_date.csv")





