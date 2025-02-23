#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import time

# ملفات البيانات المتاحة
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    يسأل المستخدم عن المدينة والشهر واليوم لتحليل البيانات.
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # اختيار المدينة
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington?\n").lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid input. Please choose one of the following: Chicago, New York City, or Washington.")
    
    # اختيار الشهر
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Which month? January, February, March, April, May, June, or 'all' to not filter by month?\n").lower()
        if month in months:
            break
        else:
            print("Invalid input. Please choose a valid month or 'all'.")
    
    # اختيار اليوم
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or 'all' to not filter by day?\n").lower()
        if day in days:
            break
        else:
            print("Invalid input. Please choose a valid day or 'all'.")
    
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    تحميل البيانات وتصفيتها بناءً على المدخلات (المدينة، الشهر، اليوم).
    """
    # تحميل بيانات المدينة المحددة
    df = pd.read_csv(CITY_DATA[city])
    
    # تحويل عمود Start Time إلى datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # استخراج الشهر واليوم من Start Time
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    
    # تصفية البيانات حسب الشهر إذا لم يكن 'all'
    if month != 'all':
        df = df[df['month'] == month]
    
    # تصفية البيانات حسب اليوم إذا لم يكن 'all'
    if day != 'all':
        df = df[df['day_of_week'] == day]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # أكثر شهر شيوعًا
    most_common_month = df['month'].mode()[0]
    print('Most Common Month:', most_common_month)

    # أكثر يوم شيوعًا
    most_common_day = df['day_of_week'].mode()[0]
    print('Most Common Day:', most_common_day)

    # أكثر ساعة شيوعًا
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """
    Displays 5 rows of raw data at a time upon user request.
    """
    i = 0
    pd.set_option('display.max_columns', 200)
    raw = input("\nWould you like to view 5 rows of individual trip data? Enter 'yes' or 'no'.\n").lower()
    while True:
        if raw == 'no':
            break
        elif raw == 'yes':
            print(df.iloc[i:i+5])
            i += 5
            if i >= len(df):
                print("\nNo more data to display.")
                break
            raw = input("\nWould you like to view 5 more rows of data? Enter 'yes' or 'no'.\n").lower()
        else:
            raw = input("\nInvalid input. Please enter only 'yes' or 'no'.\n").lower()

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Most commonly used start station
    start_station = df['Start Station'].value_counts().idxmax()
    print('Most Commonly used start station:', start_station)

    # Most commonly used end station
    end_station = df['End Station'].value_counts().idxmax()
    print('Most Commonly used end station:', end_station)

    # Most common trip (start station + end station)
    most_common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most Common Trip:', most_common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Total travel time
    total_travel_time = sum(df['Trip Duration'])
    print('Total travel time:', round(total_travel_time / 86400, 2), "days")

    # Mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time:', round(mean_travel_time / 60, 2), "minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # User types
    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types)

    # Gender types
    try:
        gender_types = df['Gender'].value_counts()
        print('\nGender Types:\n', gender_types)
    except KeyError:
        print("\nGender Types:\nNo data available.")

    # Birth year statistics
    try:
        earliest_year = int(df['Birth Year'].min())
        print('\nEarliest Year:', earliest_year)
        most_recent_year = int(df['Birth Year'].max())
        print('Most Recent Year:', most_recent_year)
        most_common_year = int(df['Birth Year'].mode()[0])
        print('Most Common Year:', most_common_year)
    except KeyError:
        print("\nBirth Year:\nNo data available.")

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
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart != 'yes':
            break

if __name__ == "__main__":
    main()

