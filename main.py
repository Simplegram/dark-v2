import os
import random

from discord.ext import commands

client = commands.Bot(command_prefix='', help_command=None)

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

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
        await ctx.send(random.choice(warnung))
        return
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send(random.choice(warnung))
        return
    raise error
#'''
client.run('TOKEN') #Darkgloow
