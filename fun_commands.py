import discord
import random

import helperfunc
from discord.ext import commands
from databaseClient import usersDB
from datetime import date
import time

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
    @commands.guild_only()
    async def info(self, ctx, *args: discord.Member):
        if not(args):
            response = usersDB.find_one({'id': ctx.author.id})
            if not(response):
                helperfunc.generateProfile(ctx.author.id)
                response = usersDB.find_one({f'id': ctx.author.id})
            await ctx.send(embed= await self.generateInfoEmbed(response, ctx))
        elif len(args) < 6:
            query = usersDB.find({'id': {'$in': [i.id for i in args]}})
            for i in query:
                await ctx.send(embed= await self.generateInfoEmbed(i, ctx))
        else:
            await ctx.reply(f'Can only check up to a maximum of 5 profiles')

    async def generateInfoEmbed(self, userData, ctx):
        user = await self.bot.fetch_user(userData['id'])
        embed = discord.Embed(title='Player Profile', description=f'The user profile of <@{user.id}>')
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name='Points', value=userData['context']['currency'])
        embed.add_field(name='Warnings', value=len(userData['context']['moderation']['warnings'][str(ctx.guild.id)]))
        embed.set_footer(text=str(date.today()))
        return embed

    @commands.command(name='coinflip', help='Gives user info on their concurrent point status')
    async def coinflip(self, ctx, amount: int):
        absAmount = abs(amount)
        enoughCurrency = helperfunc.enoughCurrency(ctx.author.id, absAmount)
        if enoughCurrency:
            if random.choice([True, False]):
                usersDB.update_one({'id': ctx.author.id}, {'$inc': {'context.currency': absAmount}})
                await ctx.reply(f'You just won {absAmount}')
            else:
                usersDB.update_one({'id': ctx.author.id}, {'$inc': {'context.currency': -absAmount}})
                await ctx.reply(f'You just lost {absAmount}')
        else:
            await ctx.reply(f'You don\'t have enough currency to gamble with')

    @commands.command(name='leaderboard', help='Shows the global leaderboard')
    async def leaderboard(self, ctx):
        leaderboard = usersDB.find().sort('context.currency', -1)
        numerator = 1
        embed = discord.Embed(title='Leaderboard')
        board = ''
        for i in leaderboard:
            if numerator <= 10:
                user = await self.bot.fetch_user(i['id'])
                currency = i['context']['currency']
                board += f'**{numerator}. {user.name}**\n *{currency}*\n\n'
            elif i['id'] == ctx.author.id:
                currency = i['context']['currency']
                board += f'**{numerator}. {ctx.author.name}**\n *{currency}*\n'      
            numerator += 1
        embed.description=board
        await ctx.send(embed=embed)

    @commands.command(name='donate', help='Donates points to another user')
    @commands.guild_only()
    async def donate(self, ctx, amount: int, person: discord.Member):
        absAmount = abs(amount)
        enoughCurrency = helperfunc.enoughCurrency(ctx.author.id, absAmount)
        if enoughCurrency:
            usersDB.update_one({'id': person.id}, {'$inc': {'context.currency': absAmount}})
            usersDB.update_one({'id': ctx.author.id}, {'$inc': {'context.currency': -absAmount}})
            await ctx.reply(f'Succesful transfer of {absAmount} to {person.name}')
        else:
            await ctx.reply(f'You don\'t have enough currency to donate with')

    @commands.command(name='slots', help='Allows the user to play slots')
    async def slots(self, ctx, receiver):
        # allows you to play slots
        pass
