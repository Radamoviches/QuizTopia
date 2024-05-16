import numpy as np
import matplotlib.pyplot as plt
import time
import random
import string
import database
import math 
import re 
from tkinter import messagebox


""" Constants and definitions
+"""

CURRENT_ID_DEF = 0
SCORE_DEF = 0
UNIQUE_ID = 0
QUESTION_DEF = [] 


""" A node in the hash table
+"""

class Node:
    """ A node in the hash table
+
+    Each node contains a key, a value and a pointer to the next node in the 
+    linked list.
+
+    :param key: The key associated with the value
+    :type key: str
+    :param value: The value associated with the key
+    :type value: any
+    :param next: The next node in the linked list
+    :type next: Node or None
+    """

    def __init__(self, key, value):
        """ Initialize a new node
+
+        :param key: The key associated with the value
+        :type key: str
+        :param value: The value associated with the key
+        :type value: any
+        """
        self.key = key
        self.value = value
        self.next = None


""" A hash table using chaining
+"""

class ChainingHashTable:
    """ A hash table using chaining
+
+    This class implements a hash table using chaining. It uses the polynomial 
+    hash function to map keys to buckets and stores the values in a linked list
+    at each bucket.
+
+    :param capacity: The capacity of the hash table
+    :type capacity: int
+    """

    def __init__(self, capacity=19):
        """ Initialize a new hash table
+
+        :param capacity: The capacity of the hash table
+        :type capacity: int
+        """
        self.capacity = capacity
    def __init__(self):
        self.capacity = 19
        self.size = 0
        self.hash_table = [None for _ in range(self.capacity)]
        self.x = 343
        self.counted_x = [self.x ** k for k in range(8)]
        self.border = 0.5
        self.expansion = 0.6


    """ Hash function
+    """

    def __hash_func(self, key):
        """ Compute the hash value of a key
+
+        This function uses the polynomial hash function to map a key to a bucket
+        in the hash table.
+
+        :param key: The key to be hashed
+        :type key: str
+        :return: The hash value of the key
+        :rtype: int
+        """
        # classical polynomial hash function
        # x = 257
        # str_sum = sum([ord(element) * x ** k for k, element in enumerate(key)])

        # improved polynomial hash function
        # with using counted x
        # which increases speed by 64%
        if len(key) > len(self.counted_x):
            k = len(self.counted_x)
            degrees_to_add = len(key) - len(self.counted_x)
            for i in range(degrees_to_add):
                self.counted_x.append(self.x ** (k + i))

        str_sum = sum([ord(element) * self.counted_x[i] for i, element in enumerate(key)])
        return str_sum % self.capacity


    """ Add a key-value pair to the hash table
+    """

    def add(self, key, value):
        """ Add a key-value pair to the hash table
+
+        :param key: The key to be added
+        :type key: str
+        :param value: The value to be added
+        :type value: any
+        """
        h = self.__hash_func(key)
        cell = self.hash_table[h]
        node = Node(key, value)

        if not cell:
            self.hash_table[h] = node
            self.size += 1
        else:
            if self.hash_table[h].key == key:
                self.hash_table[h].value = value
            else:
                node.next = cell
                self.hash_table[h] = node
                self.size += 1

        # Check if the load factor is above the expansion point
        
        load_factor = self.size / self.capacity 
        if load_factor >= self.expansion:
            self.__expand()




    """
+    Find a key in the hash table and return its value.
+
+    If the key is not found, return "Not found".
+
+    :param key: The key to search for
+    :type key: str
+    :return: The value associated with the key if found, "Not found" otherwise
+    :rtype: str or None
+    """
    def find(self, key):
        result = "Not found"
        h = self.__hash_func(key)
        cell = self.hash_table[h]

        if not cell:
            print(result)
            return result

        while cell:
            if cell.key == key:
                result = cell.value
                break
            cell = cell.next

        print(result)
        return result

    """
+    Get all values associated with a key from the hash table.
+
+    :param key: The key to search for
+    :type key: str
+    :return: A list of values associated with the key if found, or None
+    :rtype: list or None
+    """
    def get(self, key):
        results = []
        h = self.__hash_func(key)
        cell = self.hash_table[h]

        if not cell:
            print("Not found")
            return

        while cell:
            if cell.key == key:
                results.append(cell.value)
            cell = cell.next

        if results:
            print(f"Values for key '{key}': {', '.join(map(str, results))}")
        else:
            print("Not found")

    """
+    Print the contents of the hash table.
+
+    :return: None
+    """
    def print_table(self):
        for i in range(self.capacity):
            print(f"Bucket {i}: ", end="")
            cell = self.hash_table[i]
            while cell:
                print(f"({cell.key}: {cell.value})", end=" -> ")
                cell = cell.next
            print("None")

    """
+    Expand the hash table.
-# Add this method to the ChainingHashTable class

+    This method is called when the load factor of the hash table exceeds
+    a certain threshold. It creates a new hash table with twice the capacity
+    of the current hash table and moves all elements from the old hash
+    table to the new hash table.

+    :return: None
+    """
    def __expand(self):
        self.size = 0
        old_hash_table = self.hash_table
        old_capacity = self.capacity
        self.capacity = self.capacity + int(self.capacity * self.expansion)

        self.hash_table = [None for _ in range(self.capacity)]

        for i in range(old_capacity):
            cur_cell = old_hash_table[i]
            while cur_cell:
                # print(f"Computing hash for {cur_cell.key}: {cur_cell.value}")
                self.add(cur_cell.key, cur_cell.value)
                cur_cell = cur_cell.next




