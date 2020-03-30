import discord
from discord.ext import commands

import youtube_dl
import os
import json
from functools import partial


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False # True if we are currently playing a song
        self.song_queue = [] # A list of urls for songs
        self.clear_song_data()

    def cur_client(self):
        '''Returns the current voice_client of the bot, or none of not in channel'''
        client_list = self.bot.voice_clients
        if client_list: return client_list[0]
        else:
            return None

    def cur_channel(self):
        '''Returns the voice channel the bot is currently in, or None if not in channel'''
        client = self.cur_client()
        if client:
            return client.cur_channel
        else: return None

    def is_connected(self):
        '''Returns true if the bot is currently in a voice channel'''
        if( self.cur_client() ): return self.cur_client().is_connected()
        else: return False

    async def leave_channel(self):
        '''Commands a bot to leave the current channel. Also stops and deletes any playing music. Leaves the queue intact.'''
        if( self.is_connected() ):
            await self.cur_client().disconnect()

    def clear_song_data(self):
        self.song_queue = [] # Clear all of the queue
        self.is_playing = False
        for file in os.listdir("./songs"):
            if file.endswith(".mp3"):
                os.remove( "./songs/" + file )

    async def join_channel(self, ctx):
        '''Returns true if bot was able to join the channel'''
        voice_activity = ctx.message.author.voice
        # Returns the channel that the user is sitting in, type Optional: VoiceState
        if voice_activity:
            voice_channel = voice_activity.channel
            voice_client = None
            if( voice_channel == self.cur_channel() ): # We are already connected to the voice channel
                await ctx.send( "I'm already in your chanel!" )
                return True
            else: # We are not already connected to the voice channel
                await voice_channel.connect()
                await ctx.send("Joining voice channel: " + voice_channel.name )
                return True
        else: # User is not within a voice channel
            await ctx.send("Please join a voice channel")
            return False

    @commands.command()
    async def clearqueue(self, ctx):
        '''/clearqueue.\tClears all song data as a whole.'''
        await ctx.send( "Clearing all song data." )
        for file in self.song_queue:
            if os.path.isfile(file):
                try:
                    os.remove(file)
                except:
                    print( "Error: could not remove file: " + file )
                    return
        queue = []
        await self.leave_channel()

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
        with open( "info.json" ) as file:
            ydl_opts = json.load( file )[ "ydl_opts" ]

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
        voice = self.cur_client()

        voice.play(discord.FFmpegPCMAudio(song_path), after=(lambda e: self.pop_song(ctx, song_path, e) ) ) # TODO
        voice.source = discord.PCMVolumeTransformer(voice.source)
        with open( "info.json", "r") as file:
            voice.source.volume = json.load( file )[ "var" ][ "volume" ]

    @commands.command()
    async def play(self, ctx, url ):
        '''/play <youtube-url>.\tPlays a specific youtube video's audio by its URL'''
        if( not self.is_connected() ): # We are not in a channel, we need to join one
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
        '''/leave.\t\tForces the bot to leave the voice channel, doesn't clear queue data'''
        await ctx.send( "Goodbye." )
        await self.leave_channel()

    @commands.command()
    async def queue(self, ctx):
        '''/queue.\t\tPrints out the current queue of songs in order'''
        for song in self.song_queue:
            await ctx.send( "Song in queue: " + song.split("/")[1].split("-")[0] )

    @commands.command()
    async def pause(self, ctx):
        '''/pause.\t\tPauses the current song for replay'''
        self.cur_client().pause()
        await ctx.send( "Song has been paused" )

    @commands.command()
    async def resume(self, ctx):
        '''/resume.\tResumes a song that was previously paused. Currently cannot resume after a leave.'''
        if ( self.cur_client().is_paused() ):
            await ctx.send( "Resuming the current song" )
            self.cur_client().resume()

    @commands.command()
    async def skip(self, ctx):
        '''/skip.\t\tSkips the current song and plays the next song in the queue, if any.'''
        await ctx.send( "Skipping the song" )
        if self.is_connected() and self.is_playing:
            self.cur_client().stop()
            # This calls the after function of the play routine as well

    @commands.command()
    async def volume(self, ctx, vol: float):
        '''/volume <float>.\tSets the server-wide volume of the bot. (Float value from 0 - 10)'''
        with open( "info.json", "r" ) as file:
            data = json.load( file )
        data[ "var" ][ "volume" ] = vol / 10
        with open( "info.json", "w" ) as file:
            json.dump( data, file, indent="\t" )
        await ctx.send( "Changed the volume to " + str(vol) + ". Change will take affect next song.")

    def cog_unload(self):
        print( "Unloading the voice cog" )
        self.leave_channel()
        self.clear_song_data()
        pass