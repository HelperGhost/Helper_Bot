Token = "ENTER YOUR TOKEN HERE"
import nextcord
from nextcord.ext import commands, tasks
import random

bot = commands.Bot(command_prefix="h!", intents=nextcord.Intents.all())
statuses = ["Recreated By .wuid", "h!help", "dsc.gg/binarybitlab", "dsc.gg/skelescommunity"]

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        command = ctx.command
        usage = f"Usage: `{ctx.prefix}{command.name} {command.signature}`"
        await ctx.send(f"Missing required arguments. {usage}")


@tasks.loop(minutes=5)
async def change_status():
    await bot.change_presence(activity=nextcord.Game(name=random.choice(statuses)))

bot.load_extension('cogs-helper.Moderation')
bot.load_extension('cogs-helper.Utilities')
bot.load_extension('cogs-helper.logs')
bot.load_extension('cogs-helper.Quick-Server')
bot.remove_command("help")
@bot.command(name='help', aliases=['commands'], help="**No One Can Help You Now.....**")
async def help_command(ctx, *, command_name=None):
    if command_name:
        command = bot.get_command(command_name)
        if command:
            # Display specific command help
            embed = nextcord.Embed(title=f"Help for `{command.name}`", description=command.help, color=nextcord.Color.blue())
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Command '{command_name}' not found.")
    else:
        # Display general help for all commands
        embed = nextcord.Embed(title="Command List and Help", color=nextcord.Color.green())

        for cog in bot.cogs.values():
            if len(cog.get_commands()) > 0:
                command_list = '\n'.join([f"`{cmd.name}` - {cmd.short_doc}" for cmd in cog.get_commands()])
                embed.add_field(name=f"{cog.qualified_name} Commands", value=command_list, inline=False)

        embed.set_footer(text=f"Use '{ctx.prefix}help [command]' for more information on a specific command.")
        await ctx.send(embed=embed)

bot.run(Token)
