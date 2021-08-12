import discord

from discord.ext import commands

pcode = 22283
link = f'https://{pcode}.live.streamtheworld.com/PRAMBORS_FM.mp3'

class prambors(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def prambors(self, ctx):
        channel = ctx.message.author.voice.channel

        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}

        if not ctx.voice_client:
            await ctx.send('Loading...')
            vc = await channel.connect()
            vc.play(discord.FFmpegOpusAudio(link, **FFMPEG_OPTIONS))
            await ctx.send('Playing Prambors Radio')
        elif ctx.voice_client:
            await ctx.send('Loading...')
            ctx.voice_client.play(discord.FFmpegOpusAudio(link, **FFMPEG_OPTIONS))
            await ctx.send('Playing Prambors Radio')
        else:
            await ctx.send('lu masuk ke voice channel dulu dong')

def setup(client):
    client.add_cog(prambors(client))