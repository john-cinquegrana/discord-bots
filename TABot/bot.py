# Discord based files
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='$')

@bot.command()
async def setTAchannel(ctx):
    channel_list = ctx.message.channel_mentions
    if( len(channel_list) > 1 ):
        await ctx.send("Err: Please only mention one voice channel in your command.")
        return
    elif( len(channel_list) < 1):
        await ctx.send("Err: Please mention a voic channel in your command.")
        return
    # Invariant, channel_list contains the mention of a single channel
    chan = channel_list[0] #Type discord.abc.GuildChannel
    await ctx.send("Setting the TA channel to be " + chan.name + ".")

@bot.command()
async def setup(ctx):
    await ctx.send( "Setting up TA-office hours organization." )