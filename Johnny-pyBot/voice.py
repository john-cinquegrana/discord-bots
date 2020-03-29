import discord
from discord.ext import commands

import youtube_dl
import os
import asyncio
from functools import partial


class MusicWIP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.cur_channel = None
        self.cur_client = None # discord.VoiceChannel to discord.VoiceClient
        self.is_playing = False # True if we are currently playing a song
        self.song_queue = [] # A list of urls for songs

    def clear_song_data(self):
        self.song_queue = [] # Clear all of the queue
        for file in os.listdir("./songs"):
            if file.endswith(".mp3"):
                os.remove( "./songs/" + file )

    @commands.command()
    async def clearqueue(self, ctx):
        await ctx.send( "Clearing all song data." )
        self.clear_song_data()

    @commands.command()
    async def mychannel(self, ctx):
        '''returns the current voice channel your sitting in'''
        voice_activity = ctx.message.author.voice
        # Returns the channel that the user is sitting in, type Optional: VoiceChannel
        if voice_activity:
            await ctx.send("You are in voice channel: " + voice_activity.channel.name )
        else:
            await ctx.send("Please join a voice channel")

    async def join_channel(self, ctx):
        '''Returns true if bot was able to join the channel'''
        voice_activity = ctx.message.author.voice
        # Returns the channel that the user is sitting in, type Optional: VoiceState
        if voice_activity:
            voice_channel = voice_activity.channel
            voice_client = None
            if( voice_channel == self.cur_channel ): # We are already connected to the voice channel
                await ctx.send( "I'm already in your chanel!" )
                return True
            else: # We are not already connected to the voice channel
                self.cur_channel = voice_channel
                self.cur_client = await voice_channel.connect()
                await ctx.send("Joining voice channel: " + voice_channel.name )
                return True
        else: # User is not within a voice channel
            await ctx.send("Please join a voice channel")
            return False

    async def leave_channel(self):
        if( self.cur_client ):
            await self.cur_client.disconnect()
            self.cur_channel = None
            self.cur_client = None

    @commands.command()
    async def join(self, ctx):
        '''joins a specific voice channel'''
        if self.cur_client:
            await ctx.send( "I am already in a channel (" + self.cur_channel.name + ")! I can't join another." )
            return
        #End of if statement
        await self.join_channel(ctx)

    def pop_song(self, ctx, old_song, e):
        '''Deletes the old song, and plays the next song.
        Does nothing if an error occurs.'''
        print( "Song has ended" )
        if e:
            self.song_queue = []
            print( "An error occured in the song play." )
            return
        # Assuming everything went okay
        if os.path.isfile(old_song):
            try:
                os.remove(old_song)
            except:
                print( "Error: could not remove song file" )
                return
        # Old song has been deleted
        if self.song_queue:
            next_song_path = self.song_queue.pop(0)
            self.play_song( ctx, next_song_path )
        else:
            self.is_playing = False

    def download_song(self, url):
        '''Downloads a song url from youtube, returns the path to the download'''
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                new_name = "songs/" + name
                print( "Renaming song to: " + new_name )
                os.rename(name, new_name)
                return new_name

    def play_song(self, ctx, song_path):
        '''Plays a given song by mp3 path, make sure no other song is currently playing
        before calling this function. Use download_song to download the song before
        calling this function to play it.'''
        print( "Playing song: " + song_path)
        voice = self.cur_client

        voice.play(discord.FFmpegPCMAudio(song_path), after=(lambda e: self.pop_song(ctx, song_path, e) ) ) # TODO
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07

    @commands.command()
    async def play(self, ctx, url ):
        if( not self.cur_client ): # We are not in a channel, we need to join one
            if not await self.join_channel(ctx):
                await ctx.send( "Cannot play the song, please joing a voice channel.")
                return
        if self.is_playing:
            await ctx.send( "Your song has been added to the queue." )
            self.song_queue.append( self.download_song( url ) )
            return
        # We play their song right now
        song_path = self.download_song( url )
        self.play_song(ctx, song_path)
        print( "Song path is: " + song_path )
        self.is_playing = True

    @commands.command()
    async def leave(self, ctx):
        '''leaves the voice channel'''
        await ctx.send( "Leaving your channel." )
        await self.leave_channel()