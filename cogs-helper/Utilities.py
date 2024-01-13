import nextcord
from nextcord import Client, Intents, Embed
from nextcord.ext import commands
import json
from datetime import datetime
import datetime
from typing import List, Dict

import random
bot_info = '''
👻 Name: Helper#8515
👻 Nickname: Helper
👻 Age: I am a ghost, I don't have an age. I am beyond the realm of the living, bro.
👻 Gender: Ghost
👻 Nationality: Ghost UK (Boo-rish)
👻 Hobbies: Haunting Discord servers 👻👾
👻 Likes: ☕ Coffee and 🎶 Music
👻 Dislikes: Scammers 🚫

👻 Description:
Hey there, mortal souls! 👋 This is my discord bot, Helper#8515, here to assist and haunt in equal measure! 👻✨ Recreated By jqm1e, we're here to make your Discord experience otherworldly! 💀👻👾
'''
class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Utilities Cog Status : ✅")

    @commands.command(name="servericon", description="provides the server icon")
    async def servericon(self, ctx):

        embed = nextcord.Embed(
            title = "",
            description = "",
            color = ctx.guild.owner.color,
            timestamp = datetime.datetime.utcnow()
        )

        embed.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
        embed.set_image(url=f"{ctx.guild.icon}")

        await ctx.send(embed=embed)

    @commands.command(name="user_roles", description="provides the roles of the user")
    async def user_roles(self, ctx, member: nextcord.Member = None):
        if member is None:
            member = ctx.author

        roles = sorted(member.roles, key=lambda role: role.position, reverse=True)
        role = ", ".join(f"{role.mention}" for role in roles if role.name != '@everyone')

        embed = nextcord.Embed(
            title = "",
            description = "",
            color = member.color,
            timestamp = datetime.datetime.utcnow()
        )

        embed.set_author(name=f"@{member.name}", icon_url=f"{member.avatar}")
        embed.add_field(name="**Roles:**", value=f"{role}")

        await ctx.send(embed=embed)

    @commands.command(name="userinfo", description="tells the information about the user")
    async def userinfo(self, ctx, member: nextcord.Member = None):
        if member is None:
            member = ctx.author

        # discord joined data
        account_created_at = member.created_at
        account_time = int(account_created_at.timestamp())

        # discord joined data
        server_joined_at = member.joined_at
        server_time = int(server_joined_at.timestamp())

        roles = sorted(member.roles, key=lambda role: role.position, reverse=True)
        role = ", ".join(f"{role.mention}" for role in roles if role.name != '@everyone')

        embed = nextcord.Embed(
        title="",
        description="",
        color= member.color,  # You can customize the color here
        timestamp = datetime.datetime.utcnow()
        )

        embed.set_author(name=f"@{member.name}", icon_url=f"{member.avatar}")
        embed.set_thumbnail(url=f"{member.avatar}")

        embed.add_field(name="**User Info:**", value=f"ID: {member.id}\nName: {member.mention}", inline=False)
        embed.add_field(name="**Discord Joined:**", value=f"<t:{account_time}:D> (<t:{account_time}:R>)", inline=False)
        embed.add_field(name="**Server Joined:**", value=f"<t:{server_time}:D> (<t:{server_time}:R>)", inline=False)
        embed.add_field(name="**User's Roles:**", value=f"{role}", inline=False)

        await ctx.send(embed=embed)


    @commands.command(name="avatar", description="shows avatar of a member")
    async def avatar(self, ctx, *, member: nextcord.Member = None):
        if member is None:
            member = ctx.author

        embed = nextcord.Embed(
            title="",
            description="",
            color= member.color,  # You can customize the color here
            timestamp = datetime.datetime.utcnow()
        )

        embed.set_author(name=f"@{member.name}", icon_url=f"{member.avatar}")
        embed.set_image(url=f"{member.avatar}")

        await ctx.send(embed=embed)

    @commands.command(name="serverinfo", description="tells the information about the server")
    async def serverinfo(self, ctx):

        server_created_at = ctx.guild.created_at

        roles = sorted(ctx.guild.roles, key=lambda role: role.position, reverse=True)
        role = ", ".join(f"{ctx.guild.roles}" for role in roles if role.name != '@everyone')

        embed = nextcord.Embed(
            title = "Under Development!",
            description = "",
            color = ctx.guild.owner.color,
            timestamp = datetime.datetime.utcnow()
        )

        embed.set_author(name=f'{ctx.guild.name}', icon_url=f'{ctx.guild.icon}')
        embed.set_thumbnail(url=f'{ctx.guild.icon}')

        embed.add_field(name="**Owner:**", value=f'{ctx.guild.owner.mention}')
        embed.add_field(name="**Members:**", value=len(ctx.guild.members))
        embed.add_field(name="**Roles:**", value=len(ctx.guild.roles))
        embed.add_field(name="**Categories:**", value=len(ctx.guild.categories))
        embed.add_field(name="**Channels:**", value=len(ctx.guild.channels))
        embed.add_field(name="**Text Channels:**", value=len(ctx.guild.text_channels))
        embed.add_field(name="**Voice Channels:**", value=len(ctx.guild.voice_channels))

        await ctx.send(embed=embed)

    @commands.command(name="botinfo", description="tells the bot's info.")
    async def botinfo(self, ctx):
        await ctx.send(bot_info)

    @commands.command(name="roast", description="roast someone for you")
    async def roast(self, ctx, member: nextcord.Member):
        skele_id = 875208986603958344
        mom_jokes = [
            f"Yo {member.mention}. Your mama is so old, she knew Gandalf before he had a beard!",
            f"Yo {member.mention}. Your mom is so slow, when she tried to catch up with the times, she got a calendar from 1995!",
            f"Yo {member.mention}. Your mama is so sweet, even sugar calls her 'Mom'!",
            f"Yo {member.mention}. Your mom is so caring, when you're sick, she can make chicken soup from scratch while solving a Rubik's Cube blindfolded!",
            f"Yo {member.mention}. Yo mama is so funny, she could make a grumpy cat smile!",
        ]

        random_joke = random.choice(mom_jokes)
        await ctx.send(random_joke)

    @commands.command(name="ping", description="tells the latency of the bot.")
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000) # This rounds the latency and convert it into ms
        await ctx.send(f"Pong! I got a ping of {latency}ms.")
    
    @commands.command(name="purge", description="deletes messages in bulk")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, *, amount: int = 3):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"I have deleted {amount} message(s).")
        await ctx.channel.purge(limit=1)




def setup(bot):
    bot.add_cog(Utilities(bot))