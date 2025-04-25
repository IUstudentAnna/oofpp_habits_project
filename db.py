import sqlite3
from datetime import date
import pandas as pd

def create_db(name="main.db"):
    """
    Create the sqlite3 database and all  tables if they do not exist yet.

    :param name: name of the database = main.db
    :return: Builds a database in sqlite3 and connects to the database
    """
    db = sqlite3.connect(name)
    create_db_tables(db)
    return db

def create_db_tables(db):
    """
    Creates the required tables 'habit' and 'habit_records' in the database main.db-
    The table habit has the columns name, description, created, periodicity and the table
    habit_records has the columns date, habitName. Both tables are connected by the key 
    habit(name) and habit_records(habitName).

    :param db: sqlite3 database main.db
    """
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS habit (
        name TEXT PRIMARY KEY,
        description TEXT,
        created TEXT,
        periodicity TEXT
        )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS habit_records (
        date TEXT,
        habitName TEXT,
        FOREIGN KEY (habitName) REFERENCES habit(name)
        )""")
    db.commit()

def no_habit_exists(db, name):
    """
    Checks if a certain habit name is already in the database.

    :param db: the created sqlite3 database main.db
    :param name: name of the habit to look for
    :return: True, if the habit already exists in the database
    """
    cur = db.cursor()
    cur.execute("SELECT name FROM habit WHERE name=?", (name,))
    result_exists = cur.fetchall()

    if not result_exists:
        return True
    else:
        return False


def add_new_habit(db, name, description, created, periodicity):
    """
    Add new habit to habit table.

    :param db: the created sqlite3 database main.db
    :param name: name of the new habit
    :param description: short description of the new habit
    :param created: timestamp of creating the new habit
    :param periodicity: periodicity of the new habit
    """
    cur = db.cursor()
    cur.execute("INSERT OR REPLACE INTO habit VALUES (?, ?, ?, ?)", 
                (name, description, created, periodicity))
    db.commit()

def checkoff_habit(db, name, checkoff_date=None):
    """
    check off a existing habit. If no checkoff_date is given, the habit is checked off for today.
    If a checkoff_date is given, the habit is checked off retrospective.

    :param db: the created sqlite3 database main.db
    :param name: name of the existing habit
    :param checkoff_date: today's date or a given retrospecitve date of the check off
    """
    cur = db.cursor()
    if not checkoff_date:
        checkoff_date = str(date.today())
    cur.execute("INSERT INTO habit_records VALUES (?, ?)", (checkoff_date, name))
    db.commit()

def get_all_habit_data(db):
    """
    Get all data for all habits in database.

    :param db: the created sqlite3 database main.db
    :return: table with name, creation date, periodicity and check offs for all tracked habits
    """
    df = pd.read_sql("""SELECT name, created, periodicity, date FROM habit 
                INNER JOIN habit_records ON habit_records.habitName = habit.name""", 
                db)
    return df

def get_all_habits(db):
    """
    Get all habits from the habit table

    :param db: the created sqlite3 database main.db
    :return: list of all habits in the habit table
    """
    cur = db.cursor()
    cur.execute("SELECT name, description, periodicity, created FROM habit")
    return cur.fetchall()

def get_all_habits_by_periodicity(db, periodicity):
    """
    Get all habits from the habit table filtered by periodicity
    
    :param db: the created sqlite3 database main.db
    :param periodicity: weekly or daily
    :return: list of all habits in the habit table
    """
    cur = db.cursor()
    cur.execute("SELECT name, description, created FROM habit WHERE periodicity=?", (periodicity, ))
    return cur.fetchall()

def get_habit_names_by_periodicity(db, periodicity):
    """
    Get all habit names from the habit table for one periodicity.

    :param db: the created sqlite3 database main.db
    :param periodicity: periodicity daily or weekly
    :return: list of all habit names for a given periodicity
    """
    query = f"SELECT name FROM habit WHERE periodicity='{periodicity}'"
    df_raw = pd.read_sql(query, db)
    df_pandas = pd.DataFrame(df_raw)
    df = df_pandas["name"].tolist()
    return df


def periodicity_per_habit(db, name):
    """
    Get distinct periodicity for a chosen habit.

    :param db: the created sqlite3 database main.db
    :param name: name of the habit 
    :return: periodicity as string
    """
    query = f"SELECT DISTINCT periodicity FROM habit \
            INNER JOIN habit_records ON habit_records.habitName = \
            habit.name WHERE name= '{name}'"
    unique_periodicity = pd.read_sql(query, db)
    periodicity_value = unique_periodicity['periodicity'].iloc[0]
    return periodicity_value

def delete_habit(db, name):
    """
    Delete all data for the chosen habit
    
    :param db: the created sqlite3 database main.db
    :param name: name of the habit to delete
    """
    cur = db.cursor()
    cur.execute("DELETE FROM habit WHERE name=?", (name,))
    cur.execute("DELETE FROM habit_records WHERE habitName=?", (name,))
    db.commit()
