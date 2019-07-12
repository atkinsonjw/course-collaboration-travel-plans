import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # Converts all input to lower case to reduce input errors
    city = input("What city would you like to explore: Chicago, New York City, or Washington? ").lower()
    while city not in CITY_DATA:
        print("\n**************************************************************************************")
        print("*****You entered "+ city +" which is not a participating city.  Please try again*****")
        print("**************************************************************************************\n")
        city = input("What city would you like to explore: Chicago, New York City, or Washington? ").lower()
                  
    # TO DO: get user input for month (all, january, february, ... , june)
    # Converts all input to lower case to reduce input errors
    month = input("What month: ALL, January, February, March, April, May, or June? ").lower()
    while month not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
        print("\n**************************************************************************************")
        print("*****You entered "+ month +".  Please try again*****")
        print("**************************************************************************************\n")
        month = input("What month: ALL, January, February, March, April, May, or June? ").lower()
              
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    # Converts all input to lower case to reduce input errors
    day = input("What day: ALL, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday?").lower()
    while day not in ('all','monday','tuesday','wednesday','thursday','friday','saturday','sunday'):
        print("\n**************************************************************************************")
        print("*****You entered "+ day +".  Please try again*****")
        print("**************************************************************************************\n")
        day = input("What day: ALL, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday? ").lower()      
              
              
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
    
    # load data file into a dataframe
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
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    months = ['january', 'february', 'march', 'april', 'may', 'june']


    # TO DO: display the most common month
    pop_mon = df['month'].mode()[0]
    print('The most popular month is:', months[(pop_mon-1)].title())

    #TO DO: display the most common day of week
    pop_day = df['day_of_week'].mode()[0].title()
    print("The most popular day is:" ,  pop_day)

    # TO DO: display the most common start hour
    #convert hour to am/pm
    hr=df['hour'].mode()[0]
    if hr-12 > 0:
        print("The most popular start time is",hr-12,"PM")
    else:
        print("The most popular start time is",hr,"AM")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
   
    # TO DO: display most commonly used start station
    print("The most commonly used START station is: ",df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print("The most commonly used END station is: ",df['End Station'].mode()[0])


    # TO DO: display most frequent combination of start station and end station trip
    combo = df['Start Station'] + df['End Station']
    pop_rte = combo.mode()[0]
    print("The most popular route (Start and Stop locations) is: ",pop_rte)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    tot_time = df['Trip Duration'].sum()/60
    print("Total travel time (in hours):", tot_time)

    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean()/60
    print("Mean travel time (in hours):", mean_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type = df['User Type'].value_counts()
    print("Number of Customers: {}\n"
          "Number of Subscribers: {}".format(user_type['Customer'], user_type['Subscriber']))


    # TO DO: Display counts of gender
    #Catch exceptions as Washington does not have gender data
    try:
        cnt_gen = df['Gender'].value_counts()
        print("Customer count by gender\n",cnt_gen)
    except KeyError:
        print("*****No gender data available*****")

    # TO DO: Display earliest, most recent, and most common year of birth
    #Catch exceptions for no data
    try:
        young= df['Birth Year'].max()
        old = df['Birth Year'].min()
        common = df['Birth Year'].mode()[0]
        print("The oldest birth year is: {}\nThe most recent birth year is: {}\nMost common birth year is: {} ".format(int(old),int(young),int(common)))
    except KeyError:
        print("*****No birth year data available*****")



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()