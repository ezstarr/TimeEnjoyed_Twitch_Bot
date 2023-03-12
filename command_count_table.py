import sqlite3

# establish connection to existing SQLite3 database
conn = sqlite3.connect('counter_db.db')
cursor = conn.cursor()

# create a new table for command counters if it doesn't already exit

cursor.execute('''CREATE TABLE IF NOT EXISTS command_counters (
                command string, 
                date_logged date,
                author string,
                argument string
                )''')


def add_command_count(command, author, argument, date_logged):
    parameterized_data = """INSERT INTO command_counters
                (command, author, argument, date_logged) VALUES (?,?,?,?)"""
    params = (command, author, argument, date_logged)
    cursor.execute(parameterized_data, params)
    conn.commit()


def return_command_total():
    number = cursor.execute("""SELECT command, lower(argument),
                    COUNT(distinct datetime(strftime('%Y-%m-%dT%H:%M:00', date_logged)))
                    FROM command_counters
                    WHERE command='typo'
                    GROUP BY command, lower(argument)""")
    rows = number.fetchall()
    count = len(rows)
    return count
