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

class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help", color=0x1fe2f3, description="Here are the available commands:")
        embed.set_author(name=f"@{Helper.user}", icon_url=f"{Helper.user.avatar}")
        embed.set_thumbnail(url=f"{Helper.user.avatar}")

        prefix = self.context.clean_prefix

        # Modify this part to change 'No Category' appearance
        no_category_commands = mapping.pop(None, None)  # Remove 'No Category' from mapping
        if no_category_commands:
            command_names = list({f"`{c.qualified_name}`" if hasattr(c, 'qualified_name') else "`Unnamed Command`" for c in no_category_commands})
            if command_names:
                embed.add_field(name="**Miscellaneous:**", value=", ".join(command_names), inline=False)

        for cog, commands in mapping.items():
            command_names = list({f"`{c.qualified_name}`" if hasattr(c, 'qualified_name') else "`Unnamed Command`" for c in commands})
            if command_names:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=f"**{cog_name}:**", value=", ".join(command_names), inline=False)

        embed.set_footer(text=f"Use {prefix}help [command] for more details on a specific command.")

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_error_message(self, error):
        embed = discord.Embed(title="Error!", description=error, color=discord.Color.red())
        channel = self.get_destination()

        await channel.send(embed=embed)

    async def send_command_help(self, command):
      embed = discord.Embed(
          title=f"Help for `{self.get_command_signature(command)}`",
          description=command.description or "No help available.",
          color=discord.Color.blue()
      )
      await self.get_destination().send(embed=embed)

Helper.help_command = MyHelp()

# This prints in terminal that the bot is online
@Helper.event
async def on_ready():
    await Helper.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="Your Mom!"))
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
#testing to see if push works