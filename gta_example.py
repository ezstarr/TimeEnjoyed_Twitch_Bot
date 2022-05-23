
import sqlite3

connection = sqlite3.connect("gta.db")
cursor = connection.cursor()

cursor.execute("create table gta (release_year integer, release_name text, city text)")

def add_count(word_count):
    word_count += 1
    print(word_count)

cute_count = 0

add_count(cute_count)
add_count(cute_count)


release_list = [
    (1997, "Grand Theft Auto", "state of New Guernsey"),
    (1999, "Grand Theft Auto 2", "Anywhere, USA"),
    (2001, "Grand Theft Auto III", "Liberty City"),
    (2002, "Grand Theft Auto: Vice City", "Vice City"),
    (2004, "Grand Theft Auto: San Andreas", "state of San Andreas"),
    (2008, "Grand Theft Auto IV", "Liberty City"),
    (2013, "Grand Theft Auto V", "Los Santos")
]
cursor.executemany("insert into gta values (?,?,?)", release_list)

# print database rows
for row in cursor.execute("select * from gta"):
    print(row)

# separator print
print("*********************************")
# print specific rows
cursor.execute("select * from gta where city=:c", {"c": "Liberty City"})
gta_search = cursor.fetchall()
print(gta_search)

connection.close()

"""
If I want the bot to act as a counter(for example store the number of times a command has been used, ie: "!yawn", "streamer has yawned 29 times"), I imagine I need to store the data in a database. Thinking to use SQLite3.
Is this possible? 
"""

"""
Hi again! So... I want the bot to act as a counter (for example store the number 
of times a command has been used, ie: "!yawn", "streamer has yawned 29 times"), 
I imagine I need to store the data in a database. 
I'm creating a new module with the counter code to create a database. """