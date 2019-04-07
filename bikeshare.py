# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 21:41:50 2019

@author: Graham
References: Python and Pandas documentation.  Multiple websites to gain better understanding and first hand 
knowledge of  concepts not in the Udacity materials.  I learned how to use the groupby function from a 
KnowledgeBase post by John O in July 2018.

"""

import time
import pandas as pd


CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

loop_yes = True
#
# Columns in the CSV files are:
# 	Start Time	End Time	Trip Duration	Start Station	End Station	User Type	Gender	Birth Year
#

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Asks user if they want to see only the top line of results 
    or the top five (5) lines of the results.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (int) five_lines - provides the option to display one line of results or the top 5 lines of results
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    city = ""
    bikecity = False
    while (bikecity != True):
        userInput = input('Enter City name to explore: Chicago, New York City or Washington:  ')
        city = userInput.lower()
        if (city in ['chicago', 'new york city', 'washington', 'c', 'n', 'w']):
            bikecity = True
            if city == 'c':
                city = 'chicago'
            elif city == 'n':
                city = 'new york city'
            elif city == 'w':
                city = 'washington'
        else:
            print('Sorry, {} is not a bikeshare city'.format(city.title()))
            print('Enter name of bikeshare city {}'.format('Chicago, New York City or Washington'))

    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = ""
    monthnum = 0
    bikemonth = False
    while (bikemonth != True):
        userInput = input('Enter single month or \'all\' for all months:  ')
        month = userInput.lower()
        if (month in ['all', 'january', 'february', 'march', 'april', 'may',
                      'june']):
            if month != 'all':
                monthnum = months.index(month) + 1
            else:
                monthnum = 13
            bikemonth = True
        else:
            print('Sorry, {} is not a bikeshare month'.format(month.title()))
            print('Enter name of bikeshare month {}'.format('January, February, March, April, May, June or All'))

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 
            'saturday', 'sunday', 'm']
    day = ""
    bikeday = False
    while (bikeday != True):
        userInput = input('Enter day of week or \'all\' to explore that day(s):  ')
        day = userInput.lower()
        if (day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'm']):
            if day == 'm':
                day = 'monday'
            bikeday = True
        else:
            print('Sorry, {} is not a day of the week'.format(day.title()))
    
    lines = True
    while (lines):
        userInput = input('Enter if you want to see the top line (\'1\') or top five (\'5\') lines of results:  ')
        five_lines = userInput.lower()
        if(five_lines in ['1', '5']):
            lines = False
        else:
            print('Sorry, {} is not valid.  Choose one (1) or five (5): '.format(five_lines))

    print('-'*40)
    return city, month, day, int(five_lines)


def load_data(city, month, day, five_lines):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Loads value to show top line of results or the top five (5) lines of the results.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        monthnum = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == monthnum]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                'saturday', 'sunday']
        daynum = days.index(day)
        df = df[df['day_of_week'] == daynum]

    return df, five_lines


def time_stats(df, qmonth, five_lines):
    """
    Displays statistics on the most frequent times of travel.
    Loads value to show top line of results or the top five (5) lines of the results.

    Args:
        df - Pandas DataFrame containing the city data
        (str) qmonth - name of the month to filter by, or "all" to apply no month filter
    Returns:
         Five lines display indicator
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    hour = df['Start Time'].dt.hour

    # TO DO: display the most common month
    pop_mo = df['month'].value_counts()

    if qmonth != 'all':
        print('For rental month {} there where {} rentals'.format(qmonth.title(), pop_mo.iloc[0]))
    else:
        print('The rentals for all the months are {}'.format(pop_mo.sum()))

    # TO DO: display the most common day of week
    pop_day = str(df['day_of_week'].value_counts()[:1])
    pd_idx = 0
    pd_idx = int(pop_day.split()[0])
    print('Most popular rental day of the week is {} with {} rentals'.format(days[pd_idx].title(), pop_day.split()[1]))

    # TO DO: display the most common start hour
    df['hour'] = hour
    pop_hr = str(df['hour'].value_counts()[:1])

