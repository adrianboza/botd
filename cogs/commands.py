import discord
import json, time
from discord.ext import commands


class Helpful(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def verify(self, ctx, id):
        await ctx.send("The staff are verifying your code.")
        channel = self.client.get_channel(int(open('channel_id.txt', 'r').read()))
        await channel.send(f"**{ctx.author}** has sent the code '{id}' to be verified")

    @commands.command()
    async def accept(self, ctx, user: discord.Member):
        await user.add_roles(ctx.guild.get_role(int(open('role_id.txt', 'r').read())))
        with open('server.json') as f:
            f = json.load(f)
            f['users'][user.id] = {"approved": time.time()}

        with open('server.json', 'w') as file:
            json.dump(f, file, indent=2, separators=(',', ': '))

        await ctx.send("The specified user has been given the role.")

    @commands.command()
    async def deny(self, ctx, user: discord.Member, *, reason=None):
        await user.send(f"Your code has been denied by the staff team.\nReason: {reason}")
        await ctx.send("The user has been informed of the denied code.")


def setup(client):
    client.add_cog(Helpful(client))