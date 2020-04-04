import os
import sys
import subprocess
from pathlib import Path
from configparser import ConfigParser
from datetime import datetime
from datetime import timedelta

# config parser setup
config = ConfigParser()
configFilePath = str(os.path.dirname(os.path.abspath(__file__))) + '/script.config'
config.read(configFilePath)


# global variables
directory = config.get('DEFAULT', 'directory')
state = ''

def updateCSV():
    # Use pathlib as an object-oriented way to check for covid.csv
    covid_csv = Path(directory + '/covid.csv')
    if not covid_csv.is_file():
        # file does not exist, create it
        print('Downloading covid.csv data...\n')
        subprocess.check_call('curl https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv > covid.csv')
        #covid_lines = [covid_lines[-2],covid_lines[-1]]
    else: # Read latest date in file, if not today then update file
        #current_date = datetime.today().strftime('%Y-%m-%d')
        #yesterday = datetime.today()- timedelta(days=1)
        #prev_date = yesterday.strftime('%Y-%m-%d') 
        print('Updating covid.csv data...\n')
        # Silently (-s) curl csv data
        subprocess.check_call('curl -s https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv > covid.csv', shell=True)
    
    # Return path to csv file
    return covid_csv


def getDelta(prev, latest):
    #Get change in cases and deaths from 2nd to last update and latest update
    delta_cases = latest[0] - prev[0]
    delta_deaths = latest[1] - prev[1]
    # Returns as tuple
    return delta_cases, delta_deaths

def checkState(state, covid_csv_file):
    covid_file = open(str(covid_csv_file), 'r')
    covid_lines = []

    for line in covid_file:
        line = line.rstrip()
        if state.lower() in line.lower():
            covid_lines.append(line)

    covid_file.close()

    # Return lines with data of inputted state or 0 if not found
    if len(covid_lines) > 0:
        return covid_lines
    else:
        return 0

def getData(covid_lines):
    # Get the latest updates for the last two days
    covid_lines = [covid_lines[-2],covid_lines[-1]]

    # Split data and get the number of cases and deaths
    date_one = covid_lines[0].split(',')
    # Cast string cases and deaths to integers
    date_one = [int(date_one[3]), int(date_one[4])]

    date_two = covid_lines[1].split(',')
    date_two = [int(date_two[3]), int(date_two[4])]

    # Get delta cases and delta deaths
    deltas = getDelta(date_one, date_two)
    delta_cases = deltas[0]
    delta_deaths = deltas[1]

    # Print out number of cases and deaths with their appropriate deltas
    print('Cases        Deaths')
    print(str(date_two[0]) + '(' + str(delta_cases) + '▴) ' + str(date_two[1]) + '(' + str(delta_deaths) + '☠)')

# Running program based on input
while len(state) == 0:
    state = input('Enter your US state (ex: New Jersey): ')
    # Check if csv needs to be downloaded or updated
    covid_csv = updateCSV()
    # Shortest state name has length of 4
    if len(state) > 4:
        # Check if state in lines
        state_data = checkState(state, covid_csv)
        if state_data != 0:
            getData(state_data)
