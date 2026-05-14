import discord
from discord.ext import commands
import subprocess
import os
import psutil
import platform
from datetime import datetime
from dotenv import load_dotenv

# 1. Variablen laden
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MY_ID = 1001124394950733894 

# 2. Bot Setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'--- Ghost-Shell aktiv ---')
    print(f'Eingeloggt als: {bot.user}')

@bot.command()
async def exec(ctx, *, cmd):
    if ctx.author.id != MY_ID:
        return await ctx.send("❌ Zugriff verweigert.")
    await ctx.send(f"📡 `Oracle-Shell executing:` {cmd}")
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
    except Exception as e:
        output = str(e)
    
    if len(output) > 1900:
        with open("result.txt", "w") as f: f.write(output)
        await ctx.send("⚠️ Output zu lang:", file=discord.File("result.txt"))
        os.remove("result.txt")
    else:
     await ctx.send(f"```bash\n{output}```")

@bot.command()
async def status(ctx):
    # CPU Last
    cpu_usage = psutil.cpu_percent(interval=1)
    # RAM Info
    ram = psutil.virtual_memory()
    ram_used = round(ram.used / (1024 ** 3), 2)
    ram_total = round(ram.total / (1024 ** 3), 2)
    # Festplatte
    disk = psutil.disk_usage('/')
    disk_free = round(disk.free / (1024 ** 3), 2)

    embed = discord.Embed(title="🖥️ Server Status", color=0x00ff00)
    embed.add_field(name="CPU Last", value=f"{cpu_usage}%", inline=True)
    embed.add_field(name="RAM Nutzung", value=f"{ram_used}GB / {ram_total}GB", inline=True)
    embed.add_field(name="Speicher frei", value=f"{disk_free} GB", inline=True)
    embed.add_field(name="Betriebssystem", value=f"{platform.system()} {platform.release()}", inline=False)
    embed.set_footer(text=f"Abgefragt um {datetime.now().strftime('%H:%M:%S')}")
    await ctx.send(embed=embed)

# 3. START (Muss IMMER ganz unten stehen!)
if TOKEN:
    bot.run(TOKEN)
else:
    print("FEHLER: Kein DISCORD_TOKEN gefunden!")