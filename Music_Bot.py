from contextlib import nullcontext
from operator import concat
import discord
from discord.ext import commands
import youtube_dl
import os

#* 
#    OBS: os parametros que cada função recebe são o "CTX" e "URL", contexto e link respectivamente
# *#


# Configura variavel de permisão do Bot
intents = discord.Intents.all()

# Configura o Prefixo do bot e dá as permissões a ele
bot = commands.Bot(command_prefix='s.',intents=intents)

# Inicia a conexão com o Discord
@bot.event
async def on_ready():
    print('Online.')

# play de musica
@bot.command(name='play')
async def play(ctx, url):

    #Lista de reprodução
    contador = 0
    playlistDownload = []
    playlistReproducao = []
    
    guild = ctx.message.guild
    voice_client = guild.voice_client

    playlistDownload.append(url)
    await ctx.send(f'{url} adicionado à lista de reprodução.')

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
       
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.remove(file)
                for urls in playlistDownload:
                    ydl.download([urls])
        

    channel = ctx.author.voice.channel
    if not voice_client or not voice_client.is_connected():
        voice_client = await channel.connect()

    await ctx.send(f'Tocando {url}')

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            playlistReproducao.append(file)

   # for music in playlistReproducao:
   #     await voice_client.play(discord.FFmpegPCMAudio(music))
   #     voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
   #     voice_client.source.volume = 0.10

bot.run('TOKEN')