from discord.ext import commands
import random, discord

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        # As the prefixes are callable, you can not have a static list of prefixes to respond to for help.
        # To remedy that, every time someone says something the bot can see, it gets a list of prefixes
        # available in that specific message situation. It then searches its list for all available prefixes
        # and responds if they are available. Non-statically, and with any number of prefixes.
        
        prefixes = self.bot.command_prefix(self.bot, message)
        for prefix in prefixes:
            if message.content == f"{prefix}help":
                await message.channel.send('Sending you list of commands via DM.')

def setup(bot):
    bot.add_cog(Events(bot))
