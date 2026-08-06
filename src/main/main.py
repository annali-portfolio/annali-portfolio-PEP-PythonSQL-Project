import csv
import os
import sqlite3

# Resolve the resources folder relative to this file, so paths work
# no matter what directory the script is run from.
_RESOURCES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'resources')

# Connect to the SQLite in-memory database
conn = sqlite3.connect(':memory:')

# A cursor object to execute SQL commands
cursor = conn.cursor()


def main():

    # users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        userId INTEGER PRIMARY KEY,
                        firstName TEXT,
                        lastName TEXT
                      )'''
                   )

    # callLogs table (with FK to users table)
    cursor.execute('''CREATE TABLE IF NOT EXISTS callLogs (
        callId INTEGER PRIMARY KEY,
        phoneNumber TEXT,
        startTime INTEGER,
        endTime INTEGER,
        direction TEXT,
        userId INTEGER,
        FOREIGN KEY (userId) REFERENCES users(userId)
    )''')

    # You will implement these methods below. They just print TO-DO messages for now.
    load_and_clean_users(os.path.join(_RESOURCES_DIR, 'users.csv'))
    load_and_clean_call_logs(os.path.join(_RESOURCES_DIR, 'callLogs.csv'))
    write_user_analytics(os.path.join(_RESOURCES_DIR, 'userAnalytics.csv'))
    write_ordered_calls(os.path.join(_RESOURCES_DIR, 'orderedCalls.csv'))

    # Helper method that prints the contents of the users and callLogs tables. Uncomment to see data.
    # select_from_users_and_call_logs()

    # Close the cursor and connection. main function ends here.
    cursor.close()
    conn.close()







# TODO: Implement the following 4 functions. The functions must pass the unit tests to complete the project.


# This function will load the users.csv file into the users table, discarding any records with incomplete data
def load_and_clean_users(file_path):

    clean_user_list = []

    with open(file_path, "r") as user_list:
        next(user_list)
        for line in user_list:
            split_line = line.strip().split(',')
            if len(split_line) != 2:
                continue
            if all(item.isalpha() for item in split_line):
                clean_user_list.append(split_line)

    for first_name, last_name in clean_user_list:
        cursor.execute("INSERT INTO users (firstName, lastName) VALUES (?, ?)", (first_name, last_name))


    #print("TODO: load_users")
    


# This function will load the callLogs.csv file into the callLogs table, discarding any records with incomplete data
def load_and_clean_call_logs(file_path):
    
    clean_call_logs = []

    with open(file_path, "r") as call_logs:
        next(call_logs)
        for line in call_logs:
            split_line = line.strip().split(',')
            if len(split_line) != 5:
                continue
            if all(item != "" for item in split_line):
                clean_call_logs.append(split_line)

    for phone_number, start_time, end_time, direction, user_ID in clean_call_logs:
        cursor.execute("INSERT INTO callLogs (phoneNumber, startTime, endTime, direction, userId) VALUES (?, ?, ?, ?, ?)", (phone_number, start_time, end_time, direction, user_ID))


    #print("TODO: load_call_logs")
    





# This function will write analytics data to testUserAnalytics.csv - average call time, and number of calls per user.
# You must save records consisting of each userId, avgDuration, and numCalls
# example: 1,105.0,4 - where 1 is the userId, 105.0 is the avgDuration, and 4 is the numCalls.
def write_user_analytics(csv_file_path):

    cursor.execute("SELECT userID, (endTime - startTime) FROM callLogs")
    call_logs_select_duration = cursor.fetchall()

    total_duration = {}
    call_count = {}

    for user_id, duration in call_logs_select_duration:
        total_duration[user_id] = total_duration.get(user_id, 0) + duration
        call_count[user_id] = call_count.get(user_id, 0) + 1

    avg_duration = {
        user_id : total_duration[user_id] / call_count[user_id]
        for user_id in call_count
    }

    with open(csv_file_path, "a+") as user_analytics:
        user_analytics.write("userId,avgDuration,numCalls\n")
        for user_id in avg_duration:
            user_analytics.write(f"{user_id}, {avg_duration[user_id]}, {call_count[user_id]} \n")


    #print("TODO: write_user_analytics")








# This function will write the callLogs ordered by userId, then start time.
# Then, write the ordered callLogs to orderedCalls.csv
def write_ordered_calls(csv_file_path):

    cursor.execute("""
    SELECT callId, phoneNumber, startTime, endTime, direction, userId FROM callLogs
    ORDER BY userID, startTime
    """)

    ordered_call_logs_select = cursor.fetchall()

    with open(csv_file_path, "a+") as ordered_call_logs_csv:
        ordered_call_logs_csv.write("\n")
        writer = csv.writer(ordered_call_logs_csv)
        writer.writerows(ordered_call_logs_select)
  

    #print("TODO: write_ordered_calls")
    









# No need to touch the functions below!------------------------------------------

# This function is for debugs/validation - uncomment the function invocation in main() to see the data in the database.
def select_from_users_and_call_logs():

    print()
    print("PRINTING DATA FROM USERS")
    print("-------------------------")

    # Select and print users data
    cursor.execute('''SELECT * FROM users''')
    for row in cursor:
        print(row)

    # new line
    print()
    print("PRINTING DATA FROM CALLLOGS")
    print("-------------------------")

    # Select and print callLogs data
    cursor.execute('''SELECT * FROM callLogs''')
    for row in cursor:
        print(row)


def return_cursor():
    return cursor


if __name__ == '__main__':
    main()