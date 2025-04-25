import sqlite3

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
    return result_exists


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




