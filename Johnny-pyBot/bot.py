# Discord based files
import discord
from discord.ext import commands

# Python base libraries
import random
import json

# Personally written files
import text_manip

# Personally written Cogs
import voice

bot = commands.Bot(command_prefix='/')

# Adding in all the cogs

music_cog = voice.Music(bot)
bot.add_cog( music_cog )

@bot.event
async def on_ready():
    music_cog.clear_song_data()
    await music_cog.leave_channel()
    print('Bot has alived.')

# General commands not within any cogs

@bot.command()
async def killbot(ctx):
    '''Kills the bot, and makes him offline'''
    await bot.logout()

@bot.command()
async def roll(ctx, arg: int):
    '''Gives a random number between 1 and the inputed number'''
    if (arg <= 1 or arg > 100 ):
        await ctx.send( "Please enter a number between 2 and 100 (inclusive).")
    else:
        await ctx.send( "You rolled " + str( random.randint(1, arg) ) + "!" )

@bot.command()
async def speak(ctx):
    '''Makes the bot say a random thing'''
    await ctx.send( text_manip.get_bot_response() )    

@bot.command()
async def addquote(ctx, *, str):
    '''Adds a quote to the collection of the bot, stored in a text file'''
    text_manip.add_quote(str)
    await ctx.send( "Quote added: " + text_manip.get_bot_response() )

@bot.command()
async def getquote(ctx):
    '''Gets a random quote from the bots stored collection'''
    await ctx.send( text_manip.get_quote() )

@bot.command()
async def getfact(ctx):
    '''Gets a random fact from the bots stored collection'''
    await ctx.send( text_manip.get_fact() )

@bot.command()
async def addnote(ctx, *, arg):
    '''/addnote <title> <note>. Adds a certain note into the dictionary.'''
    if "$" in arg:
        (title, note) = arg.split("$")
        if ( len(title) != 0 and len(note) != 0 ):
            await ctx.send( text_manip.add_note(title, note) )
        else:
            await ctx.send("Please enter a non-empty title and note.\nPlease enter a string of the format 'Title$Note'")
    else:
        await ctx.send("Please enter a string of the format 'Title$Note'")

@bot.command()
async def getnote(ctx, title):
    '''Returns the note from the dictionary indicated by title'''
    note = text_manip.get_note( title )
    if (note == ""):
        await ctx.send("Error: title does not correspond to a note")
    else:
        await ctx.send("Note found, it reads:")
        await ctx.send( note )

@bot.command()
async def removenote(ctx, title):
    '''Removes the note given by the specific title'''
    await ctx.send( text_manip.remove_note( title ) )

# Read the token from private files so you buggers can't steal it anymore
with open( "info.json") as json_file:
    json_data = json.load( json_file )
bot.run( json_data[ 'token' ] )
