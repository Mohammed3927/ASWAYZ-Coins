import discord
from discord.ext import commands
import json
import os
import random
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread

# File for storing coin data
COIN_FILE = "coins.json"
TIME_FILE = "time.json"

# Load or create the database for coins and message times
def load_data(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return {}

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

coins = load_data(COIN_FILE)
last_message_time = load_data(TIME_FILE)

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.messages = True
bot = commands.Bot(command_prefix='C', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.change_presence(activity=discord.Streaming(name="Live News", url="https://kick.com/mtnews"))

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    user_id = str(message.author.id)
    now = datetime.utcnow()
    
    # Check if the user is eligible for earning coins
    if user_id not in last_message_time or now - last_message_time[user_id] >= timedelta(hours=1):
        earned_coins = random.randint(3, 15)
        coins[user_id] = coins.get(user_id, 100) + earned_coins
        save_data(COIN_FILE, coins)
        last_message_time[user_id] = now
        save_data(TIME_FILE, last_message_time)
        await message.channel.send(f'🎉 {message.author.mention} earned {earned_coins} ASWAYZ Coins for chatting!')
    
    await bot.process_commands(message)

@bot.command()
async def C(ctx, member: discord.Member = None, amount: int = None):
    user_id = str(ctx.author.id)
    target_id = str(member.id) if member else None
    
    if user_id not in coins:
        coins[user_id] = 100  # Default starting coins
    if target_id and target_id not in coins:
        coins[target_id] = 100
    
    if member is None:
        await ctx.send(f'💰 **You have {coins[user_id]} ASWAYZ Coins**')
    elif amount is None:
        await ctx.send(f'💰 **{member.name} has {coins[target_id]} ASWAYZ Coins**')
    else:
        if coins[user_id] < amount:
            await ctx.send("❌ You don't have enough coins!")
            return
        
        coins[user_id] -= amount
        coins[target_id] += amount
        save_data(COIN_FILE, coins)
        await ctx.send(f'✅ **{ctx.author.name} sent {amount} ASWAYZ Coins to {member.name}!**')

@bot.command()
async def add(ctx, member: discord.Member, amount: int):
    if amount <= 0:
        await ctx.send("❌ Amount must be greater than zero!")
        return
    
    user_id = str(member.id)
    coins[user_id] = coins.get(user_id, 100) + amount
    save_data(COIN_FILE, coins)
    await ctx.send(f'✅ **Added {amount} ASWAYZ Coins to {member.name}!**')

@bot.command()
async def remove(ctx, member: discord.Member, amount: int):
    if amount <= 0:
        await ctx.send("❌ Amount must be greater than zero!")
        return
    
    user_id = str(member.id)
    if coins.get(user_id, 100) < amount:
        await ctx.send("❌ User does not have enough coins!")
        return
    
    coins[user_id] -= amount
    save_data(COIN_FILE, coins)
    await ctx.send(f'✅ **Removed {amount} ASWAYZ Coins from {member.name}!**')

# Set up Flask web server
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# Start Flask server in a separate thread
Thread(target=run_web).start()

# Run the bot
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
bot.run(TOKEN)
