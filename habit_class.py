from db import add_new_habit, checkoff_habit


class Habit:

    def __init__(self, name: str, description: str, periodicity: str, created: str):
        """
        Habit class object, to store a habit with all its parameters in an object,
        to checkoff a habit and count these events, to delete a habit

        :param name: name of the habit
        :param description: short description of the habit
        :param periodicity: periodicity of the habit
        :param created: date of creating the habit
        """
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.created = created
        self.count = 0

    def save_new_habit(self, db):
        """
        Write the new habit in the database.

        :param db: sqlite3 database main.db
        """
        add_new_habit(db, self.name, self.description, self.created, self.periodicity)

    def add_checkoff_event(self, db, date: str = None):
        """
        Add check off event to the database, either todays date or a retrospective date.

        :param db: created sqlite3 database main.db
        :param date: date of the check off event
        """
        checkoff_habit(db, self.name, date)

