
"""
+This script is a login form for the QuizTopia application.
+
+The form includes a username and password input, and buttons for logging in and signing up.
+When the user successfully logs in, their username is stored in the global variable USER_ID
+and a boolean flag, LOGIN_KEY, is set to True. When the user closes the window, the
+function close_window is called to check if the user has logged in. If not, the window is
+not closed.
+
+The signup function creates a new window with inputs for username and password, and a button
+to submit the signup form. The signup_submit function is called when the button is clicked,
+and it checks if the username already exists and if the password is at least 8 characters
+long. If both conditions are met, a new user is added to the database and the window is
+closed.
+"""

import tkinter
from tkinter import messagebox
import database
import psycopg2

LOGIN_KEY = False
USER_ID = None


window = tkinter.Tk()
window.title("Login form")
window.geometry('780x430')
window.configure(bg='#333333')

conn = database.create_user_database()

def close_window():
    """
+    Check if the user has logged in and return True if they have, False otherwise.
+    """
    global LOGIN_KEY
    global USER_ID
    if LOGIN_KEY:
        return True
    else:
        return False    
   

def login():
    """
+    Check if the user's username and password are correct.
+    If they are, set the global variable USER_ID to the user's id and LOGIN_KEY to True.
+    """
    user = database.search_user(conn, username_entry.get())
    if username_entry.get()==user[1] and password_entry.get()==user[2]:
        messagebox.showinfo(title="Login Success", message="You successfully logged in.")
        global LOGIN_KEY
        LOGIN_KEY = True
        global USER_ID
        USER_ID = user[0]
        window.destroy()
    else:  
        messagebox.showerror(title="Error", message="Invalid login.")


def signup_submit(user, password, window):
    """
+    Submit the signup form.
+    Check if the username already exists and if the password is at least 8 characters long.
+    If both conditions are met, add a new user to the database and close the window.
+    """
    username_local = user.get()
    password_local = password.get()
    if len(password_local) < 8: 
        messagebox.showerror(title="Error", message="Password must be at least 8 characters long.")
        return
    if search_user(conn, username_local) is not None:
        messagebox.showerror(title="Error", message="Username already exists.")
        return
    
    database.create_user(conn, username_local, password_local)

    window.destroy()

def search_user(conn, username):
    """
+    Search for a user in the database.
+    """
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
        user = cursor.fetchone()
        return user
    except (Exception, psycopg2.Error) as error:
        print("Error:", error)

def signup():
    """
    Create a new window for signing up.
    """
    # Destroy the login window
    window.destroy()

    # Create a new sign-up window
    signup_window = tkinter.Tk()
    signup_window.geometry('780x430')
    signup_window.configure(bg='#333333')
    signup_window.title("Sign up form")

    # Creating widgets for the sign-up window
    signup_label = tkinter.Label(
        signup_window, text="Sign Up", bg='#333333', fg="#FF3399", font=("Arial", 30))
    signup_username_label = tkinter.Label(
        signup_window, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    signup_username_entry = tkinter.Entry(signup_window, font=("Arial", 16))
    signup_password_label = tkinter.Label(
        signup_window, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    signup_password_entry = tkinter.Entry(signup_window, show="*", font=("Arial", 16))
    submit_button = tkinter.Button(
        signup_window, text="Submit", command=lambda: signup_submit(signup_username_entry, signup_password_entry, signup_window), font=("Arial", 16),
        bg="#FF3399", fg="#FFFFFF", activebackground="#FFFFFF", activeforeground="#FF3399"
    )
    # You may want to add more widgets like a button for submission and additional fields

    # Placing widgets on the screen
    signup_label.pack(pady=20)
    signup_username_label.pack()
    signup_username_entry.pack(pady=10)
    signup_password_label.pack()
    signup_password_entry.pack(pady=10)
    submit_button.pack(pady=20)

    # Start the event loop for the sign-up window
    signup_window.mainloop()



frame = tkinter.Frame(bg='#333333')

# Creating widgets
login_label = tkinter.Label(
    frame, text="Login", bg='#333333', fg="#FF3399", font=("Arial", 30))
username_label = tkinter.Label(
    frame, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
username_entry = tkinter.Entry(frame, font=("Arial", 16))
password_entry = tkinter.Entry(frame, show="*", font=("Arial", 16))
password_label = tkinter.Label(
    frame, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
login_button = tkinter.Button(
    frame, text="Login", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=login)
signup_button = tkinter.Button(
    frame, text="Sign up", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=signup
)

# Placing widgets on the screen
login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1, pady=20)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1, pady=20)
login_button.grid(row=3, column=0, columnspan=2, pady=30)
signup_button.grid(row=4, column=0, columnspan=2, pady=10)
frame.pack()

window.mainloop()
