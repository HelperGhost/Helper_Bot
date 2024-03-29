from discord.ext import commands
import discord
import os
import dotenv

dotenv.load_dotenv()
token = os.getenv("TOKEN")

class Bot(commands.Bot):
    def __init__(self, intents: discord.Intents, **kwargs):
        self.prefix = "h!"
        super().__init__(command_prefix=commands.when_mentioned_or(self.prefix, self.prefix.upper()), intents=intents, **kwargs)

    async def setup_hook(self):
        for file in os.listdir("cogs"):
            try:
                if not file.endswith(".py"):
                    return
                if file == "__init__.py":
                    return
                cog = file[:-3]
                await self.load_extension(f"cogs.{cog}")
            except Exception as e:
                print(f"Failed to load {cog} due to {e.__class__.__name__}: {e}")

    async def on_ready(self):
        await self.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="Your Mom S2!"))
        print(f"Logged on as {self.user}.")
        await self.tree.sync()

intents = discord.Intents.all()
bot = Bot(intents=intents)

bot.remove_command("help")

bot.run(token)
