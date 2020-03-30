# Discord Bots
### By John A. V. Cinquegrana
The first three folders are their own seperate bots as described below. The folder labeled "path_additions" contains cmd (windows) commands for running the bots. More information on everything below.
> All attempts are work-in-progress.
Nothing has reached a releasable state yet.
## Johnny-Bot
This was my first attempt at making a bot. It is the lowest level of bot, based completely in javascript. I based it off of the article [How to make a Discord bot](https://www.digitaltrends.com/gaming/how-to-make-a-discord-bot/) on the Digital Trends online newsletter. There are slight changes but it is almost in entirety just the blueprint they had given in the article.
About an hour into creation I had the though "Someone surely made an API for this already." This lead to me stopping the creation of this bot, and creating the second bot. I have a single file named auth.json hidden from this project for purpose of token protection, you'd require that file as the article describes.
## Johnny-pyBot
This is my second attempt at a bot. This bot uses the [discord.py](https://discordpy.readthedocs.io/en/latest/index.html) python library for easy additions. The library is amazing, check it out if you have any questions. 
### Using the pyBot
#### File requirements
The pybot first and foremost requires an 'info.json' folder. A sample file is given below. Don't give anyone access to this json folder as it holds your bot key.

{  
	"token": "your token here",  
	"file-paths": {  
		"responses": "bot-responses.txt",  
		"facts": "facts.txt",  
		"notes": "notes.txt",  
		"quotes": "quotes.txt"  
	},  
	"ydl_opts": {  
		"format": "bestaudio/best",  
		"postprocessors": [  
			{  
				"key": "FFmpegExtractAudio",  
				"preferredcodec": "mp3",  
				"preferredquality": "192"  
			}  
		]  
	},  
	"var": {  
		"volume": 0.2  
	}  
}  

The text files mentioned in the 'info.json' file should also exist. As of now the code may err if they don't exist, however in some cases it may create them instead of erring (Update to be fixed soon so that none of them err). The volume field is a float 0-1 that indicates how load music is played. It can be set by the 'volume' command.
#### Bot commands
This is directly copied from the /help command of the bot   
##### Music:   
  clearqueue    
  leave      leaves the voice channel, doesn't clear queue   
  mychannel  returns the current voice channel your sitting in   
  pause      Pauses the current song for replay   
  play       Plays a specific youtube video's audio by its URL   
  queue      Prints out the current queue of songs in order   
  resume     Resumes a song that was previously paused.  
  skip       Skips the current song and plays the next song in the queue. 
  volume     Sets the server-wide volume of the bot. (Float value from 0 - 10)   
​##### No Category:   
  addnote    /addnote <title> <note>. Adds a certain note into the dictionary.   
  addquote   Adds a quote to the collection of the bot, stored in a text file   
  getfact    Gets a random fact from the bots stored collection   
  getnote    Returns the note from the dictionary indicated by title   
  getquote   Gets a random quote from the bots stored collection   
  help       Shows this message   
  killbot    Kills the bot, and makes him offline   
  removenote Removes the note given by the specific title   
  roll       Gives a random number between 1 and the inputed number   
  speak      Makes the bot say a random thing   
### Known errors with Johnny-pyBot
If you are downloading a youtube video that is very large, the bot may timeout enough that it calls the on_ready function in the middle of downloading when a new command is run. This has the bot attempt to delete the song as it is downloading it. Keep the songs you are downloading under thirty minutes, and this shouldn't happen.
## TABot
Outside of discord I'm currently a Teacher's Assistant at Stevens Institute of Technology. Due to the coronovirus all classes went online. This bot was created with the purpose of managing students in and out of a voice channel, with a residing TA or professor, with organization and efficiency. The bot is no where near finished, it's barely even started.
I hope to add the functionality of queing students for a spot in the TA's voice chat, moving students in and out, and providing a proper suite of commands for organization of these effects.
Currently, the bot does basically nothing.
## Path_additions
In order for any of these cmd files to work you need to add them to your PATH variable. Honestly they're all very simple, I'm just lazy and don't like typing out long commands more than a few times.
'run_bot' this .cmd file just runs the bot in it's own cmd window. Close the window (or ctrl+c the process) to stop the bot from running.
If you're having issues knowing when the bot is running or not, and you're on windows, run the command 'tasklist | findstr "python.exe"'. If you see a process named "python.exe" running, it is most likely your bot. It might be any other python process however, and I don't know how to tell what python file the process is running.