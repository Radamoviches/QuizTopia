import tkinter as tk
from tkinter import messagebox


def get_sets(conn, user_id):
    """
+    Retrieves all flashcard sets belonging to a user
+
+    Args:
+        conn (object): a database connection object
+        user_id (int): the id of the user whose sets are to be retrieved
+
+    Returns:
+        dict: a dictionary of sets (name: id)
+    """
    cursor = conn.cursor()

    # Execite SQL query to fetch all flashcard sets
    cursor.execute('''
        SELECT id, name FROM flashcard_sets WHERE user_id = %s
        ''', (user_id,))

    rows = cursor.fetchall()
    sets = {row[1]: row[0] for row in rows}  # Create a dictionary of sets (name: id)
    sets = {row[1]: row[0] for row in rows} # Create a dictionary of sets (name: id)

    return sets


def create_set(conn, user_id, name):
    cursor = conn.cursor()

    # Insert the set name into flashcard_sets table

    cursor.execute(f"INSERT INTO flashcard_sets (user_id, name) VALUES (%s, %s)", (user_id, name))
    set_id = cursor.lastrowid
    conn.commit()

    return set_id

# Function to add a flashcard to the database

def create_card(conn, user_id, set_id, word, definition):
    """
+    +    Adds a new flashcard to the database
+    +    
+    +    Args:
+    +        conn: a database connection object
+    +        user_id: the id of the user who owns the flashcard
+    +        set_id: the id of the flashcard set where the card belongs
+    +        word: the word to be stored in the flashcard
+    +        definition: the definition of the word in the flashcard
+    +    
+    +    Returns:
+    +        The id of the newly inserted card
+    +    """
    cursor = conn.cursor()

    # Execute SQL query to insert a new flashcard into the database
    cursor.execute('''
        INSERT INTO flashcards (user_id, set_id, word, definition)
        VALUES (%s, %s, %s, %s)
    ''', (user_id, set_id, word, definition,))

    # Get the ID of the newly inserted card
    card_id = cursor.lastrowid
    conn.commit()

    return card_id


# Function to retrieve all flashcard sets from the database

# Function to retrieve all flashcards of a specific set
def get_cards(conn, user_id, set_id):
    """
+    Retrieves all flashcards of a specific set
+
+    Args:
+        conn (object): a database connection object
+        user_id (int): the id of the user who owns the cards
+        set_id (int): the id of the flashcard set whose cards are to be retrieved
+
+    Returns:
+        list: a list of flashcards (word, definition)
+    """
    cursor = conn.cursor()

    cursor.execute('''
        SELECT word, definition FROM flashcards
        WHERE user_id = %s AND set_id = %s
    ''', (user_id, set_id,))

    rows = cursor.fetchall()
    cards = [(row[0], row[1]) for row in rows]  # Create a list of cards (word, definition)
    cards = [(row[0], row[1]) for row in rows] # Create a list of cards (word, definition)

    return cards



# Function to delete a flashcard set from the database
def delete_set(conn, user_id, set_id, sets_combobox, word_label, definition_label):
    """
++    Deletes a flashcard set from the database
++
++    Args:
++        conn: a database connection object
++        user_id: the id of the user who owns the set
++        set_id: the id of the set to be deleted
++        sets_combobox: a tkinter combobox containing all the sets
++        word_label: a tkinter Label to display the word of the current card
++        definition_label: a tkinter Label to display the definition of the current card
++
++    """
    cursor = conn.cursor()

    # Execute SQL query to delete a flashcard set
    cursor.execute('''
        DELETE FROM flashcards WHERE user_id = %s AND set_id = %s
        ''', (user_id, set_id,))
    
    cursor.execute('''
        DELETE FROM flashcard_sets
        WHERE user_id = %s AND id = %s
    ''', (user_id, set_id,))

    conn.commit()
    sets_combobox.set('')
    clear_flashcard_display(word_label, definition_label)
    populate_sets_combobox(conn, user_id, sets_combobox)

    # Clear the CURRENT_CARDS list and reset CARD_INDEX
    global CURRENT_CARDS, CARD_INDEX
    CURRENT_CARDS = []
    CARD_INDEX = 0


