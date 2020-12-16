import discord
from discord.ext import commands
from random import randint
import json, random, requests, praw, datetime, time, urllib.request, io, os, aiohttp

data = json.load(open("config/reddit_data.json"))

def generate_image():
    request = requests.get('http://inspirobot.me/api?generate=true')
    if request.status_code != 200:
        return "OFFLINE"
    else:
        return request.text

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    async def on_ready(self):
        print("Fun Cog was loaded sucessfully!")

    @commands.command()
    async def hug(self, ctx, user: discord.Member):
        """give someone a hug"""
        sender = ctx.message.author
        if sender == user:
            await ctx.send("{} gave.. Aww, you can't hug yourself!".format(sender.mention), file=discord.File('images/hugging_gifs/unabletofinduser.gif'))
        else:
            # Array used to get a random hugging gif from the images\hugging_gifs folder.
            hugginggifs = [
                discord.File('images/hugging_gifs/d69b8ce822eac0d007aeeb26228e8a50.gif'),
                discord.File('images/hugging_gifs/hugtime.gif'),
                discord.File('images/hugging_gifs/RevolvingWigglyDikkops-size_restricted.gif'),
                discord.File('images/hugging_gifs/Tumblrshit.gif'),
                discord.File('images/hugging_gifs/V47M1S4.gif'),
                discord.File('images/hugging_gifs/F2805f274471676c96aff2bc9fbedd70.gif')
            ] 
            await ctx.send("{} gave {} a hug!".format(sender.mention, user.mention), file=random.choice(hugginggifs))


    @hug.error # Error handling
    async def hug_handler(self, ctx, error):
        sender = ctx.message.author
        if error.param.name == 'user': # Finds the missing parameter (argument) of your command.
            await ctx.send("{} gave... Hang on a minute, I think you forgot to mention someone to hug.".format(sender.mention), file=discord.File('images/hugging_gifs/unabletofinduser.gif'))

    @commands.command(aliases=['8ball']) # Pretty striaghtforward, makes it to where the command can be ran using $8ball intead of $eightball
    async def eightball(self, ctx, args):
        """Magic 8ball!"""
        possibleresponses = [
            "Yes.",
            "Sure, why not?",
            "Without a doubt B)",
            "You may rely on it.",
            "Yeah, probably.",
            "I don't feel like answering right now. Try again later.",
            "Cannot predict now.",
            "Buzz off.",
            "Fuck no!",
            "Nope!",
            "My reply is no.",
            "My sources say no, and fuck off.",
            "Very doubtful."
        ]

        await ctx.send("{} :8ball: || ".format(ctx.message.author.mention) + random.choice(possibleresponses))

    @eightball.error
    async def eightball_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'args':
                await ctx.send("{} :8ball: || You need to ask a question. Any question!".format(ctx.message.author.mention))

    @commands.command()
    async def reddit(self, ctx, *, subreddit: str):
        """Random Hot post from desired subreddit"""

        reddit = praw.Reddit(client_id=data['clientid'],
                             client_secret=data['clientsecret'],
                             user_agent=data['useragent']) 
        subreddit = reddit.subreddit(subreddit)

        await ctx.message.channel.trigger_typing()
        
        # Declaring The variables that determine what post to display and what the current post iteration is at.
        pick=random.randrange(1,21)
        current=1

        # Iterate (loop) over the top 20 items in 'hot category' to select a correct (non stickied) choice.
        for submission in subreddit.hot(limit=20):

            # If the current iteration is the correct selection but it is also a stickied, increase the correct post's rank by one.
            if current == pick and submission.stickied:
                pick += 1
                pass

            # If the current iteration is the correct selection (specifically after the previous if).
            if current == pick:

                embed = discord.Embed(title=submission.title, color=0xff8040, url=submission.shortlink)
                embed.set_image(url=submission.url) # This makes the image of the reddit post appear on the embed.
                embed.set_footer(text='Served hot from r/' + subreddit.display_name)

                await ctx.send(embed=embed)
                break

            # Else, Reiterate over the next post to check for the variables.
            else:
                current += 1
                pass

    @commands.command()
    async def inspire(self, ctx):
        '''Become inspired with AI generated inspirtational quotes'''
        await ctx.message.channel.trigger_typing()
        image = generate_image()
        e = discord.Embed(title="Inspirational Quote")
        e.set_image(url=image)
        e.set_footer(text="Powered by inspirobot.me")
        await ctx.send(embed=e)

    @commands.command(aliases=['f', 'F'])
    async def ftopayrespects(self, ctx):
        """send F to pay respects"""
        sender = ctx.message.author
        hearts = [
            ':heart:',
            ':purple_heart:',
            ':blue_heart:',
            ':green_heart:'
        ]
        await ctx.send("{} Has paid their respects {}".format(sender.mention, random.choice(hearts)))

    @commands.command()
    async def pinged(self, ctx):
        """who pinged you?!"""
        await ctx.send(file=discord.File('images/Tenor.gif'))

    @commands.command(pass_context = True)
    async def say(self, ctx, *args):
        '''Make Bounty repeat your messages'''
        mesg = ' '.join(args)
        await ctx.message.delete()
        await ctx.send(mesg)

    @commands.command(pass_context=True)
    async def tts(self, ctx, *args):
        '''Make Bounty repeat your messages, in tts'''
        mesg = ' '.join(args)
        await ctx.message.delete()
        await ctx.send(mesg, tts=True)

    @commands.command(pass_context=True)
    async def chucknorris(self, ctx):
        """Displays random Chuck Norris Joke (WARNING: Very 2009 humour)"""
        url = 'https://api.chucknorris.io/jokes/random'
        jokeJSON = requests.get(url).json()['value']
        await ctx.send(jokeJSON)

    @commands.command(pass_context=True)
    async def advice(self, ctx):
        """Dislays advice to help you in your life"""
        url = 'https://api.adviceslip.com/advice'
        r = requests.get(url).json()
        advice = {
        'advice' : r['slip']['advice']
        }
        await ctx.send(advice['advice'])

    @commands.command(pass_context=True)
    async def dadjoke(self, ctx):
        """Generates random dad joke"""
        url = 'https://icanhazdadjoke.com/'
        joke = requests.get(url, headers={"Accept":'application/json '}).json()
        await ctx.send(joke['joke'])

    @commands.command()
    async def lmgtfy(self, ctx, *, search_terms : str):
        """Creates a lmgtfy link"""
        search_terms = search_terms.replace(" ", "+")
        await ctx.send("https://lmgtfy.com/?q={}".format(search_terms))

    @commands.command(pass_context = True)
    async def bam(self, ctx, user:discord.Member=None):
        """Tells someone they're bammed."""
        if user != None:
            embed = discord.Embed(title = "Bammed!", color = 0x000000)
            embed.add_field(name = "User", value = format(user.mention) + " was bammed from the server")
            embed.add_field(name = "Reason", value = "YICKY! get this unholy member out of here! I need to wash my sin away after that.")
            embed.add_field(name = "Issuer", value = format(user.mention) + " was bammed by " + ctx.message.author.mention)
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("I'm sorry sir but you need to @ someone in order for this to work")

    @commands.command()
    async def swear(self, ctx):
        """Naughty Naugthy boy"""
        await ctx.send("https://imgur.com/gallery/Ol05I")
        
    @commands.command(pass_context = True)
    async def xkcd(self, ctx, *, entry_number=None):
        """Post a random xkcd"""

        # Creates random number between 0 and number of comics and queries xkcd
        headers = {"content-type": "application/json"}
        url = "https://xkcd.com/info.0.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                xkcd_latest = await response.json()
                xkcd_max = xkcd_latest.get("num") + 1

        if entry_number is not None and int(entry_number) > 0 and int(entry_number) < xkcd_max:
            i = int(entry_number)
        else:
            i = randint(0, xkcd_max)
        headers = {"content-type": "application/json"}
        url = "https://xkcd.com/" + str(i) + "/info.0.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                xkcd = await response.json()

        # Build Embed
        embed = discord.Embed()
        embed.title = xkcd["title"] + " (" + xkcd["day"] + "/" + xkcd["month"] + "/" + xkcd["year"] + ")"
        embed.url = "https://xkcd.com/" + str(i)
        embed.description = xkcd["alt"]
        embed.set_image(url=xkcd["img"])
        embed.set_footer(text="Powered by xkcd")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def roll(self, ctx, toRoll, *args):
        """Rolls dice
            Format: 2d6+3
            Rolls 2 six sided dice and adds 3

            Format alt: 2d6
        """
        toSay = toRoll
        rolls = []

        toRoll = toRoll.replace("+", "d").split("d")

        if len(toRoll) == 2:
            toRoll.append("0")

        total = int(toRoll[2])

        for n in range(int(toRoll[0])):
            rolls.append(random.randint(1,int(toRoll[1])))
            total += int(rolls[-1])

        embed = discord.Embed(colour=0xdd2c22)
        embed.add_field(name="Dice Roller", value=f"{ctx.message.author.mention}\nRoll: {toSay} {rolls} + {toRoll[-1]}\nRoll: {total}")
        embed.set_footer(text="Bounty By Lukim - Command Written By Tis Tiller")

        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def rollstats(self, ctx):
        """
        Rolls Dungeons and Dragons Stat Blocks
        """
        rolls = []

        for n in range(6):
            temp = []
            for x in range(4):
                temp.append(random.randint(1,6))
            temp.sort()
            rolls.append(temp)
        
        toOut = ""
        for x in rolls:
            toOut += str(x)
            total = 0
            for y in x:
                total += y
            toOut += "\t: " + str(total) + "\n"
        await ctx.send(f"Rolls: \n{toOut}")


    @commands.command(pass_context=True)
    async def flip(self, ctx, user : discord.Member=None):
        """Flips a coin... or a user.

        Defaults to coin.
        """
        if user != None:
            msg = ""
            if user.id == self.bot.user.id:
                user = ctx.message.author
                msg = "Nice try. You think this is funny? How about *this* instead:\n\n"
            char = "abcdefghijklmnopqrstuvwxyz"
            tran = "ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz"
            table = str.maketrans(char, tran)
            name = user.display_name.translate(table)
            char = char.upper()
            tran = "∀qƆpƎℲפHIſʞ˥WNOԀQᴚS┴∩ΛMX⅄Z"
            table = str.maketrans(char, tran)
            name = name.translate(table)
            await ctx.send(msg + "(╯°□°）╯︵ " + name[::-1])
        else:
            await ctx.send("*flips a coin and... " + random.choice(["HEADS!*", "TAILS!*"]))

    @commands.command()
    async def ship(self, ctx, first_item, second_item):
        """Ship two things together.

        Example usage:

        +ship @Lukim @Bounty
        or
        +ship luk im
        """

        rating = abs(hash(first_item) - hash(second_item)) % 101
        await ctx.send ("I rate this ship a " + str(rating) + "/100!")

    @commands.group()
    async def triggered(self, ctx, *args):
        """The navy seals copypasta with some variations"""

        # arguments is a list that gives all extra values after +triggered. 
        # If there are none, tell the user that you need a triggered type.
        arguments = [item for item in enumerate(args)]
        if arguments == []:
            await ctx.send("Requires a type. help triggered shows you.")
        elif arguments[0][1] == "help":
            await ctx.send("""\n
```australian  Australian variation of navy seals
clean       Clean variation of navy seals
hacker      hacker variation of navy seals
minion      minion variation of navy seals
original    Insult people with this superb paragraph
owo         owo variation of navy seals
piglatin    pig latin variation of navy seals
shakespeare shakespearean variation of navy seals
translate   Navy seals but it's been translated several times through Google```
                """)
        elif arguments[0][1] == "original":
            await ctx.send("What the fuck did you just fucking say about me, you little bitch? I’ll have you know I graduated top of my class in the Navy Seals, and I’ve been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I’m the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You’re fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that’s just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little “clever” comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn’t, you didn’t, and now you’re paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You’re fucking dead, kiddo")
        elif arguments[0][1] == "clean":
            await ctx.send("What the jiminy crickets did you just flaming say about me, you little bozo? I’ll have you know I graduated top of my class in the Cub Scouts, and I’ve been involved in numerous secret camping trips in Wyoming, and I have over 300 confirmed knots. I am trained in first aid and I’m the top bandager in the entire US Boy Scouts (of America). You are nothing to me but just another friendly face. I will clean your wounds for you with precision the likes of which has never been seen before on this annual trip, mark my words. You think you can get away with saying those shenanigans to me over the Internet? Think again, finkle. As we speak I am contacting my secret network of MSN friends across the USA and your IP is being traced right now so you better prepare for the seminars, man. The storm that wipes out the pathetic little thing you call your bake sale. You’re frigging done, kid. I can be anywhere, anytime, and I can tie knots in over seven hundred ways, and that’s just with my bare hands. Not only am I extensively trained in road safety, but I have access to the entire manual of the United States Boy Scouts (of America) and I will use it to its full extent to train your miserable butt on the facts of the continents, you little schmuck. If only you could have known what unholy retribution your little “clever” comment was about to bring down upon you, maybe you would have held your silly tongue. But you couldn’t, you didn’t, and now you’re paying the price, you goshdarned sillyhead. I will throw leaves all over you and you will dance in them. You’re friggin done, kiddo.")
        elif arguments[0][1] == "australian":
            await ctx.send("What didja just call me, mate? I’ll have ya know I graduated top of my class in the Australian Army, and I’ve been involved in numerous beer sculling contests in Carlton, and I have over 300 slabs of XXXX drunk. I am trained in vocal abuse towards umpires and I am the top snag eater in the entire city of Carlton. You are nothing to me but a Collingwood fan. I will drop ya the fuck out with VB bottles the likes of which has never been smashed before on this Earth, mark my fucking words, mate. Ya think ya can get away with saying that bullshit to me over the Internet? Think again, mate. As we speak I am contacting Malcolm Turnbull and the Australian Federal Police and your IP is being traced right now so ya better prepare for the thunder, mate. The thunder that wipes out the pathetic little thing ya call your life. You’re fucking dead, prick. I can be anywhere, anytime, and I can drop you in over seven hundred ways, and that’s just with by smashed bottle of VB and a cricket bat. Not only am I extensively trained in dropping pricks, but I have access to the entire shed of cricket bats of the Melbourne Cricket Ground and I will use it to its full extent to hit ya for out of the outback, you prick. If only ya coulda known what bullshit your little “clever” backchat was about ta bring down upon ya, maybe ya woulda held your fucking tongue. But ya couldn’t, ya didn’t, and now you’re paying the price, mate. I will shit fury all over ya and you’re gonna drown in it. You’re fucking dead, mate.")
        elif arguments[0][1] == "owo":
            await ctx.send("What the fuck did you just fucking say about me, you wittwe bitch? I'ww have you knyow I gwaduated top of my cwass in the Nyavy Seaws, and I've been invowved in nyumewous secwet waids on Aw-Quaeda, and I have uvw 300 confiwmed kiwws. I am twainyed in gowiwwa wawfawe and I'm the top snyipew in the entiwe US awmed fowces. You awe nyothing to me but just anyothew tawget. I wiww wipe you the fuck out with pwecision the wikes of which has nyevew been seen befowe on this Eawth, mawk my fucking wowds. You think you can get away with saying that shit to me uvw the Intewnyet? Think again, fuckew. As we speak I am contacting my secwet nyetwowk of spies acwoss the USA and youw IP is being twaced wight nyow so you bettew pwepawe fow the stowm, maggot. The stowm that wipes out the pathetic wittwe thing you caww youw wife. You'we fucking dead, kid. I can be anywhewe, anytime, and I can kiww you in uvw seven hundwed ways, and that's just with my bawe hands. Nyot onwy am I extensivewy twainyed in unyawmed combat, but I have access to the entiwe awsenyaw of the Unyited States Mawinye Cowps and I wiww use it to its fuww extent to wipe youw misewabwe ass off the face of the continyent, you wittwe shit. If onwy you couwd have knyown what unhowy wetwibution youw wittwe 'cwevew' comment was about to bwing down upon you, maybe you wouwd have hewd youw fucking tongue. But you couwdn't, you didn't, and nyow you'we paying the pwice, you goddamn idiot. I wiww shit fuwy aww uvw you and you wiww dwown in it. You'we fucking dead, kiddo.")
        elif arguments[0][1] == "shakespeare":
            await ctx.send("What the alas didst thee just fucking sayeth about me, thee dram wench? I’ll has't thee knoweth I graduat'd top of mine own class in the Navy Seals, and I’ve been involv'd in num'rous secret raids on Al-Quaeda, and I has't ov'r 300 confirm'd kills. I hath did train in g'rilla warfare and I am m the top snip'r in the entire US cap-a-pe f'rces. Thou art nothing to me but just anoth'r targeteth. I shall wipeth thee the alas out with precision the likes of which hast nev'r been seen bef're on this earth, marketh mine own fucking w'rds. Thee bethink thee can receiveth hence with declaring yond the horror to me ov'r the int'rnet? Bethink again, alas'r. As we speaketh i am contacting mine own secret netw'rk of spies across the USA and thy IP is being trac'd even but now so thee bett'r prepareth f'r the st'rm, maggot. The st'rm yond wipes out the pathetic dram thing thee calleth thy life. You’re fucking dead, peat. I can beest anywh're, anytime, and i can killeth thee in ov'r seven hundr'd ways, and that’s just with mine own bareth hands. Not only hath i extensively train'd in unarm'd combat, but I has't access to the entire arsenal of the Unit'd States Marine C'rps and i shall useth 't to its full extent to wipeth thy mis'rable rampallian off the visage of the continent, thee dram the horror. If 't be true only thee couldst has't known what unholy retribution thy dram “clev'r” comment wast about to bringeth down upon thee, haply thee wouldst has't did hold thy fucking tongue. But thee couldn’t, thee didn’t, and anon you’re paying the price, thee goddamn clotpole. I shall the horror fury all ov'r thee and thee shall drowneth in t. Thou art fucking dead, kiddo")
        elif arguments[0][1] == "piglatin":
            await ctx.send("at-Whay e-thay uck-fay id-day ou-yay ust-jay ucking-fay ay-say about-way e-may, ou-yay ittle-lay itch-bay? I'll ave-hay ou-yay ow-knay I-way aduated-gray op-tay of-way y-may ass-clay in-way e-thay avy-Nay eals-Say, and-way I've een-bay involved-way in-way umerous-nay ecret-say aids-ray on-way Al-Quaeda, and-way I-way ave-hay over-way 300 onfirmed-cay ills-kay. I-way am-way ained-tray in-way orilla-gay arfare-way and-way I'm e-thay op-tay iper-snay in-way e-thay entire-way US-way armed-way orces-fay. ou-Yay are-way othing-nay o-tay e-may ut-bay ust-jay another-way arget-tay. I-way ill-way ipe-way ou-yay e-thay uck-fay out-way ith-way ecision-pray e-thay ikes-lay of-way ich-whay as-hay ever-nay een-bay een-say efore-bay on-way is-thay Earth-way, ark-may y-may ucking-fay ords-way. ou-Yay ink-thay ou-yay an-cay et-gay away-way ith-way aying-say at-thay it-shay o-tay e-may over-way e-thay Internet-way? ink-Thay again-way, ucker-fay. As-way e-way eak-spay I-way am-way ontacting-cay y-may ecret-say etwork-nay of-way ies-spay across-way e-thay USA-way and-way our-yay IP-way is-way eing-bay aced-tray ight-ray ow-nay o-say ou-yay etter-bay epare-pray or-fay e-thay orm-stay, aggot-may. e-Thay orm-stay at-thay ipes-way out-way e-thay athetic-pay ittle-lay ing-thay ou-yay all-cay our-yay ife-lay. You're ucking-fay ead-day, id-kay. I-way an-cay e-bay anywhere-way, anytime-way, and-way I-way an-cay ill-kay ou-yay in-way over-way even-say undred-hay ays-way, and-way that's ust-jay ith-way y-may are-bay ands-hay. ot-Nay only-way am-way I-way extensively-way ained-tray in-way unarmed-way ombat-cay, ut-bay I-way ave-hay access-way o-tay e-thay entire-way arsenal-way of-way e-thay United-way ates-Stay arine-May orps-Cay and-way I-way ill-way use-way it-way o-tay its-way ull-fay extent-way o-tay ipe-way our-yay iserable-may ass-way off-way e-thay ace-fay of-way e-thay ontinent-cay, ou-yay ittle-lay it-shay. If-way only-way ou-yay ould-cay ave-hay own-knay at-whay unholy-way etribution-ray our-yay ittle-lay 'clever' omment-cay as-way about-way o-tay ing-bray own-day upon-way ou-yay, aybe-may ou-yay ould-way ave-hay eld-hay our-yay ucking-fay ongue-tay. ut-Bay ou-yay couldn't, ou-yay didn't, and-way ow-nay you're aying-pay e-thay ice-pray, ou-yay oddamn-gay idiot-way. I-way ill-way it-shay ury-fay all-way over-way ou-yay and-way ou-yay ill-way own-dray in-way it-way. You're ucking-fay ead-day, iddo-kay.")
        elif arguments[0][1] == "translate":
            await ctx.send("What are you talking about? I don't know, I used to take part in the countless secret raids of my 'Navy fleet of Al Qaeda, ' More than 300 confirmed that he killed people. I was trained in the Gorilla Wars and even had an American army sniper. Yes, but only for other purposes. I've never seen this world, exact, my word. You think this thing can surf the internet? I thought anew. I've contacted my mystery, spies, United States, now that we have a better storm, ready for maggots. A storm that wiped away life. You and my girlfriend have sex with me anytime, anywhere, and I can kill you in 700 ways, it's just in his hands. The formation of martial arts skills is easy, but in the arsenal of the American navy, I use it to remove the unfortunate group of donkeys. If you know that you are ready to pay a little bit of a 'smart ' comment, you might start looking for him and follow the fall. But no, it's soup, you fool. Rage, the whole world goes to hell and sinks. You slept with my girlfriend.")
        elif arguments[0][1] == "minion":
            await ctx.send("Whaaat? ta ptt deep to sola fucking tom cama me, to ipo ip? i’ll kaylay to cono ka pyerid zzz de mi leko een ta fon seals, yee i’ve bem zitho een yawha idsleg go en al-quaeda, yee ka kaylay fino 300 nutgee kills. Ka am zincot een gorilla abasod yee i’m ta zzz sniper een ta notpac nos aas ailnu. To nama secmop da me pelo sola muggey emubus. Ka sama wipe to ta ptt kapee com varbit ta att de tika hego nopa bem gad bidom en ba hom, yuk mi fucking mew. To pensa to pudum linda cos com atnil pak ptt da me fino ta ganlot? pensa unama, fucker. Sim pem dub ka am contacting mi idsleg dawpat de spies bodbag ta USA yee tu bes tis pig traced recha prompo la to showlee migels nunu ta mad, maggot. Ta mad pak wipes kapee ta pathetic ipo tipa to cora tu levo. You’re fucking big, ar. Ka pudum be resgid, anytime, yee ka pudum bin to een fino ifs zooma nut, yee that’s sola com mi bare kor. Non solo am ka nthtab zincot een unarmed albcue, pelo ka kaylay discue da ta notpac arsenal de ta berka powmis ins yee ka sama uso pik da ti lemo dayais da wipe tu miserable butt dak ta face de ta continent, to ipo ptt. Asa solo to tup kaylay ain Whaaat? unholy retribution tu ipo “clever” cigmar tos cama da toka koop ahs to, yay to polo kaylay nep tu fucking tongue. Pelo to couldn’t, to didn’t, yee prompo you’re moblie ta ton, to goddamn idiot. Ka sama ptt fury tadda fino to yee to sama drown een pik. You’re fucking big, kiddo")
        elif arguments[0][1] == "hacker":
            await ctx.send("What the fuck did you just fucking say about me, you little bitch? I’ll have you know I graduated top of my class in the Purple republic and 4chan, and I’ve been involved in numerous secret raids on club penguin, and I have over 300 confirmed DDOSES. I am trained in ddosing and I’m the top hacker in the entire 4chan armed forces. You are nothing to me but just another target. I will ddos you the fuck out with precision the likes of which has never been seen before on this Internet, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies and neckbeards across the 4chans and deep web and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your internet. You’re fucking booted, kid. I can be anywhere, anytime, and I can ddos you in over seven hundred ways, and that’s just with my bare hands. Not only am I extensively trained in unarmed hacking, but I have access to the entire arsenal of the hacker known as Anonymous and I will use it to its full extent to wipe your miserable ass off the face of the Internet, you little shit. If only you could have known what unholy retribution your little “clever” comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn’t, you didn’t, and now you’re paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You’re fucking booted, kiddo.") 
        elif arguments[0][1] == "school":
            await ctx.send("What the frick did you just fricking say about me, you little normie? I’ll have you know I graduated top of my class in Study of Religion, and I’ve been involved in numerous secret bible study nights, and I have over 300 marks in the ATAR system. I am trained in Skills for Work and I’m the top writer in the entire English Co-hort. You are nothing to me but just another target. I will wipe you the frick out with elitism the likes of which has never been seen before on this playground, mark my fricking work. You think you can get away with saying that crap to me over the Internet? Think again, you Fricking frick! As we speak I am contacting my secret network of nerds across Grade 11 and your IP is being traced right now so you better prepare for the storm, dropkick. The storm that wipes out the pathetic little thing you call your admin privelages. You’re fricking gone, mate. I can be anywhere, anytime, and I can delete your assessment in over seven hundred ways, and that’s just with the recycle bin. Not only am I extensively trained in Business and IT, but I have access to the entire arsenal of the Brisbane Catholic Education and I will use it to its full extent to wipe your miserable grades off the face of the continent, you waste of oxygen. If only you could have known what unholy retribution your little “clever” comment was about to bring down upon you, maybe you would have used duck duck go. But you couldn’t, you didn’t, and now you’re paying the price, you goddamn Normie. I will shove my massive influence all in your report card and you will cry over it. You’re going to need to leave the class, kiddo.")
    
    @triggered.command()
    async def original(self, ctx):
        """Insult people with this superb paragraph"""
        pass

    @triggered.command()
    async def clean(self, ctx):
        """Clean variation of navy seals"""
        pass

    @triggered.command()
    async def australian(self, ctx):
        """Australian variation of navy seals"""
        pass

    @triggered.command()
    async def owo(self, ctx):
        """owo variation of navy seals"""
        pass
    
    @triggered.command()
    async def shakespeare(self, ctx):
        """shakespearean variation of navy seals"""
        pass

    @triggered.command()
    async def piglatin(self, ctx):
        """pig latin variation of navy seals"""
        pass

    @triggered.command()
    async def translate(self, ctx):
        """Navy seals but it's been translated several times through Google Translate and then back into English"""
        pass

    @triggered.command()
    async def minion(self, ctx):
        """minion variation of navy seals"""
        pass

    @triggered.command()
    async def hacker(self, ctx):
        """hacker variation of navy seals"""
        pass
    
    @triggered.command(hidden=True)
    async def school(self, ctx):
        pass

def setup(bot):
    bot.add_cog(Fun(bot))
