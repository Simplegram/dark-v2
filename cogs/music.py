import discord
import youtube_dl
import asyncio

from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
from discord.ext import commands, tasks

bot = discord.Client

quelink = []
quetitle = []
quedur = []

repeat = False

title = ''
mus_format = ''
duration = 0

playing = False

async def que(ctx):
    global title
    global quetitle
    global duration

    i = 0

    if len(quetitle) > 0:
        for x in quetitle:
            if x == quetitle[0]:

                menit = quedur[i] // 60
                detik = quedur[i] % 60

                await ctx.send('> ' + x + ' ' + f'{menit}:{detik}' + ' ' + '< CURRENTLY PLAYING')
                i += 1
            else:
                menit = quedur[i] // 60
                detik = quedur[i] % 60

                await ctx.send('> ' + x + ' ' + f'{menit}:{detik}')
                i += 1
    elif len(quetitle) == 0:
        await ctx.send('ga ada apa apa di queue')

async def ulangan():
    global repeat

    if repeat == False:
        repeat = True
    elif repeat == True:
        repeat = False

async def nuke(ctx):
    global quelink
    global quetitle
    global quedur

    if len(quelink) > 0:
        ctx.voice_client.stop()
        quelink.clear()
        quetitle.clear()
        quedur.clear()

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

async def send_playing(ctx):
    embed = discord.Embed(title="Playing now:", description=title)
    await ctx.send(embed=embed)

async def player_handler(ctx):
    global playing
    global duration

    loop = asyncio.get_event_loop()

    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                      'options': '-vn'}

    if playing == False and len(quelink) > 0 and not ctx.voice_client.is_playing():
        playing = True
        ctx.voice_client.play(discord.FFmpegPCMAudio(mus_format, **FFMPEG_OPTIONS), after=lambda e:asyncio.run_coroutine_threadsafe(played(ctx), loop))
        await send_playing(ctx)
    elif playing == False and len(quelink) == 0:
        await ctx.send('queue abis!')
    elif playing == True:
        embed = discord.Embed(title="Queued!", description=title)
        await ctx.send(embed=embed)

async def load(ctx, word):
    global title
    global mus_format
    global duration
    global playing

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

        if not ctx.voice_client:
            channel = ctx.message.author.voice.channel

            await asyncio.gather(channel.connect(), load(ctx. word))
            await player_handler(ctx)
        elif ctx.voice_client:
            await load(ctx, word)
            await player_handler(ctx)
        else:
            await ctx.send('masuk ke voice channel dulu dong!')

    @commands.command()
    async def remot(self, ctx):

        await ctx.send(
            'Magic Remote XM-1000:tm:',
            components=[
                [Button(style=ButtonStyle.blue, label='pause'),
                Button(style=ButtonStyle.blue, label='play'),
                Button(style=ButtonStyle.blue, label='skip'),
                Button(style=ButtonStyle.red, label='clear')],
                [Button(style=ButtonStyle.blue, label='repeat'),
                Button(style=ButtonStyle.blue, label='queue')]
            ]
        )

        pos = await self.client.wait_for('button_click')
        if pos:
            ctx.voice_client.pause(),

        plei = await self.client.wait_for('button_click')
        if plei:
            ctx.voice_client.resume()

        sekip = await self.client.wait_for('button_click')
        if sekip:
            await missile(ctx)

        klir = await self.client.wait_for('button_click')
        if klir:
            await nuke(ctx)

        ripit = await self.client.wait_for('button_click')
        if ripit:
            await ulangan()

        kyu = await self.client.wait_for('button_click')
        if kyu:
            await que(ctx)

    @commands.command()
    async def pergi(self, ctx):
        if not ctx.voice_client:
            await ctx.send('gw ga ada di channel manapun gan')
        elif ctx.voice_client:
            await nuke(ctx)
            await ctx.send('Ok gw pergi bos')
            await ctx.voice_client.disconnect()


'''
    @yt.error
    async def yt_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('masukin judul lagu yang mau di puter dong')
'''

def setup(client):
    client.add_cog(music(client))
