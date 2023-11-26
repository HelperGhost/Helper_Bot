import discord
from discord.ext import bridge, commands

class Quick_Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(name="quickchannels", description="makes a server for you")
    @commands.has_permissions(administrator=True)
    async def quickchannels(self, ctx):

        await ctx.respond("Making Channels...")

        support_category = await ctx.guild.create_category_channel("🧰︱Support")
        general_category = await ctx.guild.create_category_channel("🌐︱General")
        community_category = await ctx.guild.create_category_channel("👥︱Community")
        events_category = await ctx.guild.create_category_channel("🎊︱Events")
        music_category = await ctx.guild.create_category_channel("📻︱Music")
        voice_category = await ctx.guild.create_category_channel("🔊︱Voice Channels")
        staff_category = await ctx.guild.create_category_channel("🚨︱Staff")
        logs_category = await ctx.guild.create_category_channel("📀︱Logs")
        closed_tickets_category = await ctx.guild.create_category_channel("🎫︱Closed Tickets")

        await staff_category.set_permissions(ctx.guild.default_role, view_channel=False)
        await logs_category.set_permissions(ctx.guild.default_role, view_channel=False)
        await closed_tickets_category.set_permissions(ctx.guild.default_role, view_channel=False)

        if support_category:
            ticket_channel = await ctx.guild.create_text_channel("🎫〢make-a-ticket", category=support_category)

        if general_category:
            rules_channel = await ctx.guild.create_text_channel("📜〢rules", category=general_category)
            announcements_channel = await ctx.guild.create_text_channel("📢〢announcements", category=general_category)
            boost_channel = await ctx.guild.create_text_channel("🔮〢server-boost", category=general_category)
            levelups_channel = await ctx.guild.create_text_channel("🦉〢level-ups", category=general_category)

        if community_category:
            general_channel = await ctx.guild.create_text_channel("💬〢general-chat", category=community_category)
            cmds_channels = await ctx.guild.create_text_channel("🤖〢bot-commands", category=community_category)
            memes_channel = await ctx.guild.create_text_channel("🐸〢memes", category=community_category)

        if events_category:
            events_announcements = await ctx.guild.create_text_channel("✨〢events_announcements", category=events_category)
            giveaways = await ctx.guild.create_text_channel("🎉〢giveaways", category=events_category)

        if music_category:
            queue_channel = await ctx.guild.create_text_channel("🥁〢music-queue", category=music_category)
            music_channel = await ctx.guild.create_voice_channel("🎸〢Music", category=music_category)

        if voice_category:
            afk_channel = await ctx.guild.create_voice_channel("💤〢AFK", category=voice_category)
            lounge_channel = await ctx.guild.create_voice_channel("🎧〢Lounge", category=voice_category)
            stream_channel = await ctx.guild.create_voice_channel("📺〢Stream", category=voice_category)
            
        if staff_category:
            staff_announcements_channel = await ctx.guild.create_text_channel("📣〢staff-announcemets", category=staff_category)
            discord_updates_channel = await ctx.guild.create_text_channel("📥〢discord-updates", category=staff_category)
            staff_chat_channel = await ctx.guild.create_text_channel("🚨〢staff-chat", category=staff_category)
            staff_cmds_channel = await ctx.guild.create_text_channel("🤖〢staff-cmds", category=staff_category)
            staff_vc_channel = await ctx.guild.create_voice_channel("🔊〢Staff VC", category=staff_category)

        if logs_category:
            message_logs = await ctx.guild.create_text_channel("📂〢message-logs", category=logs_category)
            member_logs = await ctx.guild.create_text_channel("📂〢member-logs", category=logs_category)
            vc_logs = await ctx.guild.create_text_channel("📂〢vc-logs", category=logs_category)
            server_logs = await ctx.guild.create_text_channel("📂〢server-logs", category=logs_category)
            misc_logs = await ctx.guild.create_text_channel("📂〢misc-logs", category=logs_category)

def setup(bot):
    bot.add_cog(Quick_Server(bot))      
