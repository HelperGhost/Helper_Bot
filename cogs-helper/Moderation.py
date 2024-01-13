import nextcord
from nextcord import Client, Intents, Embed
from nextcord.ext import commands
import json
from datetime import datetime
import datetime
from typing import List, Dict
class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Moderation Cog Status : ✅")

    @commands.command(name="kick", help="Kick Users,  \n Ex. h!kick [member] [reason] | k, kick", aliases=["k", "bick"])
    @commands.has_permissions(ban_members=True)
    async def kickuser(self, ctx, user: nextcord.Member, *, reason):
        if ctx.author.top_role > user.top_role:
            try:
                await user.kick(reason=reason)
                await ctx.send(f"Kicked {user.mention} For {reason}")
            except nextcord.Forbidden:
                await ctx.send("Error: Permission Needed | I Dont Have Perms To Kick Users.")
            except Exception as e:
                await ctx.send("Error: Invaild Permissions")
                print(f"{e}")
        else:
            await ctx.send("Invaild Perms.")
    
    @commands.command(name="timeout", help="Timeout Users. \n Ex. h!timeout @no_gaming_01 | h!kick [member] [reason]")
    @commands.has_permissions(kick_members=True)
    async def timeout(self, ctx, member: nextcord.Member, time: int = 10, *, reason: str ="No reason provided"):
        duration = datetime.datetime.utcnow() + datetime.timedelta(minutes=time)
        await member.timeout(duration, reason=reason)
        await ctx.send(f'{member.mention} has been timed out. reason: {reason}.')

    @commands.command(name="unban", description="to unban a member.")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: nextcord.User, *, reason: str = "No reason provided"):
        try:
            await ctx.guild.unban(user=member)
            await ctx.send(f'<@{member.id}> has been unbanned. Reason: {reason}.')
        except nextcord.Forbidden:
            await ctx.send("I don't have permission to unban members.") # Bot will respond this if it does not have the permissions
        except nextcord.HTTPException:
            await ctx.send("An error occured while processing the unban command.") # Bot will respond this if there is an error while connecting to discord


    @commands.command(name="ban", aliases=["b", "kan"], help="Bans a Member \n EX. h!ban @.wuid being bad | h!ban (user) (reason)")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: nextcord.Member, *, reason=None):
    # Check if the command user has the necessary permissions
        if ctx.author.top_role > member.top_role:
            # Ban the user
            await member.ban(reason=reason)
            await ctx.send(f'{member.display_name} has been banned. Reason: {reason}')
        else:
            await ctx.send("You don't have the permission to ban this user.")


def setup(bot):
    bot.add_cog(Moderation(bot))