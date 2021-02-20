import discord
import random
import helperfunc

from discord.ext import commands
from databaseClient import usersDB
from datetime import date
import time

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='warn', help='Usage, command @user \"Reason within these quotations\", kicks the user after 3 strikes')
    @commands.has_guild_permissions(kick_members=True)
    @commands.guild_only()
    async def warn(self, ctx, person: discord.Member, reason=None):
        payload = {'warning': reason if reason else 'No reason provided', 'date': str(date.today()), 'timestamp': int(time.time())}
        response = usersDB.find_one({'id': person.id})
        if response:
            if len(response['context']['moderation']['warnings'][str(ctx.guild.id)]) + 1 >= 3:
                usersDB.update_one({'id': person.id}, {'$push': {f'context.moderation.warnings.{ctx.guild.id}': payload}, '$inc': {f'context.moderation.kicked': 1}}, upsert=True)
                await person.kick(reason='Kicked for exceeding 3 warning limit')
                await ctx.reply(f'Succesfully kicked {person.name} for exceding 3 warning limit')
            else:
                usersDB.update_one({'id': person.id}, {'$push': {f'context.moderation.warnings.{ctx.guild.id}': payload}}, upsert=True)
            await ctx.reply(f'Succesfully warned {person.name} for Reason: \"{reason}\"')
        else:
            helperfunc.generateProfile(person.id)
            usersDB.update_one({'id': person.id}, {'$push': {f'context.moderation.warnings.{ctx.guild.id}': payload}}, upsert=True)
            await ctx.reply(f'Succesfully warned {person.name} for {reason}')

    @commands.command(name='kick', help='Usage, command @user \"Reason within these quotations\"')
    @commands.has_guild_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self, ctx, person: discord.Member, reason=None):
        response = usersDB.find_one({'id': person.id})
        if response:
            usersDB.update_one({'id': person.id}, {'$inc': {f'context.moderation.kicked': 1}}, upsert=True)
            await person.kick(reason=(reason if reason else 'No reason'))
            await ctx.reply(f'Succesfully kicked {person.name} for Reason: {reason}')
        else:
            helperfunc.generateProfile(person.id)
            usersDB.update_one({'id': person.id}, {'$inc': {f'context.moderation.kicked': 1}}, upsert=True)
            await person.kick(reason=(reason if reason else 'No reason'))
            await ctx.reply(f'Succesfully kicked {person.name} for Reason: {reason}')

    @commands.command(name='ban', help='Usage, command @user \"Reason within these quotations\"')
    @commands.has_guild_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self, ctx, person: discord.Member, reason=None):
        response = usersDB.find_one({'id': person.id})
        if response:
            usersDB.update_one({'id': person.id}, {'$inc': {f'context.moderation.bans': 1}}, upsert=True)
            await person.ban(reason=(reason if reason else 'No reason'))
            await ctx.reply(f'Succesfully banned {person.name} for Reason: {reason}')
        else:
            helperfunc.generateProfile(person.id)
            usersDB.update_one({'id': person.id}, {'$inc': {f'context.moderation.bans': 1}}, upsert=True)
            await person.ban(reason=(reason if reason else 'No reason'))
            await ctx.reply(f'Succesfully banned {person.name} for Reason: {reason}')

    @commands.command(name='logs', help='Usage, command @user or multiple users, under 5, returns logs of a given player and all the warnings they attained in the server')
    @commands.has_guild_permissions(kick_members=True)
    @commands.guild_only()
    async def logs(self, ctx, *args: discord.Member):
        if len(args) < 6:
            query = usersDB.find({'$and': [{'id': {'$in': [i.id for i in args]}}, {f'context.moderation.warnings.{ctx.guild.id}': {'$exists': True}}]})
            for i in query:
                await ctx.send(embed= await self.generateLogsEmbed(i, ctx.guild.id))
        else:
            await ctx.reply(f'Can only check up to a maximum of 5 profiles')

    async def generateLogsEmbed(self, userData, guildID):
        user = await self.bot.fetch_user(userData['id'])
        descriptor = f'The logs of <@{user.id}>\n\n'
        embed = discord.Embed(title='Log Profile')
        embed.set_thumbnail(url=user.avatar_url)
        for i in userData['context']['moderation']['warnings'][str(guildID)]:
            warning = i['warning']
            dateEmbed = i['date']
            warningID = i['timestamp']
            descriptor += f'**Warning ID: {warningID} ** \n Reason: \n*{warning}* \n Received at: \n *{dateEmbed}*\n\n'
        embed.set_footer(text=f'Log created on: {str(date.today())}')
        embed.description=descriptor
        return embed