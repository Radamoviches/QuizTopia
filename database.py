import psycopg2

def clean_database_table(conn, table_name):
    """
+    Cleans a table in the PostgreSQL database by deleting all records.
+    
+    Args:
+    - conn (psycopg2 connection): Connection object connected to the PostgreSQL database.
+    - table_name (str): Name of the table to clean.
+    
+    Returns:
+    - None
+    """
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_name}")
    print("Database cleaned successfully.")
    conn.commit()
    conn.close()

def delete_data(conn, user_id, table_name, question):
    """
+    Deletes a record from a table in the PostgreSQL database.
+    
+    Args:
+    - conn (psycopg2 connection): Connection object connected to the PostgreSQL database.
+    - user_id (int): User identifier to filter records.
+    - table_name (str): Name of the table to query.
+    - question (str): Question to filter records.
+    
+    Returns:
+    - None
+    """
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_name} WHERE user_id = %s AND question = %s", (user_id, question))
    conn.commit()


def insert_data_general(conn, user_id, table_name, data):
    """
+    Inserts data into a table in the PostgreSQL database.
+    
+    Args:
+    - conn (psycopg2 connection): Connection object connected to the PostgreSQL database.
+    - user_id (int): User identifier to track data.
+    - table_name (str): Name of the table to insert data into.
+    - data (list): List of data to insert.
+    
+    Returns:
+    - None
+    """
    if table_name == "questions_tf":
        """
+        Inserts data into questions_tf table.
+        
+        Args:
+        - conn (psycopg2 connection): Connection object connected to the PostgreSQL database.
+        - user_id (int): User identifier to track data.
+        - data (list): List of data to insert, format: [question, answer]
+        """
        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO {table_name} (user_id, question, answer) VALUES (%s, %s, %s)", (user_id, data[0], data[1]))
        conn.commit()
    elif table_name == "questions_def":
        """
+        Inserts data into questions_def table.
+        
+        Args:
+        - conn (psycopg2 connection): Connection object connected to the PostgreSQL database.
+        - user_id (int): User identifier to track data.
+        - data (list): List of data to insert, format: [question, choice1, choice2, choice3, choice4, answer]
+        """
        cursor = conn.cursor()
        #cursor.execute(f"INSERT INTO {table_name} (user_id, question, choice1, choice2, choice3, choice4, answer) VALUES (%s, %s, %s, %s, %s, %s, %s)", (user_id, data[0], data[1], data[2], data[3], data[4], data[5]))
        cursor.execute(f"INSERT INTO {table_name} (user_id, question, choice1, choice2, choice3, choice4, answer) VALUES (%s, %s, %s, %s, %s, %s, %s)", (user_id, data[0], data[1], data[2], data[3], data[4], data[5]))
        conn.commit()
    elif table_name == "questions_user_def":
        """
+        Inserts data into questions_user_def table.
+        
+        Args:
+        - conn (psycopg2 connection): Connection object connected to the PostgreSQL database.
+        - user_id (int): User identifier to track data.
+        - data (list): List of data to insert, format: [question, answer]
+        """
        cursor = conn.cursor()
        print(user_id, data[0], data[1])
        cursor.execute(f"INSERT INTO {table_name} (user_id, question, answer) VALUES (%s, %s, %s)", (user_id, data[0], data[1]))
        conn.commit()



def search_data(conn, table_name, question):
    """
+    Searches for a given question in a table of the PostgreSQL database.
+
+    Args:
+    - conn (psycopg2 connection): Connection object connected to the PostgreSQL database.
+    - table_name (str): Name of the table to search in.
+    - question (str): Question to search for.
+
+    Returns:
+    - List of rows that match the question in the table. Each row contains the question, user_id, choice1, choice2, choice3, choice4, and answer for a given question.
+    """
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name} WHERE question = '{question}'")
    return cursor.fetchall()