def plot_chaining():
    """
+    Plot the performance of the chaining hash table using a stress test
+
+    This function generates a hash table with 100,000 random key-value pairs
+    and times how long it takes to add, find, and delete each key.
+
+    The results are plotted as a time-vs-step graph.
+
+    :return: None
+    """
    cht = ChainingHashTable()

    # need generate data for best/mean/worst case
    # inp_dict = {
    #     "'": "23",
    #     ":": "14",
    #     "M": "3",
    #     "`": "900",
    #     "s": "12",
    # }
    #
    # standard_x = np.array([5e-5, 10e-5, 15e-5, 20e-5, 25e-5])
    # x = []

    # stress test
    inp_dict = {}
    letters = string.ascii_lowercase
    keys = [''.join(random.choice(letters) for _ in range(12)) for _ in range(100000)]
    values = [i+1 for i in range(100000)]

    for i in range(len(values)):
        inp_dict[keys[i]] = values[i]

    std_x = [1 for i in range(100000)]
    standard_x = np.array(std_x)
    x = []

    for key, value in inp_dict.items():
        start_time = time.time()
        cht.add(key, value)
        x.append(time.time() - start_time)

    for key in inp_dict.keys():
        # start_time = time.time()
        cht.find(key)
        # x.append(time.time() - start_time)

    for key in inp_dict.keys():
        # start_time = time.time()
        cht.delete(key)
        # x.append(time.time() - start_time)

    x = np.array(x)
    print(x)
    plt.plot(x, 'r', standard_x, 'b')
    plt.ylabel("time")
    plt.xlabel("step")
    plt.title("add")
    plt.show()

    # while True:
    #     inp_string = input().split()
    #     command = inp_string[0]
    #     number = inp_string[1]
    #     if command == 'add':
    #         try:
    #             name = inp_string[2]
    #             cht.add(number, name)
    #         except IndexError:
    #             print("You need to type value, try again!")
    #     else:
    #         if command == 'find':
    #             cht.find(number)
    #         elif command == 'del':
   #             cht.delete(number)
    #         else:
    #             print("Bad command!\nType this commands:\nadd, find, del")


def preprocess_text(text):
    """
+    Preprocess a text string
+
+    This function converts the text to lowercase, removes non-alphanumeric
+    characters, and returns the resulting string.
+
+    :param text: The text to preprocess
+    :type text: str
+    :return: The preprocessed text
+    :rtype: str
+    """
    # Convert text to lowercase
    text = text.lower()
    # Remove non-alphanumeric characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

def calculate_cosine_similarity(vec1, vec2):
    """
+    Calculate the cosine similarity between two vectors
+
+    This function calculates the dot product of the two vectors, calculates
+    the magnitudes of the vectors, and then returns the cosine similarity
+    as the dot product divided by the product of the magnitudes.
+
+    :param vec1: The first vector
+    :type vec1: dict
+    :param vec2: The second vector
+    :type vec2: dict
+    :return: The cosine similarity of the two vectors
+    :rtype: float
+    """
    # Calculate dot product
    dot_product = sum(vec1[key] * vec2.get(key, 0) for key in vec1)
    # Calculate magnitudes
    magnitude1 = math.sqrt(sum(val ** 2 for val in vec1.values()))
    magnitude2 = math.sqrt(sum(val ** 2 for val in vec2.values()))
    # Calculate cosine similarity
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    else:
        return dot_product / (magnitude1 * magnitude2)

