import discord
import asyncio

from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

info_picture = 'https://cdn.discordapp.com/attachments/645509827321266189/874995412061278290/pia24430-1041.jpg'

class general(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('')

    @commands.command()
    async def ping(self, ctx):
        msg = await ctx.send(f'Pong! {format(round(self.client.latency * 1000))} ms')
        await asyncio.sleep(1.5)
        await ctx.message.delete()
        await msg.delete()

    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(title="Darkgloow", description="A gloow bot products")
        embed.set_thumbnail(url=info_picture)
        embed.add_field(name="Version", value="Dark v2.4", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def tolong(self, ctx):
        embed = discord.Embed(title="Command List", description="Semua command dari Darkgloow (saat ini tidak ada prefix)")
        embed.add_field(name="info", value="Shows the bot\'s info", inline=True)
        embed.add_field(name="log", value="Update log!", inline=True)
        embed.add_field(name="ping", value="Measure the bot\'s ping", inline=True)
        embed.add_field(name="invite", value="Sends an invite link of this bot", inline=True)
        embed.add_field(name="yt", value="Plays a query or link from youtube search", inline=True)
        embed.add_field(name="que", value="Displays the current song queue", inline=True)
        embed.add_field(name="brenti", value="Pause currently playing song", inline=True)
        embed.add_field(name="klir", value="Nuke the whole queue, clearing it out in the process", inline=True)
        embed.add_field(name="sekip", value="Shot down the currently playing song, replacing it with the next one", inline=True)
        embed.add_field(name="lanjut", value="Resume currently paused song", inline=True)
        embed.add_field(name="vol, volum", value="Change the bot's global volume", inline=True)
        embed.add_field(name="ff", value="Make your song travel forward in time", inline=True)
        embed.add_field(name="pos", value="Shows the timestamp of your current song", inline=True)
        embed.add_field(name="pilih", value="Random choice generator", inline=True)
#        embed.add_field(name="prambors", value="Summon the Prambors power to your nearest voice channel", inline=False)
#        embed.add_field(name="pergi", value="Kick the bot from its current workplace", inline=True)
        embed.add_field(name="tolong", value="Shows this embed", inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def log(self, ctx):
        embed = discord.Embed(title="Change log", description="P r o g r e s s")
        embed.add_field(name="Aug 9", value="First script rebuilding attempts, prambors spawner, music bot spawner", inline=True)
        embed.add_field(name="Aug 10", value="More enhanced music bot (queue system, etc), prambors patches", inline=True)
        embed.add_field(name="Aug 11", value="Music bot patches, bot basic functions are kinda finished, might not update this bot after today", inline=True)
        embed.add_field(name="Aug 13", value="Major Music code changes, music bot spam rate reduced by 70%",inline=False)
        embed.add_field(name="Aug 14", value="Music bot patches", inline=False)
        embed.add_field(name="Aug 15", value="Major music bot overhaul, ported to Lavalink, Prambors feature reported missing from the update", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        await ctx.message.delete()
        await ctx.send('https://discord.com/api/oauth2/authorize?client_id=815794671955345438&permissions=26624&scope=bot')


'''
    @commands.command()
    async def tust(self, ctx):
        number = ['1', '2', '3', '4']
        embed = discord.Embed(title='test')
        for i in number:
            embed.add_field(value=i)
        await ctx.send(embed=embed)

'''

def setup(client):
    client.add_cog(general(client))