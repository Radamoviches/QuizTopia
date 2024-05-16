"""
+This module contains functions related to multiple choice quiz.
+"""

from tkinter import messagebox 
import database
import queue
import tkinter as tk

"""
+Global variables used throughout the module
+"""

CURRENY_ID_MULTIPLE = 0  # current id of the question being shown
SCORE_MULTIPLE = 0  # score of the user
QUESTION_MULTIPLE = None  # the question being shown
QUEUE_MC = None  # the queue of questions
MODE_TYPE_MC = None  # whether the quiz is using general or user-defined questions

def random_question(conn, user_id, MIN_ID, MAX_ID):
    """
+    Get a random question from the database for the given user.
+
+    :param conn: The database connection
+    :param user_id: The id of the user
+    :param MIN_ID: The minimum id of the questions
+    :param MAX_ID: The maximum id of the questions
+    :return: A tuple containing the question and its choices
+    """
    cur = conn.cursor()
    query = f"SELECT * FROM questions_def WHERE user_id = '{user_id}' AND id BETWEEN %s AND %s ORDER BY RANDOM() LIMIT 1;"
    cur.execute(query, (MIN_ID, MAX_ID))
    question = cur.fetchone()
    cur.close()
    return question

def show_question(conn, MIN_ID, MAX_ID, number_of_questions, choice_buttons_multiple, qs_label, feedback_label, next_button):
    """
+    Display a question and its choices.
+
+    :param conn: The database connection
+    :param MIN_ID: The minimum id of the questions
+    :param MAX_ID: The maximum id of the questions
+    :param number_of_questions: The number of questions
+    :param choice_buttons_multiple: A list of buttons for the choices
+    :param qs_label: A label for the question
+    :param feedback_label: A label for the feedback
+    :param next_button: A button for going to the next question
+    """
    global QUESTION_MULTIPLE
    QUESTION_MULTIPLE = QUEUE_MC.dequeue()
    qs_label.config(text=QUESTION_MULTIPLE[2])
    choices = [QUESTION_MULTIPLE[3], QUESTION_MULTIPLE[4], QUESTION_MULTIPLE[5], QUESTION_MULTIPLE[6]]
    if number_of_questions.get() == 0:
        for i in range(4): 
            choice_buttons_multiple[i].config(text=choices[i], state="disabled")
        return 
    
    for i in range(4): 
        choice_buttons_multiple[i].config(text=choices[i], state="normal")

    feedback_label.config(text="")
    next_button.config(state="disabled")

def check_answer(conn, choice, number_of_questions, score_label, feedback_label, choice_buttons_multiple, next_button):
    """
+    Check the user's answer against the correct answer.
+
+    :param conn: The database connection
+    :param choice: The index of the choice the user chose
+    :param number_of_questions: The number of questions
+    :param score_label: A label for the score
+    :param feedback_label: A label for the feedback
+    :param choice_buttons_multiple: A list of buttons for the choices
+    :param next_button: A button for going to the next question
+    """
    selected_choice = choice_buttons_multiple[choice].cget("text")
    if selected_choice == QUESTION_MULTIPLE[7]:
        global SCORE_MULTIPLE
        SCORE_MULTIPLE += 1
        score_label.config(text="SCORE: {}/{}".format(SCORE_MULTIPLE, number_of_questions.get()))
        feedback_label.config(text="Correct!", foreground="green")
    else:
        feedback_label.config(text="Incorrect!", foreground="red")

    choice_buttons_multiple[0].config(state="disabled")
    choice_buttons_multiple[1].config(state="disabled")
    choice_buttons_multiple[2].config(state="disabled")
    choice_buttons_multiple[3].config(state="disabled")
    next_button.config(state="normal")

def next_question(conn, MIN_ID, MAX_ID, number_of_questions, choice_buttons_multiple, qs_label, feedback_label, next_button):
    """
+    Go to the next question.
+
+    :param conn: The database connection
+    :param MIN_ID: The minimum id of the questions
+    :param MAX_ID: The maximum id of the questions
+    :param number_of_questions: The number of questions
+    :param choice_buttons_multiple: A list of buttons for the choices
+    :param qs_label: A label for the question
+    :param feedback_label: A label for the feedback
+    :param next_button: A button for going to the next question
+    """
    global CURRENY_ID_MULTIPLE 
    CURRENY_ID_MULTIPLE += 1

    if CURRENY_ID_MULTIPLE < number_of_questions.get():
        show_question(conn, MIN_ID, MAX_ID, number_of_questions ,choice_buttons_multiple, qs_label, feedback_label, next_button)
    else:
        messagebox.showinfo("Quiz Completed",
                            "Quiz Completed! Final SCORE: {}/{}".format(SCORE_MULTIPLE, number_of_questions.get()))
        #root.destroy()

def restart_quiz(conn, MIN_ID, MAX_ID, user_id,number_of_questions , qs_label_multiple, score_label_multiple,feedback_label_multiple, choice_buttons_multiple, next_button_multiple):
    """
+    Restart the quiz.
+
+    :param conn: The database connection
+    :param MIN_ID: The minimum id of the questions
+    :param MAX_ID: The maximum id of the questions
+    :param user_id: The id of the user
+    :param number_of_questions: The number of questions
+    :param qs_label_multiple: A label for the question
+    :param score_label_multiple: A label for the score
+    :param feedback_label_multiple: A label for the feedback
+    :param choice_buttons_multiple: A list of buttons for the choices
+    :param next_button_multiple: A button for going to the next question
+    """
    global SCORE_MULTIPLE
    SCORE_MULTIPLE = 0 
    global CURRENY_ID_MULTIPLE
    CURRENY_ID_MULTIPLE = 0

    score_label_multiple.config(text="Score: 0/{}".format(number_of_questions.get()))

    tmp = tk.BooleanVar(value=True)
    if not MODE_TYPE_MC:
        tmp.set(False)

    switch_mode(conn, MIN_ID, MAX_ID, user_id, tmp, number_of_questions)
    show_question(conn, MIN_ID, MAX_ID, number_of_questions ,choice_buttons_multiple, qs_label_multiple, feedback_label_multiple, next_button_multiple)

def switch_mode(conn, MIN_ID, MAX_ID, user_id, mode_var, number_of_questions):
    """
+    Switch between using general or user-defined questions.
+
+    :param conn: The database connection
+    :param MIN_ID: The minimum id of the questions
+    :param MAX_ID: The maximum id of the questions
+    :param user_id: The id of the user
+    :param mode_var: A boolean variable indicating whether to use general or user-defined questions
+    :param number_of_questions: The number of questions
+    """
    global MODE_TYPE_MC
    MODE_TYPE_MC = mode_var.get()

    global QUEUE_MC 
    QUEUE_MC = queue.Queue()

    if MODE_TYPE_MC:
        for i in range(number_of_questions.get()):
            QUEUE_MC.enqueue(random_question(conn, user_id, MIN_ID, MAX_ID))
    elif not MODE_TYPE_MC:
        questions = database.get_data_from_table(conn, user_id, "questions_def")
        for question in questions:
            QUEUE_MC.enqueue(question)
    else:
        QUEUE_MC = None
        print("Queue is emptry!")
   
