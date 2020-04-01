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
        self.cur_song = "None"
        self.clear_song_data()

    # Defining groups of the commands
    @commands.group()
    async def song(self, ctx):
        '''/song <sub>.\tCommand used to interact with songs'''
        if ctx.invoked_subcommand is None:
            await ctx.send("Run '/help song' to see a list of valid subcommands.")

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

    @song.command()
    async def clearqueue(self, ctx):
        '''/song clearqueue.\tClears all song data as a whole.'''
        await ctx.send( "Clearing all song data." )
        self.is_playing = False
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
        if os.path.isfile(old_song) and not (old_song in self.song_queue):
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
            self.cur_song = "None"
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
                if os.path.isfile(new_name):
                    # Delete the new download, and leave the old song there
                    os.remove( name )
                else:
                    # Create the new song path
                    os.rename(name, new_name)
                return new_name

    def play_song(self, ctx, song_path):
        '''Plays a given song by mp3 path, make sure no other song is currently playing
        before calling this function. Use download_song to download the song before
        calling this function to play it.'''
        print( "Playing song: " + song_path)
        voice = self.cur_client()

        self.cur_song = "-".join( song_path.split("/")[1].split("-")[:-1] ) + "\n"
        voice.play(discord.FFmpegPCMAudio(song_path), after=(lambda e: self.pop_song(ctx, song_path, e) ) ) # TODO
        voice.source = discord.PCMVolumeTransformer(voice.source)
        with open( "info.json", "r") as file:
            voice.source.volume = json.load( file )[ "var" ][ "volume" ]

    @song.command()
    async def play(self, ctx, url):
        '''/song play <youtube-url>.\tPlays a specific youtube video's audio by its URL'''
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

    @song.command()
    async def queue(self, ctx):
        '''/song queue.\tPrints out the current queue of songs in order'''
        if not self.song_queue:
            await ctx.send( "Queue is empty" )
            return
        my_embed = discord.Embed(
            title = "Song Queue",
            description = "The songs that are about to play, in order.",
            colour = discord.Colour.magenta()
        )
        song_queue = ""
        song_num = 1
        for song in self.song_queue:
            song_queue += str(song_num) + ". " + "-".join( song.split("/")[1].split("-")[:-1] ) + "\n"
            song_num += 1
        my_embed.add_field( name="Queue", value=song_queue, inline=False )
        await ctx.send( "Here is the queue:", embed=my_embed)

    @song.command()
    async def pause(self, ctx):
        '''/song pause.\tPauses the current song for replay'''
        self.cur_client().pause()
        await ctx.send( "Song has been paused" )

    @song.command()
    async def resume(self, ctx):
        '''/song resume.\tResumes a song that was previously paused. Currently cannot resume after a leave.'''
        if ( self.cur_client().is_paused() ):
            await ctx.send( "Resuming the current song" )
            self.cur_client().resume()

    @song.command()
    async def skip(self, ctx):
        '''/song skip.\tSkips the current song and plays the next song in the queue, if any.'''
        await ctx.send( "Skipping the song" )
        if self.is_connected() and self.is_playing:
            self.cur_client().stop()
            # This calls the after function of the play routine as well
        else:
            await ctx.send( "There's no song to skip." )

    @song.command()
    async def volume(self, ctx, vol: float):
        '''/song volume <float>.\tSets the server-wide volume of the bot. (Float value from 0 - 10)'''
        with open( "info.json", "r" ) as file:
            data = json.load( file )
        data[ "var" ][ "volume" ] = vol / 10
        with open( "info.json", "w" ) as file:
            json.dump( data, file, indent="\t" )
        await ctx.send( "Changed the volume to " + str(vol) + ". Change will take affect next song.")

    @song.command()
    async def curvolume(self, ctx):
        '''/song curvolume.\tDisplays the current server volume. (Float value from 0 - 10)'''
        with open( "info.json", "r" ) as file:
            data = json.load( file )
        await ctx.send( "Current Volume is: " + str(data[ "var" ][ "volume" ]*10) )

    @song.command()
    async def current(self, ctx):
        '''/song current.\tStates the song that is currently playing.'''
        await ctx.send( "Currently playing: " + self.cur_song )

    # Joke commands
    async def not_admin(self, ctx):
        '''Returns true if author of message is NOT an admin'''
        if not ctx.author.guild_permissions.administrator:
            await ctx.send( "Only admins can use this command." )
            return True
        return False



    @song.command()
    async def loop(self, ctx, url: str, num: int):
        '''/song loop <url> <num>.\tLoops the song the given amount of times'''
        if( num < 2 ):
            await ctx.send( "Please pick a higher number" )
            return
        if( not self.is_connected() ): # We are not in a channel, we need to join one
            if not await self.join_channel(ctx):
                await ctx.send( "Cannot play the song, please joing a voice channel.")
                return
        song_path = self.download_song( url )
        if self.is_playing:
            await ctx.send( "Your song has been added to the queue." )
            self.song_queue.append( song_path )
            return
        # We play their song right now
        self.play_song(ctx, song_path)
        print( "Song path is: " + song_path )
        self.is_playing = True
        for i in range(1, num): self.song_queue.append( song_path )




    def cog_unload(self):
        print( "Unloading the voice cog" )
        self.leave_channel()
        self.clear_song_data()
        pass