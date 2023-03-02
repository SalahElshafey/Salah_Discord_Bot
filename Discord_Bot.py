import discord
from discord.ext import commands,tasks
from random import choice
import random
import os
import youtube_dl
import asyncio


client=commands.Bot(command_prefix="-",intents=discord.Intents.all())
voice_clients = {}
yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': "-vn"}


sad_words=["sad","depressed","unhappy","angry","miserable","depressing","engineer"]

starter_encouragements=[ "Cheer up!" ,"Hang in there","You are a Great Person"]

status=["Sleeping","Games","Reading","Sports","having breakfast"]

punch_gifs=['https://media.tenor.com/_R4OnJYIeYcAAAAS/anime-kick.gif','https://media.tenor.com/f3J-yZcZfU0AAAAM/cat-punch.gif','https://media.tenor.com/aAnyOtOeCqEAAAAM/punch-punching.gif','https://media.tenor.com/scEQBySFfUMAAAAM/markiplier.gif']
punch_names=['punches you!']

slap_gifs=['https://media.tenor.com/EzwsHlQgUo0AAAAM/slap-in-the-face-angry.gif','https://media.tenor.com/nbT_cwrKGjwAAAAC/baby-slap.gif','https://media.tenor.com/R6LaPVpPwfcAAAAM/slap-slapping.gif','https://media.tenor.com/W0K0vteByOoAAAAC/slap-in-the-face-slap.gif','https://media.tenor.com/i3cGrnkMWl8AAAAM/slap-slapping.gif','https://media.tenor.com/LsJz2eP0FqQAAAAM/smack-slap.gif']
slap_names=['slaps you!']

clap_gifs=['https://media.tenor.com/BCZb5mOO80QAAAAS/the-wolf-of-wall-street-clap.gif','https://media.tenor.com/pFqa1UWBcdMAAAAM/applause-applaud.gif','https://media.tenor.com/YVY3T0uwt9QAAAAM/clap-clap-clap.gif','https://media.tenor.com/S7hPlmnHKLoAAAAM/steve-harvey-happy.gif','https://media.tenor.com/sQoO99AYlcUAAAAM/girl-happy.gif','https://media.tenor.com/hYVihOZcKj4AAAAM/drake-stand-up.gif']
claps=[f"{client.user}Claps!"]


Love_gifs=['https://tenor.com/view/hi-love-you-gif-25149741','https://media.tenor.com/OxjBFBS8GLoAAAAM/%D8%AD%D8%A8-%D8%B5%D9%88%D8%B1.gif','https://media.tenor.com/mabjMYRKhwIAAAAM/i-love-you.gif','https://media.tenor.com/u7yDZgVVkN4AAAAM/love-caseylina.gif','https://media.tenor.com/HZIYs5Yt53cAAAAM/love-you.gif','https://media.tenor.com/j0WJMlwc1jcAAAAM/love-stich.gif']
loves=["Loves you!"]


cry_gif=['https://media.tenor.com/6uIlQAHIkNoAAAAS/cry.gif','https://media.tenor.com/P8OYV56HSRAAAAAM/cry-sad.gif','https://media.tenor.com/FantEuP4bd4AAAAM/alex-cry.gif','https://media.tenor.com/A_ZtGhRQ4fcAAAAM/crying.gif','https://media.tenor.com/UIXwsWt9n9cAAAAS/crying-girl-crying.gif','https://media.tenor.com/pRTPXrxI2UAAAAAM/crying-meme-black-guy-cries.gif','https://media.tenor.com/K61LBZu_g70AAAAM/cry-dog.gif']
cry_=["Cries"]


@client.event
async def on_message(msg):
    if msg.content.startswith("-play"):

        try:
            voice_client = await msg.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client
        except:
            print("error")

        try:
            url = msg.content.split()[1]

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            song = data['url']
            player = discord.FFmpegPCMAudio(song, **ffmpeg_options)

            voice_clients[msg.guild.id].play(player)

        except Exception as err:
            print(err)


    if msg.content.startswith("-pause"):
        try:
            voice_clients[msg.guild.id].pause()
        except Exception as err:
            print(err)

    # This resumes the current song playing if it's been paused
    if msg.content.startswith("-resume"):
        try:
            voice_clients[msg.guild.id].resume()
        except Exception as err:
            print(err)

    # This stops the current playing song
    if msg.content.startswith("-stop"):
        try:
            voice_clients[msg.guild.id].stop()
            await voice_clients[msg.guild.id].disconnect()
        except Exception as err:
            print(err)


