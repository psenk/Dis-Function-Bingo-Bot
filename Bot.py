import logging
import os
import random
import uuid
from datetime import datetime

import discord
import discord.ext
import discord.ext.commands
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv(override=True)
import Util
from ApproveTool import ApproveTool
from BonusTool import BonusTool
from ConfirmTool import ConfirmTool
from LogTool import LogTool
from QueryTool import QueryTool
from SubmitTool import SubmitTool
from TeamOptionsTool import TeamOptionsTool
from TeamsTool import TeamsTool

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GOOGLE_SHEETS_KEY = os.getenv("GOOGLE_SHEETS_KEY")
DB_LOCALHOST = os.getenv("MYSQL_LOCALHOST")
DB_USER_NAME = os.getenv("MYSQL_USER_NAME")
DB_PW = os.getenv("MYSQL_PW")
GUILD_TEST = discord.Object(969399636995493899)  # ! SWAP DURING LIVE BINGO

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="!bingo", intents=intents)
handler = logging.FileHandler(filename="logs\\discord.log", encoding="utf-8", mode="w")

# TODO: teams database?  expand!!
# TODO: cox purples as enum?
# ! TODO: reject task message?
# ! TODO: approve/reject logs!!
# ! TODO: delete bonus bot message
# ! TODO: Literal['Yes','No'] on SithBot?
# ! TODO: refresh sheets?

@bot.command()
async def submit(ctx: commands.Context) -> None:
    """
    param: Discord context object
    description: Submits task for approval
    return: None
    """
    print(f"Submit command used by: {ctx.author}")

    cmd = ctx.message.content.split()
    if len(cmd) == 1:
        await ctx.send("No bingo task number detected with post.")
        return

    team: str = Util.get_user_team(ctx.author.roles)
    if team not in Util.BINGO_TEAM_NAMES_LIST:
        await ctx.send("You are not authorized to use this command!")
        return
    if ctx.channel.id != Util.TEST_SUBMISSION_CHANNELS[team]:
        await ctx.send("This is not your teams bingo submission channel!")
        return

    screenshots: list = ctx.message.attachments
    if not screenshots:
        await ctx.send("No screenshots detected with submission.")
        return

    # submit purple for joe award
    if cmd[1] == "bonus":
        # ! TODO: delete all messages made
        print(f"Bonus command used by: {ctx.author}")
        date_format = "%m-%d-%y"
        time_format = "%H:%M"

        bonus_view = BonusTool()
        await ctx.send("Select a purple from the dropdown menu:\n_ _", view=bonus_view)
        await bonus_view.wait()
        purple = bonus_view.purp

        # get the date, time, player info
        date = await Util.prompt_for_date(ctx, bot, date_format)
        time = await Util.prompt_for_time(ctx, bot, time_format)
        player = await Util.prompt_for_player(ctx, bot)

        if date is None or time is None or player is None:
            await ctx.send("Bonus submission canceled.")
            return

        # confirm submission details
        confirm_view = ConfirmTool()
        await ctx.send(f"Player **{player}** obtained a **{purple}** for team **{team}** on **{date}** at **{time}**.  Does this all look correct?\n_ _", view=confirm_view)
        await confirm_view.wait()

        # handle confirmation response
        if confirm_view.confirm.lower() == "no":
            await ctx.send("Bonus submission canceled.")
            return

        uuid_bonus = uuid.uuid1()
        date_bonus = datetime.combine(date, time)
        async with QueryTool() as tool:
            await tool.submit_task(998, player, team, uuid_bonus, ctx.message.jump_url, str(ctx.message.id), purple)
            log_tool = LogTool(ctx, bot.get_channel(Util.TEST_LOGS_CHANNEL_ID), False, team, 998, date_bonus, uuid_bonus)
            await log_tool.create_log_embed()
        await ctx.send("Your bonus submission has been sent to the bingo admin team.")
        return

    task_id: int = int(cmd[1])
    task_id_check: bool = Util.check_task_id(task_id)
    # task no out of bounds error
    if not task_id_check:
        await ctx.send("Your task ID is out of bounds.")
        return
    async with QueryTool() as tool:
        day = await tool.get_day()
    if task_id > day * 9:
        await ctx.send("This task is not available yet!")
        return

    multi: bool = len(screenshots) > 1

    uuid_no = uuid.uuid1()
    # task_id = 999 # ! UNCOMMENT DURING LIVE CODE
    submit_tool = SubmitTool(ctx, bot.get_channel(Util.TEST_LOGS_CHANNEL_ID), task_id, team, multi, uuid_no)
    await submit_tool.create_submit_tool_embed()


@bot.command()
async def helpadmin(ctx: commands.Context) -> None:
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
    help_embed.add_field(name="!bingotask", value="Prints out the provided bingo task.", inline=True)

    await ctx.send(embed=help_embed)


