# Imoprt the following libraries to make the bot.
import discord 
from discord.ext import commands
import os # import os for the import token from .env file
import datetime # import datetime to have a track of the time for mute and ban
import dotenv # import .env to to use your token

dotenv.load_dotenv() # now load the .evn file
token = str(os.getenv("TOKEN")) # now import your token
Helper = discord.Bot()

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

# This prints in terminal that the bot is online
@Helper.event
async def on_ready():
    print(f"Logged in as {Helper.user}.")

# Welcome message is not working
@Helper.event
async def on_member_join(member):
    await member.send(f"Welcome to the server, {member.mention}!")

# This is the command to show the latency of the bot
@Helper.command(name="ping", description="tells the latency of the bot.")
async def ping(ctx):
    latency = round(Helper.latency * 1000) # This rounds the latency and convert it into ms
    await ctx.respond(f"Pong! I got a ping of {latency}ms.")

#This is for the information about the bot
@Helper.command(name="botinfo", description="tells the bot's info.")
async def botinfo(ctx):
    await ctx.respond(bot_info)

# This is the command to ban people in the server
@Helper.command(name="ban", description="to ban any member in the server")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    try:
        await member.ban()
        await ctx.respond(f'<@{member.id}> has been banned. Reason: {reason}.')
    except discord.Forbidden:
        await ctx.respond("I don't have permission to ban members.") # Bot will respond this if it does not have the permissions
    except discord.HTTPException:
        await ctx.respond("An error occured while processing the ban command.") # Bot will respond this if there is an error while connecting to discord

# Timeout command now works
@Helper.command(name="timeout", descrition="to timeout a member in the server")
@commands.has_permissions(kick_members=True)
async def timeout(ctx, member: discord.Member, time: int = 0, *, reason: str ="No reason provided"):
    duration = datetime.datetime.utcnow() + datetime.timedelta(minutes=time)
    await member.timeout(duration, reason=reason)
    await ctx.respond(f'{member.mention} has been timed out. reason: {reason}.')
    
Helper.run(token)