#   Output of the most popular time the Bikesahre rentals are used
    pop_time = int(pop_hr.split()[0])
    if pop_time < 12:
        str_pop_hr = str(pop_time) + ' AM'
    else:
        str_pop_hr = str(pop_time - 12) + ' PM'
    print('Most popular rental hour is {} with {} rentals'.format(str_pop_hr, pop_hr.split()[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return five_lines


def station_stats(df, five_lines):
    """
    Displays statistics on the most popular stations and trip.
    Loads value to show top line of results or the top five (5) lines of the results.

    Args:
        df - Pandas DataFrame containing the city data
    Returns:
         Five lines display indicator
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].value_counts()
    print('Start Station', '*'*10)
    if five_lines < 5:
        print('The most popular start station is {} with {} rentals \n'.format(start_station.index[0], start_station.get(start_station.index[0])))
    else:
        print('The most popular start station and rental numbers are: ')
        print('{} \n'.format(start_station.iloc[0:5]))
#        print('{} \n'.format(start_station.index[0:5]))

    # TO DO: display most commonly used end station
    end_station = df['End Station'].value_counts()
    print('End Station', '*'*10)
    if five_lines < 5:
        print('The most popular end station is {} with {} rentals \n'.format(end_station.index[0], end_station.get(start_station.index[0])))
    else:
        print('The most popular end station and rental numbers are: ')
        print('{} \n'.format(end_station.iloc[0:5]))
#        print('{} \n'.format(end_station.index[0:5]))

    # TO DO: display most frequent combination of start station and end station trip
    if five_lines < 5:
        result = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().nlargest(1)
        print('\nTthe most popular station-to-station trip is: \n{} \n'.format(result))
    else:
        result = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().nlargest(5)
        print('\nTthe most popular station-to-station trips are: \n')
        print('{} \n'.format(result))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    userInput = input('Would you like to continue to view five lines of results? (\'y\' or \'n\') ')
    continue_five = userInput.lower()
    if continue_five == 'y':
        five_lines = 5
    else:
        five_lines = 1
    
    return five_lines


def trip_duration_stats(df, five_lines):
    """
    Displays statistics on the total and average trip duration.
    Loads value to show top line of results or the top five (5) lines of the results.

    Args:
        df - Pandas DataFrame containing the city data
    Returns:
         Five lines display indicator
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    travel_tt = df['Trip Duration'].sum()
    print('Total travel time of all users is {}'.format(travel_tt))

    # TO DO: display mean travel time
    travel_mt = df['Trip Duration'].mean()
    print('Mean travel time of all users is {}'.format(travel_mt))

    # TO DO: display mode travel time
    travel_mt = df['Trip Duration'].mode()
    print('Most common travel time of all users is {}'.format(travel_mt))

#    Tried to display a histogram or bar plot of the length of the trip, but  
#    was not able to parse out the data and generate the right plot.
#    travel_times = df['Trip Duration'].value_counts().plot()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return five_lines


def user_stats(df, five_lines):
    """
    Displays statistics on bikeshare users.
    Loads value to show top line of results or the top five (5) lines of the results.

    Args:
        df - Pandas DataFrame containing the city data
    Returns:
         Five lines display indicator
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    ut_counts = df['User Type'].value_counts()      
    print('User Types: \n{}\n'.format(ut_counts))

    # TO DO: Display counts of gender
    # Check to see if there is valid data in the data set
    try:
        ut_gender = df['Gender'].value_counts()
        print('User Gender: \n{}\n'.format(ut_gender))
    # Only recover from the specific error.  Did not leave a bare 'except' 
    except KeyError:   
        print('Gender data not available.')

    # TO DO: Display earliest, most recent, and most common year of birth
    # Check to see if there is valid data in the data set
    try:
        comm_birthyr = df['Birth Year'].value_counts()
        if five_lines < 5:
            print('Most common birth year {} with {} users'.format(comm_birthyr.index[0], comm_birthyr.tolist()[0]))
            print('Most common rider age is {} years old\n'.format(2019 - comm_birthyr.index[0]))
        else:
            print('Five most common birth years are: ')
            print('{} with '.format(comm_birthyr.iloc[0:5]))
            print('Five most common rider ages are: ')

            age_list = list(2019 - comm_birthyr.index[0:5])
            print('{} years old\n'.format(age_list))

        youngest = df['Birth Year'].max()
        print('Youngest birth year {}'.format(youngest))
        print('The youngest riders are {} years old\n'.format(2019 - int(youngest)))

        oldest = df['Birth Year'].min()
        print('Oldest birth year {}'.format(oldest))
        print('The oldest riders are {} years old\n'.format(2019 - int(oldest)))

#        df.hist(column='Birth Year', figsize=(12,8), color='#b02091', frontcolor='red')

    # Only recover from the specific error.  Did not leave a bare 'except'
    except KeyError:
        print('Birth Year data not available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    userInput = input('Would you like to continue to view five lines of results? (\'y\' or \'n\') ')
    continue_five = userInput.lower()
    if continue_five == 'y':
        five_lines = 5
    else:
        five_lines = 1
    return five_lines


def raw_user_data(df, five_lines):
    """
    Displays statistics on bikeshare users.
    Loads value to show top line of results or the top five (5) lines of the results.

    Args:
        df - Pandas DataFrame containing the city data
    Returns:
         Five lines display indicator
    """

    print('\nDisplay raw User data entries...\n')
    raw_lines = True
    start_line = 0
 
    while (raw_lines):
        userInput = input('Would you like to see raw user data entries? (\'y\' or \'n\'): ')
        show_raw = userInput.lower()
        if (show_raw in ['y', 'n']):
            raw_lines = False
            start_line += 1
            if start_line > 10:
                 raw_lines = False
        else:
            print('Sorry, {} is not valid.  Choose one \'y\' or \'n\': '.format(show_raw))

    raw_lines = True
    start_line = 0
    end_line = 5
    while (raw_lines):
        if show_raw == 'n':
            raw_lines = False
        else:
            print(df[start_line:end_line])
            userInput = input('Press any key to see 5 more lines or \'n\' to quit): ')
            show_raw = userInput.lower()
            start_line += 5
            end_line += 5

    return five_lines


def main():
    while True:
        city, month, day, lines = get_filters()
        print('You chose to explore the bikeshare program for')
        print('the city of {} for the month(s) of {} and for finer details of {}\n'.format(city.title(), month.title(), day.title()))
        df, lines = load_data(city, month, day, lines)

        lines = time_stats(df, month, lines)
        lines = station_stats(df, lines)
        lines = trip_duration_stats(df, lines)
        lines = user_stats(df, lines)
        lines = raw_user_data(df, lines)

        restart = input('\nWould you like to make another study? [ \'y\' (for yes) or any key for no ] ')
        restart = restart.lower()[0]
#        print(restart)
        if (restart.lower() != 'y'):
            break


if __name__ == "__main__":
	main()