def find_min_max(conn, user_id, table_name):
    """
+    Finds the minimum and maximum id of a given user in a table of the PostgreSQL database.
+
+    Args:
+    - conn (psycopg2 connection): Connection object connected to the PostgreSQL database.
+    - user_id (int): User identifier to filter records.
+    - table_name (str): Name of the table to query.
+
+    Returns:
+    - A tuple containing the minimum and maximum id of the given user in the table.
+    """
def find_min_max(conn, user_id ,table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT MIN(id), MAX(id) FROM {table_name} WHERE user_id = '{user_id}' ")
    return cursor.fetchall()


def length_table(conn, user_id, table_name):
    """
+    Finds the number of records of a given user in a table of the PostgreSQL database.
+
+    Args:
+    - conn (psycopg2 connection): Connection object connected to the PostgreSQL database.
+    - user_id (int): User identifier to filter records.
+    - table_name (str): Name of the table to query.
+
+    Returns:
+    - The number of records of the given user in the table.
+    """
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE user_id = '{user_id}' ")
    return cursor.fetchall()



def connector_db_tf():
    """
++    Connects to the PostgreSQL database and creates the 'questions_tf' table if it does not exist.
++
++    Returns:
++    - A connection object to the PostgreSQL database.
++
++    Raises:
++    - psycopg2.Error: If there is an error connecting to the database or creating the table.
++    """
    try:
        conn = psycopg2.connect(dbname='QuizTopia',
                                user='alex',
                                password='26031998DDvS',
                                host='localhost',
                                port=5432)

        cursor = conn.cursor()

        # Create the 'questions_tf' table if it does not exist
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS questions_tf (id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL ,question VARCHAR(1000), answer VARCHAR(5), FOREIGN KEY (user_id) REFERENCES users(id))"
        )
        conn.commit()

        return conn


    except (Exception, psycopg2.Error) as error:
        print("Error:", error)
        



def connector_db_def():
    """
++    Connects to the PostgreSQL database and creates the 'questions_def' table if it does not exist.
++
++    Returns:
++    - A connection object to the PostgreSQL database.
++
++    Raises:
++    - psycopg2.Error: If there is an error connecting to the database or creating the table.
++    """
    try:
        conn = psycopg2.connect(dbname="QuizTopia",
                                user="alex",
                                password="26031998DDvS",
                                host="localhost",
                                port=5432)
        
        cursor = conn.cursor()
        # Create the 'questions_def' table if it does not exist
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS questions_def (id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL ,question VARCHAR(1000), choice1 VARCHAR(1000), choice2 VARCHAR(1000), choice3 VARCHAR(1000), choice4 VARCHAR(1000), answer VARCHAR(1000), FOREIGN KEY (user_id) REFERENCES users(id))"
        )
        conn.commit()

        return conn 
    
    except (Exception, psycopg2.Error) as error:
        print("Error:", error)

            
def connector_db_user_def():
    """
+    Connects to the PostgreSQL database and creates the 'questions_user_def' table if it does not exist.
+    
+    Returns:
+    - A connection object to the PostgreSQL database.
+    
+    Raises:
+    - psycopg2.Error: If there is an error connecting to the database or creating the table.
+    """
    try:
        conn = psycopg2.connect(dbname="QuizTopia",
                                user="alex",
                                password="26031998DDvS",
                                host="localhost",
                                port=5432)
        
        cursor = conn.cursor()
        # Create the 'questions_user_def' table if it does not exist
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS questions_user_def (id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL ,question VARCHAR(2000), answer VARCHAR(10000), FOREIGN KEY (user_id) REFERENCES users(id))"
        )
        conn.commit()

        return conn

    except (Exception, psycopg2.Error) as error:
        print("Error:", error)



def create_test_table():
    """
+    Connects to the PostgreSQL database and creates the 'flashcard_sets' and 'flashcards' tables if they do not exist.
+    
+    Returns:
+    - A connection object to the PostgreSQL database.
+    
+    Raises:
+    - psycopg2.Error: If there is an error connecting to the database or creating the tables.
+    """
    try:
        conn = psycopg2.connect(dbname="QuizTopia",
                                user="alex",
                                password="26031998DDvS",
                                host="localhost",
                                port=5432)
        cursor = conn.cursor()
        # Create the 'flashcard_sets' table if it does not exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS flashcard_sets (id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL, name TEXT NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id))''')
        
        # Create the 'flashcards' table if it does not exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS flashcards (id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL, set_id INTEGER NOT NULL, word TEXT NOT NULL, definition TEXT NOT NULL, FOREIGN KEY (set_id) REFERENCES flashcard_sets(id), FOREIGN KEY (user_id) REFERENCES users(id))''')
        conn.commit()

        return conn
    
    except (Exception, psycopg2.Error) as error:
        print("Error:", error)



def get_data_from_table(conn, user_id, table_name):
    """
+    Gets all data from a PostgreSQL table for a given user.
+    
+    Args:
+    - conn: psycopg2 connection object connected to the PostgreSQL database.
+    - user_id: User identifier to filter the data.
+    - table_name: Name of the table to query.
+    
+    Returns:
+    - A list of tuples containing the data from the table for the given user.
+    """
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name} WHERE user_id = %s", (user_id,))
    return cursor.fetchall()
    cursor.execute(f"SELECT * FROM {table_name} WHERE user_id = '{user_id}'")
    return cursor.fetchall()  


