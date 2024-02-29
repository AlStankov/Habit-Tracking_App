from database import habit_create, habit_insert


class Habit:

    # this variable will be used to retrieve the longest streak ever of all habits
    habit_with_longest_streak = None

    # this variable will be used to retrieve the longest current streak of all habits
    habit_with_longest_current_streak = None

    def __init__(self, name, description, periodicity):
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.count = 1      # the streak is initially set to 1
        self.max_count = 1    # longest streak

        # updates the habit with the longest streak if needed
        if not Habit.habit_with_longest_streak or self.max_count > Habit.habit_with_longest_streak.max_count:
            Habit.habit_with_longest_streak = self

        # updates the habit with the longest current streak if needed
        if not Habit.habit_with_longest_current_streak or self.count > Habit.habit_with_longest_current_streak.count:
            Habit.habit_with_longest_current_streak = self

    # returns the habit with its corresponding current streak
    def __str__(self):
        return f'The habit \"{self.name}\" has been successfully completed {self.count} times in a row.' \
               f'The longest streak for this habit is {self.max_count}'

    # increases the streak with 1. Will be called in case of consecutive check-off
    def streak_increase(self):
        self.count += 1

        # if the current streak is longer than the longest streak, then the longest streak is updated
        if self.count >= self.max_count:
            self.max_count = self.count

        # updates the habit with the longest streak if needed
        if not Habit.habit_with_longest_streak or self.max_count > Habit.habit_with_longest_streak.max_count:
            Habit.habit_with_longest_streak = self

        # updates the habit with the longest current streak if needed
        if not Habit.habit_with_longest_current_streak or self.count > Habit.habit_with_longest_current_streak.count:
            Habit.habit_with_longest_current_streak = self

    '''resets the streak to 1 in case of a check-off, given that a check-off has been previously missed, i.e. the streak
    has been lost'''
    def streak_reset(self):
        self.count = 1

    # defines a new habit and stores it in the database
    def define(self, db):
        habit_create(self.name, self.description, self.periodicity, db)

    # adds a new check-off event to a given habit (in the database)
    def checkoff(self, db, date: str = None):
        habit_insert(self.name, db, date)