# Function to create a new flashcard set
def create_set(conn, user_id, set_name_var, word_var, definition_var, sets_combobox):
    """
++    Creates a new flashcard set
++
++    Args:
++        conn: a database connection object
++        user_id: the id of the user who owns the new set
++        set_name_var: a tkinter StringVar containing the name of the new set
++        word_var: a tkinter StringVar containing the word of the new flashcard
++        definition_var: a tkinter StringVar containing the definition of the new flashcard
++        sets_combobox: a tkinter combobox containing all the sets
++
++    Returns:
++        None
++    """
    set_name = set_name_var.get()
    if set_name:
        if set_name not in get_sets(conn, user_id):
            set_id = create_set(conn, user_id, set_name)
            populate_sets_combobox(conn, user_id, sets_combobox)
            set_name_var.set('')

            # Clear the input fields
            set_name_var.set('')
            word_var.set('')
            definition_var.set('')



def add_word(conn, user_id, set_name_var, sets_combobox, word_var, definition_var):
    """
+    Adds a new flashcard to a set
+
+    Args:
+        conn (object): a database connection object
+        user_id (int): the id of the user who owns the flashcard
+        set_name_var (tkinter StringVar): a tkinter StringVar containing the name of the set
+        sets_combobox (tkinter Combobox): a tkinter combobox containing all the sets
+        word_var (tkinter StringVar): a tkinter StringVar containing the word of the new flashcard
+        definition_var (tkinter StringVar): a tkinter StringVar containing the definition of the new flashcard
+
+    Returns:
+        None
+    """
    set_name = set_name_var.get()
    word = word_var.get()
    definition = definition_var.get()

    if set_name and word and definition:
        # If the set doesn't exist, create it
        print(get_sets(conn, user_id))
        if set_name not in get_sets(conn, user_id):
            set_id = create_set(conn, user_id, set_name)
        else:
            set_id = get_sets(conn, user_id)[set_name]

        # Add the new flashcard to the database
        create_card(conn, user_id, set_id, word, definition)

        # Clear the input fields
        word_var.set('')
        definition_var.set('')

        # Refresh the sets combobox
        populate_sets_combobox(conn, user_id, sets_combobox)


def populate_sets_combobox(conn, user_id, sets_combobox):
    """
+    Populates the sets combobox with the sets of a user
+
+    Args:
+        conn (object): a database connection object
+        user_id (int): the id of the user whose sets are to be retrieved
+        sets_combobox (tkinter Combobox): a tkinter combobox containing all the sets
+
+    Returns:
+        None
+    """
    sets_combobox['values'] = tuple(get_sets(conn, user_id).keys())


# Function to delete a selected flashcard set
def delete_selected_set(conn, user_id, sets_combobox, word_label, definition_label):
    """
+    Deletes a flashcard set from the database
+
+    Args:
+        conn (object): a database connection object
+        user_id (int): the id of the user who owns the set
+        sets_combobox (tkinter Combobox): a tkinter combobox containing all the sets
+        word_label (tkinter Label): a tkinter Label to display the word of the current card
+        definition_label (tkinter Label): a tkinter Label to display the definition of the current card
+
+    """
    set_name = sets_combobox.get()

    if set_name:
        # Ask for confirmation before deleting the set
        result = messagebox.askyesno(
            'Confirmation', f'Are you sure you want to delete the "{set_name}" set?'
        )

        if result == tk.YES:
            # Delete the set from the database
            set_id = get_sets(conn, user_id)[set_name]
            delete_set(conn, user_id, set_id, sets_combobox, word_label, definition_label)

            # Refresh the sets combobox
            populate_sets_combobox(conn, user_id, sets_combobox)

            # Clear the current cards list and reset CARD_INDEX
            clear_flashcard_display(word_label, definition_label)



