import nextcord
from nextcord import Client, Intents, Embed
from nextcord.ext import commands
import json
from datetime import datetime
import datetime
from typing import List, Dict

import random


class logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f"logs Cog Status : ✅")

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
                embed = nextcord.Embed(
                    title="Message Edited!",
                    description=f"Message edited in {before.channel.mention} [Link]({message_link}).",
                    color=nextcord.Color.blurple(),
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
                embed = nextcord.Embed(
                    title="Message Deleted!",
                    description=f"A message was deleted in {message.channel.mention}.",
                    color=nextcord.Color.red(),
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
                embed = nextcord.Embed(
                    title="Member Joined!",
                    description="",
                    color=nextcord.Color.blurple(),
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
                embed = nextcord.Embed(
                    title="Member Left!",
                    description="",
                    color=nextcord.Color.red(),
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_author(name=f"@{member.name}", icon_url=member.avatar)
                embed.set_thumbnail(url=member.avatar)
                embed.add_field(name="User info:", value=f"ID: {member.id}\nName: {member.mention}", inline=False)

                await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        query = "SELECT channel_id FROM member_logs WHERE server_id = ?"
        result = await self.bot.get_cog("QuickServer").execute_query(query, (before.guild.id,), fetchone=True)

        if result:
            channel_id = result[0]
            logs_channel = self.bot.get_channel(channel_id)

            if logs_channel:
                if before.nick != after.nick:
                    embed = nextcord.Embed(
                        title="Nickname Changed!",
                        description=f"{after.mention} nickname was changed.",
                        color=0xFFA500,
                        timestamp=datetime.datetime.utcnow()
                    )
                    embed.set_author(name=f"@{after.name}", icon_url=after.avatar)
                    embed.set_thumbnail(url=after.avatar)
                    embed.add_field(name="Before:", value=before.nick or "None", inline=False)
                    embed.add_field(name="After:", value=after.nick or "None", inline=False)
                    
                    await logs_channel.send(embed=embed)

                added_roles = set(after.roles) - set(before.roles)
                if added_roles:
                    embed = nextcord.Embed(
                        title="Role Added!",
                        description="",
                        color=0x1FE231,
                        timestamp=datetime.datetime.utcnow()
                    )
                    embed.set_author(name=f"@{after.name}", icon_url=after.avatar)
                    embed.set_thumbnail(url=after.avatar)
                    embed.add_field(name="Added Role:", value=", ".join(role.mention for role in added_roles), inline=False)
                    
                    await logs_channel.send(embed=embed)

                removed_roles = set(before.roles) - set(after.roles)
                if removed_roles:
                    embed = nextcord.Embed(
                        title="Role Removed!",
                        description="",
                        color=0xFF0000,
                        timestamp=datetime.datetime.utcnow()
                    )
                    embed.set_author(name=f"@{after.name}", icon_url=after.avatar)
                    embed.set_thumbnail(url=after.avatar)
                    embed.add_field(name="Removed Role:", value=", ".join(role.mention for role in removed_roles), inline=False)

                    await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        query = "SELECT channel_id FROM member_logs WHERE server_id = ?"
        result = await self.bot.get_cog("QuickServer").execute_query(query, (guild.id,), fetchone=True)

        if result:
            channel_id = result[0]
            logs_channel = self.bot.get_channel(channel_id)

            if logs_channel:
                embed = nextcord.Embed(
                    title="Member Banned!",
                    description=f"{user.mention} has been banned from the server.",
                    color=nextcord.Color.red(),
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_author(name=f"@{user.name}", icon_url=user.avatar)
                embed.set_thumbnail(url=user.avatar)

                await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        query = "SELECT channel_id FROM member_logs WHERE server_id = ?"
        result = await self.bot.get_cog("QuickServer").execute_query(query, (guild.id,), fetchone=True)

        if result:
            channel_id = result[0]
            logs_channel = self.bot.get_channel(channel_id)

            if logs_channel:
                embed = nextcord.Embed(
                    title="Member Unbanned!",
                    description=f"{user.mention} has been unbanned from the server.",
                    color=nextcord.Color.red(),
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_author(name=f"@{user.name}", icon_url=user.avatar)
                embed.set_thumbnail(url=user.avatar)

                await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        query = "SELECT channel_id FROM vc_logs WHERE server_id = ?"
        result = await self.bot.get_cog("QuickServer").execute_query(query, (member.guild.id,), fetchone=True)

        if result:
            channel_id = result[0]
            logs_channel = self.bot.get_channel(channel_id)

            if logs_channel:
                if not before.channel and after.channel:
                    embed = nextcord.Embed(
                        title="Member Joined Voice Channel!",
                        description=f"{member.mention} joined the voice channel {after.channel.mention}",
                        color=0x00FF00,
                        timestamp=datetime.datetime.utcnow()
                    )
                    embed.set_author(name=f"@{member.name}", icon_url=member.avatar)
                    embed.set_thumbnail(url=member.avatar)
                    
                    await logs_channel.send(embed=embed)

                elif before.channel and not after.channel:
                    embed = nextcord.Embed(
                        title="Member Left Voice Channel!",
                        description=f"{member.mention} left the voice channel {before.channel.mention}",
                        color=0xFF0000,
                        timestamp=datetime.datetime.utcnow()
                    )
                    embed.set_author(name=f"@{member.name}", icon_url=member.avatar)
                    embed.set_thumbnail(url=member.avatar)

                    await logs_channel.send(embed=embed)

                elif before.channel and after.channel and before.channel != after.channel:
                    embed = nextcord.Embed(
                        title="Member Moved Between Voice Channels!",
                        description=f"{member.mention} moved from {before.channel.mention} to {after.channel.mention}",
                        color=0x0000FF,
                        timestamp=datetime.datetime.utcnow()
                    )
                    embed.set_author(name=f"@{member.name}", icon_url=member.avatar)
                    embed.set_thumbnail(url=member.avatar)

                    await logs_channel.send(embed=embed)

                elif before.mute != after.mute or before.deaf != after.deaf:
                    mute_status = "muted" if after.mute else "unmuted"
                    embed = nextcord.Embed(
                        title="Member Mic Got Updated!",
                        description=f"{member.mention} was {mute_status}.",
                        color=0xFFFF00,
                        timestamp=datetime.datetime.utcnow()
                    )
                    embed.set_author(name=f"@{member.name}", icon_url=member.avatar)
                    embed.set_thumbnail(url=member.avatar)

                    await logs_channel.send(embed=embed)
                
                elif before.deaf != after.deaf:
                    deaf_status = "deafened" if after.deaf else "undeafened"
                    embed = nextcord.Embed(
                        title="Member Speaker Got Updated!",
                        description=f"{member.mention} was {deaf_status}.",
                        color=0XFFF00,
                        timestamp=datetime.datetime.utcnow()
                    )
                    embed.set_author(name=f"@{member.name}", icon_url=member.avatar)
                    embed.set_thumbnail(url=member.avatar)

                    await logs_channel.send(embed=embed)























def setup(bot):
    bot.add_cog(logs(bot))