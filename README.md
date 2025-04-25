# Welcome to Habit Hero!

Ready to become the best version of yourself? Track your habits, celebrate your progress, and build the routines that lead to real change. Every big achievement starts with a single step—let’s make today count!


This command line interface (CLI) tool allows you to create, delete and analyse your habits. You data is saved localy in a lightweight disk-based database using the SQLite3 module. 

## Features
The App consists of 2 main modules: 1. Habit Management and 2. Analytics. 

In the Habit Management module you can:

* create a habit (by giving a name, a short description and a periodicity (weekly or daily))
* check off a habit for the current day
* check off a habit retrospectively (in case you forgott to track your success)
* delete a habit

To analyze you habits you can:

* return a list with all your habits
* return a list with all your habits by a periodicity
* return your longest streak for a chosen habit
* return your longest streak for all habits of a chosen periodicity

A streak is defined as completing a task (your defined habit) x consecutive periods (days oder weeks) in a row, without breaking the habit. 


## Usage:
To start the app use your terminal:
```
python main.py
```


