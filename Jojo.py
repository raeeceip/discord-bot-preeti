import discord
import os
import pyjokes
import random
import requests
import json
from dotenv import load_dotenv
import discord.ext
from discord.ext import commands
from discord.ext.commands import Bot

# get token, server id from env
load_dotenv(".env")
token = os.getenv("TOKEN")


client = discord.Client(intents=discord.Intents.all())

Bot.command.prefix = "!"


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]["q"] + " -" + json_data[0]["a"]
    return quote


def get_meme():
    response = requests.get("https://meme-api.herokuapp.com/gimme")
    json_data = json.loads(response.text)
    meme = json_data["url"]
    return meme


def get_jokes():
    joke = pyjokes.get_joke()
    return joke


@client.event
async def on_ready():
    print(" {0.user} is logged in".format(client))
    print("bot online")
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="you")
    )


@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f"{username}: {user_message} {channel}")

    if message.author == client.user:
        return

    if message.channel.name == "general":
        if user_message.lower() == "hey preeti":
            await message.channel.send(f"Hello {username} how can I help you today")
            return
        elif user_message.lower() == "byee":
            await message.channel.send("Bye! <3")
            return
        elif user_message.lower() == "joke":
            await message.channel.send(get_jokes())
            return
        elif user_message.lower() == "cow joke":
            # fetch jokes from external file
            jokes = open("jokes.txt", "r")
            joke = random.choice(jokes.readlines())
            await message.channel.send(joke)
            return
        elif user_message.lower() == "quote":
            quote = get_quote()
            await message.channel.send(quote)
            return
        elif user_message.lower() == "meme":
            meme = get_meme()
            await message.channel.send(meme)
            return
        elif user_message.lower() == "how pretty am i today?":
            responses = [
                f"On a scale of 1-100, you are a {random.randrange(500,1000,400)}, shatter my scale kodi!",
                f'Based on my calculations, it looks like you"re a solid {random.randrange(500,1000,220)} today, amazing!',
                f"Oh my! I've never measured a {random.randrange(10,1000,100)} on my metre before, this reading is off the charts!",
                f"From what I see, I don't think i can measure it accurately, my apologies <3",
                f"Unfortunately, I can't measure prettiness levels over {random.randrange(500,1000,5)}, make my machine no break abeg",
                f"Oh sunshine, there's no one that can compare to how pretty you are today; keep shining! <3",
            ]
            await message.channel.send(responses[random.randrange(0, 5, 1)])
            return
        elif user_message.lower() == "tell me i'm pretty today":
            await message.channel.send("You're so pretty Kodi")
            return


@client.event
async def on_member_join(member):
    print(f"{member} has joined the server")
    await member.send(f"Hi {member.name}, welcome to the server!")
    await member.send("I'm Preeti, your personal assistant")
    await member.send("How can I help you today?")
    await member.send("Type 'help' to see what I can do for you")
    return


# on guild join
@client.event
async def on_guild_join(guild):
    guild = guild
    channel = "general"
    await channel.send(f"Hi there, my name's Preeti,wannatry me out?")


@Bot.command
async def ping(ctx):
    await ctx.send(
        "pong!"
    )  # simple command so that when you type "!ping" the bot will respond with "pong!"


async def kick(ctx, member: discord.Member):
    try:
        await member.kick(reason=None)
        await ctx.send(
            "kicked " + member.mention
        )  # simple kick command to demonstrate how to get and use member mentions
    except:
        await ctx.send("bot does not have the kick members permission!")


client.run(token)
