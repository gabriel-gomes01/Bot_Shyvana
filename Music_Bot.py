from contextlib import nullcontext
from operator import concat
import discord
from discord.ext import commands
import youtube_dl
import os

#* 
#    OBS: os parametros que cada função recebe são o "CTX" e "URL", contexto e link respectivamente
# 
# 
# *#


# Configura variavel de permisão do Bot
intents = discord.Intents.all()

# Configura o Prefixo do bot e dá as permissões a ele
bot = commands.Bot(command_prefix='s.',intents=intents)

#Lista de reprodução
playlist = []

# Inicia a conexão com o Discord
@bot.event
async def on_ready():
    print('Online.')

# Join channel
@bot.command(name='join')
async def join(ctx):
   
   if not ctx.author.voice:
       await ctx.send("Entre em um Canal de Voz")
   else:
        channel = ctx.author.voice.channel
        voice_client = await  channel.connect()
        await ctx.send("Entrei na Call")
    
   
#Sair do canal de voz
@bot.command(name="leave")
async def leave(ctx):
    await ctx.voice_client.disconnect()

# play de musica
@bot.command(name='play')
async def play(ctx, url):

    guild = ctx.message.guild
    voice_client = guild.voice_client

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


    channel = ctx.author.voice.channel
    if not voice_client or not voice_client.is_connected():
        voice_client = await channel.connect()

    await ctx.send(f'Tocando {url}')


bot.run('TOKEN')