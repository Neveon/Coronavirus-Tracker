# os and Path used to get path
import os
from pathlib import Path
# To use terminal command line
import subprocess
# For dealing with date and updating covid.csv
from datetime import datetime
from datetime import timedelta
# For downloading csv fileand writing to file
import requests
requests.packages.urllib3.disable_warnings()
import shutil

# path to current working directory (cwd)
FILE_PATH = os.path.abspath(os.getcwd())

# global variables
directory = FILE_PATH
state = ''

def downloadCSV():

    url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
    r = requests.get(url, verify=False, stream=True)
    if r.status_code != 200:
        print(r)
        print("Failure!")
        exit()
    else:
        r.raw.decode_content = True
        with open("covid.csv", "wb") as f:
            shutil.copyfileobj(r.raw, f)
        print("Successfully Updated CSV file \n- Note some states may not have a change from a previous date, so their date is not updated")

# Update covid.csv file based on last data point in given array
def update_csv(covid_lines):

    # Read latest date in file, if not today then update file
    current_date = datetime.today().strftime('%Y-%m-%d')

    # csv_date is based on latest date in file
    last_data = covid_lines[-1]
    csv_date = last_data.split(",")[0]

    # python 3 print format
    print(f"\n\nFile last updated: {csv_date}")

    # Check if file does not need to be updated by reading latest line of data
    if current_date != csv_date:
        print('Updating covid.csv data...\n')
        # Silently (-s) curl csv data

        downloadCSV()

        # Check if data in file updated successfully
        file_handle = open(str(directory + '/covid.csv'), 'r')
        line = file_handle.readlines()[-1]
        csv_date = line.split(",")[0]
        file_handle.close()

        csv_datetime = datetime.strptime(csv_date, "%Y-%m-%d")

        if current_date != csv_date:
            print(f"Your state has not updated their data to today\'s date. \nMost recent Data is from: {csv_datetime.strftime('%Y-%m-%d')}\n")
        else:
            print('Successfully updated covid.csv\n')

# Get change in date
def delta(prev, latest):
    #Get change in cases and deaths from 2nd to last update and latest update
    delta_cases = latest[0] - prev[0]
    delta_deaths = latest[1] - prev[1]
    # Returns as tuple
    return delta_cases, delta_deaths

# Check if state exists in file
def checkState(state):
    # Check if covid.csv exists
    csv = Path(directory + '/covid.csv')
    if not csv.is_file():
        # file does not exist, create it
        print('Downloading covid.csv data...\n')
        downloadCSV()

    covid_file = open(csv, 'r')
    covid_lines = []

    for line in covid_file:
        line = line.rstrip()
        if state.lower() in line.lower():
            covid_lines.append(line)

    covid_file.close()

    # Return lines with data of inputted state or 0 if not found
    if len(covid_lines) > 0:
        # Check if csv needs to be updated using the last data point in lines with state
        update_csv(covid_lines)

        return covid_lines
    else:
        print("State not found")
        return 0

def getData(covid_lines):
    # Get the latest updates for the last two days
    covid_lines = [covid_lines[-2], covid_lines[-1]]

    # Split data and get the number of cases and deaths
    date_one = covid_lines[0].split(',')
    # Cast string cases and deaths to integers
    date_one = [int(date_one[3]), int(date_one[4])]

    date_two = covid_lines[1].split(',')
    date_two = [int(date_two[3]), int(date_two[4])]

    # Get delta cases and delta deaths
    deltas = delta(date_one, date_two)
    delta_cases = deltas[0]
    delta_deaths = deltas[1]

    # Print out number of cases and deaths with their appropriate deltas
    print('Cases        Deaths')
    print(str(date_two[0]) + '(' + str(delta_cases) + '▴) ' + str(date_two[1]) + '(' + str(delta_deaths) + '☠ ▴)')

# Running program based on input
while len(state) < 4:
    state = input('Enter your US state (ex: New Jersey): ')

    # Shortest state name has length of 4
    if len(state) >= 4:

        # Check if state in csv file
        state_data = checkState(state)

        # Check if there is any state data by the return value of checkState()
        if state_data != 0:
            getData(state_data)
            break
        else:
            # Reset state input since not found
            state = ''
    else:
        # Any input less than 4 letters is not a state
        print("State not found")