@bot.command()
async def teams(ctx: commands.Context) -> None:
    """
    Prints bingo teams and their info
    param: Discord Context object
    return: None
    """
    print(f"Teams command used by: {ctx.author}")
    if not Util.is_admin(ctx):
        await ctx.send("You are not authorized to use this command!")
        return
    async with QueryTool() as tool:
        teams = await tool.get_teams()
    teams_tool = TeamsTool(teams)
    await ctx.send("Which team would you like to view?\n_ _", view=teams_tool)
    await teams_tool.wait()
    team = teams_tool.team

    async with QueryTool() as tool:
        info = await tool.get_team(team)
        info = info[0]
    await ctx.send(f"_ _\nInformation for **{info['team_name']}:**\n**Captain**: {info['captain']}\n**Role ID**: {info['role_id']}\n**Submission Channel ID**: {info['channel_id']}")
    team_options_tool = TeamOptionsTool(team)
    await ctx.send(f"_ _\nWhat would you like to do with {team}?\n_ _", view=team_options_tool)
    await team_options_tool.wait()
    option = team_options_tool.option
    # 0: upd team name, 1: upd captain, 2: upd r_id, 3: upd ch_id
    match int(option):
        case 0:
            await ctx.send("_ _\nInput the new team name below (limit 100 characters):")
            new_team_name = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
            async with QueryTool() as tool:
                await tool.update_team_info(team, "team_name", info["team_name"], new_team_name.content)
        case 1:
            await ctx.send("_ _\nInput the new captain below:")
            new_captain = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
            async with QueryTool() as tool:
                await tool.update_team_info(team, "captain", info["captain"], new_captain.content)
        case 2:
            await ctx.send("_ _\nInput the new role ID below:")
            new_role_id = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
            async with QueryTool() as tool:
                await tool.update_team_info(team, "role_id", info["role_id"], new_role_id.content)
        case 3:
            await ctx.send("_ _\nInput the new channel ID below:")
            new_channel_id = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
            async with QueryTool() as tool:
                await tool.update_team_info(team, "channel_id", info["channel_id"], new_channel_id.content)
    await ctx.send("Update successful.")


@bot.tree.command(description="Display bingo task information.")
@app_commands.describe(task_id="Bingo Task Number")
@app_commands.checks.has_permissions(manage_guild=True)
@app_commands.guilds(GUILD_TEST)
async def task(interaction: discord.Interaction, task_id: int) -> None:
    """
    Displays bingo task information.
    param interaction: Discord Interaction instance
    param task_id: int - bingo task number
    return: None
    """
    await interaction.response.send_message(f"Task # {task_id}: {Util.TASK_NUMBER_DICT.get(task_id)}")

@bot.tree.command(description="Kill the bot.")
@app_commands.checks.has_permissions(manage_guild=True)
@app_commands.guilds(GUILD_TEST)
async def kill(interaction: discord.Interaction) -> None:
    """
    Closes the bot.
    param interaction: Discord Interaction instance
    return: None
    """
    await interaction.response.send_message("Later nerds.")
    await bot.close()

@bot.tree.command(description="Set day of bingo.")
@app_commands.describe(day="Day of bingo")
@app_commands.checks.has_permissions(manage_guild=True)
@app_commands.guilds(GUILD_TEST)
async def day(interaction: discord.Interaction, day: int) -> None:
    """
    Updates the current day of the bingo.
    param interaction: Discord Interaction instance
    param day: int - day of bingo
    return: None
    """
    async with QueryTool() as tool:
        day = await tool.update_day(day)
        
    await interaction.response.send_message(f"Day of bingo updated to: {day}")

@bot.tree.command(description="Opens tool for reviewing active bingo submissions.")
@app_commands.checks.has_permissions(manage_guild=True)
@app_commands.guilds(GUILD_TEST)
async def approve(interaction: discord.Interaction) -> None:
    """
    Opens tool for reviewing active bingo submissions.
    param interaction: Discord Interaction instance
    return: None
    """
    global bot
    approve_tool = ApproveTool(interaction, bot)
    await approve_tool.create_approve_embed()

@bot.tree.command(description="Bingo butt!")
@app_commands.guilds(GUILD_TEST)
async def butt(interaction: discord.Interaction) -> None:
    """
    Ping pong command as bingo butt.  Sith tradition.
    param interaction: Discord Interaction instance
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
    await interaction.response.send_message(word + "~,.")

@bot.tree.command(description="Ram Ranch really rocks!")
@app_commands.guilds(GUILD_TEST)
async def ranch(interaction: discord.Interaction) -> None:
    """
    Ping pong command as ram ranch image.  Custom command.
    param interaction: Discord Interaction instance
    return: None
    """
    
    await interaction.response.send_message("https://cdn.discordapp.com/attachments/1195577008973946890/1265373919788011540/Screenshot_2024-07-12_115957.jpg?ex=66a53b4b&is=66a3e9cb&hm=662036eb2d866fbf462af74a746926fdb5750e3a2022c8afa0b94b46b48fc0f7&")

@bot.tree.command(description="Displays bot help menu.")
@app_commands.guilds(GUILD_TEST)
async def help(interaction: discord.Interaction) -> None:
    """
    Shows help menu for normal users.
    param: Discord Interaction instance
    return: None
    """
    help_embed = discord.Embed(title="Bingo Bonanza Bot Commands", color=0xFFFF00)
    help_embed.set_thumbnail(url=bot.user.avatar.url)
    help_embed.add_field(name="/help", value="Displays this help menu.", inline=True)
    help_embed.add_field(name="!bingosubmit X", value="Submit bingo task X to bingo admin team.\nUse '!bingosubmit bonus' to submit a purple for the Twisted Joe Award.", inline=True)
    help_embed.add_field(name="", value="", inline=True)
    help_embed.add_field(name="/ranch", value="Ram Ranch really rocks!", inline=True)
    help_embed.add_field(name="/butt", value="Bingo butt!", inline=True)
    help_embed.add_field(name="", value="", inline=True)

    await interaction.response.send_message(embed=help_embed)

@bot.event
async def on_ready() -> None:
    """
    param: None
    description: This code runs every time the bot boots up
    return: None
    """
    await bot.get_channel(Util.TEST_LOGS_CHANNEL_ID).send("Cowabunga nerds!")
    print(f"Bingo Bot online as of {datetime.now()}.")
    await bot.tree.sync(guild=GUILD_TEST)


bot.run(DISCORD_TOKEN, log_handler=handler, log_level=logging.DEBUG)
