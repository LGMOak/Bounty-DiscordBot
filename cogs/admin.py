import discord
import random
import asyncio
from discord.ext import commands

dMember = discord.Member

class Admin(commands.Cog):
    def __init__(self, bot):
        bot.self = bot


    async def on_ready(self):
        print("Admin Cog was loaded successfully!")


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=30):
        """Mass delete messages"""
        maxPurge = 250
        sender = ctx.message.author
        if amount > maxPurge:
            await ctx.send("{} || Failed to purge messages! **(The max amount of messages you can purge is {}!)**".format(sender.mention, maxPurge))
        else:
            if amount == 1:
                await ctx.channel.purge(limit=amount)
                await asyncio.sleep(1)
                await ctx.send("{} || Sucessfully purged **1** message.".format(sender.mention))
            else:
                await ctx.channel.purge(limit=amount)
                await asyncio.sleep(1)
                await ctx.send("{} || Sucessfully purged **{}** messages.".format(sender.mention, amount))


    @purge.error
    async def clear_handler(self, ctx, error):
        sender = ctx.message.author
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("{} || Failed to purge messages! **(You don't have permissions to use this command!)**".format(sender.mention))

    @commands.command()
    @commands.has_permissions(view_audit_log=True)
    async def viewlogs(self, ctx, amount=30):
        """Views a number of audit logs."""
        returnval = f"```Entry ID    -   Performer   -   Action  -   Target"
        async for entry in ctx.message.guild.audit_logs(limit=amount):
            if str(entry.action) in ["AuditLogAction.kick", "AuditLogAction.ban", "AuditLogAction.member_role_update"]:
                returnval += f"\n{entry.id} - {entry.user.name}#{entry.user.discriminator} - {entry.action} - {entry.target.name}#{entry.target.discriminator}"
            else:
                returnval += f"\n{entry.id} - {entry.user.name}#{entry.user.discriminator} - {entry.action}"
        returnval += "```"
        await ctx.send(returnval)
    
    @viewlogs.error
    async def log_handler(self, ctx, error):
        sender = ctx.message.author
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("{} || Failed to read audit logs! **(You don't have permissions to use this command!)**".format(sender.mention))

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: dMember, override=""):
        """kicks members"""
        sender = ctx.message.author
        if sender.top_role == user.top_role:
            if sender == user and override != "override":
                await ctx.send("{} || You can't kick yourself!".format(sender.mention))
                await ctx.send(f"Well I mean you could. Put override on the end of the command to kick yourself.")
            elif sender == user and override == "override":
                try:
                    await ctx.send(f"{sender.mention} is kicking themself.")
                    await dMember.kick(user, reason=None)
                except Exception as e:
                    await ctx.send(f"Error: {e}")
            else:
                await ctx.send("{} || Can't kick someone who has the same role as yours.".format(sender.mention))
        else:
            if sender.top_role < user.top_role:
                await ctx.send("{} || Can't kick a role that's higher than yours!".format(sender.mention))
            else:
                await ctx.send("{} || Sucessfully kicked **{}**".format(sender.mention, user))
                await dMember.kick(user, reason=None)

    @kick.error
    async def kick_handler(self, ctx, error):
        sender = ctx.message.author
        if error.param.name == 'user':
            await ctx.send("{} || You need to mention someone to kick.".format(sender.mention))
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("{} || You don't have the permissions to use that command!".format(sender.mention))

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: dMember, *, banReason):
        """bans members"""
        sender = ctx.message.author
        if sender.top_role == user.top_role:
            await ctx.send("{} || Can't ban someone who has the same role as yours.".format(sender.mention))
        else:
            if sender.top_role < user.top_role:
                await ctx.send("{} || Can't ban a role that's higher than yours!".format(sender.mention))
            else:
                if sender == user:
                    await ctx.send("{} || You can't ban yourself!".format(sender.mention))
                else:
                    await ctx.send("{} || Sucessfully banned **{}** for {}".format(sender.mention, user, banReason))
                    await dMember.ban(user, reason=banReason)

    @ban.error
    @commands.has_permissions(ban_members=True)
    async def ban_handler(self, ctx, error):
        sender = ctx.message.author
        if error.param.name == 'user':
            await ctx.send("{} || You need to mention someone to ban.".format(sender.mention))
        if error.param.name == 'banReason':
            await ctx.send("{} || You need to give a reason to ban that user.".format(sender.mention))
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("{} || You don't have the permissions to use that command!")

def setup(bot):
    bot.add_cog(Admin(bot))