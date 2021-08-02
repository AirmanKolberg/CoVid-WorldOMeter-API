from json_tools import json_to_dict

"""
This file can be used to get specific
CoVid-19 data from any and all available
countries.
"""


class CoVidData:
    def __init__(self, 
                 total_cases=0,
                 new_cases=1,
                 total_deaths=2,
                 new_deaths=3,
                 total_recovered=4,
                 new_recovered=5,
                 active_cases=6,
                 serious_critical=7,
                 total_cases_per_million=8,
                 deaths_per_million=9,
                 total_tests=10,
                 test_per_million=11,
                 population=12):
        self.total_cases = total_cases
        self.new_cases = new_cases
        self.total_deaths = total_deaths
        self.new_deaths = new_deaths
        self.total_recovered = total_recovered
        self.new_recovered = new_recovered
        self.active_cases = active_cases
        self.serious_critical = serious_critical
        self.total_cases_per_million = total_cases_per_million
        self.deaths_per_million = deaths_per_million
        self.total_tests = total_tests
        self.test_per_million = test_per_million
        self.population = population


# Create a data_points class object for each country's CoVid-19 data
data_points = CoVidData()


def get_framework_datapoint(country, data):

    framework = json_to_dict('CoVid-Data.json')

    variable = framework[country][data]

    return variable


if __name__ == '__main__':

    # This example is just a test...
    data = get_framework_datapoint('USA', data_points.population)
    print(data)
