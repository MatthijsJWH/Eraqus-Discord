# bot.py
import discord
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

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game('BUG FIXING!')
    )

    print('Bot online!')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'Unknown command! Try `~help` to see a list of all commands')

    if isinstance(error, commands.MissingRequiredArgument):
        embed = Embed(
            title = '❌ Missing argument!',
            color = Color.red(),
            description = 'You have not provided all the necessary arguments to execute this command! \n To see all the necessary argument use `~help <command>`.'
        )
        await ctx.send(embed=embed)

    else:
        print(error)


@bot.command(name='load')
@commands.has_guild_permissions(administrator=True)
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command(name='unload')
@commands.has_guild_permissions(administrator=True)
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

@bot.command(name='reload')
@commands.has_guild_permissions(administrator=True)
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

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

bot.run(TOKEN)