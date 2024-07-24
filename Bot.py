import datetime
import logging
import os
import random
import uuid

import discord
import discord.ext
from discord.ext import commands
import discord.ext.commands
from dotenv import load_dotenv

from SheetsTool import SheetsTool

load_dotenv(override=True)
from ConfirmTool import ConfirmTool
import Util
from ApproveTool import ApproveTool
from BonusTool import BonusTool
from QueryTool import QueryTool
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
    if len(cmd) == 1:
        await ctx.send("No bingo task number detected with post.")
        return

    if cmd[1] == "bonus":
        team: str = Util.get_user_team(ctx.author.roles)
        bonus_view = BonusTool()
        await ctx.send("Select a purple from the dropdown menu:", view=bonus_view)
        await bonus_view.wait()
        purple = bonus_view.purp
        
        await ctx.send("Please enter the date listed on the Clan Events plugin in the screenshot below.\nUse the following format: MM-DD-YY\nExample: **08-16-91**")
        date = await bot.wait_for("message")
        
        await ctx.send("Please enter the time listed on the Clan Events plugin in the screenshot below.\nUse the following format: HH:MM:SS PM\nExample: **10:52:01 AM**")        
        time = await bot.wait_for("message")
        
        await ctx.send("Please enter the name of the player that obtained the drop below.")
        player = await bot.wait_for("message")
        
        confirm_view = ConfirmTool()
        await ctx.send(f"Player **{player.content.strip()}** obtained a **{purple}** for team **{team}** on **{date.content.strip()}** at **{time.content.strip()}**.  Does this all look correct?", view=confirm_view)
        await confirm_view.wait()
        
        if confirm_view.confirm == "No":
            await ctx.send("Bonus submission cancelled.")
            return
        else:
            await ctx.send("Your bonus submission has been sent to the bingo admin team.")
            SheetsTool.add_purple(purple, team, date.content, time.content, player.content)
            return

    task_id: int = int(cmd[1])
    task_id_check: bool = Util.check_task_id(task_id)
    # task no out of bounds error
    if not task_id_check:
        await ctx.send("Your task ID is out of bounds.")
        return
    day = await QueryTool.get_day()
    if task_id > day * 9:
        await ctx.send("This task is not available yet!")
        return
    screenshots: list = ctx.message.attachments
    # no screenshots error
    if not screenshots:
        await ctx.send("No screenshots detected with submission.")
        return

    multi: bool = len(screenshots) > 1

    team: str = Util.get_user_team(ctx.author.roles)

    uuid_no = uuid.uuid1()
    # task_id = 999 # ! UNCOMMENT DURING LIVE CODE
    submit_tool = SubmitTool(ctx, bot.get_channel(LOGS_CHANNEL), task_id, team, multi, uuid_no)
    await submit_tool.create_submit_tool_embed()


@bot.command()
async def approve(ctx: discord.ext.commands.Context) -> None:
    """
    param: Discord context object
    description: Prints list of tasks that require submission
    return: None
    """
    approve_tool = ApproveTool(ctx, bot)
    await approve_tool.create_approve_embed()


@bot.command()
async def ranch(ctx: discord.ext.commands.Context) -> None:
    """
    param: Discord Context object
    description: Sends Ram Ranch team photo
    return: None
    """
    await ctx.send("https://tinyurl.com/3ab8ptjt")


@bot.command()
async def day(ctx: discord.ext.commands.Context) -> None:
    """
    param: Discord Context object
    description: updates day of bingo
    return: None
    """
    cmd: list = ctx.message.content.split()
    if len(cmd) == 1:
        await ctx.send("No bingo task number detected with post.")
        return
    day = cmd[1]
    await QueryTool.update_day(day)
    await QueryTool.get_day()
    await ctx.send(f"Day of bingo updated to: {day}")


@bot.command()
async def helpme(ctx: discord.ext.commands.Context) -> None:
    """
    param: Discord Context object
    description: Shows list of commands available to normal users
    return: None
    """
    help_embed = discord.Embed(title="Bingo Bonanza Bot Commands", color=0x0000FF)
    help_embed.add_field(name="!bingohelpme", value="Shows a list of bot commands.", inline=True)
    help_embed.add_field(name="!bingosubmit X", value="Submit bingo task X to bingo admin team.", inline=True)
    help_embed.add_field(name="", value="", inline=True)
    help_embed.add_field(name="!bingoranch", value="Ram Ranch Really Rocks!", inline=True)
    help_embed.add_field(name="!bingobutt", value="Bingo butt!", inline=True)
    help_embed.add_field(name="", value="", inline=True)

    await ctx.send(embed=help_embed)


@bot.command()
async def helpadmin(ctx: discord.ext.commands.Context) -> None:
    """
    param: Discord Context object
    description: Shows list of commands available to admin users
    return: None
    """
    if not Util.is_admin(ctx):
        await ctx.send("You are not authorized to use this command!")
        return
    help_embed = discord.Embed(title="Bingo Bonanza Bot Commands", color=0x0000FF)
    help_embed.add_field(name="!bingoapprove", value="Shows interactive window for approving bingo submissions.", inline=True)
    help_embed.add_field(name="!bingoday X", value="Sets the day of the bingo to X.", inline=True)
    help_embed.add_field(name="", value="", inline=True)

    await ctx.send(embed=help_embed)


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
