# Discord libraries
import discord
from discord.ext import commands

class Admin_Only(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def not_admin(self, ctx):
        '''Returns true if author of message is NOT an admin'''
        if not ctx.author.guild_permissions.administrator:
            await ctx.send( "Only admins can use this command." )
            return True
        return False

    @commands.command()
    async def killbot(self, ctx ):
        '''/killbot.\tMakes bot offline. The bot won't recognize commands anymore.
        Does not remove any cache data, use with caution.'''
        if await self.not_admin(ctx): return
        await ctx.send( "Goodbye" )
        print( "Killing the bot." )
        await self.bot.logout()
