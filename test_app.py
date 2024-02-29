from tracker import Habit
from database import (get_db, habit_create, habit_insert, return_data_for_habit, return_all_data,
                      return_given_periodicity)
import os


class TestHabit:

    def setup_method(self):
        
        self.test_db = get_db(db_name="test_1.db")

        habit_create("Teeth", "Brush your teeth every day", "every day", self.test_db)
        habit_create("Gym", "Go to the gym every week", "every week", self.test_db)
        habit_create("Water", "Drink at least 1.5l. water every day", "every day", self.test_db)
        habit_create("Steps", "Walk at least 10 000 steps every day", "every day", self.test_db)
        habit_create("Chocolate", "Eat no more than 100g chocolate per day", "every day",
                     self.test_db)

        # habit check-offs for Teeth
        habit_insert("Teeth", self.test_db, "2024-01-10")
        habit_insert("Teeth", self.test_db, "2024-01-12")
        habit_insert("Teeth", self.test_db, "2024-01-16")
        habit_insert("Teeth", self.test_db, "2024-01-30")
        habit_insert("Teeth", self.test_db, "2024-01-31")
        habit_insert("Teeth", self.test_db, "2024-02-01")
        habit_insert("Teeth", self.test_db, "2024-02-02")
        habit_insert("Teeth", self.test_db, "2024-02-05")
        habit_insert("Teeth", self.test_db, "2024-02-06")
        habit_insert("Teeth", self.test_db, "2024-02-07")

        # habit check-offs for Gym
        habit_insert("Gym", self.test_db, "2024-01-10")
        habit_insert("Gym", self.test_db, "2024-01-17")
        habit_insert("Gym", self.test_db, "2024-01-24")
        habit_insert("Gym", self.test_db, "2024-01-30")
        habit_insert("Gym", self.test_db, "2024-01-31")
        habit_insert("Gym", self.test_db, "2024-02-05")
        habit_insert("Gym", self.test_db, "2024-02-12")
        habit_insert("Gym", self.test_db, "2024-02-22")

        # habit check-offs for Steps
        habit_insert("Steps", self.test_db, "2024-01-09")
        habit_insert("Steps", self.test_db, "2024-01-11")
        habit_insert("Steps", self.test_db, "2024-01-17")
        habit_insert("Steps", self.test_db, "2024-01-30")
        habit_insert("Steps", self.test_db, "2024-02-01")
        habit_insert("Steps", self.test_db, "2024-02-03")
        habit_insert("Steps", self.test_db, "2024-02-06")
        habit_insert("Steps", self.test_db, "2024-02-09")
        habit_insert("Steps", self.test_db, "2024-02-16")

        # habit check-offs for Water
        habit_insert("Water", self.test_db, "2024-01-11")
        habit_insert("Water", self.test_db, "2024-01-12")
        habit_insert("Water", self.test_db, "2024-01-16")
        habit_insert("Water", self.test_db, "2024-01-31")
        habit_insert("Water", self.test_db, "2024-02-01")
        habit_insert("Water", self.test_db, "2024-02-02")
        habit_insert("Water", self.test_db, "2024-02-05")
        habit_insert("Water", self.test_db, "2024-02-06")
        habit_insert("Water", self.test_db, "2024-02-08")

        # habit check-offs for Chocolate
        habit_insert("Chocolate", self.test_db, "2024-01-11")
        habit_insert("Chocolate", self.test_db, "2024-01-17")
        habit_insert("Chocolate", self.test_db, "2024-01-25")
        habit_insert("Chocolate", self.test_db, "2024-02-05")
        habit_insert("Chocolate", self.test_db, "2024-02-08")

        self.test_db.commit()

    def test_checkoff_times(self):

        assert return_data_for_habit(habit_name="Water", db=self.test_db) == 9
        assert return_data_for_habit(habit_name="Steps", db=self.test_db) == 9
        assert return_data_for_habit(habit_name="Chocolate", db=self.test_db) == 5

    def test_return_periodicity(self):
        return_given_periodicity("every day", self.test_db)

    def test_return_data(self):
        return_data_for_habit("Teeth", self.test_db)
        return_all_data(self.test_db)

    def test_habit(self):

        habit = Habit("Push-ups", "Do 10 push-ups a day", "every day")

        habit.checkoff(db=self.test_db)
        habit.streak_reset()
        habit.checkoff(db=self.test_db)

    def teardown_method(self):

        try:
            self.test_db.close()
            print("Database closed")
        except Exception as e:
            print(f"Error closing database: {e}")

        try:
            os.remove("test_1.db")
            print("Database removed")
        except Exception as e:
            print(f"Error removing database file: {e}")
