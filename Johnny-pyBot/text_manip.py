# Discord imports
import discord
from discord.ext import commands

# Standard library imports
import random
import json

# Defining variables for use in the file, and reading them from json
with open( "info.json") as json_file:
    json_data = json.load( json_file )
    path_dict = json_data[ "file-paths" ]

QUOTE_PATH = path_dict[ "quotes" ]
BOT_PATH = path_dict[ "responses" ]
FACT_PATH = path_dict[ "notes" ]
NOTE_PATH = path_dict[ "quotes" ]
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

class Text(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def speak(self, ctx):
        '''/speak.\t\tMakes the bot say a random thing'''
        await ctx.send( get_bot_response() )    

    @commands.command()
    async def addquote(self, ctx, *, str):
        '''/addquote <string: quote>.\tAdds a quote to the collection of the bot, stored in a text file'''
        add_quote(str)
        await ctx.send( "Quote added: " + get_bot_response() )

    @commands.command()
    async def getquote(self, ctx):
        '''/getquote.\t\tGets a random quote from the bots stored collection'''
        await ctx.send( get_quote() )

    @commands.command()
    async def getfact(self, ctx):
        '''/getfact.\t\tGets a random fact from the bots stored collection'''
        await ctx.send( get_fact() )

    @commands.command()
    async def addnote(self, ctx, *, arg):
        '''/addnote <string: title> <string: note>.\tAdds a certain note into the dictionary.'''
        if "$" in arg:
            (title, note) = arg.split("$")
            if ( len(title) != 0 and len(note) != 0 ):
                await ctx.send( add_note(title, note) )
            else:
                await ctx.send("Please enter a non-empty title and note.\nPlease enter a string of the format 'Title$Note'")
        else:
            await ctx.send("Please enter a string of the format 'Title$Note'")

    @commands.command()
    async def getnote(self, ctx, title):
        '''/getnote <string: title>.\tReturns the note from the dictionary indicated by title'''
        note = get_note( title )
        if (note == ""):
            await ctx.send("Error: title does not correspond to a note")
        else:
            await ctx.send("Note found, it reads:")
            await ctx.send( note )

    @commands.command()
    async def removenote(self, ctx, title):
        '''/removenote <string: title>.\tRemoves the note given by the specific title'''
        await ctx.send( remove_note( title ) )