from discord.ext import commands
from discord import Member as discordMember
from discord import Embed as discordEmbed
import json

#@commands.is_owner() checks for singular owner, obselete.


# This gets a list of owner ids from config/owners.json
owners = [x for x in json.load(open("config/owners.json"))["owners"]]

# This is a modified is_owner decorator that checks whether a user is in a list of users, instead of checking for the bot owner.
def is_owner_():
    def predicate(ctx):
        if str(ctx.message.author.id) in owners:
            return True
        raise commands.errors.NotOwner("You are not an owner of the bot.")
    return commands.core.check(predicate)

#
# Begin Cog
# 

class Owner(commands.Cog):

    class NoResponseException(Exception):
        pass

    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        print("Owner Cog was loaded sucessfully!")
    
    #
    # LOADING RELATED
    #

    # This function can load, unload and reload extensions depending on typeMod
    async def mod_extension(self, ctx, cog, typeMod):

        if not cog[0:5] == "cogs.":
            cog = "cogs." + cog            

        try:
            if typeMod == "load":
                self.bot.load_extension(cog)
            if typeMod == "unload":
                self.bot.unload_extension(cog)
            if typeMod == "reload":
                await self.mod_extension(ctx, cog, "unload")
                await self.mod_extension(ctx, cog, "load")
        except Exception as unhandled:
            await ctx.send(f"**`{typeMod.upper()} ERROR: {type(unhandled).__name__} - {unhandled}`**")
        else:
            if not typeMod == "reload":
                await ctx.send(f"**`{typeMod.upper()}ED SUCCESS - {cog.upper()}`**")


    # Hidden means it won't show up on the default help.
    @commands.command(name='load')
    @is_owner_()
    async def cload(self, ctx, *, cog: str):
        """Command which Loads a Module."""
        await self.mod_extension(ctx, cog, "load")

    @commands.command(name='unload')
    @is_owner_()
    async def cunload(self, ctx, *, cog: str):
        """Command which Unloads a Module."""
        await self.mod_extension(ctx, cog, "unload")

    @commands.command(name='reload')
    @is_owner_()
    async def creload(self, ctx, *, cog: str):
        """Command which Reloads a Module."""
        await self.mod_extension(ctx, cog, "reload")

    # 
    # Other
    # 

    @commands.command(name='appinfo')
    @is_owner_()
    async def app_info(self, ctx):
        """Gives Advanced Bot Information"""
        values = await self.bot.application_info()
        await ctx.send(values)
    
    @commands.command(name='ownermod', hidden=True)
    @is_owner_()
    async def owner_mod(self, ctx, ownerMod, id=None):
        """This allows you to modify (and list) the owners of the bot without restarting."""
        try:  
            if ownerMod.lower() == "add" and not id == None:
                for x in range(len(owners)):
                    if owners[x] == str(id):
                        await ctx.send("This user is already an owner.")
                        raise self.NoResponseException
                owners.append(str(id))

            if ownerMod.lower() == "del" and not id == None:
                if id in ['188493063973371904']:
                    await ctx.send("This user cannot be removed, sorry.")
                    raise self.NoResponseException

                for x in range(len(owners)):
                    if owners[x] == str(id):
                        del owners[x]

            if ownerMod.lower() == "list":
                embed = discordEmbed(title="Owner List", color=ctx.message.author.top_role.colour)
                embed.add_field(name="-", value="{}".format(", ".join(sorted(owners))), inline=False)
                await ctx.send(embed=embed)
                raise self.NoResponseException

            if not ownerMod.lower() == "list" and id == None:
                raise self.NoResponseException

            if not ownerMod.lower() == "list": 
                temp = {"owners": [x for x in owners]}
                with open("config/owners.json", 'w') as ownerFile:
                    json.dump(temp, ownerFile)
                await self.mod_extension(ctx, "cogs.owner", "reload")
        except self.NoResponseException:
            pass
        except Exception as unhandled:
            await ctx.send(f"**`ERROR: {type(unhandled).__name__} - {unhandled}`**")
        else:
            await ctx.send(f"**`{ownerMod.upper()} SUCCESS`**")


    @commands.command()
    @is_owner_()
    async def shutdown(self, ctx):
        """stops the bot"""
        bot = ctx.bot
        await ctx.send(":wave: Bye!")
        await bot.logout()

    @shutdown.error
    async def shutdown_handler(self, ctx, error):
        sender = ctx.message.author
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Sorry {}, only bot owner can do this.".format(sender.mention))

    @commands.command(name="cogs")
    @is_owner_()
    async def _show_cogs(self, ctx):
        """Shows loaded/unloaded cogs"""
        # This function assumes that all cogs are in the cogs folder,
        # which is currently true.

        # Extracting filename from __module__ Example: cogs.owner
        loaded = [c.__module__.split(".")[1] for c in self.bot.cogs.values()]
        # What's in the folder but not loaded is unloaded
        #unloaded = [c.split(".")[1] for c in self._list_cogs()
        #            if c.split(".")[1] not in loaded]

        #if not unloaded:
        #    unloaded = ["None"]

        '''msg = ("+ Loaded\n"
               "{}\n\n"
               "- Unloaded\n"
               "{}"
               "".format(", ".join(sorted(loaded)),
                         ", ".join(sorted(unloaded)))
               )'''
        
        embed = discordEmbed(title="Cog Info", color=ctx.message.author.top_role.colour)
        embed.add_field(name="Loaded", value="{}".format(", ".join(sorted(loaded))), inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Owner(bot))