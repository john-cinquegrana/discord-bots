# Discord based files
import discord
from discord.ext import commands

# Python base libraries
import random
import json

# Personally written Cogs
import voice
import text_manip
import admin

bot = commands.Bot(command_prefix='/')

# Adding in all the cogs


music_cog = voice.Music( bot )
text_cog = text_manip.Text( bot )
admin_cog = admin.Admin_Only( bot )

bot.add_cog( music_cog )
bot.add_cog( text_cog )
bot.add_cog( admin_cog )

@bot.event
async def on_ready():
    music_cog.clear_song_data()
    await music_cog.leave_channel()
    print('Bot has alived.')

# General commands not within any cogs
@bot.command()
async def roll(ctx, arg: int):
    '''Gives a random number between 1 and the inputed number'''
    if (arg <= 1 or arg > 100 ):
        await ctx.send( "Please enter a number between 2 and 100 (inclusive).")
    else:
        await ctx.send( "You rolled " + str( random.randint(1, arg) ) + "!" )

async def post_command( ctx ):
    rand = random.randint(0,100)
    if rand > 95:
        await ctx.send( text_manip.get_bot_response() )
    elif rand > 93:
        await ctx.send( "Did you know that " + text_manip.get_fact() )
    elif rand > 91:
        await ctx.send( "You guys are so funny. Remember when we said " + text_manip.get_quote() )

bot.after_invoke( coro = post_command )

# Read the token from private files so you buggers can't steal it anymore
with open( "info.json") as json_file:
    json_data = json.load( json_file )
bot.run( json_data[ 'token' ] )
