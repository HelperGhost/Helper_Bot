import discord
from discord.ext import commands
import datetime
import os
import dotenv
import pymongo

dotenv.load_dotenv()
uri = str(os.getenv("MONGO"))

client = pymongo.MongoClient(uri)
db = client["Main"]

class LogsSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):

        if before.embeds:
            return
        
        collection = db["message_logs"]

        data = collection.find_one({"_id": before.guild.id})

        if not data:
            return
        
        channel = self.bot.get_channel(data["channel"])

        if not channel:
            return

        message_link = f"https://discord.com/channels/{before.guild.id}/{before.channel.id}/{before.id}"
        
        embed = discord.Embed(
            title="Message Edited",
            description=f"Message edited in {before.channel.mention} [Link]({message_link}).",
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
        
        collection = db["message_logs"]

        data = collection.find_one({"_id": message.guild.id})

        if not data:
            return
        
        channel = self.bot.get_channel(data["channel"])

        if not channel:
            return
        
        embed = discord.Embed(
            title="Message Deleted",
            description=f"Message deleted in {message.channel.mention}.",
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_author(name=f"@{message.author}", icon_url=message.author.avatar)
        embed.set_thumbnail(url=message.author.avatar)
        embed.add_field(name="Message:", value=message.content, inline=False)

        await channel.send(embed=embed)                

    @commands.Cog.listener()
    async def on_member_join(self, member):

        collection = db["member_logs"]

        data = collection.find_one({"_id": member.guild.id})

        if not data:
            return
        
        channel = self.bot.get_channel(data["channel"])

        if not channel:
            return

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

        collection = db["member_logs"]

        data = collection.find_one({"_id": member.guild.id})

        if not data:
            return
        
        channel = self.bot.get_channel(data["channel"])

        if not channel:
            return
        
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

    @commands.Cog.listener()
    async def on_member_update(self, before, after):

        collection = db["member_logs"]

        data = collection.find_one({"_id": before.guild.id})

        if not data:
            return
        
        channel = self.bot.get_channel(data["channel"])

        if not channel:
            return
        
        if before.nick != after.nick:
            embed = discord.Embed(
                title="Nickname Changed",
                description=f"Nickname changed for {before.mention}",
                color=discord.Color.blurple(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=f"@{before.name}", icon_url=before.avatar)
            embed.set_thumbnail(url=before.avatar)
            embed.add_field(name="Before", value=before.nick, inline=False)
            embed.add_field(name="After", value=after.nick, inline=False)

            await channel.send(embed=embed)

        if before.roles!= after.roles:
            added_roles = [role for role in after.roles if role not in before.roles]
            removed_roles = [role for role in before.roles if role not in after.roles]

            if added_roles:
                embed = discord.Embed(
                    title="Role Added",
                    description=f"Role added to {before.mention}",
                    color=discord.Color.blurple(),
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_author(name=f"@{before.name}", icon_url=before.avatar)
                embed.set_thumbnail(url=before.avatar)
                embed.add_field(name="Role:", value=", ".join(role.mention for role in added_roles), inline=False)

                await channel.send(embed=embed)

            if removed_roles:
                embed = discord.Embed(
                    title="Role Removed",
                    description=f"Role removed from {before.mention}",
                    color=discord.Color.blurple(),
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_author(name=f"@{before.name}", icon_url=before.avatar)
                embed.set_thumbnail(url=before.avatar)
                embed.add_field(name="Role:", value=", ".join(role.mention for role in removed_roles), inline=False)

                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):

        collection = db["member_logs"]

        data = collection.find_one({"_id": guild.id})

        if not data:
            return
        
        channel = self.bot.get_channel(data["channel"])

        if not channel:
            return
        embed = discord.Embed(
            title="Member Banned",
            description=f"{user.mention} was banned from the server",
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_author(name=f"@{user.name}", icon_url=user.avatar)
        embed.set_thumbnail(url=user.avatar)
        embed.add_field(name="User info:", value=f"ID: {user.id}\nName: {user.mention}", inline=False)

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):

        collection = db["member_logs"]

        data = collection.find_one({"_id": guild.id})

        if not data:
            return
        
        channel = self.bot.get_channel(data["channel"])

        if not channel:
            return
        
        embed = discord.Embed(
            title="Member Unbanned",
            description=f"{user.mention} was unbanned from the server",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_author(name=f"@{user.name}", icon_url=user.avatar)
        embed.set_thumbnail(url=user.avatar)
        embed.add_field(name="User info:", value=f"ID: {user.id}\nName: {user.mention}", inline=False)

        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(LogsSystem(bot))
