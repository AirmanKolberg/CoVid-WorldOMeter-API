import requests
import pandas as pd
from bs4 import BeautifulSoup
from json_tools import dict_to_json

"""
This file should be ran on the backend periodically
throughout the day to gather more CoVid-19 data to
post for the API's use and access.
"""

csv_file_name = 'coVidData.csv'

# List of pd.df .csv categories
categories = ['Country',
              'Total Cases',
              'New Cases',
              'Total Deaths',
              'New Deaths',
              'Total Recovered',
              'New Recovered',
              'Active Cases',
              'Serious, Critical',
              'Tot Cases/1M pop',
              'Deaths/1M pop',
              'Total Tests',
              'Tests/1M pop',
              'Population']


def fill_country_list(df):

    # Declare empty list of countries
    countries = list()

    for x in range(len(df)):
        this_section = str(df['Country'][x])
        
        if this_section not in countries:
            countries.append(this_section)

    return countries


def create_data_dict():

    # Declare empty dictionary to fill with CoVid data
    framework = dict()

    all_data = list()

    # Every 14 entries is a new country...
    for x in range(len(df)):
        for category in categories:
            this_section = str(df[category][x])

            # Remove commas and +s from numbers
            this_section = this_section.replace(',', '')
            this_section = this_section.replace('+', '')

            # Convert "nan"s to "0"
            if this_section == 'nan':
                this_section = str(0)
            
            try:
                this_section = int(this_section)
            except ValueError:
                this_section = str(this_section)

            # str() = country, int() = other 13 data points
            all_data.append(this_section)

    all_data.reverse()

    while all_data:
        var = all_data.pop()
        
        if isinstance(var, str):

            total_cases = all_data.pop()
            new_cases = all_data.pop()
            total_deaths = all_data.pop()
            new_deaths = all_data.pop()
            total_recovered = all_data.pop()
            new_recovered = all_data.pop()
            active_cases = all_data.pop()
            serious_critical = all_data.pop()
            total_cases_per_million = all_data.pop()
            deaths_per_million = all_data.pop()
            total_tests = all_data.pop()
            test_per_million = all_data.pop()
            population = all_data.pop()

            framework[var] = [total_cases, new_cases, total_deaths, new_deaths,
                              total_recovered, new_recovered, active_cases,
                              serious_critical, total_cases_per_million,
                              deaths_per_million, total_tests, test_per_million,
                              population]

        else:
            print('\nERROR:\nSee create_data_dict() function for issues...\n\n')
    
    return framework



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


if __name__ == '__main__':

    get_covid_data()

    df = pd.read_csv('coVidData.csv')

    countries = fill_country_list(df)

    framework = create_data_dict()

    dict_to_json(framework, 'CoVid-Data.json')

    print(framework)
