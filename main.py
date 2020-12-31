import discord
import json, os
import time
from discord.ext import tasks
from discord.ext import commands


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=['m.', 'M.'], case_insensitive=True, intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("m.help"))
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f"cogs.{filename[:-3]}")
    loop.start()
    print("READYY!")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("The command you specified was not found. Type f.help to see all available commands.")

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You are missing a required argument.")

    elif isinstance(error, discord.ext.commands.errors.MissingPermissions) or isinstance(error, discord.Forbidden):
        await ctx.send("Sorry. You don't have the permission for that command.")

    elif isinstance(error, discord.ext.commands.errors.CommandOnCooldown) and ctx.command.name == "report":
        await ctx.message.delete()
        await ctx.author.send(f"""Sorry, but we have made a cooldown to prevent the abuse of the command. Try again in {error.retry_after:,.2f} seconds.
If you want to report something before the cooldown is over or you made a report on accident then please contact a staff member and we will get it sorted out.""")
    elif isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
        await ctx.send(f"You need to wait {error.retry_after:,.2f} seconds before trying this command again.")

    else: await ctx.send(error)

@tasks.loop(seconds=60)
async def loop():
    timer = int(open('time.txt', 'r').read().strip())
    to_del = []
    with open('server.json') as f:
        f = json.load(f)
        for i in f['users']:
            if time.time()-int(f['users'][i]['approved'])>timer*2:
                guild = client.get_guild(int(open('guild_id.txt', 'r').read()))
                user = guild.get_member(int(i))
                await user.remove_roles(guild.get_role(int(open('role_id.txt', 'r').read())))
                await user.send("You have run out of your membership. Please refresh it with the verify command to get your role back.")
                to_del.append(i)
            elif timer < time.time()-int(f['users'][i]['approved']) < timer+100:
                user = await client.fetch_user(int(i))
                await user.send("You have run out of your membership. Please refresh it with the verify command within the next 30 days.")

    for i in to_del:
        f['users'].pop(i)

    with open('server.json', 'w') as file:
        json.dump(f, file, indent=2, separators=(',', ': '))


client.run('NzkwMzAyMTk1MzU4MzY3Nzk1.X9-oRg.H9F_l9ugwIm3BKQqb6au2LxT9Lk')
