import questionary
from datetime import datetime
from db import no_habit_exists, create_db
from habit_class import Habit

def cli():
    """
   ~~~ Habit Tracker App ~~~
    Start the habit tracker app and navigate throug the modules "Analytics" and "Habit Management"
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

        elif choice == "Manage my habits":
            select = questionary.select("What do you want to do?",
                        choices=["Create a new habit",
                                 "Checkoff an existing habit",
                                 "Checkoff an existing habit retrospecitvely",
                                 "Delete an existing habit"]).ask()

            if select == "Delete an existing habit":
                name = (questionary.text(
                        "What is the name of your habit you want to delete?").\
                            ask()).lower()
                if no_habit_exists(db, name) == True:
                    print("The Habit does not exist, please create first!")
                else:
                    habit = (Habit(name, "no description", "no periodicity",  "no creation timestamp"))
                    habit.clear_habit(db)
                    print(f"Your habit {name} has been successfully deleted!")


            elif select == "Create a new habit":
                name = (questionary.text(
                                "What is the name of your new habit?").ask()).lower()
                if no_habit_exists(db, name) == True:
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
            
            elif select == "Checkoff an existing habit":
                name = (questionary.text(
                            "What is the name of your habit you succeeded today?").\
                                ask()).lower()
                if no_habit_exists(db, name) == True:
                    print("The Habit does not exist, please create first!")
                else:
                    habit = Habit(name, "no description", "no periodicity", "no creation timestamp")
                    # habit.checkoff()
                    habit.add_checkoff_event(db)
                    print(f"Your habit {name} has been successfully checked off! Well done!")
        
            elif select == "Checkoff an existing habit retrospecitvely":
                name = (questionary.text("You forgott to checkoff a habit? No problem! What is the name of your habit you want to checkoff retrospectively?").\
                                    ask()).lower()
                if no_habit_exists(db, name) == True:
                    print("The Habit does not exist, please create first!")
                else:
                    print("Please insert the checkoff date in the following format: yyyy-mm-dd")
                    retrospective_date = (questionary.text("What is the date of the checkoff?").ask())
                    retrospective_date_reformated = datetime.strptime(retrospective_date, '%Y-%m-%d')
                    if retrospective_date_reformated > datetime.today():
                        print("The date you want to insert is in the future, please try again.")
                        question = True
                    else:
                        habit = Habit(name, "no description", "no periodicity", "no creation timestamp")
                        habit.add_checkoff_event(db, date = retrospective_date)
                        print(f"Your habit {name} has been successfully checked off for {retrospective_date}! Well done!")
        

            

    


    
if __name__ == '__main__':
    cli()

