import discord
from discord.ext import commands
import asyncio, re, pprint, random, colorsys, requests, json
import wolframalpha

keys = json.load(open("config/keys.json"))
appid = keys['wolfram_appid']

class Wolfram(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_result = None
        self.app_id = appid

        # our wolfram alpha client
        self.wolfram_client = wolframalpha.Client(self.app_id)

        # Globals for message removal
        self.messageHistory = set()
        self.compute_message_history = set()
        self.previousQuery = ''

        # Fun strings for invalid queries
        self.invalidQueryStrings = ["Nobody knows.", "It's a mystery.", "I have no idea.", "No clue, sorry!",
                                    "I'm afraid I can't let you do that.", "Ask someone else.",
                                    "It is illegal for me to have an opinion", "the government has blocked me sharing this information"
                                    "That's illegal for me to answer.", "I don't know."]

        # Regex for IP address
        self.ipv4_regex = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
        self.ipv6_regex = re.compile(
            r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))')

    async def on_ready(self):
        print("Wolfram Cog was loaded sucessfully!")

    @commands.command()
    async def ask(self, ctx, message, *, query):
        """
        Ask Bounty any question. use for open questions
        """
        computing_message = await ctx.send(":wolf: Computing '" + query + "' :computer: :thought_balloon: ...")
        self.compute_message_history.add(computing_message)
        await ctx.message.channel.trigger_typing()
        # Expanded query
        if len(query) > 1:
            if query == "are you gay":
                new_message = await ctx.send(embed=discord.Embed(title="Result",
                                                                 description=":gay_pride_flag: Sure", color=0x9700a5))
                self.messageHistory.add(new_message)
                await computing_message.edit(content=computing_message.content + "Finished! " +
                                                     ctx.message.author.mention + " :checkered_flag:")
                return
            try:
                res = self.wolfram_client.query(query, location="perth")
            except Exception as e:
                await ctx.send('I encountered an exception in the request: "' + str(e) + '"')
                return
            self.last_result = res
            if self.count_pods(res) > 0:
                if "geoIP" in str(res):
                    self.messageHistory.add(await ctx.send("_(this pod has geoIP info, so has been redacted)_"))
                    return
                n = 0
                for pod in res.pods:
                    await self.output_pod(ctx, pod, n)
                    n += 1

                await computing_message.edit(content=computing_message.content + "Finished! " +
                                                     ctx.message.author.mention + " :checkered_flag:")
                if self.count_pods(res) > 3:
                    await ctx.send(":thumbsup: :checkered_flag:  All done!")

            else:
                await ctx.send(random.choice(self.invalidQueryStrings))

                if self.count_pods(res) > 0 and len(list(res.pods)) - 2 > 0:
                    await computing_message.edit(content=computing_message.content + "Finished! " +
                                                         ctx.message.author.mention + " :checkered_flag: (" +
                                                         str(len(list(res.pods)) - 2) +
                                                         " more result pods available, rerun query using +asklong+)")
                else:
                    await computing_message.edit(content=
                                                 computing_message.content + "Finished! " + ctx.message.author.mention +
                                                 " :checkered_flag:")

    @commands.command(aliases=['shortask'])
    async def miniask(self, ctx, message, *, query):
        """
        Ask Bounty any question. Use for questions with a distinct answer
        """
        computing_message = await ctx.send(":wolf: Computing '" + query + "' :computer: :thought_balloon: ...")
        self.compute_message_history.add(computing_message)
        await ctx.message.channel.trigger_typing()

        try:
            # we "spoof" our location to somewhere so queries like 'monuments near me' don't reveal the location of
            # the server.
            res = self.wolfram_client.query(query, location="perth")
        except Exception as e:
            await ctx.send('I encountered an exception in the request: "' + str(e) + '".  This can happen if you send'
                                                                                     ' fancy unicode things :cry:')
            return

        if self.count_pods(res) > 0:
            result_present = 0
            pod_limit = 0

            #  WA returns a "result" pod for simple maths queries but for more complex ones
            #  it returns randomly titled ones
            for pod in res.pods:
                if pod.title == 'Result':
                    result_present = 1

            if "geoIP" in str(res):
                # Be safe.  Don't output any results that had geoIP info anywhere in them.
                self.messageHistory.add(await ctx.send("_(this has geoIP info, so has been redacted)_"))
                return

            for pod in res.pods:
                if self.has_text(pod):
                    if result_present == 1:
                        if pod.title == 'Result':
                            await self.output_pod(ctx, pod)
                    #  If no result pod is present, prints input interpretation and 1 other pod
                    #  (normally contains useful answer)
                    else:
                        if pod_limit < 2:
                            await self.output_pod(ctx, pod)
                            pod_limit += 1
        else:
            await ctx.send(random.choice(self.invalidQueryStrings))

        if self.count_pods(res) > 0 and len(list(res.pods)) - 2 > 0:
            await computing_message.edit(content=computing_message.content + "Finished! " +
                                                 ctx.message.author.mention + " :checkered_flag: (" + str(len(list(
                res.pods)) - 2) + " more result pods available, try using +ask)")
        else:
            await computing_message.edit(content=computing_message.content + "Finished! " +
                                                 ctx.message.author.mention + " :checkered_flag:")
        self.previousQuery = query

    async def output_pod(self, ctx, pod, n=0):
        """
        Output an wolfram results pod.  This will either call the `output_image_pod` or `output_text_pod` method based on its
        discretion
        :param pod: wolfram alpha results pod
        :param n: Tell me which pod (nth) of the results we're on, so the rainbowy embed color can be set correctly
        """
        # pprint.pprint(pod)
        color = colorsys.hsv_to_rgb(.82 + n * .1, 1, .65)
        color = discord.Color.from_rgb(int(255 * color[0]), int(255 * color[1]), int(255 * color[2]))
        if any(graph_pod in pod['@id'] for graph_pod in ("Image", "Plot", "Graph", "PopularityPod", "Flag",
                                                         "PopulationHistory", "NumberLine, Distribution",
                                                         "CategorizedList", "Integral", "Illustration")):
            await self.output_image_pod(ctx, pod, color)
        else:
            # output text (embed)
            if pod.text is not None:
                await self.output_text_pod(ctx, pod, color)
            else:
                try:
                    print("Failed recognizing pod of type " + pod['@id'] + ".  Falling back to assuming it's an image")
                    await self.output_image_pod(ctx, pod, color)
                except Exception:
                    pprint.pprint(pod)
                    embed = discord.Embed(
                        description="I had a problem parsing a bit of information to get what you wanted. " +
                                    " Sorry about that.")
                    embed.add_field(name="Pod type", value=pod['@id'])
                    #  embed.add_field(name="Pod values", value=str(pod['@subpod']), inline=True) #
                    #    ^--  very long and obnoxious
                    self.messageHistory.add(await ctx.send(embed=embed))

    async def output_image_pod(self, ctx, pod, color):
        """
        Output a pod's image in the discord chat.
        Some pods have multiple images (like graphs at different zoom levels) - it'll output all of them
        :param pod: a wolfram alpha pod, which has an image in it somewhere
        :param color: a discord.color set the embed color to
        """
        # output image
        # pprint.pprint(pod)
        if pod['@title'] == '':  # discord hates embeds having empty fields
            pod['@title'] = "Image"
        try:
            # there's just one image
            image_url = pod['subpod']['img']['@src']
            embed = discord.Embed(color=color, title=pod['@title'])
            embed.set_image(url=image_url)
            self.messageHistory.add(await ctx.send(embed=embed))
        except TypeError:
            # there's a list of multiple images
            for subsubpod in pod['subpod']:
                image_url = subsubpod['img']['@src']
                embed = discord.Embed(color=color, title=pod['@title'])
                embed.set_image(url=image_url)
                self.messageHistory.add(await ctx.send(embed=embed))

    async def output_text_pod(self, ctx, pod, color):
        """
        Output a pod's text in the discord chat.
        This will truncate text that is too long (discord throws errors if your message is huge)
        This also cleans pods of any IP addresses, because that's a good thing to do.
        At a different point in the program, we detect if the word "geoIP" appears anywhere in the response,
        cancelling all normal output if it does.
        :param pod:
        :param color:
        """
        text = pod.text
        text = text.replace("Wolfram|Alpha", "Bounty")
        text = text.replace("Wolfram", "Wolf")
        text = re.sub(self.ipv4_regex, "IP Redacted", text)
        text = re.sub(self.ipv6_regex, "IP Redacted", text)
        if len(text) > 1950:
            text = text[:1950]
            await ctx.send("Truncated:")
        if pod['@title'] == "Input interpretation" or pod['@title'] == "Input":
            color = 0xffbcf2
            embed = discord.Embed(title=pod['@title'], description=text, color=color)
        elif pod['@title'] == "Result":
            color = 0x9700a5
            embed = discord.Embed(title=pod['@title'], description=text, color=color)
        else:
            embed = discord.Embed(title=pod['@title'], description=text, color=color)

        # On exotic pod types, indicate what their id is.  This is so if you want it to be imagified, you can request
        #   it to be included in the `graphable` list in output_pod.
        # If the id is just the title, but camel cased, which it often is, then don't bother with this as it's
        #   just clutter when you could guess it
        maybe_id = ''.join(x for x in pod['@title'].title() if not x.isspace())
        if pod['@id'] != maybe_id and not pod['@id'].startswith(maybe_id):
            embed.set_footer(text=pod['@id'])

        new_message = await ctx.send(embed=embed)
        self.messageHistory.add(new_message)

    def count_pods(self, res):
        """
        Count the pods in a Result object
        :param res: the result object
        :return: how many pods there are
        """
        try:
            return len(list(res.pods))
        except AttributeError:
            return 0

    def has_text(self, pod):
        """
        :param pod: wolfram results pod
        :return: whether the pod has text
        """
        try:
            return pod.text
        except AttributeError:
            return False


# add this as a cog to the bot
def setup(bot):
	bot.add_cog(Wolfram(bot))