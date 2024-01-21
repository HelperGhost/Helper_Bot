from unittest import result
import discord
from discord.ext import commands
from helperdb import Database
import datetime

class LogsSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database("database/server.db")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.db.connect()

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.embeds:
            return

        query = "SELECT channel_id FROM message_logs WHERE guild_id =?"
        result = await self.db.fetchone(query, before.guild.id)
        if result:
            channel_id = result[0]
            channel = self.bot.get_channel(channel_id)

            if channel:
                embed = discord.Embed(
                    title="Message Edited",
                    description=f"Message edited in {before.channel.mention}",
                    color=discord.Color.blurple(),
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_author(name=f"@{before.author}", icon_url=before.author.avatar)
                embed.set_thumbnail(url=before.author.avatar)
                embed.add_field(name="Before", value=before.content, inline=False)
                embed.add_field(name="After", value=after.content, inline=False)

                await channel.send(embed=embed)
        
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.embeds:
            return
        
        query = "SELECT channel_id FROM message_logs WHERE guild_id =?"
        result = await self.db.fetchone(query, message.guild.id)
        if result:
            channel_id = result[0]
            channel = self.bot.get_channel(channel_id)

            if channel:
                embed = discord.Embed(
                    title="Message Deleted",
                    description=f"Message deleted in {message.channel.mention}",
                    color=discord.Color.red(),
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_author(name=f"@{message.author}", icon_url=message.author.avatar)
                embed.set_thumbnail(url=message.author.avatar)
                embed.add_field(name="Message:", value=message.content, inline=False)

                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        query = "SELECT channel_id FROM member_logs WHERE guild_id =?"
        result = await self.db.fetchone(query, member.guild.id)
        if result:
            channel_id = result[0]
            channel = self.bot.get_channel(channel_id)

            if channel:
                embed = discord.Embed(
                    title="Member Joined",
                    description=f"{member.mention} joined the server",
                    color=discord.Color.green(),
                    timestamp=datetime.datetime.utcnow()
                )

                account_created_at = member.created_at
                account_age = int(account_created_at.timestamp())

                embed.set_author(name=f"@{member.name}", icon_url=member.avatar)
                embed.set_thumbnail(url=member.avatar)
                embed.add_field(name="User info:", value=f"ID: {member.id}\nName: {member.mention}", inline=False)
                embed.add_field(name="Account Age:", value=f"<t:{account_age}:D> (<t:{account_age}:R>)", inline=False)

                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        query = "SELECT channel_id FROM member_logs WHERE guild_id =?"
        result = await self.db.fetchone(query, member.guild.id)
        if result:
            channel_id = result[0]
            channel = self.bot.get_channel(channel_id)

            if channel:
                embed = discord.Embed(
                    title="Member Left",
                    description=f"{member.mention} left the server",
                    color=discord.Color.red(),
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_author(name=f"@{member.name}", icon_url=member.avatar)
                embed.set_thumbnail(url=member.avatar)
                embed.add_field(name="User info:", value=f"ID: {member.id}\nName: {member.mention}", inline=False)

                await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(LogsSystem(bot))
