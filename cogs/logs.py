from discord.ext import commands
import discord
import datetime
import os
import dotenv
from pymongo import MongoClient

dotenv.load_dotenv()
uri = str(os.getenv("MONGO"))

client = MongoClient(uri)
db = client["Main"]

class Logs(commands.Cog):
    """The Logs System all events."""

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

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        collection = db["vc_logs"]

        data = collection.find_one({"_id": member.guild.id})

        if not data:
            return
        
        channel = self.bot.get_channel(data["channel"])

        if not channel:
            return
        
        if not before.channel and after.channel:
            embed = discord.Embed(
                title="Member Joined Voice Channel!",
                description=f"{member.mention} joined the voice channel {after.channel.mention}",
                color=discord.Color.blue(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=f"@{member.name}", icon_url=member.avatar)
            embed.set_thumbnail(url=member.avatar)

            await channel.send(embed=embed)

        if before.channel and not after.channel:
            embed = discord.Embed(
                title="Member Left Voice Channel!",
                description=f"{member.mention} left the voice channel {before.channel.mention}",
                color=discord.Color.red(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=f"@{member.name}", icon_url=member.avatar)
            embed.set_thumbnail(url=member.avatar)

            await channel.send(embed=embed)

        if before.channel and after.channel and before.channel != after.channel:
            embed = discord.Embed(
                title="Member Moved Between Voice Channels!",
                description=f"{member.mention} moved from {before.channel.mention} to {after.channel.mention}",
                color=discord.Color.brand_green(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=f"@{member.name}", icon_url=member.avatar)
            embed.set_thumbnail(url=member.avatar)

            await channel.send(embed=embed)

        if before.mute != after.mute:
            mute_status = "muted" if after.mute else "unmuted"
            embed = discord.Embed(
                title="Member Mic Got Updated!",
                description=f"{member.mention} was {mute_status}.",
                color=discord.Color.yellow(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=f"@{member.name}", icon_url=member.avatar)
            embed.set_thumbnail(url=member.avatar)

            await channel.send(embed=embed)

        if before.deaf != after.deaf:
            deaf_status = "deafened" if after.deaf else "undeafened"
            embed = discord.Embed(
                title="Member Speaker Got Updated!",
                description=f"{member.mention} was {deaf_status}.",
                color=discord.Color.dark_gold(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=f"@{member.name}", icon_url=member.avatar)
            embed.set_thumbnail(url=member.avatar)

            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        collection = db["server_logs"]

        data = collection.find_one({"_id": before.id})

        if not data:
            return

        channel = self.bot.get_channel(data["channel"])

        if not channel:
            return
            
        icon = after.icon
    
        if not icon:
            icon = None
        
        if before.name != after.name:
            embed = discord.Embed(
                title="Server Name Changed!",
                description=f"Server name changed from {before.name} to {after.name}.",
                color=discord.Color.blue(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=before.name, icon_url=icon)
            embed.set_thumbnail(url=before.icon)

            await channel.send(embed=embed)

        if before.icon != after.icon:
            embed = discord.Embed(
                title="Server Icon Changed!",
                description="The server icon has been changed.",
                color=discord.Color.blurple(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=before.name, icon_url=icon)
            
            if icon:
                embed.set_image(url=icon)

            await channel.send(embed=embed)

        if before.banner != after.banner:
            embed = discord.Embed(
                title="Server Banner Changed!",
                description="The server banner has been changed.",
                color=discord.Color.blurple(),
                timestamp=datetime.datetime.utcnow()
            )

            banner = after.banner

            if not banner:
                banner = None
                embed.add_field(name="Banner", description="None", inline=False)
            
            embed.set_author(name=before.name, icon_url=icon)

            if banner:
                embed.set_image(url=banner)

            await channel.send(embed=embed)

        if before.description != after.description:
            embed = discord.Embed(
                title="Server Description Changed!",
                description="The server description has been changed.",
                color=discord.Color.gold(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=before.name, icon_url=icon)
            embed.set_thumbnail(url=icon)
            embed.add_field(name="Before", value=before.description, inline=False)
            embed.add_field(name="After", value=after.description, inline=False)

            await channel.send(embed=embed)

        if before.afk_channel != after.afk_channel:
            embed = discord.Embed(
                title="AFK Channel Changed!",
                description="The AFK channel has been changed.",
                color=discord.Color.green(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=before.name, icon_url=icon)
            embed.set_thumbnail(url=icon)

            if before.afk_channel:
                embed.add_field(name="Before", value=before.afk_channel.mention, inline=False)
            else:
                embed.add_field(name="Before", value="None", inline=False)

            if after.afk_channel:
                embed.add_field(name="After", value=after.afk_channel.mention, inline=False)
            else:
                embed.add_field(name="After", value="None", inline=False)
            
            await channel.send(embed=embed)
        
        if before.afk_timeout != after.afk_timeout:
            embed = discord.Embed(
                title="AFK Timeout Changed!",
                description="The AFK timeout has been changed.",
                color=discord.Color.green(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=before.name, icon_url=icon)
            embed.set_thumbnail(url=icon)
            embed.add_field(name="Before", value=before.afk_timeout, inline=False)
            embed.add_field(name="After", value=after.afk_timeout, inline=False)

            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        collection = db["server_logs"]

        data = collection.find_one({"_id": channel.guild.id})

        if not data:
            return
        
        channel = self.bot.get_channel(data["channel"])

        if not channel:
            return
        
        icon = channel.guild.icon

        if not icon:
            icon = None
        
        embed = discord.Embed(
            title="Channel Created!",
            description=f"Channel {channel.mention} has been created.",
            color=discord.Color.blurple(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_author(name=channel.guild.name, icon_url=icon)
        embed.set_thumbnail(url=icon)
        embed.set_footer(text=f"ID: {channel.id}")

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        collection = db["server_logs"]

        data = collection.find_one({"_id": channel.guild.id})

        if not data:
            return
        
        channel = self.bot.get_channel(data["channel"])

        if not channel:
            return
        
        icon = channel.guild.icon

        if not icon:
            icon = None
        
        embed = discord.Embed(
            title="Channel Deleted!",
            description=f"Channel {channel.name} has been deleted.",
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_author(name=channel.guild.name, icon_url=icon)
        embed.set_thumbnail(url=icon)

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        collection = db["server_logs"]

        data = collection.find_one({"_id": before.guild.id})

        if not data:
            return
        
        channel = self.bot.get_channel(data["channel"])

        if not channel:
            return
        
        icon = before.guild.icon

        if not icon:
            icon = None

        if before.name != after.name:
            embed = discord.Embed(
                title="Channel Name Changed!",
                description=f"Channel name has been changed.",
                color=discord.Color.blue(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=before.guild.name, icon_url=icon)
            embed.set_thumbnail(url=icon)
            embed.add_field(name="Before", value=before.name, inline=False)
            embed.add_field(name="After", value=after.name, inline=False)

            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        collection = db["server_logs"]

        data = collection.find_one({"_id": role.guild.id})

        if not data:
            return
        
        channel = self.bot.get_channel(data["channel"])

        if not channel:
            return
        
        icon = role.guild.icon

        if not icon:
            icon = None
        
        embed = discord.Embed(
            title="Role Created!",
            description=f"Role {role.mention} has been created.",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_author(name=role.guild.name, icon_url=icon)
        embed.set_thumbnail(url=icon)
        embed.set_footer(text=f"ID: {role.id}")

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        collection = db["server_logs"]

        data = collection.find_one({"_id": role.guild.id})

        if not data:
            return
        
        channel = self.bot.get_channel(data["channel"])

        if not channel:
            return
        
        icon = role.guild.icon

        if not icon:
            icon = None

        embed = discord.Embed(
            title="Role Deleted!",
            description=f"Role {role.name} has been deleted.",
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_author(name=role.guild.name, icon_url=icon)
        embed.set_thumbnail(url=icon)

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        collection = db["misc_logs"]

        data = collection.find_one({"_id": invite.guild.id})

        if not data:
            return
        
        channel = self.bot.get_channel(data["channel"])

        if not channel:
            return
        
        icon = invite.guild.icon

        if not icon:
            icon = None

        embed = discord.Embed(
            title="Invite Created!",
            description=f"Invite {invite.url} has been created by {invite.inviter.mention}.",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_author(name=invite.guild.name, icon_url=icon)
        embed.set_thumbnail(url=icon)
        embed.set_footer(text=f"Created by {invite.inviter.name}")

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        collection = db["misc_logs"]

        data = collection.find_one({"_id": invite.guild.id})

        if not data:
            return
        
        channel = self.bot.get_channel(data["channel"])

        if not channel:
            return
        
        icon = invite.guild.icon

        if not icon:
            icon = None

        embed = discord.Embed(
            title="Invite Deleted!",
            description=f"Invite {invite.url} has been deleted.",
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_author(name=invite.guild.name, icon_url=icon)
        embed.set_thumbnail(url=icon)

        await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Logs(bot))
