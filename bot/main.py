import discord
from discord.ext import commands
import random


bot = commands.Bot(command_prefix='$')
#kick an member from the server.
@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has kicked.')

@bot.command()    
async def sai(ctx, member: discord.Member,*, reason=None):
    await member.edit(voice_channel=None)
    await ctx.send(f'User {member} foi de base.')

#its a russian roulet thats kicks from the channel you if get an double $roleta 100
@bot.command()
async def roleta(ctx, i:int):
    n = random.randint(0,i) 
    await ctx.send(f'numero {n}')
    ultimo_digito = n % 100
    z = ultimo_digito % 11
    if(z == 0):
        await sai(ctx, ctx.author)



bot.run('BOT TOKEN HERE')