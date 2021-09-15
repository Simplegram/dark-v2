import discord
import youtube_dl
import asyncio

from discord.ext import commands

bot = discord.Client

quelink = []
quetitle = []
quedur = []

title = ''
mus_format = ''
duration = 0
msg = 0

qgone = True
repeat = False
playing = False

embed_play = discord.Embed(title='N/A')
embed_edit = discord.Embed()

pcode = 22253
link = f'https://{pcode}.live.streamtheworld.com/PRAMBORS_FM.mp3'


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

    player_handler(ctx)


async def ulangan():
    global repeat

    if repeat is False:
        repeat = True
    elif repeat is True:
        repeat = False


async def nuke():
    global quelink
    global quetitle
    global quedur

    if len(quelink) > 0:
        quelink = quelink[:len(quelink) - (len(quelink) - 1)]
        quetitle = quetitle[:len(quetitle) - (len(quetitle) - 1)]
        quedur = quedur[:len(quedur) - (len(quedur) - 1)]


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


def send_playing():
    global embed_play
    global embed_edit
    global playing
    global quetitle
    global msg

    if playing is False:
        embed_play = discord.Embed(title="Playing now:", description=title)
        msg.edit(embed=embed_play)
    elif playing is True:
        embed_edit = discord.Embed(title="Queued!", description=title)
        msg.edit(embed=embed_edit)
        asyncio.sleep(1.5)
        embed_play = discord.Embed(title="Playing now:", description=quetitle[0])
        msg.edit(embed=embed_play)


def played(ctx):
    global title
    global duration
    global mus_format
    global playing
    global repeat

    if len(quelink) > 0:
        if repeat is False:
            quelink.pop(0)
            quetitle.pop(0)
            quedur.pop(0)

    if len(quelink) > 0:
        mus_format = quelink[0]
        title = quetitle[0]
        duration = quedur[0]

    playing = False
    player_handler(ctx)


def ffm(ctx):
    global playing

    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                      'options': '-vn'}

    ctx.voice_client.play(discord.FFmpegPCMAudio(mus_format, **ffmpeg_options), after=lambda e: played(ctx))
    playing = True


def player_handler(ctx):
    global playing
    global duration
    global quetitle
    global qgone
    global msg

    if playing is False and len(quetitle) > 0:
        send_playing()
        ffm(ctx)
    elif playing is False and len(quetitle) == 0:
        embed = discord.Embed(title='Queue abis')
        msg.edit(embed=embed)
        msg.delete()
        qgone = True
    elif playing is True:
        send_playing()


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
            title = 'title'
            duration = 0

    quelink.append(mus_format)
    quetitle.append(title)
    quedur.append(duration)


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    global title
    global mus_format

    @commands.command()
    async def yt(self, ctx, *args):
        global playing
        global qgone
        global msg

        await ctx.message.delete()

        word = ' '.join(args)

        if not ctx.voice_client:
            channel = ctx.message.author.voice.channel
            await asyncio.gather(channel.connect(), load(word))
            msg = await ctx.send(embed=embed_play)
            qgone = False
            player_handler(ctx)
        elif ctx.voice_client:
            if qgone is True:
                msg = await ctx.send(embed=embed_play)
                qgone = False
            await load(word)
            player_handler(ctx)
        else:
            await ctx.send('lu masuk ke voice channel dulu dong!')

    @commands.command()
    async def prambors(self, ctx):
        global qgone
        global msg

        channel = ctx.message.author.voice.channel

        await ctx.message.delete()

        if not ctx.voice_client:
            await channel.connect()
            msg = await ctx.send(embed=embed_play)
            qgone = False
            await load_prambors(ctx)
        elif ctx.voice_client:
            if qgone is True:
                msg = await ctx.send(embed=embed_play)
                qgone = False
            await load_prambors(ctx)

    @commands.command()
    async def pergi(self, ctx):
        if not ctx.voice_client:
            await ctx.send('gw ga ada di channel manapun gan')
            await asyncio.sleep(1)
            await ctx.message.delete()
        elif ctx.voice_client:
            await nuke()
            await ctx.send('Ok gw pergi bos')
            await ctx.voice_client.disconnect()
            await asyncio.sleep(1)
            await ctx.message.delete()

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
        await nuke()

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

                    embed.add_field(name='Currently Playing', value='> ' + x + ' ' + f'{menit}:{detik}')
                    i += 1
                else:
                    menit = quedur[i] // 60
                    detik = quedur[i] % 60

                    embed.add_field(name=str(i), value='> ' + x + ' ' + f'{menit}:{detik}')
                    i += 1

            quebed = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await quebed.delete()
        elif len(quetitle) == 0:
            mesg = await ctx.send('ga ada apa apa di queue')
            await asyncio.sleep(1.5)
            await mesg.delete()


def setup(client):
    client.add_cog(Music(client))
