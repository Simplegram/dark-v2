import discord
import youtube_dl
import asyncio

from discord.ext import commands

quelink = []
quetitle = []
quedur = []

repeat = False

client = discord.Client()

title = ''
mus_format = ''
duration = 0

playing = False

async def nuke(ctx):
    global quelink
    global quetitle
    global quedur

    if len(quelink) > 0:
        ctx.voice_client.stop()
        quelink.clear()
        quetitle.clear()
        quedur.clear()

async def played(ctx):
    global playing
    global title
    global duration
    global mus_format
    global repeat

    if len(quelink) > 0:
        if repeat == False:
            quelink.pop(0)
            quetitle.pop(0)
            quedur.pop(0)

    if len(quelink) > 0:
        mus_format = quelink[0]
        title = quetitle[0]
        duration = quedur[0]

    playing = False

    await player_handler(ctx)

async def missile(ctx):
    global quelink
    global quetitle
    global quedur

    if ctx.voice_client.is_playing() and len(quelink) == 0:
        ctx.voice_client.stop()
    elif len(quelink) == 0:
        await ctx.send('ga ada apa apa di queue')
    elif len(quelink) > 0:
        ctx.voice_client.stop()
        await played(ctx)

async def durian(ctx, time):
    await asyncio.sleep(time)
    await asyncio.sleep(0.5)
    await played(ctx)

async def player_handler(ctx):
    global playing
    global duration

    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                      'options': '-vn'}

    if playing == False and len(quelink) > 0:
        playing = True
        ctx.voice_client.play(discord.FFmpegPCMAudio(mus_format, **FFMPEG_OPTIONS))
        embed = discord.Embed(title="Playing now:", description=title)
        await ctx.send(embed=embed)
        await durian(ctx, duration)
    elif playing == False and len(quelink) == 0:
        await ctx.send('queue abis!')
    elif playing == True:
        if ctx.voice_client.is_playing() and len(quetitle) >= 1:
            embed = discord.Embed(title="Queued!", description=title)
            await ctx.send(embed=embed)

async def load(word):
    global title
    global mus_format
    global duration

    ydl_opts = {
        'format': 'bestaudio',
        'ignoreerrors': True,
        'default_search': 'auto',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredquality': '256',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        mus = ydl.extract_info(word, download=False)

        if 'entries' in mus:
            mus_format = str(mus['entries'][0]['formats'][0]['url'])
            title = mus['entries'][0]['title']
            duration = mus['entries'][0]['duration']
        elif 'formats' in mus:
            mus_format = str(mus['formats'][0]['url'])

    quelink.append(mus_format)
    quetitle.append(title)
    quedur.append(duration)

class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    global title
    global mus_format

    @commands.command()
    async def yt(self, ctx, *args):
        global playing
        word = ' '.join(args)
        channel = ctx.message.author.voice.channel

        if not ctx.voice_client:
            await asyncio.gather(channel.connect(), load(word))
            await player_handler(ctx)
        elif ctx.voice_client:
            await load(word)
            await player_handler(ctx)

    @commands.command()
    async def brenti(self, ctx):
        ctx.voice_client.pause()

    @commands.command()
    async def mulai(self, ctx):
        ctx.voice_client.resume()

    @commands.command()
    async  def nuklir(self, ctx):
        await nuke(ctx)

    @commands.command()
    async def misil(self, ctx):
        await missile(ctx)

    @commands.command()
    async def pergi(self, ctx):
        if not ctx.voice_client:
            await ctx.send('gw ga ada di channel manapun gan')
        elif ctx.voice_client:
            await nuke(ctx)
            await ctx.send('Ok gw pergi bos')
            await ctx.voice_client.disconnect()

    @commands.command()
    async def ulangan(self, ctx):
        global repeat

        if repeat == False:
            repeat = True
        elif repeat == True:
            repeat = False

    @commands.command()
    async def que(self, ctx):
        global title
        global quetitle
        global duration

        menit = duration // 60
        detik = duration % 60

        if len(quetitle) > 0:
            for x in quetitle:
                if x == quetitle[0]:
                    await ctx.send('> ' + x + ' ' + f'{menit}:{detik}' + ' ' + '< CURRENTLY PLAYING')
                else:
                    await ctx.send('> ' + x + ' ' + f'{menit}:{detik}')
        elif len(quetitle) == 0:
            await ctx.send('ga ada apa apa di queue')
'''
    @yt.error
    async def yt_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('masukin judul lagu yang mau di puter dong')
'''

def setup(client):
    client.add_cog(music(client))