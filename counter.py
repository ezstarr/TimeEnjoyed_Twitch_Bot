import sqlite3

cute_counter = [
    (1, "quote", "user"),
    (1, "quote", "user")
]


class Counter:
    """Returns a message to chat containing the count of a word.
    Takes in a message and the user channel"""

    def __init__(self, user, q=None):
        """Initializes a counter, takes in user, and optional quote."""
        self.count = 0
        self.user = user
        self.quote = q

    def create_db(self):
        """Creates a sqlite3 database and creates a cursor, which allows the database to be used"""
        connection = sqlite3.connect("counter.db")
        cursor = connection.cursor()

    def add_count(self):
        x_counter += (1, q, user)

class Cute(Counter):
    def __init__(self):
        super().__init__(x_conter, user, q=None)


Counter.add_count(cute_counter, cute_user, cute_q)