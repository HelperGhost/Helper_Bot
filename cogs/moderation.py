from discord.ext import commands
import discord
from typing import Optional

class Moderation(commands.Cog):
    """The Moderation Cog ig."""

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ban", description="Bans a user.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.Member, reason: Optional[str]="No reason provided."):
        await member.ban(reason=reason)
        embed = discord.Embed(title="User Banned", description=f"{member} was banned. Reason: {reason}.", color=0x00ff00)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
        embed.set_footer(text=f"User ID: {member.id}")
        await ctx.respond(embed=embed)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
