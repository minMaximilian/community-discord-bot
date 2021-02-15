import discord

from discord.ext import commands
from databaseClient import usersDB
from datetime import date

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', help='Used to test if the bot is functioning, responds with a pong')
    async def ping(self, ctx):
        await ctx.reply('pong', mention_author=False)

    @commands.command(name='pong', help='Used to test if the bot is functioning, responds with a pong')
    async def pong(self, ctx):
        await ctx.reply('ping', mention_author=False)

    @commands.command(name='info', help='Gives user info on their concurrent point status')
    async def info(self, ctx, *args: discord.Member):
        if not(args):
            response = usersDB.find_one({'id': ctx.author.id})
            if not(response):
                self.generateProfile(ctx.author.id)
                response = usersDB.find_one({f'id': ctx.author.id})
            await ctx.send(embed= await self.generateEmbed(response))
        else:
            query = usersDB.find({'id': {'$in': [i.id for i in args]}})
            for i in query:
                await ctx.send(embed= await self.generateEmbed(i))

    async def generateEmbed(self, userData):
        user = await self.bot.fetch_user(userData['id'])
        embed = discord.Embed(title='Player Profile', description=f'The user profile of <@{user.id}>')
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name='Points', value=userData['context']['currency'])
        embed.add_field(name='Warnings', value=len(userData['context']['moderation']['warnings']))
        embed.set_footer(text=str(date.today()))
        return embed

    def generateProfile(self, id):
        usersDB.insert_one({'id': id, 'context': {'currency': 100, 'moderation': {'bans': 0, 'warnings': {}}}})

    @commands.command(name='coinflip', help='Gives user info on their concurrent point status')
    async def coinflip(self, ctx, amount, flip):
        # coin flip gambling for virtual currency
        pass

    @commands.command(name='leaderboard', help='Shows the global leaderboard')
    async def leaderboard(self, ctx):
        # top 10 leaderboard
        pass

    @commands.command(name='donate', help='Donates points to another user')
    async def donate(self, ctx, receiver):
        # donation
        pass

    @commands.command(name='slots', help='Allows the user to play slots')
    async def slots(self, ctx, receiver):
        # allows you to play slots
        pass