import discord
from discord.ext import commands
import datetime

class LogsSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        # Check if the server_id exists in the message_logs table
        query = "SELECT channel_id FROM message_logs WHERE server_id = ?"
        result = await self.bot.get_cog("QuickServer").execute_query(query, (before.guild.id,), fetchone=True)

        if result:
            channel_id = result[0]
            logs_channel = self.bot.get_channel(channel_id)

            if logs_channel:
                message_link = f"https://discord.com/channels/{before.guild.id}/{before.channel.id}/{before.id}"
                # Send a message when a message is edited
                embed = discord.Embed(
                    title="Message Edited!",
                    description=f"Message edited in {before.channel.mention} [Link]({message_link}).",
                    color=discord.Color.blurple(),
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_author(name=f"@{before.author.name}", icon_url=before.author.avatar)
                embed.add_field(name="Before:", value=before.content, inline=False)
                embed.add_field(name="After:", value=after.content, inline=False)

                await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        query = "SELECT channel_id FROM message_logs WHERE server_id = ?"
        result = await self.bot.get_cog("QuickServer").execute_query(query, (message.guild.id,), fetchone=True)

        if result:
            channel_id = result[0]
            logs_channel = self.bot.get_channel(channel_id)

            if logs_channel:
                embed = discord.Embed(
                    title="Message Deleted!",
                    description=f"A message was deleted in {message.channel.mention}.",
                    color=discord.Color.red(),
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_author(name=f"@{message.author.name}", icon_url=message.author.avatar)
                embed.add_field(name="Message:", value=message.content, inline=False)

                await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        query = "SELECT channel_id FROM member_logs WHERE server_id = ?"
        result = await self.bot.get_cog("QuickServer").execute_query(query, (member.guild.id,), fetchone=True)

        if result:
            channel_id = result[0]
            logs_channel = self.bot.get_channel(channel_id)

            if logs_channel:
                account_created_at = member.created_at
                account_age = round(datetime.datetime.timestamp(account_created_at))
                embed = discord.Embed(
                    title="Member Joined!",
                    description="",
                    color=discord.Color.blurple(),
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_author(name=f"@{member.name}", icon_url=member.avatar)
                embed.set_thumbnail(url=member.avatar)
                embed.add_field(name="User info:", value=f"ID: {member.id}\nName: {member.mention}", inline=False)
                embed.add_field(name="Account Age:", value=f"<t:{account_age}:D> (<t:{account_age}:R>)", inline=False)

                await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        query = "SELECT channel_id FROM member_logs WHERE server_id = ?"
        result = await self.bot.get_cog("QuickServer").execute_query(query, (member.guild.id,), fetchone=True)

        if result:
            channel_id = result[0]
            logs_channel = self.bot.get_channel(channel_id)

            if logs_channel:
                embed = discord.Embed(
                    title="Member Left!",
                    description="",
                    color=discord.Color.red(),
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_author(name=f"@{member.name}", icon_url=member.avatar)
                embed.set_thumbnail(url=member.avatar)
                embed.add_field(name="User info:", value=f"ID: {member.id}\nName: {member.mention}", inline=False)

                await logs_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(LogsSystem(bot))
