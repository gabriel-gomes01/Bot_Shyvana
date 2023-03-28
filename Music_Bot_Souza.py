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
playlist = ["url"]
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


# Adiciona música à lista de reprodução
@bot.command(name='add')
async def add(ctx, url):
    global playlist
    playlist.append(url)
    await ctx.send(f'{url} adicionado à lista de reprodução.')


# Toca a próxima música na lista de reprodução
@bot.command(name='skip')
async def play_next(ctx):
    if playlist:
        url = playlist.pop(0)
        await play(ctx, url)
        await play_next(ctx)
    else:
        await ctx.send('Fim da lista de reprodução.')



# play de musica
@bot.command(name='play')
async def play(ctx, url):

    guild = ctx.message.guild
    voice_client = guild.voice_client

    if os.path.exists("song.mp3"):
     os.remove("song.mp3")

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
    if not voice_client or not voice_client.is_connected():
        voice_client = await channel.connect()

    await ctx.send(f'Tocando {url}')

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")

    voice_client.play(discord.FFmpegPCMAudio("song.mp3"))
    voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
    voice_client.source.volume = 0.10




#Parar a Musica
@bot.command(name='stop')
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()
    else:
        await ctx.send("Não tem nada tocando.")
        
bot.run('TOKEN')