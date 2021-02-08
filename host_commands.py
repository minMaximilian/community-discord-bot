import discord

from discord.ext import commands

class Host(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', help='Used to test if the bot is functioning, responds with a pong')
    async def ping(self, ctx):
        await ctx.reply('pong', mention_author=False)

    @commands.command(name='registry', help='Shows a tabulation of all users registered')
    async def registry(self, ctx):
        await ctx.reply('Registry', mention_author=False)

    @commands.command(name='register', help='Allows registration for a the ingame tag')
    async def register(self, ctx, tag:str, game:str):
        await ctx.reply(f'Succesfully added {tag} to the player {ctx.message.author.mention} to the {game.capitalize()} registry', mention_author=False)

    @commands.command(name='setRegistry', help='Sets the registry channel')
    async def setRegistry(self, ctx, game:str):
        await ctx.send(f'Successfuly set registry in {ctx.message.channel.mention} for {game.capitalize()}', delete_after=3.0)

    @commands.command(name='addSchedule', help='Schedules the game')
    async def addSchedule(self, ctx, schedule, game: str):
        await ctx.reply(f'Succesfully scheduled a game @{schedule} for {game.capitalize()}')

    @commands.command(name='removeSchedule', help='Removes scheduled item')
    async def removeSchedule(self, ctx, schedule, game: str):
        await ctx.reply(f'Succesfully unscheduled a game @{schedule} for {game.capitalize()}')
    
    @commands.command(name='addGame', help='Adds a game to be used within scheduler commands')
    async def addGame(self, ctx, game: str):
        await ctx.reply(f'{game.capitalize()} succesfully added')

    @commands.command(name='removeGame', help='Adds a game to be used within scheduler commands')
    async def removeGame(self, ctx, game: str):
        await ctx.reply(f'{game.capitalize()} succesfully removed')