# Imoprt the following libraries to make the bot.
import discord
from discord.ext import commands
import os
import datetime
import dotenv

dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))
Helper = discord.Bot()

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

@Helper.event
async def on_ready():
    print(f"Logged in as {Helper.user}.")

@Helper.event
async def on_member_join(member):
    await member.send(f"Welcome to the server, {member.mention}!")

@Helper.command(name="ping", description="tells the latency of the bot.")
async def ping(ctx):
    latency = round(Helper.latency * 1000)
    await ctx.respond(f"Pong! I got a ping of {latency}ms.")

@Helper.command(name="botinfo", description="tells the bot's info.")
async def botinfo(ctx):
    await ctx.respond(bot_info)

@Helper.command(name="ban", description="to ban any member in the server")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    try:
        await member.ban()
        await ctx.respond(f'{member.mention} has been banned. Reason: {reason}.')
    except discord.Forbidden:
        await ctx.respond("I don't have permission to ban members.")
    except discord.HTTPException:
        await ctx.respond("An error occured while processing the ban command.")

# Timeout command still not working.
@Helper.command(name="timeout", descrition="to timeout any member in the server for minutes")
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member, time: int = 0, *, reason: str ="No reason provided"):
    duration = datetime.timedelta(minutes=time)
    await member.timeout_for(time, reason)
    await ctx.respond(f'{member.mention} has been timed out. reason: {reason}.')

Helper.run(token)
