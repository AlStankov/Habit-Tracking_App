import questionary
from database import get_db, is_name_in_database, are_dates_consecutive, are_weeks_consecutive, \
    return_all_data, return_given_periodicity, return_data_for_habit
from tracker import Habit
from datetime import date
import os


def interface():
    os.remove('main.db')
    db = get_db('main.db')

    '''the whole menu is inserted in a while-loop. Thus, whatever the user decides to do, they will be returned to the
    main menu, referred to below as "path", unless they choose the option "Exit the app". Should they choose
    the option "Exit the app", a goodbye-statement will be printed and the loop will break'''

    while True:
        path = questionary.select(
            "What would you like to do?",
            choices=["Create a new habit", "Check-off an existing habit", "Analyse", "Exit the app"]).ask()

        # If the user chooses the first option "Create a habit"
        if path == "Create a new habit":
            maybe_predefined = questionary.select(
                "Do you want to choose from our predefined habits or create a new one?",
                choices=["Yes, show me the predefined habits", "No, i would like to create my own habit"]).ask()

            if maybe_predefined == "Yes, show me the predefined habits":
                choice_predefined = questionary.select("Choose one of the options below:", choices=[
                    "Teeth - Brush your teeth every day", "Gym - Go to the gym every week",
                    "Water - Drink at least 1.5l. water every day", "Steps - Walk at least 10 000 steps every day",
                    "Chocolate - Eat no more than 100g chocolate per day"]).ask()

                # if the user chooses the first predefined habit

                if choice_predefined == "Teeth - Brush your teeth every day":
                    # creates and stores the habit
                    Habit("Teeth", "Brush your teeth every day", "every day").define(db)

                # if the user chooses the second predefined habit
                elif choice_predefined == "Gym - Go to the gym every week":
                    # creates and stores the habit
                    Habit("Gym", "Go to the gym every week", "every week").define(db)

                # if the user chooses the third predefined habit
                elif choice_predefined == "Water - Drink at least 1.5l. water every day":
                    # creates and stores the habit
                    (Habit("Water", "Drink at least 1.5l. water every day", "every day").
                     define(db))

                # if the user chooses the fourth predefined habit
                elif choice_predefined == "Steps - Walk at least 10 000 steps every day":
                    # creates and stores the habit
                    (Habit("Steps", "Walk at least 10 000 steps every day", "every day").
                     define(db))

                # if the user chooses the fifth predefined habit
                elif choice_predefined == "Chocolate - Eat no more than 100g chocolate per day":
                    # creates and stores the habit
                    (Habit("Chocolate", "Eat no more than 100g chocolate per day", "every day").
                     define(db))

            elif maybe_predefined == "No, i would like to create my own habit":
                habit_name = questionary.text("What is the name of your habit?").ask()
                habit_desc = questionary.text("What is the description of your habit?").ask()
                habit_periodicity = questionary.select(
                    "Which periodicity would you like to follow with your habit?",
                    choices=["every day", "every week"]).ask()

                # creates a habit with the name and description from the user and stores it in the database
                Habit(habit_name, habit_desc, habit_periodicity).define(db)

        # if the user chooses the second option "Check-off an existing habit"
        elif path == "Check-off an existing habit":
            name = questionary.text("What is the name of the habit you want to check-off?").ask()

            if not is_name_in_database(name, db):
                print("Sorry, the name you inserted does not exist on the database!")

            # the variable habit_instance is artificially created 
            habit_instance = Habit(name, "description", "periodicity")
            # in the following, it is assumed that the user can not check-off a habit for any other day, except the
            # current day
            today = date.today()
            formatted_today = today.strftime('%Y-%m-%d')   # converts the date to a string
            habit_instance.checkoff(db, formatted_today)   # checks-off the habit

            if habit_instance.periodicity == "every day":
                # for consecutive dates, the streak is increased
                if are_dates_consecutive(formatted_today, db):
                    habit_instance.streak_increase()

                # for non-consecutive dates, the streak is reset
                elif not are_dates_consecutive(formatted_today, db):
                    habit_instance.streak_reset()

            elif habit_instance.periodicity == "every week":
                # for consecutive dates, the streak is increased
                if are_weeks_consecutive(formatted_today, db):
                    habit_instance.streak_increase()

                # for non-consecutive dates, the streak is reset
                elif not are_weeks_consecutive(formatted_today, db):
                    habit_instance.streak_reset()

        # if the user chooses the third option "Analyse"
        elif path == "Analyse":
            analysis_choice = questionary.select(
                "What would you like to know?",
                choices=["Show me all my current habits", "Show me all habits with a given periodicity",
                         "How many times did I check-off a habit?",
                         "What is my longest streak?"]).ask()

            if analysis_choice == "Show me all my current habits":
                print(return_all_data(db))

            elif analysis_choice == "Show me all habits with a given periodicity":
                periodicity_choice = questionary.select("Please, specify the periodicity you are interested in",
                                                        choices=["every day", "every week"]).ask()
                print(f'Periodicity chosen: {periodicity_choice}')
                print(return_given_periodicity(periodicity_choice, db))

            elif analysis_choice == "How many times did I check-off a habit?":
                _name = questionary.text(
                    "What is the name of the habit you are interested in?").ask()
                print(return_data_for_habit(_name, db))

            elif analysis_choice == "What is my longest streak?":
                streak_choice = questionary.select("Are you interested in a specific habit or in all habits?",
                                                   choices=["I am interested in a specific habit",
                                                            "Show me the longest streak from all habits",
                                                            "Show me the longest current streak from all habits"]).ask()

                if streak_choice == "I am interested in a specific habit":
                    name_ = questionary.text("What is the name of the habit you are interested in?").ask()
                    habit_instance = Habit(name_, "description", "periodicity")
                    print(habit_instance)   # This will call the __str__ function from tracker

                elif streak_choice == "Show me the longest streak from all habits":
                    # retrieves the variable habit_with_longest_streak from the Habit class
                    habit_with_longest_streak = Habit.habit_with_longest_streak
                    print(f"The habit with the longest streak ever is {habit_with_longest_streak.name}. \
                    Its longest streak ever is {habit_with_longest_streak.max_count}.")

                elif streak_choice == "Show me the longest current streak from all habits":
                    # retrieves the variable habit_with_longest_current_streak from the Habit class
                    habit_with_longest_current_streak = Habit.habit_with_longest_current_streak
                    print(f"The habit with the longest current streak is {habit_with_longest_current_streak.name}. \
                                        Its current streak is {habit_with_longest_current_streak.count}.")

        # if the user chooses to leave the app
        elif path == "Exit the app":
            print('Sad to see you go! Goodbye!')
            break


if __name__ == '__main__':
    interface()
