# Imoprt the following libraries to make the bot.
import discord 
from discord.ext import bridge, commands
import os # import os for the import token from .env file
import dotenv # import .env to to use your token

intents = discord.Intents.all()

dotenv.load_dotenv() # now load the .evn file
token = str(os.getenv("TOKEN")) # now import your token
custom_prefix = 'h!'
Helper = bridge.Bot(command_prefix=commands.when_mentioned_or(custom_prefix, custom_prefix.upper()), intents=intents)

# This prints in terminal that the bot is online
@Helper.event
async def on_ready():
    await Helper.change_presence(status=discord.Status.online, activity=discord.Game("Minecraft!"))
    print(f"Logged in as {Helper.user}.")

@Helper.event
async def on_message(message):
    introduction_channel = 1234567890 # Your introduction channel id
    if message.channel.id == introduction_channel:
        await message.add_reaction('🙋‍♀️')
    polls_channel = 1234567890 # Your polls channel id
    if message.channel.id == polls_channel:
        await message.add_reaction('👍')
        await message.add_reaction('👎')

    await Helper.process_commands(message)

@Helper.event
async def on_member_join(ctx):
    member_role_name = "Member"
    member_role = discord.utils.get(ctx.guild.roles, name=member_role_name)
    await ctx.add_roles(member_role)

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
