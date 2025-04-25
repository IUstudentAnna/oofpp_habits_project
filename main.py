import questionary



def cli():
    """
   ~~~ Habit Tracker App ~~~
    Start the habit tracker app and navigate throug the modules "Analytics" and "Habit Management"
    """

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

    
if __name__ == '__main__':
    cli()

