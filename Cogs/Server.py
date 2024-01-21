import discord
from discord.ext import bridge, commands
from helperdb import Database
import datetime
import os
import dotenv
import asyncio

dotenv.load_dotenv()
guild_id = int(os.getenv("GUILD_ID"))

class ServerSetup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database("database/server.db")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.db.connect()
        await self.create_tables()

    async def create_tables(self):
        welcomer_table = """CREATE TABLE IF NOT EXISTS welcomer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            channel_id INTEGER,
            role_id INTEGER
        )"""

        await self.db.execute(welcomer_table)

        introduction_table = """CREATE TABLE IF NOT EXISTS introduction (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            channel_id INTEGER
        )"""

        await self.db.execute(introduction_table)

        message_logs_table = """CREATE TABLE IF NOT EXISTS message_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            channel_id INTEGER
        )"""

        member_logs_table = """CREATE TABLE IF NOT EXISTS member_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            channel_id INTEGER
        )"""

        vc_logs_table = """CREATE TABLE IF NOT EXISTS vc_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            channel_id INTEGER
        )"""

        server_logs_table = """CREATE TABLE IF NOT EXISTS server_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            channel_id INTEGER
        )"""

        misc_logs_table = """CREATE TABLE IF NOT EXISTS misc_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            channel_id INTEGER
        )"""

        await self.db.execute(message_logs_table)
        await self.db.execute(member_logs_table)
        await self.db.execute(vc_logs_table)
        await self.db.execute(server_logs_table)
        await self.db.execute(misc_logs_table)

    @bridge.bridge_command(guild_id=guild_id, name="setwelcomer", description="Sets the welcomer channel and role")
    @commands.has_permissions(administrator=True)
    async def set_welcomer(self, ctx, channel: discord.TextChannel, role: discord.Role):
        
        if not channel:
            await ctx.respond("Please specify a channel!")
            return

        if not role:
            await ctx.respond("Please specify a role!")
            return

        query = "SELECT * FROM welcomer WHERE guild_id =?"
        existing_data = await self.db.fetchone(query, ctx.guild.id)
        
        if existing_data:
            existing_channel_id = existing_data["channel_id"]
            existing_role_id = existing_data["role_id"]

            if existing_channel_id == channel.id and existing_role_id == role.id:
                await ctx.respond("The welcomer channel and role are already set!")
                return
            else:
                update_query = "UPDATE welcomer SET channel_id =?, role_id =? WHERE guild_id =?"
                await self.db.execute(update_query, channel.id, role.id, ctx.guild.id)
        
        else:
            insert_query = "INSERT INTO welcomer (guild_id, channel_id, role_id) VALUES (?,?,?)"
            await self.db.execute(insert_query, ctx.guild.id, channel.id, role.id)

        embed = discord.Embed(
            title="Welcomer Set",
            description=f"The welcomer channel has been set to {channel.mention} and the role has been set to {role.mention}",
            color=0x1fe2f3,
            timestamp=datetime.datetime.utcnow()
        )

        await ctx.respond(embed=embed)

    @bridge.bridge_command(guild_id=guild_id, name="setintroduction", description="Sets the introduction channel")
    @commands.has_permissions(administrator=True)
    async def set_introduction(self, ctx, channel: discord.TextChannel):

        if not channel:
            await ctx.respond("Please specify a channel!")
            return
        
        query = "SELECT * FROM introduction WHERE guild_id =?"
        existing_data = await self.db.fetchone(query, ctx.guild.id)

        if existing_data:
            existing_channel_id = existing_data["channel_id"]

            if existing_channel_id == channel.id:
                await ctx.respond("The introduction channel is already set!")
                return
            else:
                update_query = "UPDATE introduction SET channel_id =? WHERE guild_id =?"
                await self.db.execute(update_query, channel.id, ctx.guild.id)

        else:
            insert_query = "INSERT INTO introduction (guild_id, channel_id) VALUES (?,?)"
            await self.db.execute(insert_query, ctx.guild.id, channel.id)

        embed = discord.Embed(
            title="Introduction Set",
            description=f"The introduction channel has been set to {channel.mention}",
            color=0x1fe2f3,
            timestamp=datetime.datetime.utcnow()
        )

        await ctx.respond(embed=embed)

    @bridge.bridge_command(guild_id=guild_id, name="setlogs", description="Sets the logs channel")
    @commands.has_permissions(administrator=True)
    async def set_logs(self, ctx):

        tables = {
            "message_logs": "Message Logs",
            "member_logs": "Member Logs",
            "vc_logs": "Voice Channel Logs",
            "server_logs": "Server Logs",
            "misc_logs": "Miscellaneous Logs"
        }

        for table, title in tables.items():
            await ctx.respond(f"Please specify {title} channel ID or mention (type `skip` to leave it blank):")

            try:

                message = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60)

                if message.content.lower() == "skip":
                    channel_id = None
                else:
                    channel = await commands.TextChannelConverter().convert(ctx, message.content)
                    channel_id = channel.id

                update_query = f"INSERT OR REPLACE INTO {table} (guild_id, channel_id) VALUES (?,?)"
                await self.db.execute(update_query, ctx.guild.id, channel_id)

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
        self.db = Database("database/server.db")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.db.connect()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        query = "SELECT * FROM welcomer WHERE guild_id =?"
        data = await self.db.fetchone(query, member.guild.id)

        if data:
            channel_id = data["channel_id"]
            role_id = data["role_id"]

            channel = member.guild.get_channel(channel_id)
            role = member.guild.get_role(role_id)
            await channel.send(f"Welcome to the server, {member.mention}!")
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        query_introduction = "SELECT * FROM introduction WHERE guild_id =?"
        data = await self.db.fetchone(query_introduction, message.guild.id)

        if data:
            channel_id = data["channel_id"]

            if message.channel.id == channel_id:
                await message.add_reaction("🙋‍♀️")
                return
            else:
                return
        
        await self.bot.process_commands(message)

def setup(bot):
    bot.add_cog(ServerSetup(bot))
    bot.add_cog(Server(bot))
