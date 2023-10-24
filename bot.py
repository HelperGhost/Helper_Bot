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

@Helper.event
async def on_message(message):
    introduction_channel = 1155068665818001448
    if message.channel.id == introduction_channel:
        await message.add_reaction('🙋‍♀️')
    polls_channel = 1161280893877497886
    if message.channel.id == polls_channel:
        await message.add_reaction('👍')
        await message.add_reaction('👎')

    await Helper.process_commands(message)

@Helper.event
async def on_member_join(member):
    mem = 1154350344315338792
    await member.add_role(mem)
    print("DEBUG: Auto Role Stage 1 Passed.")
    chnl = 1154326721584181329
    c = Helper.get_channel(chnl)
    print("DEBUG: Auto Role Stage 2 Passed") # Remove These When Confirmed they work.
    await c.send(f"{member.mention} Got Member Role!")


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
                print(f'{cog} has been loaded')
            except Exception as e:
                print(f"Error loading extension '{cog}': {e}")

# Call the function to load cogs
load_cogs()

Helper.run(token)
