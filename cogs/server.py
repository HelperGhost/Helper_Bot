from discord.ext import commands
import discord
from discord import File
import os
import dotenv
from pymongo import MongoClient
from easy_pil import Editor, Font, load_image_async

dotenv.load_dotenv()
uri = str(os.getenv("MONGO"))

client = MongoClient(uri)
db = client["Main"]

class Server(commands.Cog):
    """The tasks of all Server will be done here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        collection = db["welcomer"]

        data = collection.find_one({"_id": member.guild.id})

        if not data:
            return
        
        channel = self.bot.get_channel(data["channel"])

        if not channel:
            return
        
        background = Editor("asset/welcomer_background.png")
        profile_picture = await load_image_async(str(member.avatar.url))

        profile = Editor(profile_picture).resize((150, 150)).circle_image()
        text = Font.poppins(size=50, variant="bold")

        text_small = Font.poppins(size=20, variant="light")

        background.paste(profile, (325, 90))
        background.ellipse((355, 90), 150, 150, outline="white", stroke_width=5)

        background.text((400, 260), f"Welcome {member.name}#{member.discriminator}", color="white", font=text, align="center")
        background.text((400, 325), f"Have a good day in {member.guild.name}", color="white", font=text_small, align="center")

        file = File(fp=background.image_bytes, filename="image.png")
        
        await channel.send(f"Welcome to the server, {member.mention}!", file=file)

async def setup(bot):
    await bot.add_cog(Server(bot))
    