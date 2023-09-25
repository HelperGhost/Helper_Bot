import discord
from discord.ext import commands
import time

# Define your intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
intents.presences = True       # Enable presence intent

# Initialize the bot with intents
bot = commands.Bot(command_prefix='!', intents=intents)

muted_role_name = "Muted"
member_role_name = "Member"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# @bot.event
# async def on_member_join(member):
#     member_role = discord.utils.get(member.guild.roles, name = member_role_name)
#     if not member_role:
#         member_role = member.guild.create_role(name = member_role_name)
#     role_given_channel = member.guild.get_channel(1154326721584181329)
#     if role_given_channel:
#         role_given_message = f"Gave {member.name} the {member_role_name} role."
#         await role_given_channel.send(role_given_message)

#     general_channel = member.guild.get_channel(1154323890273779724)
#     if general_channel:
#         general_welcome_message = f"Welcome to the server, {member.mention}!"
#         await general_channel.send(general_welcome_message)

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'Pong! You have a ping of {latency}ms.')

@bot.event
async def on_message(message):
    if message.channel.id == 1155068665818001448:
        emoji = '\U0001F64B\u200D\u2640\uFE0F'
        await message.add_reaction(emoji)

    await bot.process_commands(message)

@bot.command()
@commands.has_permissions(manage_roles = True)
async def mute(ctx, member: discord.Member, duration: int, *, reason="No reason provided."):
    muted_role = discord.utils.get(ctx.guild.roles, name = muted_role_name)
    if not muted_role:
        muted_role = await ctx.guild.creat_role(name = muted_role_name)

    await member.add_roles(muted_role)
    await ctx.send(f"{member.name} has been muted for {duration} minutes. Reason: {reason}")

    time.sleep(duration * 60)

    await member.remove_roles(muted_role)
    await ctx.send(f"{member.name} has been unmuted after {duration} minutes.")

@bot.command()
@commands.has_permissions(manage_roles = True)
async def unmute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name = muted_role_name)
    if muted_role in member.roles:
        await member.remove_roles(muted_role)
        await ctx.send(f"{member.name} has been unmuted.")
    else:
        await ctx.send(f"{member.name} is not muted.")

# Replace 'YOUR_BOT_TOKEN' with your bot token
bot.run('MTE1NTQ2NjYxOTExNjYwMTQwNg.GXpwL_.vbwHi3c1bVrwbmjeSpAwpro9qQD-aaEgyBtHoY')
