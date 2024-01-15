# Imoprt the following libraries to make the bot.
import discord 
from discord.ext import bridge, commands
import os # import os for the import token from .env file
import dotenv # import .env to to use your token

intents = discord.Intents.all()

dotenv.load_dotenv() # now load the .evn file
token = str(os.getenv("TEST_TOKEN")) # now import your token
custom_prefix = 'h!'
Helper = bridge.Bot(command_prefix=commands.when_mentioned_or(custom_prefix, custom_prefix.upper()), intents=intents)

Helper.remove_command("help")

# This prints in terminal that the bot is online
@Helper.event
async def on_ready():
    await Helper.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="Your Mom!"))
    print(f"Logged in as {Helper.user}.")

@Helper.event
async def on_message(message):
    if '<@875208986603958344>' in message.content:
        emoji_name = 'pewpew'
        emoji = discord.utils.get(Helper.emojis, name=emoji_name)
        if emoji:
            await message.add_reaction(emoji)
        else:
            print(f"Emoji '{emoji_name}' not found.")

    await Helper.process_commands(message)

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

load_cogs()

Helper.run(token)
