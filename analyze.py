from db import get_all_habit_data, periodicity_per_habit
from datetime import date, datetime, timedelta
import pandas as pd

def get_longest_streak_per_habit(db, name):
    """
    Get the longest streak of a chosen habit.

    :param name: name of the chose habit
    :param db: the created sqlite3 database main.db
    :return: overall record streak for the chosen habit   
    """

    # Get unique periodicity for habit
    periodicity_value = periodicity_per_habit(db, name)
    if periodicity_value == "Weekly":
        return get_longest_weekly_streak(db, {name})
    elif periodicity_value == "Daily":
        return get_longest_daily_streak(db, {name}) 


def get_longest_daily_streak(db, names_list):
    """
    Get the longest daily streak of all daily habits.

    :param name_list: name list of all daily habits
    :param db: the created sqlite3 database main.db
    :return: dictionary with the longest streak of 
            all daily habits (keys: periodicity, max_habit, max_streak)
    """
    df = get_all_habit_data(db)
    df['date'] = pd.to_datetime(df['date'])
    df_daily = df[df['periodicity'] == 'Daily'].sort_values('date')

    col_names = names_list
    # Calculate maximum streak for each habit and add it to the dict
    dict_streak_habit = {}
    for name in col_names:
        df_daily_name= df_daily[df_daily["name"] == name]
        # print(df_daily_name)
        counter = 0
        max_streak = streak = 0
        count = len(df_daily_name) - 1
        if count == 0:
                streak = 0
        else:
            while counter < len(df_daily_name)-1:
                    date1 = df_daily_name.iloc[counter, 3] 
                    date2 = df_daily_name.iloc[counter+1, 3]
                    date_end = df_daily_name.iloc[len(df_daily_name) - 1, 3]
                    if date1 == date2:
                        streak += 0
                    elif date1 + timedelta(days=1) == date2 and date_end >= pd.Timestamp.today() - timedelta(days=1):
                        streak += 1
                    else:
                        streak = 0
                    counter += 1
                    max_streak = max(max_streak, streak)
        dict_streak_habit[name] = max_streak
    # Get habit with maximum streaks
    max_habit = max(dict_streak_habit, key=dict_streak_habit.get)
    max_streak = dict_streak_habit[max_habit]
    # return a dictionary with the longest streak of all daily habits
    return {
        "periodicity": "daily",
        "max_habit": max_habit, 
        "max_streak": max_streak
        }

def get_longest_weekly_streak(db, names_list):
     """
    Get the longest weekly streak of all weekly habits.

    :param name_list: name list of all weekly habits
    :param db: the created sqlite3 database main.db
    :return: dictionary with the longest streak of 
            all weekly habits (keys: periodicity, max_habit, max_streak)
    """
    df = get_all_habit_data(db)
    df_weekly = df[df['periodicity'] == 'Weekly'].sort_values('date')
    df_weekly['date'] = pd.to_datetime(df_weekly['date'])
    df_weekly['week_start'] = df_weekly['date'] - pd.to_timedelta(df_weekly['date'].dt.weekday, unit='d')

    col_names = names_list
    # Calculate maximum streak for each habit and add it to the dict
    dict_streak_habit = {}
    for name in col_names:
        df_weekly_name= df_weekly[df_weekly["name"] == name]
        counter = 0
        max_streak = streak = 0
        count = len(df_weekly_name) - 1
        if count == 0:
                streak = 0
        else:
            while counter < len(df_weekly_name)-1:
                    date1 = df_weekly_name.iloc[counter, 4] 
                    date2 = df_weekly_name.iloc[counter+1, 4]
                    date_end = df_weekly_name.iloc[len(df_weekly_name) - 1, 4]
                    if date1 == date2:
                        streak += 0
                    elif date1 + timedelta(days=7) == date2 and date_end >= pd.Timestamp.today() - timedelta(days=7):
                        streak += 1
                    else:
                        streak = 0
                    counter += 1
                    max_streak = max(streak, max_streak)
                    # print(streak, max_streak, date1, date2, date_end, pd.Timestamp.today() - timedelta(days=7))
                    # print(date1 + timedelta(days=7) == date2 )
                    # print(date_end >= pd.Timestamp.today() - timedelta(days=7))
        dict_streak_habit[name] = max_streak
    # print(dict_streak_habit)
    # Get habit with maximum streaks
    max_habit = max(dict_streak_habit, key=dict_streak_habit.get)
    max_streak = dict_streak_habit[max_habit]

    return {
        "periodicity": "daily",
        "max_habit": max_habit, 
        "max_streak": max_streak
        }
 
