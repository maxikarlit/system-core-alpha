import discord
from discord.ext import commands
import subprocess
import os
from dotenv import load_dotenv  # Neu: Zum Laden der .env Datei

# 1. Variablen laden
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MY_ID = 1001124394950733894  # Deine ID ist korrekt eingetragen

# 2. Bot Setup (Flask/keep_alive wurde entfernt, da auf Oracle unnötig)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'--- Ghost-Shell aktiv ---')
    print(f'Eingeloggt als: {bot.user}')
    print(f'Bereit für Befehle auf dem Oracle-Server.')

@bot.command()
async def exec(ctx, *, cmd):
    # SICHERHEIT: Nur du darfst das!
    if ctx.author.id != MY_ID:
        return await ctx.send("❌ Zugriff verweigert. Unauthorized Operator.")

    await ctx.send(f"📡 `Oracle-Shell executing:` {cmd}")
    try:
        # Führt den Befehl im Linux-System aus
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
    except subprocess.CalledProcessError as e:
        output = e.output.decode('utf-8')
    except Exception as e:
        output = str(e)

    # Discord Nachrichtenlimit von 2000 Zeichen beachten
    if not output:
        await ctx.send("✅ Befehl ausgeführt (kein Output).")
    elif len(output) > 1900:
        with open("result.txt", "w") as f: 
            f.write(output)
        await ctx.send("⚠️ Output zu lang, Datei angehängt:", file=discord.File("result.txt"))
        os.remove("result.txt") # Datei danach wieder löschen
    else:
     await ctx.send(f"```bash\n{output}```")

# Start
if TOKEN:
    bot.run(TOKEN)
else:
    print("FEHLER: Kein DISCORD_TOKEN in der .env Datei gefunden!")
import psutil
import platform
from datetime import datetime

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

    # Schickes Embed für Discord
    embed = discord.Embed(title="🖥️ Server Status", color=0x00ff00)
    embed.add_field(name="CPU Last", value=f"{cpu_usage}%", inline=True)
    embed.add_field(name="RAM Nutzung", value=f"{ram_used}GB / {ram_total}GB", inline=True)
    embed.add_field(name="Speicher frei", value=f"{disk_free} GB", inline=True)
    embed.add_field(name="Betriebssystem", value=f"{platform.system()} {platform.release()}", inline=False)
    embed.set_footer(text=f"Abgefragt um {datetime.now().strftime('%H:%M:%S')}")

    await ctx.send(embed=embed)