import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

#custom dictionary for position names
position_names = {0:'first', 1:'second', 2:'third', 3:'fourth', 4:'fifth'}

#list to use for months
months = ['january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    #Def function for user to input city
    def get_city():
        while True:
            city = input('Which city would you like to explore?\nChicago? New York? Washington?\n').lower()
            if city in (CITY_DATA.keys()):
                return city
            else:
                print(f'Sorry, "{city.title()}" is not a valid city, please input "Chicago", "New York", or "Washington".')

    #Def function to get user input for month (all, january, february, ... , june)
    def get_month():
        while True:
            month = input(f'Okay! Which month between January and June would you like to analyze for {city.title()}?\nUse "All" for no filter:\n').lower()
            if month in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
                return month
            else:
                print(f'Sorry, "{month}" is not a valid answer, please choose between\nJanuary, February, March, April, May, June, All (no filter)')

    #Def function to get user input for day of week (all, monday, tuesday, ... sunday)
    def get_day():
        while True:
            day = input(f'Last step! Which day of the week would you like to analyze for {city.title()} in {month.title()}?\nUse "All" for no filter:\n').lower()
            if day in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
                return day
            else:
                print(f'Sorry, "{day}" is not a valid day of the week or "All", please choose between\nMonday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, All(No filter)')

    #get user to input city, and ask user to verify the chosen city
    while True:
        city = get_city()
        city_check = input(f'Alright, let\'s explore data from {city.title()}!\nIs this correct?\nY/N: ').lower()
        while city_check not in ('y', 'n'):
            city_check = input(f'Sorry, "{city_check}" is not a valid answer, please input "Y" for "Yes" and "N" for "No".')
        if city_check == ('y'):
            break
        else:
            continue

    #get user to specify if they want to filter by month, day of the week, both or none
    filter = input(f'Do you want to filter {city.title()}\'s data by month, day, both or none?\n').lower()
    while filter not in ('month', 'day', 'both', 'none'):
        filter = input(f'{filter} is not a valid answer, please input: \n"month" if you want to filter by month \n"day" if you want to filter by day \n"both" if you want to filter by both month and day \n"none" if no filter at all \n').lower()

    if filter == 'month':
        month = get_month()
        day = 'all'
    elif filter == 'day':
        month = 'all'
        day = get_day()
    elif filter == 'both':
        month = get_month()
        day = get_day()
    else:
        month = 'all'
        day = 'all'

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    start_time = time.time()

    #load data into DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    print("\nLoading the table, this took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return df

def time_stats(df):
    """
    Display raw data at user's request

    Args:
        df - Pandas DataFrame containing city data filtered by month and day

    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_mode = df['month'].mode()[0]
    print(f'The most common month is {months[month_mode-1].title()}.')

    # display the most common day of week
    day_mode = df['day_of_week'].mode()[0]
    print(f'The most common day of the week is {day_mode.title()}.')


    # display the most common start hour
    hour_mode = df['hour'].mode()[0]
    print(f'The most common hour of the day is at {hour_mode}.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Display raw data at user's request

    Args:
        df - Pandas DataFrame containing city data filtered by month and day

    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(f'The most commonly used start station is at {df["Start Station"].mode()[0]}.')

    # display most commonly used end station
    print(f'The most commonly used end station is at {df["End Station"].mode()[0]}.')

    # display most frequent combination of start station and end station trip
    print(f'The most commonly used trip combination is {(df["Start Station"] + " to " + df["End Station"]).mode()[0]}.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Display raw data at user's request

    Args:
        df - Pandas DataFrame containing city data filtered by month and day

    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    minute, second = divmod(total_time, 60)
    hour, minute = divmod(minute, 60)
    if hour > 24:
        day, hour = divmod(hour, 24)
        print(f'The total travel time is {int(day)} days, {int(hour)} hours, {int(minute)} minutes and {int(second)} seconds.')
    else:
        print(f'The total travel time is {int(hour)} hours, {int(minute)} minutes and {int(second)} seconds.')

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    minute, second = divmod(mean_time, 60)
    if minute > 60:
        hour, minute = divmod(minute, 60)
        print(f'The total travel time is {int(hour)} hours, {int(minute)} minutes and {int(second)} seconds.')
    else:
        print(f'The total travel time {int(minute)} minutes and {int(second)} seconds.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """
    Display raw data at user's request

    Args:
        df - Pandas DataFrame containing city data filtered by month and day

    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_values = df['User Type'].value_counts().index.tolist()
    user_type_counts = df['User Type'].value_counts().tolist()
    print(f'There are {len(user_type_values)} types of users')
    for n in range(0, len(user_type_values)):
        print(f'The {position_names[n]} is {user_type_values[n]} with {user_type_counts[n]}.')

    print('')

    # Display counts of gender, and a message if gender is not available
    try:
        gender_values = df['Gender'].value_counts().index.tolist()
        gender_counts = df['Gender'].value_counts().tolist()
        #print(f'There are {len(gender_values)} types of gender')
        for n in range(0, len(gender_values)):
            print(f'There are {gender_counts[n]} {gender_values[n].lower()}s.')
    except:
        print(f'Sorry, gender is not available for {city.title()}.')

    print('')

    # Display earliest, most recent, and most common year of birth, and a message if gender is not available
    try:
        year_earliest = df['Birth Year'].min()
        year_recent = df['Birth Year'].max()
        year_mode = df['Birth Year'].mode()[0]
        print(f'The earliest birth year is {int(year_earliest)}.')
        print(f'The most recent birth year is {int(year_recent)}.')
        print(f'The most common birth year is {int(year_mode)}.')
    except:
        print(f'Sorry, birth year is not available for {city.title()}.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """
    Display raw data at user's request

    Args:
        df - Pandas DataFrame containing city data filtered by month and day

    """
    raw_start =  0

    while True:
        if raw_start == 0:
            display_more = input('Would you like to view the first five rows of the raw data? \n"Y"/"N"\n').lower()
        else:
            display_more = input('Would you like to view the next five rows of the raw data? \n"Y"/"N"\n').lower()
        while display_more not in ('y', 'n'):
            display_more = input('Sorry, {disply_more} is not a valid answer, please input "Y" for "yes and "N" for "no".')
        if display_more == 'n':
            break
        else:
            if len(df) > 5:
                if raw_start+5 < len(df):
                    print(f'You are currently viewing data from row {raw_start+1} to {raw_start+5}.')
                    print(df[raw_start:raw_start+5])
                    raw_start += 5
                else:
                    print(f'You are currently viewing data from row {raw_start+1} to {len(df)}.')
                    print(df[raw_start:])
                    print('You have reached the end of the table!')
                    break
            else:
                print(f'There is only {len(df)} entries in this table, showing all of them to you!')
                print(df)
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        input('Press any key to continue...')
        station_stats(df)
        input('Press any key to continue...')
        trip_duration_stats(df)
        input('Press any key to continue...')
        user_stats(df, city)
        input('Press any key to continue...')
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter "Y" for "yes" or "N" for "no".\n')
        while restart.lower() not in ('y', 'n'):
            restart = input(f'Sorry, {restart} is not a valid answer, please input "Y" or "N".')
        if restart.lower() != 'y':
            print('\nThank you for using this service, see you next time!')
            break
        else:
            print('Ok! Let\' go again!')


if __name__ == "__main__":
	main()
