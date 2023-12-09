import discord
from discord.ext import commands

class LogsSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        # Check if the server_id exists in the message_logs table
        query = "SELECT channel_id FROM message_logs WHERE server_id = ?"
        result = await self.bot.get_cog("Quick_Server").execute_query(query, (before.guild.id,), fetchone=True)

        if result:
            channel_id = result[0]
            logs_channel = self.bot.get_channel(channel_id)

            if logs_channel:
                # Send a message when a message is edited
                embed = discord.Embed(
                    title="Message Edited",
                    description=f"Author: {before.author.mention}\n"
                                f"Channel: {before.channel.mention}",
                    color=discord.Color.orange()
                )
                embed.add_field(name="Before", value=before.content, inline=False)
                embed.add_field(name="After", value=after.content, inline=False)

                await logs_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(LogsSystem(bot))
