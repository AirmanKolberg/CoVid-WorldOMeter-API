import requests
import pandas as pd
from bs4 import BeautifulSoup
from json_tools import dict_to_json
from system_functions import clear_screen, verify_yes_or_no, countdown, bash_command

"""
This file should be ran on the backend periodically
throughout the day to gather more CoVid-19 data to
post for the API's use and access.

Note:  Make this file run as a continuous background
process.
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


def create_country_list(df):

    # Declare empty list of countries
    countries = list()

    for x in range(len(df)):

        this_section = str(df['Country'][x])
        
        if this_section not in countries:

            countries.append(this_section)

    return countries


def create_data_dict(df):

    framework = dict()
    all_data = list()

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

            framework[var] = {'Total Cases': total_cases, 
                              'New Cases': new_cases,
                              'Total Deaths': total_deaths, 
                              'New Deaths': new_deaths,
                              'Total Recovered': total_recovered, 
                              'New Recovered': new_recovered,
                              'Active Cases': active_cases,
                              'Serious/Critical': serious_critical, 
                              'Total Cases Per Million': total_cases_per_million,
                              'Deaths Per Million': deaths_per_million, 
                              'Total Tests': total_tests,
                              'Tests Per Million': test_per_million,
                              'Population': population
                              }

        else:

            print('\nERROR:\nSee create_data_dict() function to troubleshoot issues...\n\n')
    
    return framework



def get_covid_data():

    url = "https://www.worldometers.info/coronavirus/"
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    all_data = list()

    for tr in soup.select("#main_table_countries_today tr:has(td)")[8:-8]:

        tds = [td.get_text(strip=True) for td in tr.select("td")][:15]
        all_data.append(tds)

    df = pd.DataFrame(all_data, columns=["#",
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
                                         "Population"])

    # Export data to .csv file
    df.to_csv(csv_file_name)

    return df


# Boolean value for loop
def monitor_covid_statistics(loop):

    # Scrape new data from the web
    get_covid_data()

    # Import that data as a pd.df
    df = pd.read_csv('coVidData.csv')

    """
    The following countries variable currently does
    not have a purpose, but this step will remain
    here commented out until a later time at which
    point I will decide to implement this feature.
    """

    # # Build a list of available countries from that df
    # countries = create_country_list(df)

    # Put all of the data into a beautiful dictionary
    framework = create_data_dict(df)

    # Export that beautiful dictionary as a .json file
    dict_to_json(framework, 'CoVid-Data.json')

    # Share the results with the GitHub community
    bash_command('python3 commit_and_push_all.py')

    if loop:
        
        # Check again in 30 minutes
        countdown(1800)
        monitor_covid_statistics(loop=True)


if __name__ == '__main__':

    clear_screen()

    loop_response = verify_yes_or_no(input("Do you wish to scrape on a loop?\n").lower())
    monitor_covid_statistics(loop=loop_response)
