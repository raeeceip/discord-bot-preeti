import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import openai

# Load environment variables
load_dotenv(".env")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set up OpenAI
openai.api_key = OPENAI_API_KEY

# Set up Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize conversation history
conversation_history = {}

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    await bot.change_presence(activity=discord.Game(name="Chat with me!"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        async with message.channel.typing():
            # Get or initialize conversation history
            if message.channel.id not in conversation_history:
                conversation_history[message.channel.id] = []

            # Add user message to history
            conversation_history[message.channel.id].append({"role": "user", "content": message.content})

            # Prepare messages for API call
            messages = [
                {"role": "system", "content": "You are Preeti, a friendly and helpful AI assistant in a Discord server."},
                *conversation_history[message.channel.id]
            ]

            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150
            )

            # Get response content
            ai_response = response.choices[0].message['content']

            # Add AI response to history
            conversation_history[message.channel.id].append({"role": "assistant", "content": ai_response})

            # Trim history if it gets too long
            if len(conversation_history[message.channel.id]) > 10:
                conversation_history[message.channel.id] = conversation_history[message.channel.id][-10:]

            # Send response
            await message.channel.send(ai_response)

    await bot.process_commands(message)

# Run the bot
bot.run(DISCORD_TOKEN)
