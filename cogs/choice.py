import random

from discord.ext import commands

class pilihan(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def pilih(self, ctx, *args):
        kotak = list(args)

        await ctx.send(random.choice(kotak))

def setup(client):
    client.add_cog(pilihan(client))
