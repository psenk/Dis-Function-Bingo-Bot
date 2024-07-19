import datetime
import uuid
import discord
from discord.ext import commands
import random
import logging
import os
from dotenv import load_dotenv

load_dotenv(override=True)

# custom classes
import Util
import SubmitTool


DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GOOGLE_SHEETS_KEY = os.getenv("GOOGLE_SHEETS_KEY")
DB_LOCALHOST = os.getenv("MYSQL_LOCALHOST")
DB_USER_NAME = os.getenv("MYSQL_USER_NAME")
DB_PW = os.getenv("MYSQL_PW")

LOGS_CHANNEL = 1194488938480537740 # ! SWAP DURING LIVE BINGO

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="!bingo", intents=intents)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")


# "!bingobutt" command
# For testing purposes, ping pong, bingo tradition
@bot.command()
async def butt(ctx) -> None:
    # await ctx.send("http://tinyurl.com/s8aw585y")
    word = ""
    for i in "bingobutt":
        val = random.randint(0, 5)
        if val == 3:
            word += "..zzt.."
        elif val == 2:
            word += "*"
        else:
            word += i
    await ctx.send(word + "~,.")


# "!bingosubmit" command
# For submitting a bingo task to the admin team
@bot.command()
async def submit(ctx) -> None:

    cmd: list = ctx.message.content.split()

    # no task number error
    if len(cmd) == 1:
        await ctx.send("No bingo task number detected with post.")
        return
    task_id: int = int(cmd[1])
    task_id_check: bool = Util.check_task_id(task_id)
    # task no out of bounds error
    if not task_id_check:
        await ctx.send("Your task ID is out of bounds.")
        return
    
    screenshots: list = ctx.message.attachments
    # no screenshots error
    if not screenshots:
        await ctx.send("No screenshots detected with submission.")
        return
    multi: bool = len(screenshots) > 1

    team: str = Util.get_user_team(ctx.author.roles)

    # create submission embed
    uuid_no = uuid.uuid1()
    await SubmitTool.create_submit_tool_embed(ctx, bot.get_channel(LOGS_CHANNEL), task_id, team, multi, uuid_no)

""" # FOR TESTING ONLY
# Test "!bingosubmit" command
@bot.command()
async def test(ctx) -> None:
    await ctx.send("!bingosubmit")#, file = discord.File("thisisfine.jpg"))
 """

# "!bingoapprove" command
# Shows list of bingo tasks awaiting approval
# Allows task approval/rejection
@bot.command()
async def approve(ctx) -> None:
    pass



# Ran every time bot boots up
@bot.event
async def on_ready():
    # LOG
    print(f"Bingo Bot online as of {datetime.datetime.now()}.")


bot.run(DISCORD_TOKEN, log_handler=handler, log_level=logging.DEBUG)
