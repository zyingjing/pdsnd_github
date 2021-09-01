import time
import pandas as pd
import numpy as np

# some dictionaries and lists being used
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday','thursday','friday','saturday','sunday']


# functions to get user input
def get_month():
    """ 
    Gets user input for month (all, january, february, ... , june) 
    Returns: month (str)
    """
    month = input("Which month? January, February, March, April, May, June or all? ").lower()
    while month not in months and month != 'all':
        month = input("Please enter a valid month name: ").lower()
    return month

def get_day():
    """ 
    Gets user input for day of week (all, monday, tuesday, ... sunday) 
    Returns: day (str)
    """
    day = input("Which day of week? Monday, Tuesday, ... Sunday or all? ").lower()
    while day not in days and day != 'all':
        day = input("Please enter a valid week day name: ").lower()
    return day

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Needs the functions get_month() and get_day()

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Would you like to see data for Chicago, New York City or Washington?\n").lower()
    while city not in CITY_DATA:
        city = input("Please enter a valid city: ").lower()
        
    choosefilter = input("Would you like to filter the data by month, day, both or not at all?\n").lower()
    while choosefilter not in ['not at all', 'both', 'month', 'day']:
        choosefilter = input("Input not valid, try again! ").lower()
    
    if choosefilter == 'not at all':
        month = 'all'
        day = 'all'
    elif choosefilter == 'both':
        month = get_month()
        day = get_day()
    elif choosefilter == 'month':
        month = get_month()
        day = 'all'
    elif choosefilter == 'day':
        month = 'all'
        day = get_day()
        
    print('-'*40)
    print("Your filter settings: \n")
    print("City:", city.title())
    print("Month:", month.title()) 
    print("Day of Week:", day.title())
    print('-'*40)
    return city, month, day


# create dataframe based on selected filters    

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name       # this is used in pandas version 0.22
    #df['day_of_week'] = df['Start Time'].dt.day_name()          # this works starting from pandas version 0.23


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

    return df


# functions for statistics

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Common Month:', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Common Week Day:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0] 
    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most popular start station:', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most popular end station:', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['Combined Start End'] = 'FROM ' + df['Start Station'] + ' TO ' + df['End Station']
    print('Most popular combination of start and end station:',  df['Combined Start End'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time_sec =  df['Trip Duration'].sum()
    travel_time_h = travel_time_sec / 3600 
    print("Total travel time:", travel_time_sec, "seconds or ", travel_time_h , "hours")

    # display mean travel time
    print("Mean travel time:", df['Trip Duration'].mean(), "seconds")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of user types:')
    print(df['User Type'].value_counts())
    print()
    
    if city != 'washington':
        # Display counts of gender
        print('Counts of gender:')
        print(df['Gender'].value_counts())
        print()
    
        # Display earliest, most recent, and most common year of birth
        print("Earliest birth year: ", df['Birth Year'].min())
        print("Most recent birth year: ", df['Birth Year'].max())
        print("Most common birth year: ", df['Birth Year'].mode()[0])
    else:
        print("We don't have data about gender or birth year for Washington.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        rawdata = input('\nDo you want to see the (filtered) raw data? If yes, please enter yes:\n')
        rowcount = 0
        while rawdata.lower() == 'yes':
            if (rowcount + 5) < df.index.size:
                print(df[rowcount:rowcount + 5])
                rowcount += 5
            else:
                print('You reached the end of the table!')
                break
            rawdata = input('Do you want to see 5 more rows? If yes, please enter yes:\n')

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
