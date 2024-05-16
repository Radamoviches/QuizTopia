
"""
+Functions for the True or False Quiz
+"""

import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style
import database
import queue



# Global variables
SCORE = 0  # Score of the user
CURRENT_ID = 0  # Current question id
QUESTION = None  # Current question
MODE_TYPE = False  # True if True or False mode, False if User defined mode
QUEUE = queue.Queue()  # Queue of questions



def random_question(conn, user_id, MIN_ID, MAX_ID) -> tuple:
    """
+    Get a random question from the database for the user.
+
+    Args:
+        conn (psycopg2 connection object): Database connection
+        user_id (int): User id
+        MIN_ID (int): Minimum id of the questions
+        MAX_ID (int): Maximum id of the questions
+
+    Returns:
+        tuple: A tuple containing the question id, question, and answer
+    """
def random_question(conn, user_id, MIN_ID, MAX_ID):
    cur = conn.cursor()
    query = f"SELECT * FROM questions_tf WHERE user_id = '{user_id}' AND id BETWEEN %s AND %s ORDER BY RANDOM() LIMIT 1;"
    cur.execute(query, (MIN_ID, MAX_ID))
    question = cur.fetchone()
    cur.close()
    return question


def show_question(conn, MIN_ID, MAX_ID, number_tf_questions, qs_label, feedback_label, choice_buttons, next_button):
    """
+    Show a question to the user.
+
+    Args:
+        conn (psycopg2 connection object): Database connection
+        MIN_ID (int): Minimum id of the questions
+        MAX_ID (int): Maximum id of the questions
+        number_tf_questions (tk.IntVar): Number of questions in the quiz
+        qs_label (tk.Label): Label to show the question text
+        feedback_label (tk.Label): Label to show the feedback
+        choice_buttons (list of tk.Button): Two buttons to choose True or False
+        next_button (tk.Button): Button to go to the next question
+    """
    global QUESTION
    QUESTION = QUEUE.dequeue()
    qs_label.config(text=QUESTION[2])

    if number_tf_questions.get() == 0:
        choice_buttons[0].config(text="True", state="disabled")
        choice_buttons[1].config(text="False", state="disabled")
        return 

    choice_buttons[0].config(text="True", state="normal")
    choice_buttons[1].config(text="False", state="normal")
    
    feedback_label.config(text="")
    next_button.config(state="disabled")


def check_answer(conn, choice, number_tf_questions, score_label, feedback_label, choice_buttons, next_button):
    """
+    Check if the user's answer is correct.
+
+    Args:
+        conn (psycopg2 connection object): Database connection
+        choice (int): Index of the chosen button (0 for True, 1 for False)
+        number_tf_questions (tk.IntVar): Number of questions in the quiz
+        score_label (tk.Label): Label to show the score
+        feedback_label (tk.Label): Label to show the feedback
+        choice_buttons (list of tk.Button): Two buttons to choose True or False
+        next_button (tk.Button): Button to go to the next question
+    """
def check_answer(conn, choice, number_tf_questions,score_label, feedback_label, choice_buttons, next_button):
    selected_choice = choice_buttons[choice].cget("text")

    if selected_choice == QUESTION[3]:
        global SCORE
        SCORE += 1
        score_label.config(text="Score: {}/{}".format(SCORE, number_tf_questions.get()))
        feedback_label.config(text="Correct!", foreground="green")
    else:
        feedback_label.config(text="Incorrect!", foreground="red")

    choice_buttons[0].config(state="disabled")
    choice_buttons[1].config(state="disabled")
    next_button.config(state="normal")


def next_question(conn, MIN_ID, MAX_ID, number_tf_questions, qs_label, feedback_label, choice_buttons, next_button):
    """
+    Go to the next question.
+
+    Args:
+        conn (psycopg2 connection object): Database connection
+        MIN_ID (int): Minimum id of the questions
+        MAX_ID (int): Maximum id of the questions
+        number_tf_questions (tk.IntVar): Number of questions in the quiz
+        qs_label (tk.Label): Label to show the question text
+        feedback_label (tk.Label): Label to show the feedback
+        choice_buttons (list of tk.Button): Two buttons to choose True or False
+        next_button (tk.Button): Button to go to the next question
+    """
    global CURRENT_ID 
    CURRENT_ID += 1

    if CURRENT_ID < number_tf_questions.get():
        show_question(conn, MIN_ID, MAX_ID, number_tf_questions, qs_label, feedback_label, choice_buttons, next_button)
    else:
        messagebox.showinfo("Quiz Completed",
                            "Quiz Completed! Final score: {}/{}".format(SCORE, number_tf_questions.get()))
        #root.destroy()


def restart_quiz(conn, MIN_ID, MAX_ID, user_id, number_tf_questions, qs_label, score_label, feedback_label, choice_buttons, next_button):
    """
+    Restart the quiz.
+
+    Args:
+        conn (psycopg2 connection object): Database connection
+        MIN_ID (int): Minimum id of the questions
+        MAX_ID (int): Maximum id of the questions
+        user_id (int): User id
+        number_tf_questions (tk.IntVar): Number of questions in the quiz
+        qs_label (tk.Label): Label to show the question text
+        score_label (tk.Label): Label to show the score
+        feedback_label (tk.Label): Label to show the feedback
+        choice_buttons (list of tk.Button): Two buttons to choose True or False
+        next_button (tk.Button): Button to go to the next question
+    """
    global SCORE
    SCORE = 0
    global CURRENT_ID
    CURRENT_ID = 0
    score_label.config(text="Score: 0/{}".format(number_tf_questions.get()))

    tmp = tk.BooleanVar(value=True)

    if not MODE_TYPE: 
        tmp.set(False)
    switch_mode(conn, MIN_ID, MAX_ID, user_id, tmp, number_tf_questions)
    show_question(conn, MIN_ID, MAX_ID, number_tf_questions, qs_label, feedback_label, choice_buttons, next_button)



def switch_mode(conn, MIN_ID, MAX_ID , user_id, mode_var, number_tf_questions=0):
    """
+    Switch between True or False and User defined modes.
+
+    Args:
+        conn (psycopg2 connection object): Database connection
+        MIN_ID (int): Minimum id of the questions
+        MAX_ID (int): Maximum id of the questions
+        user_id (int): User id
+        mode_var (tk.BooleanVar): Variable to indicate whether to use True or False mode or User defined mode
+        number_tf_questions (int, optional): Number of questions in the quiz. Defaults to 0.
    """
    global MODE_TYPE
    MODE_TYPE = mode_var.get()
    global QUEUE
    QUEUE = queue.Queue()

    if MODE_TYPE:
        for i in range(number_tf_questions.get()):
            QUEUE.enqueue(random_question(conn, user_id ,MIN_ID, MAX_ID))
    elif not MODE_TYPE:
        questions = database.get_data_from_table(conn, user_id, "questions_tf")
        for question in questions:
            QUEUE.enqueue(question)
    else: 
        QUEUE = None
        print("Queue is empty!")
        print("Queue is emptry!")

