from discord.ext import commands
import discord
from typing import Optional
import asyncio
import datetime

class Moderation(commands.Cog):
    """The Moderation Cog ig."""

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ban", description="Bans a user.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason: Optional[str]="No reason provided."):
        await member.ban(reason=reason)
        embed = discord.Embed(title="User Banned", description=f"{member} was banned. Reason: {reason}.", color=0x00ff00)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
        embed.set_footer(text=f"User ID: {member.id}")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="kick", description="Kicks a user.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason: Optional[str]="No reason provided"):
        await member.kick(reason=reason)
        embed = discord.Embed(title="User Kicked", description=f"{member} was kicked. Reason: {reason}.", color=0xff0000)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
        embed.set_footer(text=f"User ID: {member.id}")
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name="mute", description="Mutes a user.")
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx: commands.Context, member: discord.Member, time: Optional[int]=10, *, reason: Optional[str]="No reason provided"):
        duration = datetime.datetime.utcnow() + datetime.timedelta(minutes=time)
        await member.timeout(duration, reason=reason)
        embed = discord.Embed(title="User Muted", description=f"{member} was muted for {time} minutes. Reason: {reason}.", color=0xffff00)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
        embed.set_footer(text=f"User ID: {member.id}")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="unban", description="Unbans a user.")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx: commands.Context, user: discord.User, *, reason: Optional[str]="No reason provided"):
        await ctx.guild.unban(discord.Object(id=user.id), reason=reason)
        embed = discord.Embed(title="User Unbanned", description=f"Unbanned {user.name}. Reason: {reason}.", color=0x00ff00)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
        embed.set_footer(text=f"User ID: {user.id}")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name = "unmute", description = "Unmutes a user.")
    @commands.has_permissions(kick_members = True)
    async def unmute(self, ctx: commands.Context, member: discord.Member, *, reason: Optional[str]="No reason provided"):
        await member.remove_timeout()
        embed = discord.Embed(title="User Unmuted", description=f"{member} was unmuted  Reason: {reason}.", color=0x00ff00)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
        embed.set_footer(text=f"User ID: {member.id}")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="purge", description="Bulk deletes messages.")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context, limit: Optional[int]=3):
        await ctx.send(f"Purging {limit} messages...")
        await ctx.channel.purge(limit=limit)
        await asyncio.sleep(3)
        await ctx.send(f"{limit} messages purged")
        await ctx.channel.purge(limit=1)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
