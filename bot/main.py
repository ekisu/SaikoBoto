import discord
import json
from discord.ext import commands
import random
import datetime
from pytz import common_timezones, timezone
import time
from jikanpy import Jikan
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient


bot = commands.Bot(command_prefix='$')

@bot.command()
async def on_message(ctx): 
    embedVar = discord.Embed(title="Title", description="Desc", color=0x00ff00)
    embedVar.add_field(name="Field1", value="hi", inline=False)
    embedVar.add_field(name="Field2", value="hi2", inline=False)
    await ctx.send(embed=embedVar)

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

@bot.command()
#
async def rankedmapsby(ctx, user:str):
    
    osuid = oauth.get(f'https://osu.ppy.sh/api/v2/users/{user}') #pegando id do usuario
    id = osuid.json()["id"] #pegou id do usuario
    mapsearch= oauth.get(f'https://osu.ppy.sh/api/v2/beatmapsets/search/?q={id}&sort=ranked_desc') #procurando os mapas do usuario pelo id
    beatmapsets = mapsearch.json()['beatmapsets'] #pega a resposta do site do osu e transforma em um dicionario do python

    def chave(beatmap): #retorna a dificuldade do beatmap.
        print(beatmap)
        return beatmap['difficulty_rating']

    for set in beatmapsets:
        artista = set["artist"]
        titulo = set["title"]
        beatmaplink = f'https://osu.ppy.sh/beatmapsets/{set["id"]}'
        cover = set["covers"]["card"]
        beatmaps = sorted(set['beatmaps'], key = chave)
        dificuldades = []
        
        for diff in beatmaps:
            novadificuldade = diff["version"]        
            ar = str(diff["ar"])
            accuracy = str(diff['accuracy'])
            cs = str(diff["cs"])
            bpm = str(diff["bpm"])
            #max_combo = str(diff["max_combo"]) max combo ficou meio ruim na exibicao

            dificuldades.append(novadificuldade + ' | AR: ' + ar + ' | CS: ' + cs + ' | OD: ' + accuracy + ' | bpm: ' + bpm) #+ ' max combo: '+ max_combo)

        dificuldadejuntas = '\n'.join(dificuldades)

        embedVar = discord.Embed(title= titulo,url=beatmaplink, description= artista, color=0x00ff00)
        embedVar.add_field(name="Link", value=beatmaplink, inline=False)
        embedVar.add_field(name="Dificuldades", value=dificuldadejuntas, inline=False)
        embedVar.set_image(url=cover)
        await ctx.send(embed=embedVar)


f = open("config.json", "r")
config = json.load(f)

client_id = config['osu-client-id']
client_secret = config['osu-client-secret']
scopes = ['public']
client = BackendApplicationClient(client_id=client_id, scope = scopes)


oauth = OAuth2Session(client=client, scope = scopes)
token = oauth.fetch_token(token_url='https://osu.ppy.sh/oauth/token', client_id=client_id, client_secret=client_secret)


bot.run(config['token'])
