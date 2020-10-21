import discord
import json

from discord.colour import Color
from discord.embeds import Embed
from discord.ext import commands

with open('../db/db.json') as f:
    data = json.load(f)

def write_to_db():
    with open('../db/db.json', 'w') as f:
        json.dump(data, f)

class Subscriber(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Commands
    @commands.command(name='add', help='Add new subscriber list')
    @commands.has_guild_permissions(administrator=True)
    async def add_list(self, ctx, tag_name):
        if tag_name in data:
            embed = Embed(
                title = '❌ List already exists!',
                color = Color.red(),
                description = f'The tag `{tag_name}` already exists.'
            )
            await ctx.send(embed=embed)
            return

        data[tag_name] = []
        write_to_db()

        embed = Embed(
            title = ':white_check_mark: List created.',
            color = Color.green(),
            description = f'The tag `{tag_name}` has been created.'
        )
        await ctx.send(embed=embed)

    @commands.command(name='remove')
    @commands.has_guild_permissions(administrator=True)
    async def remove_list(self, ctx, tag):
        if tag in data:
            data.pop(tag)
            write_to_db()

            embed = Embed(
                title = ':white_check_mark: List deleted.',
                color = Color.green(),
                description = f'The tag `{tag}` has been removed.'
            )
            await ctx.send(embed=embed)
            return

        embed = Embed(
            title = '❌ List doesn\'t exists!',
            color = Color.red(),
            description = f'The tag `{tag}` does not exist.'
        )
        await ctx.send(embed=embed)

    @add_list.error
    @remove_list.error
    async def permission_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = Embed(
                title = '❌ Command denied!',
                color = Color.red(),
                description = 'You do not have the correct permissions to execute this command!'
            )
            await ctx.send(embed=embed)
            return

        embed = Embed(
            title = '❌ An error ocurred!',
            color = Color.red(),
            description = 'An unknown error occured, try again later.'
        )
        await ctx.send(embed=embed)

    @commands.command(name='sub')
    async def sub(self, ctx, tag):
        if tag in data:
            if ctx.message.author.id in data[tag]:
                embed = Embed(
                    title = '❌ Already subscribed!',
                    color = Color.red(),
                    description = f'You are already subscribed to the tag `{tag}`.'
                )
                await ctx.send(embed=embed)
                return

            data[tag].append(ctx.message.author.id)

            write_to_db()

            embed = Embed(
                title = ':white_check_mark: Subscribed.',
                color = Color.green(),
                description = f'You are now subscribed to the tag `{tag}`.'
            )
            await ctx.send(embed=embed)
            return

        embed = Embed(
            title = '❌ List doesn\'t exists!',
            color = Color.red(),
            description = f'The tag `{tag}` does not exist.'
        )
        await ctx.send(embed=embed)

    @commands.command(name='unsub')
    async def unsub(self, ctx, tag):
        if tag in data:
            if ctx.message.author.id in data[tag]:
                data[tag].remove(ctx.message.author.id)
                write_to_db()

                embed = Embed(
                    title = ':white_check_mark: Unsubscribed.',
                    color = Color.green(),
                    description = f'You are now no longer subscribed to the tag `{tag}`.'
                )
                await ctx.send(embed=embed)
                return

            embed = Embed(
                title = '❌ Not subscribed!',
                color = Color.red(),
                description = f'You are not subscribed to the tag `{tag}`.'
            )
            await ctx.send(embed=embed)
            return

        embed = Embed(
            title = '❌ List doesn\'t exists!',
            color = Color.red(),
            description = f'The tag `{tag}` does not exist.'
        )
        await ctx.send(embed=embed)

    @commands.command(name='announce')
    async def announce(self, ctx, tag, *message):
        tag_string = f'[`{tag}`] '
        message_string = " ".join(message[:])

        if tag in data:
            users_string = ''
            for userID in data[tag]:
                user = ctx.guild.get_member(userID)
                if userID != ctx.message.author.id:
                    users_string += f'{user.mention}, '

            final = tag_string + users_string + message_string

            await ctx.send(final)
            return

        embed = Embed(
            title = '❌ List doesn\'t exists!',
            color = Color.red(),
            description = f'The tag `{tag}` does not exist.'
        )
        await ctx.send(embed=embed)

    @commands.command(name='tags')
    async def tags(self, ctx):
        tags = '\n - '.join(data.keys())
        await ctx.send(f'Current tags:\n - {tags}')

def setup(bot):
    bot.add_cog(Subscriber(bot))