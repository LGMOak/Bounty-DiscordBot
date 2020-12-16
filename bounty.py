#---------------------------------------------------------------
import discord
import asyncio
import logging
import datetime
from discord import Intents
from discord.ext import commands
from json import load as jsonload

# This gets the app keys from config/keys.json
keys = jsonload(open("config/keys.json"))

# This gets configuration information
config = jsonload(open("config/config.json"))
logLevel = config["logLevel"]

def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Notice how you can use spaces in prefixes. Try to keep them simple though.
    prefixes = '!', '-'

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow + to be used in DMs
        return '!'

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)
#---------------------------------------------------------------

bot = commands.Bot(command_prefix=get_prefix, description='Bounty by Lukim#6823', pm_help = True, intents=Intents.all())
# Should be pretty straightfoward, this is what should happen when the bot is turned on.

# This is a test

# -----------------------------------------
# Logging Configuration
class _fileStream():
    def __init__(self, bot):
        self.bot = bot
    def write(self, stdin):
        time = datetime.datetime.now()
        date = f"{time.year}-{time.month}-{time.day}"
        try:
            with open(f"logs/{date}", 'a') as log:
                log.write(stdin)
        except FileNotFoundError:
            with open(f"logs/{date}", 'w') as log:
                log.write(stdin)

stream = _fileStream(bot)

if not logLevel == "NONE":

    levels = {"CRITICAL": 50, "ERROR": 40, "WARNING": 30, "INFO": 20, "DEBUG": 10}
    for x in levels:
        if logLevel == x:
            logLevelNum = levels[x]
    logger = logging.getLogger('discord')
    logger.setLevel(logLevelNum)
    handler = logging.StreamHandler(stream=stream)
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

def botLog(text=None):
    for x in range(5):
        if x == 2:
            txt = text
        else:
            txt = ""
        logger.critical(txt)


# -----------------------------------------
# Ready Event
@bot.event
async def on_ready():
    print("-----------------")
    print(f"""
    Bounty  Copyright (C) 2019  Lukim#6823
    This program comes with ABSOLUTELY NO WARRANTY; for details, see LICENSE.
    This is free software, and you are welcome to redistribute it
    under certain conditions; see LICENSE for details.
    """)
    print("Discord.py Version {}".format(discord.__version__))
    print("Logged in as:\n\tUser ID: {}\n\tUser Name: {}#{}".format(bot.user.id, bot.user.name, bot.user.discriminator))
    print("Running in {} servers!".format(len(list(bot.guilds))))
    print("Logging Level: {}".format(logLevel))
    print("Ready for use!")
    print("-----------------")
    while True:
        # A status can be added with (status=discord.Status.*)
        # Statuses include: dnd, online, offline, idle, invisible
        await bot.change_presence(activity=discord.Game(name='Bounty by Lukim™'))
        await asyncio.sleep(152)
        await bot.change_presence(activity=discord.Game(name='+help for commands'))
        await asyncio.sleep(152)
        await bot.change_presence(activity=discord.Game(name=" in {} servers!".format(len(list(bot.guilds)))))
        await asyncio.sleep(152)
        await bot.change_presence(activity=discord.Game(name=" with {} users!".format(len(list(bot.users)))))
        await asyncio.sleep(152)
        await bot.change_presence(activity=discord.Game(name='sudo help for commands'))
        await asyncio.sleep(152)

unloaded = ["cleverbot"]
extensions = ["general", "admin", "owner", "events", "music", "fun", "wolfram"]
for extension in extensions:
    try:
        bot.load_extension(str("cogs." + extension))
    except ModuleNotFoundError:
        print(f"Bot extension: {extension} not found.")
    except Exception as ExtensionLoadFail:
        print(f"An exception has occured when trying to load an extension:\n{ExtensionLoadFail}")

print(f"Unloaded: {unloaded}")
for extension in unloaded:
    print(f"Bot extension: {extension} not loaded.")

if __name__ == "__main__":
    botLog("Attempting to start the bot.")

    bot.run(keys['discord_token'])

    botLog("Attempting to stop the bot.")
