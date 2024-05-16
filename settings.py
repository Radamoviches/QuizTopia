import psycopg2
import database
import re
from tkinter import filedialog

"""
+Class to handle database operations related to user's data
+"""

class Settings:
    """
+    Constructor for the Settings class.
+
+    Args:
+        user_id (int): User identifier
+        conn (psycopg2 connection object): Database connection
+        table_name (str): Name of the table to perform operations on
+    """
    def __init__(self, user_id, conn, table_name):
        self.user_id = user_id
        self.conn = conn
        self.table_name = table_name

    """
+    Add a question to the database
+
+    Args:
+        data (tk.StringVar): Variable holding the text to be inserted into the database
+        success_label (tk.Label): Label to display success/failure message
+    """
    def add_question_to_db(self, data, success_label):
        text = data.get()
        tuple_data = tuple(re.split(r',\s*|\s*,', text))

        try : 
            # Insert data into the database
            database.insert_data_general(self.conn, self.user_id, self.table_name, tuple_data)
            # Set the label text to success message
            success_label.config(text="Question added successfully!", foreground="green")
        except (Exception, psycopg2.Error) as error: 
            # Set the label text to error message
            success_label.config(text="Something went wrong ;(", foreground="red")
        
        data.set("")

        def clear_success_message():
            # Clear the success message after 3 seconds
            success_label.config(text="")
        
        # Set the callback to clear the success message
        success_label.after(3000, clear_success_message)

    """
+    Delete a question from the database
+
+    Args:
+        data (tk.StringVar): Variable holding the text to be deleted from the database
+        success_label (tk.Label): Label to display success/failure message
+    """
    def delete_question_from_db(self, data, success_label):
        text = data.get()

        try: 
            # Delete data from the database
            database.delete_data(self.conn, self.user_id, self.table_name, text)
            # Set the label text to success message
            success_label.config(text="Question deleted successfully!", foreground="green")
        except (Exception, psycopg2.Error) as error:
            # Set the label text to error message
            success_label.config(text="Something went wrong ;(", foreground="red")
        
        data.set("")

        def clear_success_message():
            # Clear the success message after 3 seconds
            success_label.config(text="")

        # Set the callback to clear the success message
        success_label.after(3000, clear_success_message)

    """
+    Print all questions from the database to a file
+
+    Returns:
+        None
+    """
    def print_questions_from_db(self):
        """
+        Save the questions from the database to a text file.

+        Returns:
+            None
+        """
        filename = "questions_list.txt"

        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], initialfile=filename)

        if filepath:
            cursor = self.conn.cursor()
            query = f"SELECT * FROM {self.table_name} WHERE user_id = {self.user_id}"
            query = f"SELECT * FROM {self.table_name} WhERE user_id = {self.user_id}"
            cursor.execute(query)
            questions = cursor.fetchall()
    
            with open(filepath, 'w') as file:
                for question in questions:
                    file.write(question[2] + ', ' + question[3] + '\n')

