import random

# Defining variables for use in the file
QUOTE_PATH = 'quotes.txt'
BOT_PATH = 'bot-responses.txt'
FACT_PATH = 'fun-facts.txt'
NOTE_PATH = 'notes.txt'
# NOTE - non of these files can be empty, except for the new-quotes file.

def __get_random_line(file_path): #Private function
    file = open(file_path,"r") #Open the file for reading (type: File_object)
    quote_list = file.readlines() #Gives a list where each element is a quote
    file.close() #Close the file
    return random.choice( quote_list ) #returns a random element from that list

def __append_line(file_path, str):
    file = open(file_path,"a") #Open the file for reading (type: File_object)
    file.write(str + '\n' ) #Append the new line onto the end of the file
    file.close() #Close the file
    # End function

def get_quote():
    return str.strip(__get_random_line( QUOTE_PATH ))

def add_quote(str):
    __append_line( QUOTE_PATH, str)

def get_bot_response():
    return str.strip(__get_random_line( BOT_PATH ))

def add_bot_response(str):
    __append_line( BOT_PATH, str)

def get_fact():
    return str.strip(__get_random_line( FACT_PATH ))

def add_fact(str):
    __append_line( FACT_PATH, str)

def get_note(title):
    '''Returns the note string corresponding to the given title, or an empty string if nothing was found.'''
    file = open(NOTE_PATH,"r") #Open the file for reading (type: File_object)
    line_list = file.readlines() #Gives a list where each element is a quote
    file.close() #Close the file
    for str in line_list:
        if title == str.split("$")[0]: return str.split("$")[1].strip()
    return ""

def line_in_note(line_list, title):
    '''Takes in a list of lines of the form 'title$note' and returns true if the test title is a title'''
    for str in line_list:
        if title == str.split("$")[0]: return True
    return False

def add_note(title, note):
    # Returns a string stating whether or not the add was succesful or not
    file = open(NOTE_PATH,"r") #Open the file for reading (type: File_object)
    line_list = file.readlines() #Gives a list where each element is a quote
    file.close() #Close the file
    if line_in_note(line_list, title):
        return "Error: Duplicate title detected, please enter a distinct note"
    else:
        file = open(NOTE_PATH,"a") #Open the file for reading (type: File_object)
        file.write(title + "$" + note + '\n' )
        file.close() #Close the file
        return "Note succesfully added! Access it with '/getnote " + title + "'."

def remove_note(title):
    file = open(NOTE_PATH,"r") #Open the file for reading (type: File_object)
    line_list = file.readlines() #Gives a list where each element is a quote
    file.close()
    result = "Error: could note remove the title/note."
    for str in line_list:
        if title == str.split("$")[0]:
            line_list.remove(str)
            result = "Succesfully removed the note: " + str.split("$")[1].strip()
    file = open(NOTE_PATH, "w")
    for str in line_list:
        file.write( str )
    file.close() #Close the file
    return result
