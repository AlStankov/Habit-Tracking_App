import sqlite3
from datetime import date, timedelta, datetime


def get_db(db_name="default.db"):
    db = sqlite3.connect(db_name)
    create_table(db)
    return db


def create_table(db):
    cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS habit_definition (
        name VARCHAR(50) PRIMARY KEY ,
        description TEXT,
        periodicity VARCHAR(20))""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS habit_follow(
        name VARCHAR(50),
        date DATE,
        FOREIGN KEY (name) REFERENCES habit_definition(name))""")

    db.commit()


def habit_create(name, description, periodicity, db):
    cursor = db.cursor()

    # the new habit is being inserted to the database, provided it does not exist there already
    cursor.execute("INSERT INTO habit_definition (name, description, periodicity) VALUES(?, ?, ?)",
                   (name, description, periodicity))
    db.commit()


def habit_insert(name, db, follow_date):
    cursor = db.cursor()

    # if the follow_date is not specified, the current follow_date is taken
    if follow_date is None:
        adjusted_follow_date = str(date.today())
    else:
        adjusted_follow_date = str(follow_date)
    # the new habit check-off is being inserted to the database, provided it does not exist there already

    try:
        cursor.execute("INSERT INTO habit_follow (name, date) VALUES(?, ?)", (name, adjusted_follow_date))
        db.commit()
    except sqlite3.IntegrityError as e:
        # handles the unique constraint violation
        print(f"Warning: {e}")


# returns everything from the db
def return_all_data(db):
    cursor = db.cursor()

    cursor.execute("SELECT DISTINCT name FROM habit_definition")
    results = cursor.fetchall()

    # formats the results
    adjusted_results = ', '.join(result[0] for result in results)
    return adjusted_results


def return_given_periodicity(periodicity, db):
    cursor = db.cursor()

    cursor.execute("SELECT name FROM habit_definition WHERE periodicity = ?", (str(periodicity),))
    results = cursor.fetchall()

    # formats the results
    formatted_results = ', '.join(result[0] for result in results)
    return formatted_results

# returns everything from the db for the specified tracker


def return_data_for_habit(habit_name, db):
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(DISTINCT date) FROM habit_follow WHERE name = ?", (habit_name,))
    count_tuple = cursor.fetchone()  # fetches a single tuple
    return count_tuple[0]  # returns the count value


# this function will be used to check if the name of the habit the user wants to check-off, actually exists
def is_name_in_database(name_to_check, db, table_name="habit_definition"):
    cursor = db.cursor()

    try:
        # executes a query to check if the name exists in a specific table
        cursor.execute("SELECT COUNT(*) FROM {} WHERE name = ?".format(table_name), (name_to_check,))
        # returns the count
        result = cursor.fetchone()

        # checks if the count is greater than 0, i.e. name exists, or not
        return result[0] > 0

    except sqlite3.OperationalError:
        return False
        # the print statement is executed in main.py


# this function checks if the check-off of a daily habit happens for a consecutive day
def are_dates_consecutive(today, db):
    cursor = db.cursor()

    # retrieves the most recent check-off date
    cursor.execute("SELECT MAX(date) FROM habit_follow")
    most_recent_checkoff_day = cursor.fetchone()[0]

    # converts the most recent check-off date to a datetime object
    most_recent_checkoff_datetime = datetime.strptime(most_recent_checkoff_day, '%Y-%m-%d')

    # checks if the difference between the current date and the most recent check-off date is one day
    return today - most_recent_checkoff_datetime == timedelta(days=1)


def are_weeks_consecutive(today, db):
    cursor = db.cursor()

    # retrieves the most recent check-off date
    cursor.execute("SELECT MAX(date) FROM habit_follow")
    most_recent_checkoff_day = cursor.fetchone()[0]

    # converts the most recent check-off date to a datetime object
    most_recent_checkoff_datetime = datetime.strptime(most_recent_checkoff_day, '%Y-%m-%d')

    ''' checks if the difference between the current date and the most recent check-off date 
    is in the range of 2 consecutive weeks. This range is between 1 day (f.ex. Sunday and then Monday) and 
    13 days (f.ex. Monday and then Sunday in the next week '''

    return 1 <= (today - most_recent_checkoff_datetime.date()).days <= 13