@client.command()
async def punch(ctx):
  embed=discord.Embed(
    color=(discord.Color.random()),
    description=f"{ctx.author.mention} {(random.choice(punch_names))}"
  )
  embed.set_image(url=(random.choice(punch_gifs)))
  await ctx.send(embed=embed)

@client.command()
async def slap(ctx):
  embed=discord.Embed(
    color=(discord.Color.random()),
    description=f"{ctx.author.mention} {(random.choice(slap_names))}"
  )
  embed.set_image(url=(random.choice(slap_gifs)))
  await ctx.send(embed=embed)

@client.command()
async def love(ctx):
   embed=discord.Embed(
      color=(discord.Color.random()), description=f"{ctx.author.mention} {(random.choice(loves))}")
   embed.set_image(url=(random.choice(Love_gifs)))
   await ctx.send(embed=embed)

@client.command()
async def clap(ctx):
  embed=discord.Embed(
      color=(discord.Color.random()),description=f"{ctx.author.mention} {(random.choice(claps))}")
  embed.set_image(url=random.choice(clap_gifs))
  await ctx.send(embed=embed)

@client.command()
async def cry(ctx):
  embed=discord.Embed(
    color=(discord.Color.random()),
    description=f"{ctx.author.mention} {(random.choice(cry_))}"
  )
  embed.set_image(url=(random.choice(cry_gif)))
  await ctx.send(embed=embed)

@tasks.loop(seconds=10)
async def change_status():
 await client.change_presence(activity=discord.Game(choice(status)))


@client.event
async def on_ready():
  change_status.start()
  print("I am all set")

@client.event
async def on_message(message):
 msg=message.content
 if any(word in msg for word in sad_words):
   await message.channel.send(random.choice(starter_encouragements))
 await client.process_commands(message)


@client.command()
async def ping(ctx):
 bot_latency= round(client.latency * 1000)
 await ctx.send(f"$$ PONG! $$ latency: {bot_latency}ms")
 

@client.command()
async def talk(ctx, *,question):
  with open("./responsis.txt","r") as f:
    random_responses=f.readlines()
    response=random.choice(random_responses)

  await ctx.send(response)

@client.command()
async def inspire(ctx):
  with open("./quotes.txt","r") as f:
    random_quotes=f.readlines()
    quotes=random.choice(random_quotes)
  await ctx.send(quotes)

client.remove_command('help')
@client.command()
async def help(ctx):
  embed=discord.Embed(
    title='Bot Commands',
    description='Welcome to the help . Here are all the commands for the bot',
    color=discord.Color.green())
  
  embed.set_thumbnail(url='https://avatars.githubusercontent.com/u/112121144?s=96&v=4')
  embed.add_field(
     name= "-spirit",
     value="It gives random quotes that may make your mood positive",
    inline=True  
  )
  embed.add_field(
     name="-talk",
     value="It makes the Bot talk to you",
    inline=True  
  )
  embed.add_field(
     name="-slap",
     value="It makes the bot to send funny Gifs with slap",
    inline=True  
  )
  embed.add_field(
     name="-punch",
     value="It makes the bot to send slap Gifs",
    inline=True  
  )
  embed.add_field(
     name="-love",
     value="It makes the bot to send love Gifs ",
    inline=True  
  )
  embed.add_field(
     name="-cry",
     value="It makes the bot to send cry Gifs ",
    inline=True  
  )
  await ctx.send(embed=embed)
    
   



client.run("MTA4MDE5Nzk4NjgyNDQ5NTE3Nw.GrcLmQ.tgiWviQyPyPSsqlzVA8XOOWYM_PYojz_zj5OsY")