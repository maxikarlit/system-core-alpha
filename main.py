import discord
from discord.ext import commands
import subprocess
import os

# Hol den Token aus den Umgebungsvariablen (Sicherheit!)
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # Damit du weißt, dass die Node online ist
    print(f'Ghost-Shell aktiv: {bot.user}')
    await bot.change_presence(activity=discord.Game(name="with the Matrix"))

@bot.command()
async def exec(ctx, *, cmd):
    """Führt rohe Shell-Befehle auf dem Render-Server aus"""
    
    # Optional: Deine Discord-ID hier eintragen, damit NUR DU den Bot steuern kannst
    # if str(ctx.author.id) != "DEINE_ID_HIER":
    #    return await ctx.send("Unauthorized access. Identification failed.")

    await ctx.send(f"📡 `Executing:` {cmd}")

    try:
        # Hier passiert die Anonymous-Scheiße: Der Befehl geht direkt ins Linux-System
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
    except subprocess.CalledProcessError as e:
        output = e.output.decode('utf-8')
    except Exception as e:
        output = str(e)

    # Wenn der Output zu lang für Discord ist (max 2000 Zeichen), schick ihn als Datei
    if len(output) > 1900:
        with open("result.txt", "w") as f:
            f.write(output)
        await ctx.send("⚠️ Output exceeds limit. Sending as file:", file=discord.File("result.txt"))
        os.remove("result.txt")
    else:
        # Schicker Code-Block im Hacker-Style
        await ctx.send(f"```bash\n{output}\n```")

bot.run(TOKEN)