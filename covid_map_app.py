import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pycountry
import plotly.express as px

link=requests.get("https://www.worldometers.info/coronavirus/?fbclid=IwAR2cvtDz4w1I7jJn6y0tzl-rN8yxr6-dEvkEPQ8uZrxWPLPZVk3t0RSKRpQ")

date=link.text

soup=BeautifulSoup(date,"lxml")

#download country
spec_country=["USA","Russia","DRC","UK","Iran","Tanzania","Bolivia"]
incor_country=["United States","Russian Federation","COD","United Kingdom","Iran, Islamic Republic of","Tanzania, United Republic of","Bolivia, Plurinational State of"]
country_array=[] 
for country in soup.find_all("a",{"class":"mt_a"}):
    tmp_country=country.get_text()
    for i in range(len(spec_country)):
        if tmp_country==spec_country[i]:
            tmp_country=incor_country[i]

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
#for i in range(1,215):
#    print(totalDeaths_array[i][4].text)

#for i in range(0,212):
#    print(i+1," Country ",country_array[i]," Total Cases ", totalCases_array[i][0].text," Total Deaths ",totalDeaths_array[i+1][4].text)



countries = {}
for country in pycountry.countries:
    countries[country.name] = country.alpha_3

codes = [countries.get(country,country) for country in country_array]




mainCases=[]
mainDeaths=[]
for i in range(0,212):
    mainCases.append(totalCases_array[i][0].text)
    mainDeaths.append(totalDeaths_array[i+1][4].text)
covid_series={'country':pd.Series(country_array),'total_cases':pd.Series(mainCases),'total_deaths':pd.Series(mainDeaths),"code":pd.Series(codes)}

covid=pd.DataFrame.from_records(covid_series)     
covid.to_csv ("covid_dates.csv")
df = pd.read_csv("covid_dates.csv")

covid_date=covid.head(212)
print(covid_date.head(145))



fig = px.choropleth(covid_date, locations="code",
                    color="total_cases", 
                    hover_name="country", 
                    )
fig.show()


"""
fig = go.Figure(data=go.Choropleth(
    locations =df['country'],
    z = df['total_cases'],
    text = df['total_cases'],
    colorscale = 'Blues',
    autocolorscale=False,
    reversescale=True,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_tickprefix = '$',
    colorbar_title = 'GDP<br>Billions US$',
))

fig.update_layout(
    title_text='2014 Global GDP',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    annotations = [dict(
        x=0.55,
        y=0.1,
        xref='paper',
        yref='paper',
        text='Source: <a href="https://www.cia.gov/library/publications/the-world-factbook/fields/2195.html">\
            CIA World Factbook</a>',
        showarrow = False
    )]
)

fig.show()
"""