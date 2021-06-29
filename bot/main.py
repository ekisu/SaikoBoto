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
    await ctx.send(f'User {member.nick or member.name} has kicked.')

@bot.command()    
async def sai(ctx, member: discord.Member,*, reason=None):
    await member.edit(voice_channel=None)
    await ctx.send(f'{member.nick or member.name} foi de base.')

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
async def rankedmapsby(ctx, user:str):
    osuid = oauth_osu.get(f'https://osu.ppy.sh/api/v2/users/{user}') #pegando id do usuario
    id = osuid.json()["id"] #pegou id do usuario
    mapsearch= oauth_osu.get(f'https://osu.ppy.sh/api/v2/beatmapsets/search/?q={id}&sort=ranked_desc') #procurando os mapas do usuario pelo id
    beatmapsets = mapsearch.json()['beatmapsets'] #pega a resposta do site do osu e transforma em um dicionario do python

    def chave(beatmap): #retorna a dificuldade do beatmap.
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

@bot.command()
async def followson(ctx, user:str):
    twitch_id = oauth_twitch.get(f'https://api.twitch.tv/helix/users?login={user}')
    id = twitch_id.json()['data'][0]['id']
    follows_response = oauth_twitch.get(f'https://api.twitch.tv/helix/users/follows?from_id={id}&first=100')
    lista_de_follows = (follows_response.json()['data'])
    lista_de_ids = []

    #pega os campos to id no follow e aloca no lista_de_ids
    for follow in lista_de_follows: 
        lista_de_ids.append(follow['to_id']) 

    #ver na lista de ids se o streamer esta
    for follow_id in lista_de_ids:
        verifica_on_response = oauth_twitch.get(f'https://api.twitch.tv/helix/streams?user_id={follow_id}')
        esta_on = verifica_on_response.json()['data']
        if not len(esta_on) == 0:
            nome = esta_on[0]['user_login']
            jogo = esta_on[0]['game_name']  
            titulo = esta_on[0]['title'][:100].replace("\n"," ")
            thumb = esta_on[0]['thumbnail_url'].format(width = 250, height = 200)
            link = (f"https://twitch.tv/{nome}")
            
            embedVar = discord.Embed(title= nome,url=link , description= jogo, color=0x00ff00)
            embedVar.add_field(name="Link", value=link, inline=False)
            embedVar.add_field(name="Titulo", value=titulo, inline=False)
            embedVar.set_image(url=thumb)

            await ctx.send(embed=embedVar)
            

f = open("config.json", "r")
config = json.load(f)


def criar_client_twitch():
    client_id_twitch = config['twitch-client-id']
    client_secret_twitch = config['twitch-client-secret']
    #scopes_twitch = ['user:read:follows']
    client_twitch = BackendApplicationClient(client_id=client_id_twitch)
    oauth_twitch =  OAuth2Session(client=client_twitch)
    oauth_twitch.headers.update({'Client-Id': client_id_twitch, 'Client-Secret': client_secret_twitch} )
    token = oauth_twitch.fetch_token(include_client_id= True, token_url='https://id.twitch.tv/oauth2/token', client_id= client_id_twitch, client_secret= client_secret_twitch) 
    return oauth_twitch



def criar_client_osu():
    client_id = config['osu-client-id']
    client_secret = config['osu-client-secret']
    scopes = ['public']
    client_osu = BackendApplicationClient(client_id=client_id, scope = scopes)
    oauth = OAuth2Session(client=client_osu, scope = scopes)
    token = oauth.fetch_token(token_url='https://osu.ppy.sh/oauth/token', client_id=client_id, client_secret=client_secret)
    return oauth

oauth_osu = criar_client_osu()
oauth_twitch = criar_client_twitch()
bot.run(config['token'])
