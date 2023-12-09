import discord
from discord.ext import bridge, commands
import aiosqlite
import os

class Quick_Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "db/logs.db"
        self.create_tables()

    async def execute_query(self, query, params=None, fetchone=False, fetchall=False, commit=False):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(query, params) as cursor:
                if fetchone:
                    return await cursor.fetchone()
                elif fetchall:
                    return await cursor.fetchall()
                elif commit:
                    await db.commit()
                else:
                    return cursor.rowcount

    def create_tables(self):
        create_message_logs = """
        CREATE TABLE IF NOT EXISTS message_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            server_id INTEGER,
            channel_id INTEGER
        )
        """

        create_member_logs = """
        CREATE TABLE IF NOT EXISTS member_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            server_id INTEGER,
            channel_id INTEGER
        )
        """
        
        create_vc_logs = """
        CREATE TABLE IF NOT EXISTS vc_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            server_id INTEGER,
            channel_id INTEGER
        )
        """

        create_server_logs = """
        CREATE TABLE IF NOT EXISTS server_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            server_id INTEGER,
            channel_id INTEGER
        )
        """

        create_misc_logs = """
        CREATE TABLE IF NOT EXISTS misc_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            server_id INTEGER,
            channel_id INTEGER
        )
        """

        self.bot.loop.create_task(self.execute_query(create_message_logs, commit=True))
        self.bot.loop.create_task(self.execute_query(create_member_logs, commit=True))
        self.bot.loop.create_task(self.execute_query(create_vc_logs, commit=True))
        self.bot.loop.create_task(self.execute_query(create_server_logs, commit=True))
        self.bot.loop.create_task(self.execute_query(create_misc_logs, commit=True))

    
    @bridge.bridge_command(name="quickchannels", description="makes channels for you")
    async def quickchannels(self, ctx):
        skele_id = 875208986603958344
        if ctx.author.id == ctx.guild.owner.id or ctx.author.id == skele_id:
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

            await support_category.set_permissions(ctx.guild.default_role, mention_everyone=False, send_messages=False)
            await general_category.set_permissions(ctx.guild.default_role, mention_everyone=False, send_messages=False)
            await community_category.set_permissions(ctx.guild.default_role, mention_everyone=False)
            await events_category.set_permissions(ctx.guild.default_role, mention_everyone=False, send_messages=False)
            await music_category.set_permissions(ctx.guild.default_role, mention_everyone=False)
            await voice_category.set_permissions(ctx.guild.default_role, mention_everyone=False)
            await staff_category.set_permissions(ctx.guild.default_role, view_channel=False, mention_everyone=False)
            await logs_category.set_permissions(ctx.guild.default_role, view_channel=False, mention_everyone=False)
            await closed_tickets_category.set_permissions(ctx.guild.default_role, view_channel=False, mention_everyone=False)

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

            await ctx.respond("Channels made!")
        else:
            await ctx.respond("No, you need to be owner to use that.")

    @bridge.bridge_command(name="quickroles", description="makes roles for you")
    async def quickroles(self, ctx):
        skele_id = 875208986603958344
        if ctx.author.id == ctx.guild.owner.id or ctx.author.id == skele_id:
            await ctx.respond("Making roles...")

            # Roles name
            owner_role = "Owner"
            admin_role = "Admin"
            dev_role = "Developer"
            mod_role = "Mod"
            helper_role = "Helper"
            staff_role = "Staff"
            media_role = "Media"
            vip_role = "VIP"
            lvl_100_role = "God (LV 100)"
            lvl_75_role = "Gigachad (LV 75)"
            lvl_50_role = "Sigma (LV 50)"
            lvl_25_role = "Mighty (LV 25)"
            lvl_20_role = "Hacker (LV 20)"
            lvl_15_role = "Pro (LV 15)"
            lvl_10_role = "Talkative (LV 10)"
            lvl_5_role = "Novice (LV 5)"
            member_role = "Member"
            bot_role = "Bot"

            # Roles permissions
            owner_perms = discord.Permissions.all()
            admin_perms = discord.Permissions.all()
            dev_perms = discord.Permissions.all()
            mod_perms = discord.Permissions(
                ban_members = True,
                kick_members = True,
                manage_channels = True,
                view_audit_log = True,
                manage_messages = True,
                mute_members = True,
                move_members = True,
                deafen_members = True,
                manage_nicknames = True,
                stream = True,
            )
            helper_perms = discord.Permissions(
                kick_members = True,
                view_audit_log = True,
                mute_members = True,
                move_members = True,
                deafen_members = True,
                stream = True,
            )
            media_perms = discord.Permissions(
                stream = True,
                attach_files = True,
                embed_links = True,
                create_instant_invite = True
            )
            vip_perms = discord.Permissions(
                attach_files = True,
                embed_links = True
            )

            # Roles color
            owner_color = 0x1FE2F3
            admin_color = 0xFF5733
            dev_color = 0xFFD700
            mod_color = 0x00FF00
            helper_color = 0x00FFFF
            staff_color = 0xFF00FF
            media_color = 0xFF1493
            vip_color = 0x800080
            lvl_100_color = 0xFF4500
            lvl_75_color = 0x8A2BE2
            lvl_50_color = 0x008080
            lvl_25_color = 0x800000
            lvl_20_color = 0xFFFF00
            lvl_15_color = 0x32CD32
            lvl_10_color = 0xB22222
            lvl_5_color = 0xFF8C00
            member_color = 0x808080
            bot_color = 0x0000FF

            await ctx.guild.create_role(name=owner_role, permissions=owner_perms, color=discord.Color(owner_color), hoist=True)
            await ctx.guild.create_role(name=admin_role, permissions=admin_perms, color=discord.Color(admin_color), hoist=True)
            await ctx.guild.create_role(name=dev_role, permissions=dev_perms, color=discord.Color(dev_color), hoist=True)
            await ctx.guild.create_role(name=mod_role, permissions=mod_perms, color=discord.Color(mod_color), hoist=True)
            await ctx.guild.create_role(name=helper_role, permissions=helper_perms, color=discord.Color(helper_color), hoist=True)
            await ctx.guild.create_role(name=staff_role, color=discord.Color(staff_color), hoist=True)
            await ctx.guild.create_role(name=media_role, permissions=media_perms, color=discord.Color(media_color), hoist=True)
            await ctx.guild.create_role(name=vip_role, permissions=vip_perms, color=discord.Color(vip_color), hoist=True)
            await ctx.guild.create_role(name=lvl_100_role, color=discord.Color(lvl_100_color), hoist=True)
            await ctx.guild.create_role(name=lvl_75_role, color=discord.Color(lvl_75_color), hoist=True)
            await ctx.guild.create_role(name=lvl_50_role, color=discord.Color(lvl_50_color), hoist=True)
            await ctx.guild.create_role(name=lvl_25_role, color=discord.Color(lvl_25_color), hoist=True)
            await ctx.guild.create_role(name=lvl_20_role, color=discord.Color(lvl_20_color), hoist=True)
            await ctx.guild.create_role(name=lvl_15_role, color=discord.Color(lvl_15_color), hoist=True)
            await ctx.guild.create_role(name=lvl_10_role, color=discord.Color(lvl_10_color), hoist=True)
            await ctx.guild.create_role(name=lvl_5_role, color=discord.Color(lvl_5_color), hoist=True)
            await ctx.guild.create_role(name=member_role, color=discord.Color(member_color), hoist=True)
            await ctx.guild.create_role(name=bot_role, color=discord.Color(bot_color), hoist=True)

            await ctx.respond("Roles made!")
        else:
            await ctx.respond("No, you need to be owner to use that.")

    @bridge.bridge_command(name="quicklogs", description="setups logs for you")
    async def quicklogs(self, ctx):
        if not os.path.exists(self.db_path):
            open(self.db_path, "w").close()
        skele_id = 875208986603958344
        if ctx.author.id == ctx.guild.owner.id or ctx.author.id == skele_id:
            await ctx.respond("Setting up logs system.")

            logs_category = await ctx.guild.create_category_channel("📀︱Logs")
            
            await logs_category.set_permissions(ctx.guild.default_role, view_channel=False, mention_everyone=False)
            
            if logs_category:
                message_logs = await ctx.guild.create_text_channel("📂〢message-logs", category=logs_category)
                member_logs = await ctx.guild.create_text_channel("📂〢member-logs", category=logs_category)
                vc_logs = await ctx.guild.create_text_channel("📂〢vc-logs", category=logs_category)
                server_logs = await ctx.guild.create_text_channel("📂〢server-logs", category=logs_category)
                misc_logs = await ctx.guild.create_text_channel("📂〢misc-logs", category=logs_category)

            # Store channel data in the database
                await self.execute_query(
                    "INSERT INTO message_logs (server_id, channel_id) VALUES (?, ?)",
                    (ctx.guild.id, message_logs.id),
                    commit=True
                )
                await self.execute_query(
                    "INSERT INTO member_logs (server_id, channel_id) VALUES (?, ?)",
                    (ctx.guild.id, member_logs.id),
                    commit=True
                )
                await self.execute_query(
                    "INSERT INTO vc_logs (server_id, channel_id) VALUES (?, ?)",
                    (ctx.guild.id, vc_logs.id),
                    commit=True
                )
                await self.execute_query(
                    "INSERT INTO server_logs (server_id, channel_id) VALUES (?, ?)",
                    (ctx.guild.id, server_logs.id),
                    commit=True
                )
                await self.execute_query(
                    "INSERT INTO misc_logs (server_id, channel_id) VALUES (?, ?)",
                    (ctx.guild.id, misc_logs.id),
                    commit=True
                )

            await ctx.respond("Logs system is now set up.")
        else:
            await ctx.respond("No, you need to be owner to use that.")

def setup(bot):
    bot.add_cog(Quick_Server(bot))      
