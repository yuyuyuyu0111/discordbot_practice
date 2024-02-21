import discord
import os
from dotenv import load_dotenv
import subprocess
from discord import app_commands

load_dotenv()
TOKEN = os.environ.get('TOKEN')


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

#実行されているOSに合わせて文字コードを選択
#Windowsの場合はshift-jis
#Linuxの場合はutf-8
charset = "shift-jis" if os.name == "nt" else "utf-8"


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await tree.sync()


@tree.command(name="ping_1111", description="pingを実行します。宛先は1.1.1.1です。")
async def test_command(interaction: discord.Interaction , n: int = 4):
    await interaction.response.defer(thinking=True)
    if n>10:
        n=10
        
    result = subprocess.run(["ping", "1.1.1.1", "-n", str(n)],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding=charset)
    if result.returncode == 0:
        await interaction.followup.send(result.stdout, ephemeral=False)
    else:
        await interaction.followup.send(result.stderr, ephemeral=False)

@tree.command(name="pal_reboot" , description="パルワールドの再起動を行います。多用厳禁！")
async def pal_reboot(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    result = subprocess.run(["sudo", "systemctl", "restart", "palworld-dedicated.service"],encoding=charset)
    if result.returncode == 0:
        await interaction.followup.send(result.stdout, ephemeral=False)
    else:
        await interaction.followup.send(result.stderr, ephemeral=False)
# print(os.environ.get('TOKEN'))



client.run(TOKEN)
