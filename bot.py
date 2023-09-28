import discord
from discord.ext import commands
import asyncio

# Define your intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
intents.presences = True       # Enable presence intent

# Initialize the bot with intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Replace 'YOUR_BOT_TOKEN' with your bot token
bot_token = 'Your_Bot_Token'

# Define the name of the roles
muted_role_name = "Muted"
member_role_name = "Member"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.add_cog(ModerationCog(bot))

@bot.event
async def on_member_join(member):
    member_role = discord.utils.get(member.guild.roles, name=member_role_name)

    if not member_role:
        member_role = await member.guild.create_role(name=member_role_name)

    # Add the member role to the new member before sending the message
    await member.add_roles(member_role)

    general_channel = member.guild.get_channel('Your_Channel_ID')  # Replace with the actual channel ID
    await general_channel.send(f"Welcome to the server, {member.mention}!")

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'Pong! You have a ping of {latency}ms.')

@bot.event
async def on_message(message):
    # Replace with the actual channel ID where you want to add reactions
    if message.channel.id == 'Your_Channel_ID':
        emoji = 'Emoji'  # Replace with the desired emoji
        await message.add_reaction(emoji)

    await bot.process_commands(message)

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided."):
        try:
            await member.ban(reason=reason)
            await ctx.send(f"{member.name} has been banned. Reason: {reason}")
        except discord.Forbidden:
            await ctx.send("I don't have permission to ban members.")
        except discord.HTTPException:
            await ctx.send("An error occurred while processing the ban command.")
    
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
        if isinstance(error, commands.BadArgument):
            await ctx.send("Member not found or invalid arguments provided.")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, duration: int, *, reason="No reason provided."):
        muted_role = discord.utils.get(ctx.guild.roles, name=muted_role_name)
        if not muted_role:
            muted_role = await ctx.guild.create_role(name=muted_role_name)
        try:
            await member.add_roles(muted_role)
            await ctx.send(f"{member.name} has been muted for {duration} minutes. Reason: {reason}")

            await asyncio.sleep(duration * 60)

            await member.remove_roles(muted_role)
            await ctx.send(f"{member.name} has been unmuted after {duration} minutes.")
        except discord.Forbidden:
            await ctx.send("I don't have permission to manage roles.")
        except discord.HTTPException:
            await ctx.send("An error occurred while processing the mute/unmute command.")

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
        if isinstance(error, commands.BadArgument):
            await ctx.send("Member not found or invalid arguments provided.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, user_id):
        try:
            banned_users = await ctx.guild.bans()
            for ban_entry in banned_users:
                user = ban_entry.user
                if str(ban_entry.user.id) == str(user_id):
                    await ctx.guild.unban(ban_entry.user)
                    await ctx.send(f"{ban_entry.user.name} has been unbanned.")
                    return
            await ctx.send("Member not found in the list of banned users.")
        except discord.Forbidden:
            await ctx.send("I don't have permission to unban members.")
        except discord.HTTPException:
            await ctx.send("An error occurred while processing the unban command.")

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
        if isinstance(error, commands.BadArgument):
            await ctx.send("Member not found or invalid arguments provided.")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name=muted_role_name)
        if not muted_role:
            await ctx.send(f"The {muted_role_name} role doesn't exist.")
            return

        try:
            if muted_role in member.roles:
                await member.remove_roles(muted_role)
                await ctx.send(f"{member.name} has been unmuted.")
            else:
                await ctx.send(f"{member.name} is not muted.")
        except discord.Forbidden:
            await ctx.send("I don't have permission to manage roles.")
        except discord.HTTPException:
            await ctx.send("An error occurred while processing the unmute command.")

    # Error handler for the unmute command
    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
        if isinstance(error, commands.BadArgument):
            await ctx.send("Member not found or invalid arguments provided.") 
    
# bot.add_cog(ModerationCog(bot))

# Run the bot
bot.run(bot_token)
