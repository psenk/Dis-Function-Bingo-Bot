import datetime
import uuid
import discord
from discord.ext import commands
import random
import logging
import os
import discord.ext.commands
from dotenv import load_dotenv
import discord.ext

load_dotenv(override=True)
import Util
from ApproveTool import ApproveTool
from SubmitTool import SubmitTool


DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GOOGLE_SHEETS_KEY = os.getenv("GOOGLE_SHEETS_KEY")
DB_LOCALHOST = os.getenv("MYSQL_LOCALHOST")
DB_USER_NAME = os.getenv("MYSQL_USER_NAME")
DB_PW = os.getenv("MYSQL_PW")
LOGS_CHANNEL = 1194488938480537740  # ! SWAP DURING LIVE BINGO

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="!bingo", intents=intents)
handler = logging.FileHandler(filename="logs\\discord.log", encoding="utf-8", mode="w")


@bot.command()
async def butt(ctx: discord.ext.commands.Context) -> None:
    """
    param: Discord context object
    description: Fun ping server command
    return: None
    """
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


@bot.command()
async def submit(ctx: discord.ext.commands.Context) -> None:
    """
    param: Discord context object
    description: Submits task for approval
    return: None
    """
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


@bot.command()
async def approve(ctx: discord.ext.commands.Context) -> None:
    """
    param: Discord context object
    description: Prints list of tasks that require submission
    return: None
    """
    approve_tool = ApproveTool(ctx)
    await approve_tool.create_approve_embed()


@bot.event
async def on_ready() -> None:
    """
    param: None
    description: This code runs every time the bot boots up
    return: None
    """
    # LOG
    print(f"Bingo Bot online as of {datetime.datetime.now()}.")


bot.run(DISCORD_TOKEN, log_handler=handler, log_level=logging.DEBUG)
