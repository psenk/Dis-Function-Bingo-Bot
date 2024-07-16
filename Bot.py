import datetime
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


intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="!bingo", intents=intents)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")


# "!bingobutt" command
# For testing purposes, ping pong, bingo tradition
@bot.command()
async def butt(ctx) -> None:
    #await ctx.send("http://tinyurl.com/s8aw585y")
    word = ""
    for i in "bingobutt":
        val = random.randint(0,5)
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
    
    cmd: list= ctx.message.content.split()
    
    # no task number error
    if len(cmd) == 1:
        await ctx.send("No bingo task number detected with post.")
        return
    
    task_id: int = int(cmd[1])
    screenshots: list = ctx.message.attachments
    
    # no screenshots error
    if not screenshots:
        await ctx.send("No screenshots detected with submission.")
        return

    task_id_check: bool = Util.check_task_id(task_id)
    if not task_id_check:
        await ctx.send("Your task ID is out of bounds.")
    """
    # unsure if needed right now, let Discord engine check file types
    screenshots_check: list = Util.check_screenshots(screenshots)
    if not screenshots_check[0]:
        ctx.send(screenshots_check[1])
    """
    # create submission embed
    # get team from roles Utils.get_user_team(user)
    await SubmitTool.create_submit_tool_embed(ctx, task_id, "Team")
    
    # submit btn - save task to awaiting approval list, submission message
    # cancl btn - delete embed, cancellation message


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