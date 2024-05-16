
"""
+This module contains the main GUI application for the Quiz App.
+
+The GUI is split into several tabs:
+    - Create Set: where users can create a new flashcard set.
+    - Select Set: where users can select an existing flashcard set.
+    - Learn Mode: where users can view and learn the words in a selected set.
+    - True or False Quiz: a True or False quiz that uses questions from the database.
+
+The application uses several other modules:
+    - flash: contains functions for working with flashcards.
+    - tf_quiz: contains functions for the True or False quiz.
+    - multiple_quiz: contains functions for a multiple choice quiz.
+    - hash_quiz: contains functions for a quiz where questions are hashed.
+    - settings: contains functions for setting up the application.
+    - login: contains functions for handling user login and authentication.
+
+The application uses several databases:
+    - flashcards.db: a SQLite database for storing flashcard sets.
+    - questions_tf.db: a SQLite database for storing True or False questions.
+    - questions_def.db: a SQLite database for storing user defined questions.
+    - user_def.db: a SQLite database for storing user defined questions.
+"""

import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
import database
import tf_quiz
import settings
import multiple_quiz
import flash
import hash_quiz
import login


CURRENT_USER_ID = None

if __name__ == '__main__':
    # Connect to the SQLite databases and create tables
    # Connect to the SQLite database and create tables
    #conn_flash = sqlite3.connect('flashcards.db')
    #database.create_tables(conn_flash)

    flag = login.close_window()
    

    CURRENT_USER_ID = login.USER_ID

    if not flag:
        exit()

    conn_flash = database.create_test_table()
    conn_tf = database.connector_db_tf()
    conn_multiple = database.connector_db_def()
    conn_def = database.connector_db_user_def()


    # Create the main GUI window
    root = tk.Tk()
    root.title('Quiz App')
    root.geometry('780x430')

    # Apply styling to the GUI elements
    style = Style(theme='superhero')
    style.configure('TLabel', font=('TkDefaultFont', 18))
    style.configure('TButton', font=('TkDefaultFont', 16))

    # Set up variables for storing user input
    set_name_var = tk.StringVar()
    word_var = tk.StringVar()
    definition_var = tk.StringVar()

    # Create a notebook widget to manage tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    # Create the "Create Set" tab and its content
    create_set_frame = ttk.Frame(notebook)
    notebook.add(create_set_frame, text='Create Set')

    # Label and Entry widgets for entering set name, word and definition
    ttk.Label(create_set_frame, text='Set Name:').pack(padx=5, pady=5)
    ttk.Entry(create_set_frame, textvariable=set_name_var, width=30).pack(padx=5, pady=5)

    ttk.Label(create_set_frame, text='Word:').pack(padx=5, pady=5)
    ttk.Entry(create_set_frame, textvariable=word_var, width=30).pack(padx=5, pady=5)

    ttk.Label(create_set_frame, text='Definition:').pack(padx=5, pady=5)
    ttk.Entry(create_set_frame, textvariable=definition_var, width=30).pack(padx=5, pady=5)

    # Button to add a word to the set 
    ttk.Button(create_set_frame, text='Add Word', command=lambda : flash.add_word(conn_flash, CURRENT_USER_ID, set_name_var, sets_combobox, word_var, definition_var)).pack(padx=5, pady=10)
    
    # Button to save the set 
    ttk.Button(create_set_frame, text='Save Set', command=lambda : flash.create_set(conn_flash, CURRENT_USER_ID, set_name_var, word_var, definition_var, sets_combobox)).pack(padx=5, pady=10)

    # Create the "Select Set" tab and its content
    select_set_frame = ttk.Frame(notebook)
    notebook.add(select_set_frame, text="Select Set")

    # Combobox widget for selecting existing flashcard sets
    sets_combobox = ttk.Combobox(select_set_frame, state='readonly')
    sets_combobox.pack(padx=5, pady=40)

    # Button to select a set 
    ttk.Button(select_set_frame, text='Select Set', command=lambda : flash.select_set(conn_flash, CURRENT_USER_ID, sets_combobox, word_label, definition_label)).pack(padx=5, pady=5)

    # Button to delete a set 
    ttk.Button(select_set_frame, text='Delete Set', command=lambda: flash.delete_selected_set(conn_flash, CURRENT_USER_ID, sets_combobox, word_label, definition_label)).pack(padx=5, pady=5)

    # Create the "Learn mode" tab and its content
    flashcards_frame = ttk.Frame(notebook)
    notebook.add(flashcards_frame, text='Learn Mode')

    # Initialize variables for tracking card index and current cards
    card_index = 0
    current_tabs = []

    # Label to display the word on flashcards
    word_label = ttk.Label(flashcards_frame, text='', font=('TkDefaultFont', 24))
    word_label.pack(padx=5, pady=40)

    # Label to display the definition on flashcards
    definition_label = ttk.Label(flashcards_frame, text='')
    definition_label.pack(padx=5, pady=5)

    # Button to flip the flashcard 
    ttk.Button(flashcards_frame, text='Flip', command=lambda : flash.flip_card( definition_label)).pack(side='left', padx=5, pady=5)

    # Button to view the next flashcard 
    ttk.Button(flashcards_frame, text='Next', command=lambda : flash.next_card(word_label, definition_label)).pack(side='right', padx=5, pady=5)

    # Button to view the previous flashcard 
    ttk.Button(flashcards_frame, text='Previous', command=lambda : flash.prev_card(word_label, definition_label)).pack(side='right', padx=5, pady=5)

    flash.populate_sets_combobox(conn_flash, CURRENT_USER_ID, sets_combobox)



    # Create "True or False" tab and its content 
    # This tab allows the user to select a set of True or False questions and 
    # then start the quiz. The questions and answers are retrieved from the database.
    true_or_false_frame = ttk.Frame(notebook)
    notebook.add(true_or_false_frame, text="TF Quiz")


    # Find the minimum and maximum ids of the questions for the current user in the TF questions table
    result = database.find_min_max(conn_tf, CURRENT_USER_ID,'questions_tf')
    MIN_ID = result[0][0]
    MAX_ID = result[0][1]


    # Initialize a list to store the buttons used for choosing answers
    choice_buttons = []


    # Create a restart button to restart the quiz
    restart_button_tf = ttk.Button(
        true_or_false_frame,
        text="Restart",
        command=lambda : tf_quiz.restart_quiz(conn_tf, MIN_ID, MAX_ID, CURRENT_USER_ID ,number_tf_questions,qs_label, score_label, feedback_label, choice_buttons, next_button),
        state="normal",
        padding=10
    )
    restart_button_tf.pack(pady=10)
    restart_button_tf.place(x=10, y=10)

    # Create a variable to store the number of questions the user wants to answer
    number_tf_questions = tk.IntVar()

    # Create a label and a combobox to allow the user to select the number of questions
    number_tf_questions_label = ttk.Label(
        true_or_false_frame,
        text= "Number of questions",
        padding=10
    )
    number_tf_questions_label.pack(pady=10)
    number_tf_questions_label.place(x=10, y=60)


    amount_of_questions = ttk.Combobox(
        true_or_false_frame,
        textvariable=number_tf_questions,
        state="readonly"
    )
    amount_of_questions.pack(pady=10)
    amount_of_questions.place(x=10, y=100)

    # Set the values of the combobox to all integers from 1 to the number of questions the user has
    
    amount_of_questions['values'] = [*range(1, database.length_table(conn_tf, CURRENT_USER_ID,'questions_tf')[0][0] + 1)]

    # Create a label to display the question
    

    qs_label = ttk.Label(
        true_or_false_frame, 
        anchor="center", 
        wraplength=500, 
        padding=10
    )
    qs_label.pack(pady=10)

    # Create buttons for each possible answer and add them to the choice_buttons list
    
    for i in range(2):
        button = ttk.Button(
            true_or_false_frame,
            command=lambda i=i: tf_quiz.check_answer(conn_tf, i, number_tf_questions ,score_label, feedback_label, choice_buttons, next_button),
            state="disabled"
        )
        button.pack(pady=5)
        choice_buttons.append(button)

    # Create a button to move to the next question
    next_button = ttk.Button(
        true_or_false_frame, 
        text="Next",
        command=lambda : tf_quiz.next_question(conn_tf, MIN_ID, MAX_ID, number_tf_questions ,qs_label, feedback_label, choice_buttons, next_button),
        state="disabled"
    )
    next_button.pack(pady=10)

    # Create a label to display the feedback to the user
    feedback_label = ttk.Label(
        true_or_false_frame, 
        anchor="center",
        padding=10
    )
    feedback_label.pack(pady=10)


    # Create a label to display the score
    score_label = ttk.Label(
        true_or_false_frame, 
        text="Score: 0/{}".format(number_tf_questions.get()),
        anchor= "center",
        padding=10
    )
    score_label.pack(pady=10)

    # Create a checkbox to switch between random mode and normal mode
    check_tf_var = tk.BooleanVar()

    # Create a button to switch between random mode and normal mode
    mode_button_tf = ttk.Checkbutton(
        true_or_false_frame,
        text="Random mode",
        variable=check_tf_var,
        onvalue=True,
        offvalue=False,
        command= lambda: tf_quiz.switch_mode(conn_tf, MIN_ID, MAX_ID, CURRENT_USER_ID, check_tf_var, number_tf_questions)
    )
    mode_button_tf.pack(pady=10)
    mode_button_tf.place(x=10, y=150)

    # Switch to random mode by default
    tf_quiz.switch_mode(conn_tf, MIN_ID, MAX_ID, CURRENT_USER_ID, check_tf_var, number_tf_questions)


    # Create the "Multiple Choice Quiz" tab and its content 
    # 
    # This tab will have a combobox to select the number of questions
    # and a checkbox to switch between random mode and normal mode
    # 
    # The questions will be displayed in a label and the user can select
    # an answer from a set of buttons
    # 
    # The score and feedback will be displayed in labels
    # 
    # The user can restart the quiz or go to the next question
    # 
    
    #Create "Multiple Choice Quiz" tab and its content 

    multiple_choice_frame = ttk.Frame(notebook)
    notebook.add(multiple_choice_frame, text="MC Quiz")

    # Find the min and max id of questions for the current user
    result_multiple = database.find_min_max(conn_multiple, CURRENT_USER_ID,'questions_def')
    MIN_ID_MULTIPLE = result_multiple[0][0]
    MAX_ID_MULTIPLE = result_multiple[0][1]

    # Create a variable to store the number of questions
    amount_questions_mc = tk.IntVar()

    # Create a label and combobox for the number of questions
    number_of_questions_mc_label = ttk.Label(
        multiple_choice_frame,
        text= "Number of questions",
        padding=10
    )
    number_of_questions_mc_label.pack(pady=10)
    number_of_questions_mc_label.place(x=10, y=60)

    amount_questions_mc_label = ttk.Combobox(
        multiple_choice_frame,
        textvariable=amount_questions_mc,
        state="readonly"
    )
    amount_questions_mc_label.pack(pady=10)
    amount_questions_mc_label.place(x=10, y=100)

    # Populate the combobox with the number of questions the user has
    amount_questions_mc_label['values'] = [*range(1, database.length_table(conn_multiple, CURRENT_USER_ID,'questions_def')[0][0] + 1)]

    # Create a variable to store the state of the checkbox
    check_mc_var = tk.BooleanVar()

    # Create a button to switch between random mode and normal mode
    swtich_button_mc = ttk.Checkbutton(
        multiple_choice_frame,
        text="Random mode",
        variable=check_mc_var,
        onvalue=True,
        offvalue=False,
        command= lambda: multiple_quiz.switch_mode(conn_multiple, MIN_ID_MULTIPLE, MAX_ID_MULTIPLE, CURRENT_USER_ID, check_mc_var, amount_questions_mc)
    )
    swtich_button_mc.pack(pady=10)
    swtich_button_mc.place(x=10, y=150)


    # Create a label to display the questions
    qs_label_multiple = ttk.Label(
        multiple_choice_frame,
        anchor="center",
        wraplength=500,
        padding=10
    )
    qs_label_multiple.pack(pady=10)

    # Create a list to store the buttons for each question
    choice_buttons_multiple = []

    # Create the buttons for each question
    for i in range(4): 
        button_multiple = ttk.Button(
            multiple_choice_frame,
            command=lambda i=i: multiple_quiz.check_answer(conn_multiple, i, amount_questions_mc ,score_label_multiple, feedback_label_multiple, choice_buttons_multiple, next_button_multiple)

        )
        button_multiple.pack(pady=5)
        choice_buttons_multiple.append(button_multiple)
    
    
    # Create a label to display the feedback
    feedback_label_multiple = ttk.Label(
        multiple_choice_frame,
        anchor="center",
        padding=10
    )
    feedback_label_multiple.pack(pady=10)


    # Create a label to display the score
    score_label_multiple = ttk.Label(
        multiple_choice_frame,
        text="Score: 0/{}".format(database.length_table(conn_multiple, CURRENT_USER_ID,'questions_def')[0][0]),
        anchor="center",
        padding=10
    )
    score_label_multiple.pack(pady=10)

    # Create a button to go to the next question
    next_button_multiple = ttk.Button(
        multiple_choice_frame,
        text="Next",
        command= lambda : multiple_quiz.next_question(conn_multiple, MIN_ID_MULTIPLE, MAX_ID_MULTIPLE, amount_questions_mc, choice_buttons_multiple, qs_label_multiple, feedback_label_multiple, next_button_multiple),
        state="disabled"
    )
    next_button_multiple.pack(pady=10)
    next_button_multiple.place(x=600, y=300)

    # Create a button to restart the quiz
    restart_button_mc = ttk.Button(
        multiple_choice_frame,
        text="Restart",
        command=lambda : multiple_quiz.restart_quiz(conn_multiple, MIN_ID_MULTIPLE, MAX_ID_MULTIPLE, CURRENT_USER_ID,amount_questions_mc, qs_label_multiple, score_label_multiple ,feedback_label_multiple, choice_buttons_multiple, next_button_multiple),
        state="normal",
        padding=10
    )
    restart_button_mc.pack(pady=10)
    restart_button_mc.place(x=10, y=10)


    #multiple_quiz.show_question(conn_multiple, MIN_ID_MULTIPLE, MAX_ID_MULTIPLE, choice_buttons_multiple, qs_label_multiple, feedback_label_multiple, next_button_multiple)


    # definition questions 
    # - a tab in the main window for a hash quiz using questions defined by the user
    # - the user can select the number of questions they want to use from the questions they have defined
    # - the user can restart the quiz or go to the next question

    #definition questions 
    definition_frame = ttk.Frame(notebook)
    notebook.add(definition_frame, text="Definition Quiz")

    # variable to store the user's answer
    answer_var = tk.StringVar()

    # get all questions defined by the user
    questions_tmp = database.get_data_from_table(conn_def, CURRENT_USER_ID, "questions_user_def")

    # find the min and max id of the questions defined by the user
    results = database.find_min_max(conn_def, CURRENT_USER_ID,'questions_user_def')
    number_of_def_questions = tk.IntVar()
    MIN_ID_DEF = results[0][0]
    MAX_ID_DEF = results[0][1]

    # store the questions in a variable
    questions = questions_tmp

    # label to display the question
    question_label_def = ttk.Label(
        definition_frame,
        anchor="center",
        padding=10
    )
    question_label_def.pack(pady=10)

    # entry for the user to enter their answer
    answer_entry_def = ttk.Entry(
        definition_frame,
        textvariable=answer_var, 
        width=20
    )
    answer_entry_def.pack(pady=10)

    # button to go to the next question
    next_button_def = ttk.Button(
        definition_frame,
        text="Next",
        command= lambda : hash_quiz.next_button(hash_table, answer_var, question_label_def, feedback_label_def, score_label_def ,next_button_def), 
        padding=10,
        state="disabled"
    )
    next_button_def.pack(pady=10)

    # label to display the score
    score_label_def = ttk.Label(
        definition_frame,
        text="Score: 0/{}".format(len(questions)),
        anchor="center",
        padding=10
    )
    score_label_def.pack(pady=10)

    # label to display the feedback
    feedback_label_def = ttk.Label(
        definition_frame,
        anchor="center",
        padding=10
    )
    feedback_label_def.pack(pady=10)
    # button to restart the quiz
    restart_button_def = ttk.Button(
        definition_frame,
        text="Restart",
        command=lambda : hash_quiz.resatart(conn_def, CURRENT_USER_ID, hash_table, number_of_def_questions ,questions, answer_var, question_label_def, feedback_label_def, score_label_def ,next_button_def),
        padding=10
    )
    restart_button_def.pack(pady=10)
    restart_button_def.place(x=10, y=10)


    # combobox to select the number of questions to use
    number_def_questions_button = ttk.Combobox(
        definition_frame,
        state="readonly",
        textvariable=number_of_def_questions
    )
    number_def_questions_button.pack(pady=10)
    number_def_questions_button.place(x=10, y=60)


    # merge and delete duplicates in the questions table
    database.merge_and_delete_duplicates(conn_def, CURRENT_USER_ID,'questions_user_def', 'question')

    # populate the combobox with the number of questions the user has defined
    number_def_questions_button['values'] = [*range(1, database.length_table(conn_def, CURRENT_USER_ID,'questions_user_def')[0][0] + 1)]
    
    
    # create a hash table to store the questions
    hash_table = hash_quiz.ChainingHashTable()

    
    #store_data(conn_def, hash_table, questions)
    #test_hash.store_data(conn_def, hash_table, questions)
    #hash_quiz.get_questions_and_store(conn_def, CURRENT_USER_ID, hash_table, MIN_ID_DEF, MAX_ID_DEF, number_of_def_questions, )
    #test_hash.show_question(hash_table, answer_var, questions, question_label_def, feedback_label_def, score_label_def, next_button_def)



    
    # tf settings tab
    tf_settings_frame = ttk.Frame(notebook)
    notebook.add(tf_settings_frame, text="TF Settings")
    tf_settings = settings.Settings(CURRENT_USER_ID, conn_tf, "questions_tf")

    # label to instruct the user how to format the question
    # example: "Are you a robot?", False


    add_label_tf = ttk.Label(
        tf_settings_frame,
        text="Add Question (format example: Are you a robot?, False)",
        anchor="center",
        padding=5
    )
    add_label_tf.pack(pady=5)
    add_label_tf.place(x=10, y=10)

    # entry to enter the question
    # the question should be in the format: question, answer
    # example: "Are you a robot?", False
    question_add_tf = tk.StringVar()
    add_question_entry_tf = ttk.Entry(
        tf_settings_frame,
        textvariable=question_add_tf,
        width=20
    )
    add_question_entry_tf.pack(pady=5)
    add_question_entry_tf.place(x=10, y=60)

    # button to add the question to the database
    add_question_tf = ttk.Button(
        tf_settings_frame,
        text="Add Question",
        command=lambda : tf_settings.add_question_to_db(question_add_tf, success_label_tf),
        padding=5,
        state="normal"
    )
    add_question_tf.pack(pady=5)
    add_question_tf.place(x=10, y=100)


    # label to instruct the user how to format the question to delete
    # example: "Are you a robot?"
    delete_label_tf = ttk.Label(
        tf_settings_frame,
        text="Delete Question(format example: Are you a robot?)",
        anchor="center",
        padding=5
    )
    delete_label_tf.pack(pady=5)
    delete_label_tf.place(x=10, y=150)

    # entry to enter the question to delete
    # the question should be in the format: question
    # example: "Are you a robot?"
    question_delete_tf = tk.StringVar()
    delete_question_entry_tf = ttk.Entry(
        tf_settings_frame,
        textvariable=question_delete_tf,
        width=20
    )
    delete_question_entry_tf.pack(pady=5)
    delete_question_entry_tf.place(x=10, y=200)

    # button to delete the question from the database
    delete_question_tf = ttk.Button(
        tf_settings_frame,
        text="Delete Question",
        command=lambda : tf_settings.delete_question_from_db(question_delete_tf, success_label_tf),
        padding=5,
        state="normal"
    )
    delete_question_tf.pack(pady=5)
    delete_question_tf.place(x=10, y=240)

    # label to show the result of the operations
    success_label_tf = ttk.Label(
        tf_settings_frame,
        text="",
        anchor="center",
        padding=5
    )
    success_label_tf.pack(pady=5)
    success_label_tf.place(x=200, y=280)

    # button to print the questions from the database
    print_question_tf = ttk.Button(
        tf_settings_frame,
        text="Print Question List",
        command=lambda : tf_settings.print_questions_from_db(),
        padding=5,
        state="normal"
    )
    print_question_tf.pack(pady=5)
    print_question_tf.place(x=300, y=340)
    


    # multiple choice settings tab
    # this tab allows the user to add questions to the multiple choice questions database
    # it also allows the user to delete questions from the multiple choice questions database
    # and to print out the list of questions in the database

    mc_settings_frame = ttk.Frame(notebook)
    notebook.add(mc_settings_frame, text="MC Settings")

    settings_multiple = settings.Settings(
        CURRENT_USER_ID,
        conn_multiple,
        "questions_def"
    )
    settings_multiple = settings.Settings(CURRENT_USER_ID, conn_multiple, "questions_def")

    # label to display instructions for adding a question

    add_label_mc = ttk.Label(
        mc_settings_frame,
        text="Add Question (format example: How old are you?, 1, 2, 3, 4, answer)",
        anchor="center",
        padding=5
    )
    add_label_mc.pack(pady=5)
    add_label_mc.place(x=10, y=10)

    # variable to store the text entered in the add question entry
    question_add_mc = tk.StringVar()

    # entry to input the question
    add_question_entry_mc = ttk.Entry(
        mc_settings_frame,
        textvariable=question_add_mc,
        width=20
    )
    add_question_entry_mc.pack(pady=5)
    add_question_entry_mc.place(x=10, y=60)

    # button to add the question to the database
    add_question_mc = ttk.Button(
        mc_settings_frame,
        text="Add Question",
        command=lambda : settings_multiple.add_question_to_db(question_add_mc, success_label_mc),
        padding=5,
        state="normal"
    )
    add_question_mc.pack(pady=5)
    add_question_mc.place(x=10, y=100)

    # label to display the result of the operations
    success_label_mc = ttk.Label(
        mc_settings_frame,
        text="",
        anchor="center",
        padding=5
    )
    success_label_mc.pack(pady=5)
    success_label_mc.place(x=200, y=280)

    # label to display instructions for deleting a question
    delete_label_mc = ttk.Label(
        mc_settings_frame,
        text="Delete Question(format example: How old are you?)",
        anchor="center",
        padding=5
    )
    delete_label_mc.pack(pady=5)
    delete_label_mc.place(x=10, y=150)

    # variable to store the text entered in the delete question entry
    delete_question_mc = tk.StringVar()

    # entry to input the question to delete
    delete_question_entry_mc = ttk.Entry(
        mc_settings_frame,
        textvariable=delete_question_mc,
        width=20
    )
    delete_question_entry_mc.pack(pady=5)
    delete_question_entry_mc.place(x=10, y=200)

    # button to delete the question from the database
    delete_question_mc_button = ttk.Button(
        mc_settings_frame,
        text="Delete Question",
        command=lambda : settings_multiple.delete_question_from_db(delete_question_mc, success_label_mc),
        padding=5,
        state="normal"
    )
    delete_question_mc_button.pack(pady=5)
    delete_question_mc_button.place(x=10, y=240)

    # button to print the questions from the database
    print_question_mc = ttk.Button(
        mc_settings_frame,
        text="Print Question List",
        command=lambda : settings_multiple.print_questions_from_db(),
        padding=5,
        state="normal"
    )
    print_question_mc.pack(pady=5)
    print_question_mc.place(x=300, y=340)



    # definton question settings tab
    # This tab allows the user to add and delete questions for a specific definition
    # It also allows the user to print the questions in the definition

    defintion_settings_frame = ttk.Frame(notebook)
    notebook.add(defintion_settings_frame, text="Defintion Settings")

    definition_settings = settings.Settings(CURRENT_USER_ID, conn_def, "questions_user_def")

    # Label to display instructions for adding a question
    add_label_def = ttk.Label(
        defintion_settings_frame,
        text="Add Question (format example: What is the meaning of life?, answer)",
        anchor="center",
        padding=5
    )
    add_label_def.pack(pady=5)
    add_label_def.place(x=10, y=10)

    # Variable to store the text entered in the add question entry
    question_add_def = tk.StringVar()

    # Entry to input the question
    add_question_entry_def = ttk.Entry(
        defintion_settings_frame,
        textvariable=question_add_def,
        width=20
    )
    add_question_entry_def.pack(pady=5)
    add_question_entry_def.place(x=10, y=60)

    # Button to add the question to the database
    add_question_def = ttk.Button(
        defintion_settings_frame,
        text="Add Question",
        # Lambda function to add the question to the database
        # first argument is the question text, second argument is the success message
        command= lambda : definition_settings.add_question_to_db(question_add_def, success_label_def),
        padding=5,
        state="normal"
    )
    add_question_def.pack(pady=5)
    add_question_def.place(x=10, y=100)

    # Label to display the result of the operations
    success_label_def = ttk.Label(
        defintion_settings_frame,
        text="",
        anchor="center",
        padding=5
    )
    success_label_def.pack(pady=5)
    success_label_def.place(x=200, y=280)

    # Label to display instructions for deleting a question
    delete_label_def = ttk.Label(
        defintion_settings_frame,          
        text="Delete Question(format example: What is the meaning of life?)",
        anchor="center",
        padding=5
    )
    delete_label_def.pack(pady=5)
    delete_label_def.place(x=10, y=150)

    # Variable to store the text entered in the delete question entry
    delete_question_def = tk.StringVar()
    
    # Entry to input the question to delete
    delete_question_entry_def = ttk.Entry(
        defintion_settings_frame,
        textvariable=delete_question_def,
        width=20
    )
    delete_question_entry_def.pack(pady=5)
    delete_question_entry_def.place(x=10, y=200)

    # Button to delete the question from the database
    delete_question_def_button = ttk.Button(
        defintion_settings_frame,
        text="Delete Question",
        # Lambda function to delete the question from the database
        # first argument is the question text, second argument is the success message
        command= lambda : definition_settings.delete_question_from_db(delete_question_def, success_label_def),
        padding=5,
        state="normal"
    )
    delete_question_def_button.pack(pady=5)
    delete_question_def_button.place(x=10, y=240)

    # Button to print the questions from the database
    print_question_def = ttk.Button(
        defintion_settings_frame,
        text="Print Question List",
        # Lambda function to print the questions from the database
        command= lambda : definition_settings.print_questions_from_db(),
        padding=5,
        state="normal"
    )
    print_question_def.pack(pady=5)
    print_question_def.place(x=300, y=340)

    # Main loop
    root.mainloop()
