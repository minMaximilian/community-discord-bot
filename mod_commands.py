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
        self.insertReason(ctx, person, reason, 'warnings')
        await ctx.reply(f'Succesfully warned {person.name} for {reason}')

    @commands.command(name='kick', help='Usage, command @user \"Reason within these quotations\"')
    @commands.has_guild_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self, ctx, person: discord.Member, reason=None):
        self.insertReason(ctx, person, reason, 'kicks')
        await person.kick(reason=(reason if reason else 'No reason'))
        await ctx.reply(f'Succesfully kicked {person.name} for Reason: {reason}')

    @commands.command(name='ban', help='Usage, command @user \"Reason within these quotations\"')
    @commands.has_guild_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self, ctx, person: discord.Member, reason=None):
            self.insertReason(ctx, person, reason, 'bans')
            await person.ban(reason=(reason if reason else 'No reason'))
            await ctx.reply(f'Succesfully banned {person.name} for Reason: {reason}')

    def insertReason(self, ctx, person: discord.Member, reason, insertType: str):
        payload = {'reason': reason if reason else 'No reason provided', 'date': str(date.today()), 'timestamp': int(time.time())}        
        response = usersDB.find_one({'id': person.id})
        if response:
            usersDB.update_one({'id': person.id}, {'$push': {f'context.moderation.{insertType}.{ctx.guild.id}': payload}}, upsert=True)
        else:
            helperfunc.generateProfile(person.id)
            usersDB.update_one({'id': person.id}, {'$push': {f'context.moderation.{insertType}.{ctx.guild.id}': payload}}, upsert=True)

    @commands.command(name='logs', help='Usage, command @user or multiple users, under 5, returns logs of a given player and all the warnings they attained in the server')
    @commands.has_guild_permissions(kick_members=True)
    @commands.guild_only()
    async def logs(self, ctx, logType: str, *args: discord.Member):
        if len(args) < 6:
            query = usersDB.find({'$and': [{'id': {'$in': [i.id for i in args]}}, {f'context.moderation.{logType}.{ctx.guild.id}': {'$exists': True}}]})
            for i in query:
                await ctx.send(embed= await self.generateLogsEmbed(i, ctx.guild.id, logType))
        else:
            await ctx.reply(f'Can only check up to a maximum of 5 profiles')

    async def generateLogsEmbed(self, userData, guildID, logType: str):
        user = await self.bot.fetch_user(userData['id'])
        descriptor = f'The logs of <@{user.id}>\n\n'
        embed = discord.Embed(title='Log Profile')
        embed.set_thumbnail(url=user.avatar_url)
        for i in userData['context']['moderation'][logType][str(guildID)]:
            warning = i['reason']
            dateEmbed = i['date']
            warningID = i['timestamp']
            descriptor += f'**ID: {warningID} ** \n Reason: \n*{warning}* \n Received at: \n *{dateEmbed}*\n\n'
        embed.set_footer(text=f'Log created on: {str(date.today())}')
        embed.description=descriptor
        return embed