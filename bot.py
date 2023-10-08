# Imoprt the following libraries to make the bot.
import discord 
from discord.ext import commands
import os # import os for the import token from .env file
import datetime # import datetime to have a track of the time for mute and ban
import dotenv # import .env to to use your token
import asyncio

dotenv.load_dotenv() # now load the .evn file
token = str(os.getenv("TOKEN")) # now import your token
Helper = commands.Bot()

# This is the place for all variables I have
bot_info = '''
👻 Name: Helper#8515
👻 Nickname: Helper
👻 Age: I am a ghost, I don't have an age. I am beyond the realm of the living, bro.
👻 Gender: Ghost
👻 Nationality: Ghost UK (Boo-rish)
👻 Hobbies: Haunting Discord servers 👻👾
👻 Likes: ☕ Coffee and 🎶 Music
👻 Dislikes: Scammers 🚫

👻 Description:
Hey there, mortal souls! 👋 This is my discord bot, Helper#8515, here to assist and haunt in equal measure! 👻✨ Crafted by the ethereal being known as no_gaming_01, with a massive spectral contribution from .wuid. Together, we're here to make your Discord experience otherworldly! 💀👻👾
'''

# Welcome message is not working
@Helper.event
async def on_member_join(member: discord.Member):
    await member.send(f"Welcome to the server, {member.mention}!")

# This is the command to show the latency of the bot
@Helper.slash_command(name="ping", description="tells the latency of the bot.")
async def ping(ctx):
    latency = round(Helper.latency * 1000) # This rounds the latency and convert it into ms
    await ctx.respond(f"Pong! I got a ping of {latency}ms.")

#This is for the information about the bot
@Helper.slash_command(name="botinfo", description="tells the bot's info.")
async def botinfo(ctx):
    await ctx.respond(bot_info)

# This prints in terminal that the bot is online
@Helper.event
async def on_ready():
    print(f"Logged in as {Helper.user}.")

# Define a function to load cogs from the 'Cogs' directory
def load_cogs():
    for filename in os.listdir('./Cogs'):
        if filename.endswith('.py'):
            cog = filename[:-3]  # Remove the '.py' extension
            try:
                Helper.load_extension(f'Cogs.{cog}')
            except Exception as e:
                print(f"Error loading extension '{cog}': {e}")

# Call the function to load cogs
load_cogs()

Helper.run(token)