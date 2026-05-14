import discord
from discord.ext import commands
import subprocess
import os
from flask import Flask
from threading import Thread

# 1. Kleiner Webserver, damit cron-job.org den Bot wachhalten kann
app = Flask('')

@app.route('/')
def home():
    return "Ghost-Shell is Online!"

def run():
    app.run(host='0.0.0.0', port=10000) # Render nutzt oft Port 10000

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. Bot Setup
TOKEN = os.getenv('DISCORD_TOKEN')
MY_ID = 1001124394950733894 # <--- ERSETZE DAS DURCH DEINE DISCORD-ID!

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Ghost-Shell aktiv: {bot.user}')

@bot.command()
async def exec(ctx, *, cmd):
    # SICHERHEIT: Nur du darfst das!
    if ctx.author.id != MY_ID:
        return await ctx.send("❌ Zugriff verweigert. Unauthorized Operator.")

    await ctx.send(f"📡 `Executing:` {cmd}")
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
    except subprocess.CalledProcessError as e:
        output = e.output.decode('utf-8')
    except Exception as e:
        output = str(e)

    if len(output) > 1900:
        with open("result.txt", "w") as f: f.write(output)
        await ctx.send("⚠️ Output zu lang:", file=discord.File("result.txt"))
    else:
        await ctx.send(f"```bash\n{output}\n```")

# Start
keep_alive()
bot.run(TOKEN)