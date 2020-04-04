#!/bin/bash

function getData {
    two_days=$(grep "New Jersey" covid.csv | # Output lines only with New Jersey
                    tail -n2 | # Get last two days of data
                    head -n1 | # Output First line of file
                    cut -d"," -f 2,4,5 # Cut at every ',' (delimiter) and show specific fields
                )
    one_day=$(grep "New Jersey" covid.csv |
                    tail -1 | # Get last day of data
                    cut -d"," -f 2,4,5 # Cut at every ',' (delimiter) and show specific field 
                )
    #Date of last update
    last_update=$(echo $one_day |
                        tail -1 |
                        cut -d"," -f 1
                )
    current_date=$(date +%Y-%m-%d)
    #If last update is not equal to current date, then update covid.csv
    [[ ! $last_update =~ $current_date ]] &&
        curl -s "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv" > covid.csv

    num_cases_two=$(echo $two_days | 
                    cut -d"," -f 2
                    )
    num_cases_one=$(echo $one_day |
                    cut -d"," -f 2
                    )
    # Change in cases since last update
    delta_cases=$(($num_cases_one-$num_cases_two))
    printf '%s ' "$delta_cases ▴" 
    num_deaths_two=$(echo $two_days | 
                    cut -d"," -f 3
                    )
    num_deaths_one=$(echo $one_day | 
                    cut -d"," -f 3
                    )
    # Change in deaths since last update
    dealta_deaths=$(($num_deaths_one-$num_deaths_two))
    printf '%s' "$dealta_deaths ☠"
}

#Check if covid.csv exists in current directory
[[ $(test -f $PWD'/covid.csv') ]] && 
    # If exists, then get data
    getData |
    # If doesn't exist, curl data into covid.csv
    printf '%s\n\n' 'Downloading covid.csv data...'
    curl -s "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv" > covid.csv
    getData 
