import discord, io, aiohttp, time, asyncio, re, requests, praw
from discord.ext import tasks
from bs4 import BeautifulSoup
from discord.ext import commands
from typing import Awaitable
from urllib.request import urlopen
import urllib.request as urllib2
from datetime import datetime
from googlesearch import search 
from youtube_search import YoutubeSearch
import random as _random


r = praw.Reddit(client_id=client_id.txt,
                client_secret=client_secret.txt,
                user_agent="my user agent")


TOKEN = token.txt
bot = commands.Bot(command_prefix='$')
client = discord.Client()
bot.remove_command('help')

@bot.command() # A google command cus why not
async def google(ctx, arg):
    if arg == None:
        await ctx.send("You need to add a search term! Ex) $google Carpe Diem")
    else:
        await ctx.send("https://www.google.com/search?q=" + arg)
        query = arg
        await ctx.send("**Top 5 results for **" + arg)
        for results in search(query, stop=5):
            await ctx.send("<"+results+">")
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for $help"))
    
@bot.command()
async def spam(ctx, members: commands.Greedy[discord.Member], content):
    for member in members:
        total = '50'
        for i in range (int(total)):
            await member.send(content)
@spam.error
async def spam_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.send("Please specify a message and User!\n Ex) ```$spam @PlentyBot Hello```")
            
@bot.command() # A youtube search because also why not
async def youtube(ctx, arg):
    await ctx.send("https://www.youtube.com/results?search_query=" + arg)                                          
              
@bot.command()
async def help(message):
    embed = discord.Embed(colour=discord.Colour(0x4472e4), url="https://discordapp.com", description="**Google Search:**\n```CSS\n$google + [search term]```\n**Youtube Search:**\n```CSS\n$youtube + [search term]```\n**Memes:**\n```CSS\n$meme```\n**Spam a persons DM's:**\n```CSS\n$spam [@user] [message]```")
    embed.set_author(name="StugotsZach ⚡", url="https://www.youtube.com/channel/UCZHIDwfPGxdbttd_Xwel9lw", icon_url="https://lh3.googleusercontent.com/a-/AOh14Ghq4OX1JHecJCDgTEwr5WbTkt9jKOtkZgOTPYw_Yw=s360-c")
    embed.set_footer(text="⛆⛆⛆⛆⛆⛆⛆⛆⛆⛆⛆⛆⛆⛆⛆⛆")
    await message.channel.send(content="**Help Message**", embed=embed)


    
@bot.command() #Displays a random meme from reddit; this took way longer to figure out than it should have :(
async def meme(ctx):     
    submission = r.subreddit("dankmemes").random()
    await ctx.send(submission.url)
    
@bot.command() 
async def reddit(ctx, arg):
    try:
        submission = r.subreddit(arg).random()
        await ctx.send(submission.url) 
        
    except MissingRequiredArgument(param):
        await ctx.send("Did you input a subreddit? or misspell?\nEx) ```$reddit dankmemes")
        
@bot.command()
async def blackmagic(ctx):     
    submission = r.subreddit("blackmagicfuckery").random()
    await ctx.send(submission.url)   
    
    
@bot.command(aliases=['ysk', 'YSK'])
async def youshouldknow(message):     
    submission = r.subreddit("YouShouldKnow").random()
    text = submission.selftext
    url = submission.url
    today = datetime.today().strftime('%Y-%m-%d')
    await message.channel.send("*Note if nothing happens the post is too long*")
    embed = discord.Embed(title="Original Post", colour=discord.Colour(0xfffc5b), url=url, description="```" + text + "```")
    embed.set_footer(text="Made by StugotsZach | " + today)
    await message.channel.send(embed=embed)
    

    
@bot.command()
async def interesting(ctx):     
    submission = r.subreddit("Damnthatsinteresting").random()
    try:
        await ctx.send("**"+submission.title+"**")
        await ctx.send(submission.selftext)
        await ctx.send(submission.url)
      
      
    except:
        await ctx.send(submission.url)
        await ctx.send(submission.title)
@bot.command()
async def showerthought(ctx):   
    submission1 = r.subreddit("Showerthoughts").random()
    await ctx.send("```"+submission1.title+"```")

@bot.command()
async def profile(message, member: discord.Member):
    userAvatarUrl = member.avatar_url
    today = datetime.today().strftime('%Y-%m-%d')
    embed = discord.Embed(title="**"+str(member)+"**", colour=discord.Colour(0xfffc5b))
    embed.set_image(url=userAvatarUrl)
    embed.set_footer(text="Made By StugotsZach | " + str(today))
    await message.channel.send(embed=embed)

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member):
    if administrator == False:
        await ctx.send("Looks like you dont have the authority to ban anyone")
    else:
        await member.ban()
        await member.send(member + "Its seems you have been banned from {ctx.guild.name}")
        
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    if administrator == False:
        await ctx.send("Looks like you dont have the authority to ban anyone")
    else:
        for ban_entry in banned_users:
            user = ban_entry.user
      
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send("Unbanned @" + member)
        
@bot.command(aliases=['8ball', 'eightball'])
async def _8ball(ctx, *, question):
    responses=['As I see it, yes',
               'Ask again later',
               'Better not tell you now',
               'Cannot predict now',
               'Concentrate and ask again',
               'Don’t count on it',
               'It is certain',
               'It is decidedly so',
               'Most likely',
               'My reply is no',
               'My sources say no',
               'Outlook not so good',
               'Outlook good',
               'Reply hazy, try again',
               'Signs point to yes',
               'Very doubtful',
               'Without a doubt',
               'Yes',                 
               'Yes – definitely',
               'You may rely on it']
    await ctx.send(_random.choice(responses))
    
@bot.command()
async def clear(ctx, amount=None):
  try:
      await ctx.channel.purge(limit=int(amount))
      
  except TypeError:      
      await ctx.send("You need to have a number of messages to clear Ex) $clear 10")

@bot.command()
async def stats(ctx):
    memberss = ctx.guild.member_count
    guild_name = bot.get_guild("ID")
    await ctx.send(guild_name + "\nTotal Members in guild: `" + str(memberss) + "`")
    
@bot.command()
async def servers():
    servers = list(self.client.servers)
    await ctx.send(f"Connected on {str(len(servers))} servers:")
    await ctx.send('\n'.join(server.name for server in servers))    
    
bot.run(TOKEN)

