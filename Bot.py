import asyncio
from datetime import datetime
import logging
import os
import random
import uuid

import discord
import discord.ext
from discord.ext import commands
import discord.ext.commands
from dotenv import load_dotenv

from LogTool import LogTool
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
    print(f"Butt command used by: {ctx.author}")
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
async def ranch(ctx: discord.ext.commands.Context) -> None:
    """
    param: Discord Context object
    description: Sends Ram Ranch team photo
    return: None
    """
    print(f"Ranch command used by: {ctx.author}")
    await ctx.send("https://cdn.discordapp.com/attachments/1195577008973946890/1265373919788011540/Screenshot_2024-07-12_115957.jpg?ex=66a53b4b&is=66a3e9cb&hm=662036eb2d866fbf462af74a746926fdb5750e3a2022c8afa0b94b46b48fc0f7&")


@bot.command()
async def submit(ctx: discord.ext.commands.Context) -> None:
    """
    param: Discord context object
    description: Submits task for approval
    return: None
    """
    print(f"Submit command used by: {ctx.author}")
    # ! TODO: command can only be run in users team channel

    cmd = ctx.message.content.split()
    if len(cmd) == 1:
        await ctx.send("No bingo task number detected with post.")
        return

    team: str = Util.get_user_team(ctx.author.roles)
    if team not in Util.BINGO_TEAMS_STRS:
        await ctx.send("You are not authorized to use this command!")
        return
    
    screenshots: list = ctx.message.attachments
    if not screenshots:
        await ctx.send("No screenshots detected with submission.")
        return
    
    query_tool = QueryTool()
    # submit purple for joe award
    if cmd[1] == "bonus":
        
        # ! TODO: delete all messages made
        print(f"Bonus command used by: {ctx.author}")
        date_format = "%m-%d-%y"
        time_format = "%H:%M"

        bonus_view = BonusTool()
        await ctx.send("Select a purple from the dropdown menu:\n", view=bonus_view)
        await bonus_view.wait()
        purple = bonus_view.purp
        
        # get the date, time, player info
        date_task = asyncio.create_task(Util.prompt_for_date(ctx, bot, date_format))
        time_task = asyncio.create_task(Util.prompt_for_time(ctx, bot, time_format))
        player_task = asyncio.create_task(Util.prompt_for_player(ctx, bot))
        
        date, time, player = await asyncio.gather(date_task, time_task, player_task)
        if date is None or time is None or player is None:
            await ctx.send("Bonus submission canceled.")
            return
        
        

        # confirm submission details
        confirm_view = ConfirmTool()
        await ctx.send(f"Player **{player}** obtained a **{purple}** for team **{team}** on **{date}** at **{time}**.  Does this all look correct?\n", view=confirm_view)
        await confirm_view.wait()

        # handle confirmation response
        if confirm_view.confirm.lower() == "no":
            await ctx.send("Bonus submission canceled.")
            return

        uuid_bonus = uuid.uuid1()
        date_bonus = datetime.combine(date, time)
        await query_tool.submit_task(998, player, team, uuid_bonus, ctx.message.jump_url, ctx.message.id, purple)
        log_tool = LogTool(ctx, bot.get_channel(LOGS_CHANNEL), False, team, 998, date_bonus, uuid_bonus)
        await log_tool.create_log_embed()
        await ctx.send("Your bonus submission has been sent to the bingo admin team.")
        return

    task_id: int = int(cmd[1])
    task_id_check: bool = Util.check_task_id(task_id)
    # task no out of bounds error
    if not task_id_check:
        await ctx.send("Your task ID is out of bounds.")
        return
    day = await query_tool.get_day()
    if task_id > day * 9:
        await ctx.send("This task is not available yet!")
        return

    multi: bool = len(screenshots) > 1

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
    print(f"Approve command used by: {ctx.author}")
    approve_tool = await ApproveTool.create(ctx, bot)
    await approve_tool.create_approve_embed()


@bot.command()
async def day(ctx: discord.ext.commands.Context) -> None:
    """
    param: Discord Context object
    description: updates day of bingo
    return: None
    """
    query_tool = QueryTool()
    print(f"Day command used by: {ctx.author}")
    cmd: list = ctx.message.content.split()
    if len(cmd) == 1:
        await ctx.send("No bingo task number detected with post.")
        return
    day = cmd[1]
    day = await query_tool.update_day(day)
    await ctx.send(f"Day of bingo updated to: {day}")


@bot.command()
async def helpme(ctx: discord.ext.commands.Context) -> None:
    """
    param: Discord Context object
    description: Shows list of commands available to normal users
    return: None
    """
    print(f"HelpMe command used by: {ctx.author}")
    help_embed = discord.Embed(title="Bingo Bonanza Bot Commands", color=0x0000FF)
    help_embed.add_field(name="!bingohelpme", value="Shows a list of bot commands.", inline=True)
    help_embed.add_field(name="!bingosubmit X", value="Submit bingo task X to bingo admin team.\nUse '!bingosubmit bonus' to submit a purple for the Twisted Joe Award.", inline=True)
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
    print(f"HelpAdmin command used by: {ctx.author}")
    if not Util.is_admin(ctx):
        await ctx.send("You are not authorized to use this command!")
        return
    help_embed = discord.Embed(title="Bingo Bonanza Bot Commands", color=0x0000FF)
    help_embed.add_field(name="!bingoapprove", value="Shows interactive window for approving bingo submissions.", inline=True)
    help_embed.add_field(name="!bingoday X", value="Sets the day of the bingo to X.", inline=True)
    help_embed.add_field(name="", value="", inline=True)

    await ctx.send(embed=help_embed)


@bot.command()
async def task(ctx: discord.ext.commands.Context, task_id: int) -> None:
    """
    param: Discord Context object
    param int: bingo task number
    description: prints bingo task
    return: None
    """
    print(f"Task command used by: {ctx.author}")
    task_id = ctx.message.content.split()[1].strip()
    if not Util.is_admin(ctx):
        await ctx.send("You are not authorized to use this command!")
        return
    await ctx.send(f"Task # {task_id}: {Util.TASK_NUMBER_DICT.get(task_id)}")


@bot.command()
@commands.is_owner()
async def kill(ctx: discord.ext.commands.Context) -> None:
    """
    param: Discord context object
    description: Closes the bot
    return: None
    """
    await ctx.send("Later nerds.")
    await bot.close()


@bot.event
async def on_ready() -> None:
    """
    param: None
    description: This code runs every time the bot boots up
    return: None
    """
    await bot.get_channel(LOGS_CHANNEL).send("Cowabunga nerds!")
    print(f"Bingo Bot online as of {datetime.now()}.")


bot.run(DISCORD_TOKEN, log_handler=handler, log_level=logging.DEBUG)
