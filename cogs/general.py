import discord
from discord.ext import commands
import json, random, praw, datetime, time

start_time = time.time()

invlink = 'https://discordapp.com/oauth2/authorize?client_id=400501965383139328&scope=bot&permissions=8'
guildlink = 'https://discord.gg/Y4uXWKB'
votelink = 'https://discordbots.org/bot/400501965383139328/vote'

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        print("General Cog was loaded sucessfully!")

    @commands.command()
    async def server(self, ctx):
        """Get invite link to official discord guild"""
        sender = ctx.message.author
        await ctx.send("{} || {}".format(sender.mention, guildlink))

    @commands.command()
    async def invite(self, ctx):
        """Get my invite link to join your sever"""
        sender = ctx.message.author
        await ctx.send("{} || {}".format(sender.mention, invlink))

    @commands.command()
    async def vote(self, ctx):
        """Vote for Bounty"""
        sender = ctx.message.author
        await ctx.send('{} remember to vote every 12 hours! || {}'.format(sender.mention, votelink))

    @commands.command(pass_context=True)
    async def uptime(self, ctx):
        '''Displays bot uptime'''
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(colour=0xff8000)
        embed.add_field(name="Bot Uptime", value=text)
        embed.set_footer(text="Bounty by Lukim")
        try:
        	await ctx.send(embed=embed)
        except discord.HTTPException:
        	await ctx.send("Current uptime: " + text)
        

    @commands.command(aliases=['ping'])
    async def marco(self, ctx):
        """Marco Polo (A ping command)"""
        bot = ctx.bot
        embed = discord.Embed(colour=0xffff00)
        embed.add_field(name="Marco Polo!", value="Polo! **({} s)**".format(round(bot.latency, 3)))
        embed.set_footer(text="Bounty by Lukim")

        await ctx.send(embed=embed)

    @commands.command(aliases=['profile'])
    async def userinfo(self, ctx, user: discord.Member):
        """Displays user info"""
        embed = discord.Embed(title="User info", color=ctx.message.author.top_role.colour)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Name", value="{}".format(user.name), inline=False)
        embed.add_field(name="Name on server", value="{}".format(user.display_name), inline=False)
        embed.add_field(name="ID", value="{}".format(user.id), inline=False)
        embed.add_field(name="Status", value="{}".format(user.status), inline=False)
        embed.add_field(name="Playing/Activity", value="{}".format(user.activity), inline=False)
        embed.add_field(name="Join Date", value="{}".format(user.joined_at), inline=False)
        embed.add_field(name="Highest Role", value="{}".format(user.top_role), inline=False)
        embed.add_field(name="Account Created", value="{}".format(user.created_at), inline=False)
        await ctx.send(embed=embed)

    @userinfo.error
    async def info_handler(self, ctx, error):
        if error.param.name == 'user':
            await ctx.send("{} || I'm sorry sir but you need to @ someone in order for this to work".format(ctx.message.author.mention))

    @commands.command(pass_context = True)
    async def members (self, ctx):
        """Displays number of members in guild"""
        amount = len(ctx.message.guild.members)
        await ctx.send('There are ' + str(amount) + ' members.')

    @commands.command()
    @commands.has_permissions(create_instant_invite=True)
    async def serverinvite(self, ctx):
        """Creates and displays an ivite for that specific server"""
        inviteLink = await ctx.message.channel.create_invite()
        await ctx.send(inviteLink)


def setup(bot):
    bot.add_cog(General(bot))
