import requests
import pandas as pd
from bs4 import BeautifulSoup

csv_file_name = 'coVidData.csv'


def get_covid_data():

    url = "https://www.worldometers.info/coronavirus/"
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    all_data = list()

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

    # Export data to .csv file
    df.to_csv(csv_file_name)

    return df


# This is an experimental algorithm
def find_data_in_df(data_point):
    
    df = pd.read_csv(csv_file_name)

    searched_data = df[data_point]

    for data in searched_data:
        print(data)


# Ensure this file cannot be independently called
if __name__ == '__main__':

    pass
