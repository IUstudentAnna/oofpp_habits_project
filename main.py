import questionary
from datetime import datetime
from db import no_habit_exists, create_db, get_all_habits, get_all_habits_by_periodicity, get_habit_names_by_periodicity
from habit_class import Habit
from analyze import get_longest_streak_per_habit, get_longest_daily_streak, get_longest_weekly_streak

def cli():
    """
    ~~~ Habit Tracker App ~~~
    Start the habit tracker app and navigate through the modules "Analytics" and
    "Habit Management"
    """
    db = create_db()

    welcome_text = "Hello! Welcome to your Habit Tracker!\n "
    welcome_text += "We're excited to help you build positive routines and "
    welcome_text += "reach your goals, one day at a time. Start tracking your habits, "
    welcome_text += "celebrate your progress, and unlock your best self. "
    welcome_text += "Are you ready?"
    question = questionary.confirm(welcome_text).ask()

    while question is False:
        print("Alright! You can try again later")
        break

    while question is True:
        choice = questionary.select("What do you want to do next?",
            choices=[
                "Manage my habits",
                "Analyse my habits",
                "Exit"]
            ).ask()

        if choice == "Exit":
            print("Bye bye and see you later!\n")
            question = False

        # Habit management module
        elif choice == "Manage my habits":
            select = questionary.select("What do you want to do?",
                        choices=["Create a new habit",
                                 "Check off an existing habit",
                                 "Check off an existing habit retrospecitvely",
                                 "Delete an existing habit"]).ask()

            if select == "Delete an existing habit":
                name = (questionary.text(
                        "What is the name of your habit you want to delete?").\
                            ask()).lower()
                if no_habit_exists(db, name) == True:
                    print("The Habit does not exist, please create first!")
                else:
                    habit = (Habit(name, "no description", "no periodicity",  "no creation timestamp"))
                    habit.delete_habit(db)
                    print(f"Your habit {name} has been successfully deleted!")


            elif select == "Create a new habit":
                name = (questionary.text(
                                "What is the name of your new habit?").ask()).lower()
                if no_habit_exists(db, name) == False:
                    print("The Habit already exists, please select another name!")
                else:
                    habit_description = (questionary.text(
                                         "Please describe your new habit?").ask()).lower()
                    habit_periodicity = questionary.select(
                                        "What is the periodicity of your habit?",
                                        choices=[
                                            "Daily", 
                                            "Weekly"
                                            ]).ask()
                    creation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                    habit = Habit(name, habit_description, habit_periodicity, creation_time)
                    habit.save_new_habit(db)
                    print(f"Your new habit {name} has been successfully created!")
            
            elif select == "Check off an existing habit":
                name = (questionary.text(
                            "What is the name of your habit you succeeded today?").\
                                ask()).lower()
                if no_habit_exists(db, name) == True:
                    print("The Habit does not exist, please create first!")
                else:
                    habit = Habit(name, "no description", "no periodicity", "no creation timestamp")
                    habit.add_checkoff_event(db)
                    print(f"Your habit {name} has been successfully checked off! Well done!")
        
            elif select == "Check off an existing habit retrospecitvely":
                name = (questionary.text("You forgott to check off a habit? No problem! What is the name of your habit you want to check off retrospectively?").\
                                    ask()).lower()
                if no_habit_exists(db, name) == True:
                    print("The Habit does not exist, please create first!")
                else:
                    print("Please insert the check off date in the following format: yyyy-mm-dd")
                    retrospective_date = (questionary.text("What is the date of the check off?").ask())
                    retrospective_date_reformated = datetime.strptime(retrospective_date, '%Y-%m-%d')
                    if retrospective_date_reformated > datetime.today():
                        print("The date you want to insert is in the future, please try again.")
                        question = True
                    else:
                        habit = Habit(name, "no description", "no periodicity", "no creation timestamp")
                        habit.add_checkoff_event(db, date = retrospective_date)
                        print(f"Your habit {name} has been successfully checked off for {retrospective_date}! Well done!")
        
        
            # Analytics module
        elif choice == "Analyse my habits":
            select = questionary.select("What do you want to do?\n",
                                            choices=["Return all habits",
                                                    "Return all habits by periodicity",
                                                    "Return longest streak for one habit",
                                                    "Return longest streak per periodicity",
                                                    ]).ask()
                
            if select == "Return all habits":
                result = get_all_habits(db)
                print("List of all your tracked habits and their periodicity:")
                print("Habit - Description - Periodicity - Date of creation")
                print("")
                for current_habit in sorted(set(result)):
                    print(' - '.join(current_habit))
                print("")

            elif select == "Return all habits by periodicity":
                periodicity = questionary.select("Choose one periodicity!",
                                                choices=[
                                                    "Daily",
                                                    "Weekly"
                                                    ]).ask()
                result = get_all_habits_by_periodicity(db, periodicity)
                print(f"List of all you {periodicity} habits:")
                print("Habit - Description - Date of creation")
                print("")
                for current_habit in sorted(set(result)):
                    print(' - '.join(current_habit))
                print("")

            elif select == "Return longest streak for one habit":
                name = (questionary.text("What is the name of your habit you want to get the longest streak for?").\
                            ask()).lower()
                if no_habit_exists(db, name) == True:
                    print("The Habit does not exist, please create it first!")
                else:
                    longest_streak = get_longest_streak_per_habit(db, name)
                    print(f"The longest {longest_streak["periodicity"]} streak is tracked for your habit: {longest_streak["max_habit"]}, with {longest_streak["max_streak"]} streaks!")


            elif select == "Return longest streak per periodicity":
                periodicity = questionary.select("Choose one periodicity.",
                                                choices=[
                                                    "Daily",
                                                    "Weekly"
                                                    ]).ask()
                if periodicity == "Daily":
                    names_of_daily_habits = get_habit_names_by_periodicity(db, periodicity)
                    longest_streak = get_longest_daily_streak(db, names_of_daily_habits)
                    print(f"The longest {longest_streak["periodicity"]} streak is tracked for your habit: {longest_streak["max_habit"]}, with {longest_streak["max_streak"]} streaks!")

                elif periodicity == "Weekly":
                    names_of_weekly_habits = get_habit_names_by_periodicity(db, periodicity)
                    longest_streak = get_longest_weekly_streak(db, names_of_weekly_habits)
                    print(f"The longest {longest_streak["periodicity"]} streak is tracked for your habit: {longest_streak["max_habit"]}, with {longest_streak["max_streak"]} streaks!")
                    
                    
                    



if __name__ == '__main__':
    cli()

