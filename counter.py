import sqlite3

cute_counter = [
    (1, "quote", "user"),
    (1, "quote", "user")
]

class Counter:
    def __init__(self, user, q=None):
        self.count = 0
        self.user = user
        self.quote = q

    def create_db(self):
        connection = sqlite3.connect("counter.db")
        cursor = connection.cursor()

    def add_count(self):
        x_counter += (1, q, user)

class Cute(Counter):
    def __init__(self):
        super().__init__(x_conter, user, q=None)


add_count(cute_counter, cute_user, cute_q)