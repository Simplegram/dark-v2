import discord
import asyncio
import lavalink
import re

from discord import utils, Embed
from discord.ext import commands

title = []
url_rx = re.compile(r'https?://(?:www\.)?.+')
tracks_embed = Embed(title='N/A')
editor = 0
player = 0

qgon = True


class MusicCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.music = lavalink.Client(815794671955345438)
        self.client.music.add_node('localhost', 7000, 'hgloow2919', 'ap', 'music-node')
        self.client.add_listener(self.client.music.voice_update_handler, 'on_socket_response')
        self.client.music.add_event_hook(self.track_hook)

    @commands.command()
    async def yt(self, ctx, *, query):
        global tracks_embed
        global qgon
        global player
        global editor

        member = utils.find(lambda m: m.id == ctx.author.id, ctx.guild.members)
        if member is not None and member.voice is not None:
            vc = member.voice.channel
            plr = self.client.music.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
            if not plr.is_connected:
                plr.store('channel', ctx.channel.id)
                await self.connect_to(ctx.guild.id, str(vc.id))
                editor = await ctx.send(embed=tracks_embed)
        elif qgon is True:
            editor = await ctx.send(embed=tracks_embed)

        try:
            player = self.client.music.player_manager.get(ctx.guild.id)

            query = query.strip('<>')

            if not url_rx.match(query):
                query = f'ytsearch:{query}'

            results = await player.node.get_tracks(query)

            if results['loadType'] == 'PLAYLIST_LOADED':
                tracks = results['tracks']

                for x in tracks:
                    player.add(requester=ctx.author.id, track=x)

                tracks_embed = Embed(title='Playlist queued:', description=f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks')
                msg = await ctx.send(embed=tracks_embed)
                await ctx.message.delete()
                await asyncio.sleep(3)
                await msg.delete()
            else:
                tracks = results['tracks'][0:5]

                res_embed = Embed()

                i = 1
                for x in tracks:
                    res_embed.add_field(name=f'> {i}', value=x['info']['title'])
                    i += 1

                await ctx.send(embed=res_embed)

                await ctx.message.delete()

                def check(m):
                    return m.author.id == ctx.author.id

                response = await self.client.wait_for('message', check=check)
                track = tracks[int(response.content) - 1]

                await response.delete()

                player.add(requester=ctx.author.id, track=track)

            if not player.is_playing:
                await player.play()

        except Exception as error:
            print(error)

    @commands.command()
    async def sekip(self, ctx):
        await ctx.message.delete()
        await player.skip()

    @commands.command()
    async def paus(self, ctx):
        await player.set_pause(True)
        await ctx.message.delete()

    @commands.command()
    async def lanjut(self, ctx):
        await player.set_pause(False)
        await ctx.message.delete()

    @commands.command()
    async def setop(self, ctx):
        await player.stop()
        await ctx.message.delete()

    @commands.command()
    async def klir(self, ctx):
        player.queue.clear()
        await ctx.message.delete()

    @commands.command()
    async def ff(self, ctx, args: int):
        args = args * 1000
        await player.seek(args)
        await ctx.message.delete()

    @commands.command()
    async def que(self, ctx):
        que = player.queue
        new = []

        await ctx.message.delete()

        i = 0
        for x in que:
            one = str(que[i]).split('title=')
            one.pop(0)

            two = one[0].split('identifier=')
            two.pop(1)

            new.append(two[0])
            i += 1

        quebed = Embed()
        i = 0
        for x in new:
            quebed.add_field(name=f'> {i+1}', value=new[i])
            i += 1

        que = await ctx.send(embed=quebed)
        await asyncio.sleep(6)
        await que.delete()

    @commands.command()
    async def acak(self, ctx):
        player.shuffle
        await ctx.message.delete()

    async def track_hook(self, event):
        global qgon
        global tracks_embed

        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)

            qgon = True
            await editor.delete()

    async def track_hook(self, event):
        global qgon
        global tracks_embed

        if isinstance(event, lavalink.events.TrackStartEvent):
            qgon = False

            await asyncio.sleep(1)

            tracks_embed = Embed(title='Now playing:', description=player.current.title)
            await editor.edit(embed=tracks_embed)

    async def connect_to(self, guild_id: int, channel_id: str):
        ws = self.client._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)


def setup(client):
    client.add_cog(MusicCog(client))