def select_set(conn, user_id, sets_combobox, word_label, definition_label):
    """
+    Selects a flashcard set and displays its cards
+
+    Args:
+        conn (object): a database connection object
+        user_id (int): the id of the user who owns the set
+        sets_combobox (tkinter Combobox): a tkinter combobox containing all the sets
+        word_label (tkinter Label): a tkinter Label to display the word of the current card
+        definition_label (tkinter Label): a tkinter Label to display the definition of the current card
+
+    """
    set_name = sets_combobox.get()

    if set_name:
        set_id = get_sets(conn, user_id)[set_name]
        cards = get_cards(conn, user_id, set_id)

        if cards:
            display_flashcards(cards, word_label, definition_label)
        else:
            word_label.config(text="No cards in this set")
            definition_label.config(text='')
    else:
        # Clear the current cards list and reset card index
        global CURRENT_CARDS, CARD_INDEX
        CURRENT_CARDS = []
        CARD_INDEX = 0
        clear_flashcard_display(word_label, definition_label)


def display_flashcards(cards, word_label, definition_label):
    """
+    Displays the given flashcards
+
+    Args:
+        cards (list): the list of flashcards to be displayed
+        word_label (tkinter Label): a tkinter Label to display the word of the current card
+        definition_label (tkinter Label): a tkinter Label to display the definition of the current card
+
+    """
    global CARD_INDEX
    global CURRENT_CARDS

    CARD_INDEX = 0
    CURRENT_CARDS = cards
    
    # Clear the display
    if not cards:
        clear_flashcard_display(word_label, definition_label)
    else:
        show_card(word_label, definition_label)
    
    show_card(word_label, definition_label)


def clear_flashcard_display(word_label, definition_label):
    """
+    Clears the display of the flashcards
+
+    Args:
+        word_label (tkinter Label): a tkinter Label to display the word of the current card
+        definition_label (tkinter Label): a tkinter Label to display the definition of the current card
+
+    """
    word_label.config(text='')
    definition_label.config(text='')


# Function to display the current flashcards word

def show_card(word_label, definition_label):
    """
++    Displays the word of the current flashcard and clears the definition label
+
++    Args:
++        word_label (tkinter Label): a tkinter Label to display the word of the current card
++        definition_label (tkinter Label): a tkinter Label to display the definition of the current card
++
++    """
    global CARD_INDEX
    global CURRENT_CARDS

    if CURRENT_CARDS:
        if 0 <= CARD_INDEX < len(CURRENT_CARDS):
            word, _ = CURRENT_CARDS[CARD_INDEX]
            word_label.config(text=word)
            definition_label.config(text='')
        else:
            clear_flashcard_display(word_label, definition_label)
    else:
        clear_flashcard_display(word_label, definition_label)


# Function to flip the current card and display its definition
def flip_card(definition_label):
    """
++    Flips the current flashcard and displays its definition
+
++    Args:
++        definition_label (tkinter Label): a tkinter Label to display the definition of the current card
++
++    """
    global CARD_INDEX
    global CURRENT_CARDS

    if CURRENT_CARDS:
        _, definition = CURRENT_CARDS[CARD_INDEX]
        definition_label.config(text=definition)


# Function to move to the next card
def next_card(word_label, definition_label):
    """
++    Moves to the next flashcard and displays its word
+
++    Args:
++        word_label (tkinter Label): a tkinter Label to display the word of the current card
++        definition_label (tkinter Label): a tkinter Label to display the definition of the current card
++
++    """
    global CARD_INDEX
    global CURRENT_CARDS

    if CURRENT_CARDS:
        CARD_INDEX = min(CARD_INDEX + 1, len(CURRENT_CARDS) -1)
        show_card(word_label, definition_label)


# Function to move to the previous card
def prev_card(word_label, definition_label):
    """
++    Moves to the previous flashcard and displays its word
+
++    Args:
++        word_label (tkinter Label): a tkinter Label to display the word of the current card
++        definition_label (tkinter Label): a tkinter Label to display the definition of the current card
++
++    """
    global CARD_INDEX
    global CURRENT_CARDS

    if CURRENT_CARDS:
        CARD_INDEX = max(CARD_INDEX - 1, 0)
        show_card(word_label, definition_label)

