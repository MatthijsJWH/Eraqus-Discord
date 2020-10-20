# bot.py
import discord
import json
import os
import random

from discord.colour import Color
from discord.embeds import Embed
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

with open('db/db.json') as f:
    data = json.load(f)

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='add', help='Add new subscriber list')
async def add_list(ctx, tag_name):
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

@bot.command(name='remove')
async def remove_list(ctx, tag):
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


@bot.command(name='sub')
async def sub(ctx, tag):
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

@bot.command(name='unsub')
async def unsub(ctx, tag):
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

@bot.command(name='announce')
async def announce(ctx, tag, *message):
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

@bot.command(name='tags')
async def tags(ctx):
    tags = '\n - '.join(data.keys())
    await ctx.send(f'Current tags:\n - {tags}')

@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

def write_to_db():
    with open('db/db.json', 'w') as f:
        json.dump(data, f)

bot.run(TOKEN)