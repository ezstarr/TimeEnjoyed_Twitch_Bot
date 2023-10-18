import sqlite3

tarot_ratings = [
    (id, username, rating, datetime),

]

# Database for tarot reading
tarot_rating = sqlite3.connect('tarot_ratings_db.db')
cursor = tarot_rating.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS test_counts (
    a_count integer, 
    date_logged date
    )""")


# TODO: to get twitch_user_id for v2, need to ask helix api for the username id conversions.
# TODO: parameterized quotes for v2, limit to 3 words for v3

# Example of parameterized statement.
# sqlite3 will escape the quotes in any strings.


# Main.py needs to trigger a count.

def trigger_a_count():
    # cursor.execute("INSERT INTO test_counts VALUES (1,'date'")
    new_count_total = 0
    cursor.execute('INSERT INTO test_counts (a_count, date_logged) VALUES (?, datetime("now"))', (1,))
    count_conn.commit()


def return_test_number():
    for row in cursor.execute('SELECT sum(a_count) FROM test_counts'):
        print(row[0])
        return row[0]
