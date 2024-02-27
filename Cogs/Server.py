import discord
from discord.ext import bridge, commands
import datetime
import os
import dotenv
import asyncio
import pymongo

dotenv.load_dotenv()
guild_id = int(os.getenv("GUILD_ID"))
uri = str(os.getenv("MONGO"))

client = pymongo.MongoClient(uri)
db = client["Main"]

class ServerSetup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(guild_id=guild_id, name="setwelcomer", description="Sets the welcomer channel and role")
    @commands.has_permissions(administrator=True)
    async def set_welcomer(self, ctx, channel: discord.TextChannel):
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
            color=0x1fe2f3,
            timestamp=datetime.datetime.utcnow()
        )

        await ctx.respond(embed=embed)

    @bridge.bridge_command(guild_id=guild_id, name="setlogs", description="Sets the logs channel")
    @commands.has_permissions(administrator=True)
    async def set_logs(self, ctx):

        collections = {
            "message_logs": "Message Logs",
            "member_logs": "Member Logs",
            "vc_logs": "Voice Channel Logs",
            "server_logs": "Server Logs",
            "misc_logs": "Miscellaneous Logs"
        }

        for collection_name, title in collections.items():
            await ctx.respond(f"Please specify {title} channel ID or mention (type `skip` to leave it blank):")

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
                        color=0x1fe2f3,
                        timestamp=datetime.datetime.utcnow()
                    )
                    await ctx.respond(embed=embed)
                else:
                    embed = discord.Embed(
                        title=f"{title} Set",
                        description=f"The {title} channel has been removed!",
                        color=0x1fe2f3,
                        timestamp=datetime.datetime.utcnow()
                    )
                    await ctx.respond(embed=embed)

            except commands.ChannelNotFound:
                await ctx.respond("Please specify a valid channel!")
            except asyncio.TimeoutError:
                await ctx.respond("You took too long to respond!")

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        collection = db["welcomer"]

        data = collection.find_one({"_id": member.guild.id})

        if not data:
            return
        
        channel = self.bot.get_channel(data["channel"])

        if not channel:
            return
        
        await channel.send(f"Welcome to the server, {member.mention}!")

def setup(bot):
    bot.add_cog(ServerSetup(bot))
    bot.add_cog(Server(bot))
