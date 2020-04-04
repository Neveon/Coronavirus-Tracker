#!/bin/bash

function getData {
    printf '%s' 'Input any US state (Ex: New Jersey): '
    read input_state
    # Translate lines in file to lowercase and input_state to lowercase to
    input_state=$(echo $input_state | tr '[A-Z]' '[a-z]')
    check_state=$(cat covid.csv | tr '[A-Z]' '[a-z]' | grep "$input_state" | wc -l)
    [[ ! $check_state -gt 0 ]] && echo "$input_state is not a valid state. Check spelling and casing of input" && exit 1
    # If state is found in lines then above will not go through
    # Get last two days of data
    two_days=$(cat covid.csv | tr '[A-Z]' '[a-z]' | grep "$input_state" |  # echo lines only with New Jersey
                    tail -n2 | # Get last two days of data
                    head -n1 | # Output First line of file
                    cut -d"," -f 2,4,5 # Cut at every ',' (delimiter) and show specific fields
                )
    one_day=$(cat covid.csv | tr '[A-Z]' '[a-z]' | grep "$input_state" |
                    tail -1 | # Get last day of data
                    cut -d"," -f 2,4,5 # Cut at every ',' (delimiter) and show specific field 
                )
    #Date of last update
    last_update=$(stat -c %y covid.csv |
                       cut -d' ' -f 1
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
    delta_cases=$(($num_cases_one - $num_cases_two))
    printf '%s(%s) ' "$num_cases_one" "$delta_cases ▴" 
    num_deaths_two=$(echo $two_days | 
                    cut -d"," -f 3
                    )
    num_deaths_one=$(echo $one_day | 
                    cut -d"," -f 3
                    )
    # Change in deaths since last update
    delta_deaths=$(($num_deaths_one - $num_deaths_two))
    printf '%s(%s)\n' "$num_deaths_one" "$delta_deaths ☠"
}

#Check if covid.csv exists in current directory
[[ $(test -f $PWD'/covid.csv') ]] && 
    # If exists, then get data
    getData |
    # If doesn't exist, curl data into covid.csv
    printf '%s\n\n' 'Downloading covid.csv data...'
    curl -s "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv" > covid.csv
    getData 
