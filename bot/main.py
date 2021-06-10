import discord
import json
from discord.ext import commands
import random
import datetime
from pytz import all_timezones, common_timezones, timezone
import time


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

@bot.command()
async def converter(ctx, horario: str, tz1: str, tz2 : str):
    try:
        agora = datetime.datetime.now()
        horario_obj = time.strptime(horario, '%H:%M:%S')
        horario_obj2 = datetime.time(horario_obj.tm_hour,horario_obj.tm_min, horario_obj.tm_sec)
        horario_combinado = datetime.datetime.combine(agora, horario_obj2)
        recebe_tz1 = timezone(tz1)
        recebe_tz2 = timezone(tz2)
        horario_combinadotz1 = recebe_tz1.localize(horario_combinado)
        horario_timezone = horario_combinadotz1.astimezone(recebe_tz2)
        h_formatado = horario_timezone.strftime('%H:%M:%S')
        await ctx.send(f'Horario {horario} na time zone {tz2} é de: {h_formatado}')
    except:
        await ctx.send(f'Digitou o formato do horario errado, ou o TIMEZONE errado')


@bot.command()
async def timezones(ctx):
    i = common_timezones
    n = 6
    len_i = len(i) 
    i_splited = []
    for x in range(n):
        start = int(x*len_i/n)
        end = int((x+1)*len_i/n)
        i_splited.append(i[start:end])
    for item in i_splited:
        await ctx.send(f'{item}')




f = open("config.json", "r")
config = json.load(f)


bot.run(config['token'])