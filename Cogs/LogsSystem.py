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

def setup(bot):
    bot.add_cog(LogsSystem(bot))
