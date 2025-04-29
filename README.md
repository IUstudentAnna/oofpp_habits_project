# Welcome to Habit Hero!

Ready to become the best version of yourself? Track your habits, celebrate your progress, and build the routines that lead to real change. Every big achievement starts with a single step—let’s make today count!


This command line interface (CLI) tool allows you to create, complete and analyse your habits. Your data is saved locally in a lightweight disk-based database using the SQLite3 module. 

## Features
The App consists of 2 main modules: 1. **Habit Management** and 2. **Analytics**. 

In the Habit Management module you can:

* create a habit (by giving a name, a short description and a periodicity (weekly or daily))
* check off a habit for the current day
* check off a habit retrospectively (in case you forgott to track your success)
* delete a habit

To analyze your habits you can:

* return a list with all your habits
* return a list with all your habits by periodicity
* return your longest streak for a chosen habit
* return your longest streak for all habits of a chosen periodicity

A **streak** is defined as completing a task (your defined habit) x consecutive periods (days or weeks) in a row, without breaking the habit. A habit is considered active, when it is completed on the current time period (today or this week).


# Installation
## Prerequisites
Python 3.12.7 or later  
pytest module  
questionary module

Install requirements:
```
pip install questionary
pip install pytest
```

## Usage
- Clone repository to your local computer and go to the folder *oofpp_habits_project*
- Run the following command in your command line and follow the instructions using the arrow keys:
```
python main.py
```
## Testing 
Test the main components with pytest:
```
pytest . -v
```