def vectorize_text(text):
    """
+    Vectorize a text string
+
+    This function splits the text into words, counts the frequency of each word,
+    and returns a dictionary of word frequencies.
+
+    :param text: The text to vectorize
+    :type text: str
+    :return: The vectorized text
+    :rtype: dict
+    """
    # Split text into words
    words = text.split()
    # Count word frequencies
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    return word_freq



def store_data(conn, hash_table, questions):
    """
+    Store the questions into the hash table
+    :param conn: A database connection
+    :type conn: psycopg2 connection
+    :param hash_table: A ChainingHashTable object
+    :type hash_table: ChainingHashTable
+    :param questions: A list of questions
+    :type questions: list of tuples
+    """
    for question in questions:
        hash_table.add(question[2], question[3])


def check_answer(hash_table, user_answer, questions, qs_label, feedback_label, score_label, next_button):
    """
+    Check if the user's answer is correct
+    :param hash_table: A ChainingHashTable object
+    :type hash_table: ChainingHashTable
+    :param user_answer: A tkinter StringVar object
+    :type user_answer: tkinter StringVar
+    :param questions: A list of questions
+    :type questions: list of tuples
+    :param qs_label: A tkinter Label object
+    :type qs_label: tkinter Label
+    :param feedback_label: A tkinter Label object
+    :type feedback_label: tkinter Label
+    :param score_label: A tkinter Label object
+    :type score_label: tkinter Label
+    :param next_button: A tkinter Button object
+    :type next_button: tkinter Button
+    """
    asnwer = user_answer.get()

    user_resposne = preprocess_text(asnwer)
    
    # Get the correct answer from the hash table
    correct_answer = preprocess_text(hash_table.find(questions[CURRENT_ID_DEF][2]))

    # Vectorize the user's response and the correct answer
    user_vec = vectorize_text(user_resposne)
    answer_vec = vectorize_text(correct_answer)

    # Calculate the cosine similarity between the two vectors
    similarity = calculate_cosine_similarity(user_vec, answer_vec)

    # Determine if the answer is correct
    if similarity > 0.2:
        # Increase the score and update the label
        global SCORE_DEF
        SCORE_DEF += 1
        score_label.config(text="Score: {}/{}".format(SCORE_DEF, len(questions)))
        # Print a message to the console
        print("Correct!")
        # Update the feedback label
        feedback_label.config(text="Correct!", foreground="green")
    else:
        # Update the feedback label
        feedback_label.config(text="Incorrect!", foreground="red")
    
    # Enable the next button and reset the user's answer
    next_button.config(state="normal")
    user_answer.set("")


def show_question(hash_table, user_answer, questions, qs_label, feedback_label, score_label, next_button):
    """
+    Shows the current question in the GUI
+    :param hash_table: A ChainingHashTable object
+    :type hash_table: ChainingHashTable
+    :param user_answer: A tkinter StringVar object
+    :type user_answer: tkinter StringVar
+    :param questions: A list of questions
+    :type questions: list of tuples
+    :param qs_label: A tkinter Label object
+    :type qs_label: tkinter Label
+    :param feedback_label: A tkinter Label object
+    :type feedback_label: tkinter Label
+    :param score_label: A tkinter Label object
+    :type score_label: tkinter Label
+    :param next_button: A tkinter Button object
+    :type next_button: tkinter Button
+    """
    qs_label.config(text=questions[CURRENT_ID_DEF][2])
    next_button.config(state="normal")
    score_label.config(text="Score: {}/{}".format(SCORE_DEF, len(questions)))
    #feedback_label.config(text="")

def next_button(hash_table, user_answer, qs_label, feedback_label, score_label, next_button):
    """
+    Shows the next question in the GUI if there are more questions, otherwise shows a message box with the final score and quits the quiz
+    :param hash_table: A ChainingHashTable object
+    :type hash_table: ChainingHashTable
+    :param user_answer: A tkinter StringVar object
+    :type user_answer: tkinter StringVar
+    :param qs_label: A tkinter Label object
+    :type qs_label: tkinter Label
+    :param feedback_label: A tkinter Label object
+    :type feedback_label: tkinter Label
+    :param score_label: A tkinter Label object
+    :type score_label: tkinter Label
+    :param next_button: A tkinter Button object
+    :type next_button: tkinter Button
+    """
    check_answer(hash_table, user_answer,  QUESTION_DEF, qs_label, feedback_label, score_label, next_button)
    global CURRENT_ID_DEF
    CURRENT_ID_DEF += 1

    if CURRENT_ID_DEF < len(QUESTION_DEF):
        show_question(hash_table, user_answer, QUESTION_DEF, qs_label, feedback_label, score_label, next_button)
    else:
        score_label.config(text="Score: {}/{}".format(SCORE_DEF, len(QUESTION_DEF)))
        messagebox.showinfo("Quiz Completed",
                            "Quiz Completed! Final score: {}/{}".format(SCORE_DEF, len(QUESTION_DEF)))
        #root.destroy()


