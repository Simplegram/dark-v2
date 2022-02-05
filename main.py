import os
import random
import discord
import asyncio

from random import choice
from discord.ext import commands
from discord_components.client import DiscordComponents

client = commands.Bot(command_prefix='', help_command=None)

@client.event
async def on_ready():
    print('Bot dah jalan')
    client.loop.create_task(status_update())
    DiscordComponents(client)

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.message.delete()

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def status_update():
    status = ['Cyberpunk 2077',
                  'Satisfactory',
                  'Grand Theft Auto V',
                  'Counter-Strike: Global Offensive',
                  'VALORANT',
                  "Stellaris",
                  'Space Engineers',
                  'ROBLOX']

    while True:
        await client.change_presence(activity=discord.Game(choice(status)))
        await asyncio.sleep(1800)

warnung = ['tulis command nya yang bener dong',
           'bisa tulis command yang bener ga',
           'walah lu salah command bang',
           'salah ini command nya gan',
           'salah command nih, coba refer ke \'tolong\'',
           'wah tiba tiba error nih bot nya'
          ]

#Error Handler
#'''
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        msg = await ctx.send(random.choice(warnung))
        await asyncio.sleep(1)
        await msg.delete()
        return
    elif isinstance(error, commands.CommandInvokeError):
        msg = await ctx.send(random.choice(warnung))
        await asyncio.sleep(1)
        await msg.delete()
        return
    raise error
#'''
client.run('your_code_here')
