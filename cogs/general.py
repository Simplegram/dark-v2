import discord
import asyncio

from random import choice
from discord.ext import commands

info_picture = 'https://cdn.discordapp.com/attachments/645509827321266189/874995412061278290/pia24430-1041.jpg'

class general(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot dah jalan')

        status = ['Cyberpunk 2077',
                  'Satisfactory',
                  'Grand Theft Auto V',
                  'Counter-Strike: Global Offensive',
                  'VALORANT',
                  "Stellaris",
                  'Space Engineers',
                  'ROBLOX']

        while True:
            await self.client.change_presence(activity=discord.Game(choice(status)))
            await asyncio.sleep(30)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong!')
        await asyncio.sleep(0.2)
        await ctx.send('{} ms'.format(round(self.client.latency * 1000)))

    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(title="Darkgloow", description="A gloow bot products")
        embed.set_thumbnail(url=info_picture)
        embed.add_field(name="Version", value="Dark v2.3", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def tolong(self, ctx):
        embed = discord.Embed(title="Command List", description="Semua command dari Betagloow dengan prefix \"\"")
        embed.add_field(name="info", value="Shows the bot\'s info", inline=True)
        embed.add_field(name="log", value="Update log!", inline=True)
        embed.add_field(name="ping", value="Measure the bot\'s ping", inline=True)
        embed.add_field(name="yt [input]", value="Plays a music from youtube search", inline=True)
        embed.add_field(name="que", value="Displays the current song queue", inline=True)
        embed.add_field(name="brenti", value="Pause currently playing song", inline=True)
        embed.add_field(name="nuklir", value="Nuke the whole queue, clearing it out in the process", inline=True)
        embed.add_field(name="misil", value="Shot down the currently playing song, replacing it with the next one", inline=True)
        embed.add_field(name="mulai", value="Resume currently paused song", inline=True)
        embed.add_field(name="pilih [input]", value="Random choice generator", inline=True)
        embed.add_field(name="prambors", value="Summon the Prambors power to your nearest voice channel", inline=False)
        embed.add_field(name="pergi", value="Kick the bot from its current workplace", inline=True)
        embed.add_field(name="tolong", value="Shows this embed", inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def log(self, ctx):
        embed = discord.Embed(title="Change log", description="P r o g r e s s")
        embed.add_field(name="Aug 9", value="First script rebuilding attempts, prambors spawner, music bot spawner", inline=True)
        embed.add_field(name="Aug 10", value="More enhanced music bot (queue system, etc), prambors patches", inline=True)
        embed.add_field(name="Aug 11", value="Music bot patches, bot basic functions are kinda finished, might not update this bot after today", inline=True)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(general(client))