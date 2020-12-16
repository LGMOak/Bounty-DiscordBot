# BountyBot

>An all in one utility bot for discord

 Bounty - A discord bot written in python with an abundance of features. It is  your all in one bot including moderation, music, fun, api comands and much more

## Installation

```sh
git clone https://github.com/Lukkkim/BountyBot
```

## Commands

Some commands to get you started
```
+help to show all commands and get a general feel
+marco to get a response (A ping command)
+uptime to display bot uptime
Speak in DM to initate cleverbot and chat with Bounty
+miniask[inquiry] to get answers to a question
+server to get an invite link to Bounty official development server
and many many more
```
Commands are split into cogs for organisation

```python
general
admin
events
owner
cleverbot
music
fun
wolfram
```

## Logging

Log Levels are in config/config.json

There are many levels of data logging, these levels are:

* CRITICAL - Only failures
* ERROR - Errors, Default Setting -
* WARNING - Warnings, possible faults
* INFO - Most Information
* DEBUG - Everything
* NONE - Does not log


## Development setup

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```sh
pip install discord.py[voice] praw datetime youtube_dl asyncio pprint discord wolframalpha grequests
```

## Release History
* 0.1.9
    * Updated to v1.5 discord API
    * General refinements
    * Many bug fixes
* 0.1.8
    * Many bug fixes
    * Added roll and rollstats command
    * Converted from discord.py[rw] to discord.py
* 0.1.7
    * Added Logging
    * Fixed a bug where you could add an owner twice
* 0.1.6
    * Added xkcd command 
    * Fixed music cog commands 
    * small changes to code
* 0.1.5
    * Allows you to have more than one bot owner. Add user ID to config/owners.json
    * Added bot info commands
    * Fixed Cleverbot... Again
* 0.1.4
    * Adding Separate File for API Keys (Discord, Cleverbot, Wolfram Alpha)
    * Made it so that cleverbot doesnt kill the bot when you talk to it.
    * Overhauled voice module
* 0.1.3
    * Minor changes
    * Code neatened 
    * Github established
    * 24/7 hosting
* 0.1.2
    * Added a few more (ultimately useless) apis/commands:
	* Dad jokes
	* advice
	* Chuck Norris
* 0.1.1
    * Wolfram cog successfully added
    * Reworked Reddit command so any subreddit can be searched
	* Casino cog started
* 0.1.0
    * Successfully fully converted to python3.7
    * Added Cleverbot Integration
    * Music cog added
* 0.0.1
    * Work in progress
    * Archived

## Meta

Lukim – [@Reddit](https://reddit.com/u/LukimOfficial)

Tis Tiller - [@Reddit](https://www.reddit.com/user/TissleTassle)

## Contributing

1. Fork it (<https://github.com/Lukkkim/BountyBot/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -m 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
