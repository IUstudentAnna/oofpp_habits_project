from datetime import datetime, date
import pytest
from db import get_all_habit_data, create_db
from habit_class import Habit
from analyze import get_longest_streak_per_habit, get_longest_daily_streak, get_longest_weekly_streak

@pytest.fixture
def db_connection(tmp_path):
    """
    Fixture creating a temporary database
    """
    db_path = tmp_path / "test.db"
    conn = create_db(db_path)
    yield conn
    conn.close()

class TestClass:
    @pytest.fixture(autouse=True)
    def setup_db_connection(self, db_connection):
        """ 
        Inject database connection into test class and fill it
        with sample data.
        """
        self.db = db_connection

        habit = Habit(name="meditation", 
                    description="find stillness",
                    created = datetime(2025,3,1).strftime("%Y-%m-%d %H:%M:%S.%f"),
                    periodicity="Daily"
                    )
        habit.save_new_habit(self.db)
        habit.add_checkoff_event(self.db, "2025-03-01")
        habit.add_checkoff_event(self.db, "2025-03-02")
        habit.add_checkoff_event(self.db, "2025-03-03")
        habit.add_checkoff_event(self.db, "2025-03-04")
        habit.add_checkoff_event(self.db, "2025-03-05")
        habit.add_checkoff_event(self.db, "2025-03-08")
        habit.add_checkoff_event(self.db, "2025-03-20")
        habit.add_checkoff_event(self.db, "2025-03-21")
        habit.add_checkoff_event(self.db, "2025-03-22")
        habit.add_checkoff_event(self.db, "2025-03-23")
        habit.add_checkoff_event(self.db, str(date.today()))

        habit = Habit(name="workout",
                    description="get stronger",
                    created=datetime(2025,3,1).strftime("%Y-%m-%d %H:%M:%S.%f"),
                    periodicity="Weekly")
        habit.save_new_habit(self.db)
        habit.add_checkoff_event(self.db, "2025-03-03")
        habit.add_checkoff_event(self.db, "2025-03-10")
        habit.add_checkoff_event(self.db, "2025-03-17")
        habit.add_checkoff_event(self.db, "2025-03-24")
        habit.add_checkoff_event(self.db, str(date.today()))


        return db_connection

    def test_db_content(self):
        """
        Test the length of samples in database
        """
        db_data = get_all_habit_data(self.db)
        assert len(db_data) == 16

    def test_longest_daily_streak(self):
        """
        Test function get_longest_daily_streak(db, name)
        """
        daily_streaks = get_longest_daily_streak(self.db, {"meditation"})
        assert daily_streaks == {'periodicity': 'daily', 'max_habit': 'meditation', 'max_streak': 4}
   
    def test_longest_weekly_streak(self):
        """
        Test function get_longest_weekly_streak(db, name)
        """
        weekly_streaks = get_longest_weekly_streak(self.db, {"workout"})
        assert weekly_streaks == {'periodicity': 'weekly', 'max_habit': 'workout', 'max_streak': 3}
   
    def test_longest_streak_per_habit(self):
        """
        Test function get_longest_streak_per_habit(db, name)
        """
        longest_streak = get_longest_streak_per_habit(self.db, "workout")
        assert longest_streak == {'periodicity': 'weekly', 'max_habit': 'workout', 'max_streak': 3}
