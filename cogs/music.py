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

msg = 0
qgone = True

embed_play = discord.Embed(title='N/A')
embed_edit = discord.Embed()

pcode = 22283
link = f'https://{pcode}.live.streamtheworld.com/PRAMBORS_FM.mp3'

loop = asyncio.get_event_loop()

playing = False

async def load_prambors(ctx):
    global quelink
    global quetitle
    global quedur

    global mus_format
    global title
    global duration

    global link

    mus_format = link
    title = 'PramborsFM'
    duration = 599940

    quelink.append(mus_format)
    quetitle.append(title)
    quedur.append(duration)

    await player_handler(ctx)

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
    global quetitle

    if ctx.voice_client.is_playing() and len(quetitle) == 0:
        ctx.voice_client.stop()
    elif len(quetitle) == 0:
        await ctx.send('ga ada apa apa di queue')
    elif len(quetitle) > 0:
        ctx.voice_client.pause()
        await asyncio.sleep(3)
        ctx.voice_client.stop()

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
    global embed_play
    global embed_edit
    global playing
    global msg
    global quetitle

    if playing == False:
        embed_play = discord.Embed(title="Playing now:", description=title)
        await msg.edit(embed=embed_play)
    elif playing == True:
        embed_edit = discord.Embed(title="Queued!", description=title)
        await msg.edit(embed=embed_edit)
        await asyncio.sleep(2)
        embed_play = discord.Embed(title="Playing now:", description=quetitle[0])
        await msg.edit(embed=embed_play)

async def player_handler(ctx):
    global playing
    global duration
    global quetitle
    global loop
    global msg

    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                      'options': '-vn'}

    if playing == False and len(quetitle) > 0:
        await send_playing(ctx)
        ctx.voice_client.play(discord.FFmpegPCMAudio(mus_format, **FFMPEG_OPTIONS),
                              after=lambda e: asyncio.run_coroutine_threadsafe(played(ctx), loop))
        playing = True
    elif playing == False and len(quetitle) == 0:
        embed = discord.Embed(title='Queue abis')
        await msg.edit(embed=embed)
        await asyncio.sleep(0.5)
        await msg.delete()
        qgon = True
    elif playing == True:
        await send_playing(ctx)

async def load(word):
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
        global msg
        global qgone

        await ctx.message.delete()

        word = ' '.join(args)

        if not ctx.voice_client:
            channel = ctx.message.author.voice.channel
            await asyncio.gather(channel.connect(), load(word))
            msg = await ctx.send(embed=embed_play)
            await player_handler(ctx)
        elif ctx.voice_client:
            if qgone == True:
                msg = await ctx.send(embed=embed_play)
            await load(word)
            await player_handler(ctx)
        else:
            await ctx.send('lu masuk ke voice channel dulu dong!')

    @commands.command()
    async def prambors(self, ctx):
        global msg

        channel = ctx.message.author.voice.channel

        await ctx.message.delete()

        if not ctx.voice_client:
            vc = await channel.connect()
            msg = await ctx.send(embed=embed_play)
            await load_prambors(ctx)
        elif ctx.voice_client:
            if qgone == True:
                msg = await ctx.send(embed=embed_play)
            await load_prambors(ctx)

    @commands.command()
    async def pergi(self, ctx):
        if not ctx.voice_client:
            await ctx.send('gw ga ada di channel manapun gan')
        elif ctx.voice_client:
            await nuke(ctx)
            await ctx.send('Ok gw pergi bos')
            await ctx.voice_client.disconnect()

    @commands.command()
    async def brenti(self, ctx):
        await ctx.message.delete()
        ctx.voice_client.pause()

    @commands.command()
    async def lanjut(self, ctx):
        await ctx.message.delete()
        ctx.voice_client.resume()

    @commands.command()
    async def sekip(self, ctx):
        await ctx.message.delete()
        await missile(ctx)

    @commands.command()
    async def klir(self, ctx):
        await ctx.message.delete()
        await nuke(ctx)

    @commands.command()
    async def que(self, ctx):
        global title
        global quetitle
        global duration

        await ctx.message.delete()

        i = 0

        if len(quetitle) > 0:
            embed = discord.Embed()
            for x in quetitle:
                if x == quetitle[0]:

                    menit = quedur[i] // 60
                    detik = quedur[i] % 60

                    embed.add_field(name='Currently Playing' ,value='> ' + x + ' ' + f'{menit}:{detik}')
                    i += 1
                else:
                    menit = quedur[i] // 60
                    detik = quedur[i] % 60

                    embed.add_field(name=i, value='> ' + x + ' ' + f'{menit}:{detik}')
                    i += 1

            quebed = await ctx.send(embed=embed)
            await asyncio.sleep(6)
            await quebed.delete()
        elif len(quetitle) == 0:
            mesg = await ctx.send('ga ada apa apa di queue')
            await asyncio.sleep(3)
            await mesg.delete()

def setup(client):
    client.add_cog(music(client)) 