def resatart(conn, user_id, hash_table, number_def_questions,questions, user_answer, qs_label, feedback_label, score_label, next_button):
    """
+    Resets the quiz by setting the current question to the first question, resetting the score, clearing the feedback label and populating the hash table with the questions
+    :param conn: A SQLite connection object
+    :type conn: sqlite3.Connection
+    :param user_id: The user's ID
+    :type user_id: int
+    :param hash_table: A ChainingHashTable object
+    :type hash_table: ChainingHashTable
+    :param number_def_questions: A tkinter IntVar object
+    :type number_def_questions: tkinter.IntVar
+    :param questions: A list of questions
+    :type questions: list of tuples
+    :param user_answer: A tkinter StringVar object
+    :type user_answer: tkinter.StringVar
+    :param qs_label: A tkinter Label object
+    :type qs_label: tkinter.Label
+    :param feedback_label: A tkinter Label object
+    :type feedback_label: tkinter.Label
+    :param score_label: A tkinter Label object
+    :type score_label: tkinter.Label
+    :param next_button: A tkinter Button object
+    :type next_button: tkinter.Button
+    """
    global CURRENT_ID_DEF
    global SCORE_DEF
    CURRENT_ID_DEF = 0
    SCORE_DEF = 0

    global QUESTION_DEF
    QUESTION_DEF = []
    for i in range(number_def_questions.get()):
        QUESTION_DEF.append(questions[i])

    feedback_label.config(text="")
    get_questions_and_store(conn, user_id, hash_table, MIN_ID=1, MAX_ID=2, number_def_questions=number_def_questions, questions=QUESTION_DEF)
    show_question(hash_table, user_answer, QUESTION_DEF, qs_label, feedback_label, score_label, next_button)




def random_question(conn, MIN_ID, MAX_ID):
    """
+    Get a random question from the database between the given IDs
+    :param conn: A SQLite connection object
+    :type conn: sqlite3.Connection
+    :param MIN_ID: The minimum id to consider
+    :type MIN_ID: int
+    :param MAX_ID: The maximum id to consider
+    :type MAX_ID: int
+    :return: A tuple containing the question's id, text, and answer
+    :rtype: tuple of (int, str, str)
+    """
    cur = conn.cursor()
    query = f"SELECT * FROM questions_tf WHERE id BETWEEN %s AND %s ORDER BY RANDOM() LIMIT 1;"
    cur.execute(query, (MIN_ID, MAX_ID))
    question = cur.fetchone()
    cur.close()
    return question


def get_questions_and_store(conn, user_id, hash_table, MIN_ID=None, MAX_ID=None, number_def_questions=None, questions=None):
    """
+    Store the given questions in the hash table
+    :param conn: A SQLite connection object
+    :type conn: sqlite3.Connection
+    :param user_id: The user's id
+    :type user_id: int
+    :param hash_table: A ChainingHashTable object
+    :type hash_table: ChainingHashTable
+    :param MIN_ID: The minimum id of the questions to store (default is None, which means all id are considered)
+    :type MIN_ID: int, optional
+    :param MAX_ID: The maximum id of the questions to store (default is None, which means all id are considered)
+    :type MAX_ID: int, optional
+    :param number_def_questions: The number of questions to store (default is None, which means all questions are stored)
+    :type number_def_questions: int, optional
+    :param questions: The questions to store (default is None, which means all questions from the database are stored)
+    :type questions: list of tuples, optional
+    :return: None
+    :rtype: None
+    """
    #global QUESTION_DEF
    #QUESTION_DEF = database.get_data_from_table(conn, user_id, "questions_user_def")

    for question in questions:
        #hash_table.add(QUESTION_DEF[_][2], QUESTION_DEF[_][3])
        hash_table.add(question[2], question[3])
    #hash_table.print_table()
    #print(number_def_questions)
        