def merge_and_delete_duplicates(connection, user_id, table_name, field_name):
    """
    Function to merge the 'answer' field of duplicate rows and delete the duplicate rows in a PostgreSQL table.
    
    Args:
    - connection: psycopg2 connection object connected to the PostgreSQL database.
    - user_id: User identifier to ensure we're only merging duplicates for a given user.
    - table_name: Name of the table to search for duplicates.
    - field_name: Name of the field to check for duplicates.
+    
+    Returns:
+    None
+    
+    Raises:
+    - psycopg2.Error: If there is an error merging and deleting duplicates in PostgreSQL.
+    """
    """
+    This function merges the 'answer' field of duplicate rows and deletes the duplicate rows in a PostgreSQL table.
+    It does this by first selecting all rows grouping by the specified field and counting occurrences.
+    Then it fetches rows with duplicate values for the specified field and merges their 'answer' fields.
+    Finally, it updates the first row with the merged 'answer' field and deletes the duplicate rows except the first one.
    """
    try:
        cursor = connection.cursor()
        # Select all rows grouping by the specified field and count occurrences
        query = f"SELECT {field_name}, COUNT(*) FROM {table_name} WHERE user_id = %s GROUP BY {field_name} HAVING COUNT(*) > 1"
        cursor.execute(query, (user_id,))
        duplicate_groups = cursor.fetchall()

        for group in duplicate_groups:
            # Fetch rows with duplicate values for the specified field
            cursor.execute(f"SELECT * FROM {table_name} WHERE {field_name} = %s AND user_id = %s", (group[0], user_id))
            duplicate_rows = cursor.fetchall()

            # Merge the 'answer' field of duplicate rows
            merged_answer = ' '.join([row[3] for row in duplicate_rows])  # Assuming 'answer' is the third column

            # Update the first row with the merged 'answer' field
            cursor.execute(f"UPDATE {table_name} SET answer = %s WHERE id = %s AND user_id = %s", (merged_answer, duplicate_rows[0][0], user_id))

            # Delete duplicate rows except the first one
            for row in duplicate_rows[1:]:
                cursor.execute(f"DELETE FROM {table_name} WHERE id = %s AND user_id = %s", (row[0], user_id))

        connection.commit()
        print("Duplicates merged and deleted successfully.")
        
    except (Exception, psycopg2.Error) as error:
        print("Error while merging and deleting duplicates in PostgreSQL:", error)

    finally:
        if cursor:
            cursor.close()




def create_user_database():
    """
+    Connects to the PostgreSQL database and creates the 'users' table if it does not exist.
+
+    Returns:
+        A connection object to the PostgreSQL database.
+
+    Raises:
+        psycopg2.Error: If there is an error connecting to the database or creating the table.
+    """
    try:
        conn = psycopg2.connect(dbname="QuizTopia",
                                user="alex",
                                password="26031998DDvS",
                                host="localhost",
                                port=5432)

            
        cursor = conn.cursor()
        # Create the 'users' table if it does not exist
        cursor.execute(
                "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL)"
        )
        conn.commit()

        return conn 
    
            
    except (Exception, psycopg2.Error) as error:
        print("Error:", error)

def search_user(conn, username):
    """
+    Searches for a user in the 'users' table of the PostgreSQL database.
+
+    Args:
+        conn: A connection object to the PostgreSQL database.
+        username: The username to search for.
+
+    Returns:
+        A tuple containing the user's id, username, and password if the user is found.
+        Otherwise, returns None.
+
+    Raises:
+        psycopg2.Error: If there is an error searching for the user in the database.
+    """
    cursor = conn.cursor()
    try: 
        # Execute a query to search for the user
        cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
        user = cursor.fetchone()
        return user
    except (Exception, psycopg2.Error) as error:
        print("Error:", error)
    

def create_user(conn, username, password):
    """
+    Creates a user in the 'users' table of the PostgreSQL database.
+
+    Args:
+        conn: A connection object to the PostgreSQL database.
+        username: The username to create.
+        password: The password to create for the user.
+
+    Returns:
+        None
+
+    Raises:
+        psycopg2.Error: If there is an error creating the user in the database.
+    """
    cursor = conn.cursor()
    try:
        # Use parameterized query to prevent SQL injection
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error:", error)
