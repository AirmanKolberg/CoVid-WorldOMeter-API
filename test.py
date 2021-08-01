import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_covid_data():

    url = "https://www.worldometers.info/coronavirus/"
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    all_data = []
    for tr in soup.select("#main_table_countries_today tr:has(td)")[8:-8]:
        tds = [td.get_text(strip=True) for td in tr.select("td")][:15]
        all_data.append(tds)

    df = pd.DataFrame(
        all_data,
        columns=[
            "#",
            "Country",
            "Total Cases",
            "New Cases",
            "Total Deaths",
            "New Deaths",
            "Total Recovered",
            "New Recovered",
            "Active Cases",
            "Serious, Critical",
            "Tot Cases/1M pop",
            "Deaths/1M pop",
            "Total Tests",
            "Tests/1M pop",
            "Population",
        ],
    )

    df.to_csv('myData.csv')

    return df


def find_data_in_df(data_point):
    
    df = pd.read_csv('myData.csv')

    searched_data = df[data_point]

    for data in searched_data:
        print(data)


if __name__ == '__main__':

    find_data_in_df('Country')
