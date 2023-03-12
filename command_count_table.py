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


def add_command_count(command, date_logged, author, argument):
    parameterized_data = """INSERT INTO command_counters
                (command, date_logged, author, argument) VALUES (?,?,?,?)"""
    params = (command, date_logged, author, argument)
    cursor.execute(parameterized_data, params)
    conn.commit()


def return_command_total():
    # number = cursor.execute("""SELECT count(*) FROM command_counters WHERE command='type'""")

    # number1 = cursor.execute("""SELECT DATETIME(ROUND(date_logged/(1000*300))) FROM command_counters""")

    number2 = cursor.execute("""SELECT command, lower(argument), 
                    COUNT(distinct datetime(strftime('%Y-%m-%dT%H:%M:00', date_logged))) 
                    FROM command_counters
                    WHERE command='typo' 
                    GROUP BY command, lower(argument)""")
    print(number2.fetchall())
    print(type(number2))


    return number2

    # select count() as count
    # from (select *
    #       from counter
    #       where command = 'some_command'
    #       and lower(argument) = 'some_argument'
    #       group by lower(argument), datetime(CAST(julianday(date_logged) * 1440 AS INTEGER) / 1440.0));
