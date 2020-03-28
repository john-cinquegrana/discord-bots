import discord
from discord.ext import commands

class MusicWIP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.cur_channel = None
        self.cur_client = None # discord.VoiceChannel to discord.VoiceClient

    @commands.command()
    async def mychannel(self, ctx):
        '''returns the current voice channel your sitting in'''
        voice_activity = ctx.message.author.voice
        # Returns the channel that the user is sitting in, type Optional: VoiceChannel
        if voice_activity:
            await ctx.send("You are in voice channel: " + voice_activity.channel.name )
        else:
            await ctx.send("Please join a voice channel")


    @commands.command()
    async def play(self, ctx):
        '''plays a given url'''
        if self.cur_client:
            await ctx.send( "I am already in a channel (" + self.cur_channel.name + ")! I can't join another." )
            return
        #End of if statement
        voice_activity = ctx.message.author.voice
        # Returns the channel that the user is sitting in, type Optional: VoiceChannel
        if voice_activity:
            voice_channel = voice_activity.channel
            voice_client = None
            if( voice_channel == self.cur_channel ): # We are already connected to the voice channel
                await ctx.send( "I'm already in your chanel!" )
            else: # We are not already connected to the voice channel
                self.cur_channel = voice_channel
                self.cur_client = await voice_channel.connect()
                await ctx.send("Joining voice channel: " + voice_channel.name )
        else: # User is not within a voice channel
            await ctx.send("Please join a voice channel")

    @commands.command()
    async def leave(self, ctx):
        '''leaves the voice channel'''
        if( self.cur_client ):
            await self.cur_client.disconnect()
            await ctx.send("Disconnected from channel: " + self.cur_channel.name )
            self.cur_channel = None
            self.cur_client = None
        else:
            await ctx.send("I am not currently in a channel")

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name}'.format(member))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member