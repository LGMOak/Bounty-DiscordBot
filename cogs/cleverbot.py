import discord
import asyncio
import requests
import json

keys = json.load(open("config/keys.json"))

class Cleverbot(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def on_ready(self):
		print("Cleverbot Cog was loaded sucessfully!")

	async def on_message(self, message):
		if not message.author.bot and (message.guild == None or keys['cleverbot_user'] in message.mentions):
			await message.channel.trigger_typing()
			txt = message.content.replace(message.guild.me.mention,'') if message.guild else message.content
			r = json.loads(requests.post('https://cleverbot.io/1.0/ask', json={'user':keys['cleverbot_user'], 'key':keys['cleverbot_key'], 'nick':'bounty', 'text':txt}).text)
			await message.channel.trigger_typing()
			if r['status'] == 'success':
				await message.channel.send(r['response'] )

requests.post('https://cleverbot.io/1.0/create', json={'user':keys['cleverbot_user'], 'key':keys['cleverbot_key'], 'nick':'bounty'})

def setup(bot):
    bot.add_cog(Cleverbot(bot)) 
