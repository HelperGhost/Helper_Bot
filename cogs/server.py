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
        welcomer_collection = db["welcomer"]

        welcomer_data = welcomer_collection.find_one({"_id": member.guild.id})

        if not welcomer_data:
            return
        
        channel = self.bot.get_channel(welcomer_data["channel"])

        if not channel:
            return
        
        background = Editor("asset/welcomer_background.jpg")
        profile_picture = await load_image_async(str(member.avatar.url))

        profile = Editor(profile_picture).resize((125, 125)).circle_image()
        text = Font.poppins(size=40, variant="bold")
        text_small = Font.poppins(size=20, variant="light")

        center_x = (background.image.width - profile.image.width) // 2
        center_y = (background.image.height - profile.image.height) // 2 - 40

        background.paste(profile, (center_x, center_y))
        background.ellipse((center_x, center_y), 125, 125, outline="white", stroke_width=5)

        text_x = background.image.width // 2
        text_y = center_y + profile.image.height + 15

        background.text((text_x, text_y), f"Welcome {member.name}#{member.discriminator}", color="white", font=text, align="center")
        background.text((text_x, text_y + 65), f"Have a good day in {member.guild.name}", color="white", font=text_small, align="center")

        file = File(fp=background.image_bytes, filename="image.png")
        
        await channel.send(f"Welcome to the server, {member.mention}!", file=file)

        autorole_collection = db["autorole"]

        autorole_data = autorole_collection.find_one({"_id": member.guild.id})

        if not autorole_data:
            return
        
        role = member.guild.get_role(autorole_data["role"])

        if not role:
            return
        
        await member.add_roles(role)

async def setup(bot):
    await bot.add_cog(Server(bot))
    