from discord.ext import commands
import discord
import os
import dotenv
from pymongo import MongoClient
import asyncio

dotenv.load_dotenv()
uri = str(os.getenv("MONGO"))

client = MongoClient(uri)
db = client["Main"]

class Configuration(commands.Cog):
    """The Configuartion Cog."""

    def __init__(self, bot):
        self.bot = bot
        self.emoji = "🔨"

    @commands.hybrid_command(name="setwelcomer", description="Sets the welcomer channel.")
    @commands.has_permissions(administrator=True)
    async def set_welcomer(self, ctx: commands.Context, channel: discord.TextChannel):
        collection = db["welcomer"]
        
        if not channel:
            channel = ctx.channel
        
        collection.update_one(
            {"_id": ctx.guild.id},
            {"$set": {"channel": channel.id}},
            upsert=True
        )

        embed = discord.Embed(
            title="Welcomer Set",
            description=f"The welcomer channel has been set to {channel.mention}.",
            color=0x1fe2f3
        )

        await ctx.send(embed=embed)

    @commands.hybrid_command(name="autorole", description="Sets the autorole.")
    @commands.has_permissions(administrator=True)
    async def autorole(self, ctx: commands.Context, role: discord.Role):
        collection = db["autorole"]

        collection.update_one(
            {"_id": ctx.guild.id},
            {"$set": {"role": role.id}},
            upsert=True
        )

        embed = discord.Embed(
            title="Autorole Set",
            description=f"{role.mention} has been set as autorole.",
            color=0x1fe2f3
        )

        await ctx.send(embed=embed)

    @commands.hybrid_command(name="setlogs", description="Sets the logs channel.")
    @commands.has_permissions(administrator=True)
    async def set_logs(self, ctx: commands.Context):

        collections = {
            "message_logs": "Message Logs",
            "member_logs": "Member Logs",
            "vc_logs": "Voice Channel Logs",
            "server_logs": "Server Logs",
            "misc_logs": "Miscellaneous Logs"
        }

        for collection_name, title in collections.items():
            await ctx.send(f"Please specify {title} channel ID or mention (type `skip` to leave it blank):")

            try:
                message = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60)

                if message.content.lower() == "skip":
                    channel_id = None
                else:
                    channel = await commands.TextChannelConverter().convert(ctx, message.content)
                    channel_id = channel.id

                collection = db[collection_name]
                collection.update_one(
                    {"_id": ctx.guild.id},
                    {"$set": {"channel": channel_id}},
                    upsert=True
                )

                if channel_id:
                    embed = discord.Embed(
                        title=f"{title} Set",
                        description=f"The {title} channel has been set to {channel.mention}",
                        color=0x1fe2f3
                    )
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title=f"{title} Set",
                        description=f"The {title} channel has been removed!",
                        color=0x1fe2f3
                    )
                    await ctx.send(embed=embed)

            except commands.ChannelNotFound:
                await ctx.send("Please specify a valid channel!")
            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond!")

async def setup(bot):
    await bot.add_cog(Configuration(bot))
