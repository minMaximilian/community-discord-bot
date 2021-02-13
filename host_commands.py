import discord

from discord.ext import commands
from databaseClient import serversDB

class Host(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='registry', help='Shows a tabulation of all users registered')
    @commands.has_guild_permissions(administrator=True)
    @commands.guild_only()
    async def registry(self, ctx, game:str):
        if serversDB.find({f'{ctx.guild.id}.{game.lower()}': {'$exists': True}}).count() > 0:
                await ctx.reply(f'Succesfully set the {ctx.message.channel.mention} channel as the registry for {game}', mention_author=False, delete_after=3.0)
                embed = await ctx.send(embed=await self.generateEmbed(ctx, game))
                serversDB.update({f'{ctx.guild.id}.{game.lower()}': {'$exists': True}}, {'$set': {f'{ctx.guild.id}.{game.lower()}.registry.embed': embed.id, f'{ctx.guild.id}.{game.lower()}.registry.channel': ctx.message.channel.id}},upsert=True)
        else:
            await ctx.reply(f'Couldn\'t find the game within the possible candidates')

    @commands.command(name='register', help='Allows registration for a the ingame tag')
    @commands.guild_only()
    async def register(self, ctx, tag:str, game:str):
        if serversDB.find({f'{ctx.guild.id}.{game.lower()}': {'$exists': True}}).count() > 0:
            serversDB.update({str(ctx.guild.id): {'$exists': True}}, {'$set': {f'{ctx.guild.id}.{game.lower()}.registry.players.{ctx.author.id}': tag}}, upsert=True)
            await ctx.reply(f'Succesfully added {tag} to the player {ctx.message.author.mention} to the {game.capitalize()} registry', mention_author=False)
            if serversDB.find({f'{ctx.guild.id}.{game.lower()}.registry.embed': {'$exists': True}}).count() > 0:
                data = serversDB.find_one({f'{ctx.guild.id}': {'$exists': True}}, {f'{ctx.guild.id}.{game.lower()}.registry': 1})
                channel = self.bot.get_channel(int(data[str(ctx.guild.id)][game.lower()]['registry']['channel']))
                embed = await channel.fetch_message(int(data[str(ctx.guild.id)][game.lower()]['registry']['embed']))
                await embed.edit(embed=await self.generateEmbed(ctx, game))
        else:
            await ctx.reply(f'{game.capitalize()} is not a possible canddiate for registries, try correcting the game name')
            
    @commands.command(name='addGame', help='Adds the game as a possible candidate for scheduling and registries')
    @commands.has_guild_permissions(administrator=True)
    @commands.guild_only()
    async def addGame(self, ctx, game:str):
        if serversDB.find({f'{ctx.guild.id}.{game.lower()}': {'$exists': True}}).count() > 0:
            await ctx.reply(f'{game.capitalize()} already exists as a possible candidate')
        else:
            payload = {
                    'registry': {'players': {}},
                    'schedule': {}
            }   
            serversDB.update({str(ctx.guild.id): {'$exists': True}}, {'$set': {f'{ctx.guild.id}.{game.lower()}': payload}}, upsert=True)
            await ctx.reply(f'Succesfully added {game.capitalize()} as a possible candidate for scheduling and registries')
        
    
    @commands.command(name='removeGame', help='Adds a game to be used within scheduler commands')
    @commands.has_guild_permissions(administrator=True)
    @commands.guild_only()
    async def removeGame(self, ctx, game: str):
        if serversDB.find({f'{ctx.guild.id}.{game.lower()}': {'$exists': True}}).count() > 0:
                serversDB.update({str(ctx.guild.id): {'$exists': True}}, {'$unset': {f'{ctx.guild.id}.{game.lower()}': {}}})
                await ctx.reply(f'{game.capitalize()} succesfully removed')
        else:
            await ctx.reply(f'{game.capitalize()} doesn\'t exist')

    @commands.command(name='addSchedule', help='Schedules the game')
    @commands.has_guild_permissions(administrator=True)
    @commands.guild_only()
    async def addSchedule(self, ctx, schedule, game: str):
        await ctx.reply(f'Succesfully scheduled a game @{schedule} for {game.capitalize()}')

    @commands.command(name='removeSchedule', help='Removes scheduled item')
    @commands.has_guild_permissions(administrator=True)
    @commands.guild_only()
    async def removeSchedule(self, ctx, schedule, game: str):
        await ctx.reply(f'Succesfully unscheduled a game @{schedule} for {game.capitalize()}')

    async def generateEmbed(self, ctx, game):
        iterable = serversDB.find_one({f'{ctx.guild.id}': {'$exists': True}}, {f'{ctx.guild.id}.{game.lower()}.registry.players': 1})
        descriptor = ''
        for key, val in iterable[str(ctx.guild.id)][game.lower()]['registry']['players'].items():
            descriptor += f'<@{key}>: {val}\n'
        return discord.Embed(title=f"Concurrently {len(iterable.items())} registered for {game.capitalize()}", description=descriptor)
