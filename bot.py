# Imoprt the following libraries to make the bot.
import discord 
from discord.ext import commands
import os # import os for the import token from .env file
import datetime # import datetime to have a track of the time for mute and ban
import dotenv # import .env to to use your token
import asyncio

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
muted_role_name = "Muted"

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

# This is the command to timeout people int the server
@Helper.command(name="timeout", descrition="to timeout a member in the server")
@commands.has_permissions(kick_members=True)
async def timeout(ctx, member: discord.Member, time: int = 0, *, reason: str ="No reason provided"):
    duration = datetime.datetime.utcnow() + datetime.timedelta(minutes=time) # Define the time for timeout
    await member.timeout(duration, reason=reason) # Set the time and reason
    await ctx.respond(f'{member.mention} has been timed out. reason: {reason}.')

# This is the command to mute people in the server
@Helper.command(name="mute", description="to mute a member in discord server")
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, time: int = 10, reason: str ="No reason provided"):
    muted_role = discord.utils.get(ctx.guild.roles, name=muted_role_name)
    duration = time * 60
    try:
        if not muted_role:
            muted_role = ctx.guild.create_role(name=muted_role_name)
        
        await member.add_roles(muted_role, reason=reason)
        await ctx.respond(f'{member.name} has been muted for {time} minutes. Reason: {reason}')

        await asyncio.sleep(duration)

        await member.remove_roles(muted_role)
        await ctx.respond(f'{member.mention} has been unmuted after {time} minutes.')
    except discord.Forbidden:
        await ctx.respond("I don't have permission to mute members.") # Bot will respond this if it does not have the permissions
    except discord.HTTPException:
        await ctx.respond("An error occured while processing the mute command.") # Bot will respond this if there is an error while connecting to discord

# This is the command to unmute people in the server
@Helper.command(name="unmute", description="to unmute a member in discord server.")
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member, *, reason: str = "No reason provided"):
    muted_role = discord.utils.get(ctx.guild.roles, name=muted_role_name)
    try:
        if not muted_role:
            await ctx.respond("The Muted role doesn't exist.")
            return
        
        if muted_role not in member.roles:
            ctx.respond(f'{member.name} is not muted.')
            return
        
        await member.remove_roles(muted_role)
        await ctx.respond(f'{member.mention} has been unmuted. Reason: {reason}.')
    except discord.Forbidden:
        await ctx.respond("I don't have permission to unmute members.") # Bot will respond this if it does not have the permissions
    except discord.HTTPException:
        await ctx.respond("An error occured while processing the unmute command.") # Bot will respond this if there is an error while connecting to discord

# This is the command to kick people in the server
@Helper.command(name="kick", description="to kick a member in the discord server.")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason: str = "No reason provided"):
    try:
        await member.kick(reason=reason)
        await ctx.respond(f'<@{member.id}> has been kicked from the server. Reason: {reason}.')
    except discord.Forbidden:
        await ctx.respond("I don't have permission to kick members.") # Bot will respond this if it does not have the permissions
    except discord.HTTPException:
        await ctx.respond("An error occured while processing the kick command.") # Bot will respond this if there is an error while connecting to discord

Helper.run(token)
