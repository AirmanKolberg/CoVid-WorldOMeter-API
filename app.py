from bs4 import BeautifulSoup
import requests
from os import system
from json_tools import *

"""
Steps:

1. Grab page data
2. Remove all irrelevant lines from source code
3. Clean relevant lines down to the data
4. Identify patterns in the data's organisation (ie rows, columns, etc.)
5. (Write this step when it's time to start Step 2...)
"""

url = 'https://www.worldometers.info/coronavirus/'
table_id = 'main_table_countries_today'
table_end = '</table>'

# List of lines to exclude from table data
exclusions = ['<td></td>',
              '<tr style=',
              '<tbody class="',
              '<td>',
              '</tr>',
              '</tbody>',
              '<tbody>',
              '</table>',
              '<table>',
              '<tr style="">',
              '<tr class="row_continent total_row',
              '<table class="table table-bordered table-hover main_table_countries" id="main_table_countries_today" style="width:100%;margin-top: 0px !important;display:none;">']

# List of lines to show
inclusions = list()

# List of all lines
all_lines = list()



class Bot:

    def __init__(self,
                 line_added=False,
                 looking_for_start=True,
                 looking_for_end=False):

        self.line_adding = line_added
        self.looking_for_start = looking_for_start
        self.looking_for_end = looking_for_end
    
    def set_line_adding(self, bool):

        self.line_adding = bool

    def set_start_look(self, bool):

        self. looking_for_start = bool

    def set_end_look(self, bool):

        self.looking_for_end = bool



if __name__ == '__main__':

    all_lines = list()

    # Start with a fresh Terminal emulator
    _ = system('clear')
    
    my_bot = Bot()

    r = requests.get(url).text
    all_r = r.split('\n')

    for rs in all_r:

        if my_bot.looking_for_start and table_id in rs:
                
            my_bot.set_line_adding(True)
            my_bot.set_end_look(True)
            my_bot.set_start_look(False)
        
        if my_bot.looking_for_end and table_end in rs:    
                
            my_bot.set_line_adding(False)
            my_bot.looking_for_end(False)
        
        if my_bot.line_adding:

            all_lines.append(rs)
        

        for lines in all_lines:
            print(lines)
        
        print('\n\n\n\n')
        print(len(all_lines))

    # framework = {
    #     'all': all_r
    # }

    # dict_to_json(framework, 'testJSON.json')



    # soup = BeautifulSoup(r)
    # my_table = soup.find_all('table', {'id': table_id})

    # for current_line in my_table:

    #     page_lines = str(current_line).split('\n')

    #     for line in page_lines:
    #         all_lines.append(line)

    # for line in all_lines:
    #     print(line)

    # print('\n\n')
    # print(len(all_lines))
