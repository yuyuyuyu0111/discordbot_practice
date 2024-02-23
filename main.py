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

# 実行されているOSに合わせて文字コードを選択
# Windowsの場合はshift-jis
# Linuxの場合はutf-8
charset = "shift-jis" if os.name == "nt" else "utf-8"


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await tree.sync()


@tree.command(name="ping_1111", description="pingを実行します。宛先は1.1.1.1です。")
async def test_command(interaction: discord.Interaction, n: int = 4):
    await interaction.response.defer(thinking=True)
    if n > 10:
        n = 10
    try:

        if os.name == "nt":
            result = subprocess.run(["ping", "1.1.1.1", "-n", str(n)],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding=charset)
        else:
            result = subprocess.run(["ping", "1.1.1.1", "-c", str(n)],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding=charset)
        await interaction.followup.send(result.stdout, ephemeral=False)
        return
    except Exception as e:
        await interaction.followup.send(str(e), ephemeral=False)
        return


@tree.command(name="pal_reboot", description="パルワールドの再起動を行います。多用厳禁！")
async def pal_reboot(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    try:
        result = subprocess.run(
            ["sudo", "systemctl", "restart", "palworld-dedicated.service"], encoding=charset)
        
        await interaction.followup.send("再起動コマンドを発行しました\n"+result.stdout, ephemeral=False)

    except Exception as e:
        await interaction.followup.send("パルワールドの再起動時にエラーが発生しました。", ephemeral=False)
        return



@tree.command(name="sudo_test", description="sudoできるかテストします。")
async def sudo_test(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    try:
        result = subprocess.run(["sudo", "whoami"], encoding=charset)

        await interaction.followup.send(result.stdout, ephemeral=False)
    except Exception as e:
        await interaction.followup.send(str(e), ephemeral=False)
        return
# print(os.environ.get('TOKEN'))


client.run(TOKEN)
