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

def setup(bot):
    bot.add_cog(LogsSystem(bot))
