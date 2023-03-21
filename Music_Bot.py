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

# Inicia a conexão com o Discord
@bot.event
async def on_ready():
    print('Online.')

# Join channel
@bot.command(name='join')
async def join(ctx):

    channel = ctx.author.voice.channel
    voice_client = await  channel.connect()  
    await ctx.send("Entrei na Call")
    print("Entrei na call")


#Sair do canal de voz
@bot.command(name="leave")
async def leave(ctx):
    await ctx.voice_client.disconnect()

#play de musica
@bot.command(name='play')
async def play(ctx, url):

    #guild = ctx.message.guild
    #voice_client = guild.voice_client

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

    song = os.path.isfile("song.mp3")
    try:
        if song:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Espere até que a música acabe, ou use leave/stop")
        return

    channel = ctx.author.voice.channel
    voice_client = await channel.connect()
    await ctx.send(f'Tocando {url}')

    #*for file in os.listdir("./"):
    #    if file.endswith(".mp3"):
    #        os.rename(file, "song.mp3")

    #voice_client.play(discord.FFmpegPCMAudio("song.mp3"))
    #voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
    #*#voice_client.source.volume = 0.10


#Pausa a Musica
@bot.command(name='stop')
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()
    else:
        await ctx.send("Não tem nada tocando.")
        
bot.run('')