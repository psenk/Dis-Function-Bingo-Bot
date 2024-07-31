import logging
import os
import random
import uuid
from datetime import datetime
from typing import List

import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(override=True)

from Game import Game
from tools.ApproveTool import ApproveTool
from tools.LogTool import LogTool
from tools.QueryTool import QueryTool
from tools.SubmitTool import SubmitTool
from tools.YesNoTool import YesNoTool
from unused.test.TeamOptionsTool import TeamOptionsTool
from unused.test.TeamsTool import TeamsTool
from utils import Choices, Constants, Functions

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

bot_logger = logging.getLogger(__name__)
bot_logger.addHandler(logging.FileHandler(filename="logs/bot.log", encoding="utf-8", mode="w"))
bot_logger.setLevel(logging.DEBUG)

# TODO: teams database?  expand!!
# ! TODO: reject task message?
# ! TODO: approve/reject logs!!
# ! TODO: improve embed designs?

# * # * # ADMIN COMMANDS # * # * #


@bot.tree.command(description="Displays bot help menu for bingo admins.")
@app_commands.checks.has_role(Constants.BINGO_ADMIN_ROLE_ID)
@app_commands.guilds(Constants.GUILD)
async def helpadmin(interaction: discord.Interaction) -> None:
    """
    Shows list of commands available to bingo admins.
    param interaction: Discord Interaction instance
    return: None
    """
    help_embed = discord.Embed(title="Foki Bot Admin Commands", color=0xFFFF00)
    help_embed.set_thumbnail(url=bot.user.avatar.url)
    help_embed.add_field(name="/approve", value="Opens tool for reviewing active bingo submissions.\nOnly usable in the bingo admin channel.", inline=True)
    help_embed.add_field(name="/day X", value="Set day of bingo to X.", inline=True)
    help_embed.add_field(name="", value="", inline=True)
    help_embed.add_field(name="/task", value="Display bingo task information.", inline=True)
    await interaction.response.send_message(embed=help_embed)
    bot_logger.info(f"/helpadmin used by -> {interaction.user.display_name}")


# ? # ? # ? # ? #


@bot.tree.command(description="Display bingo task information.")
@app_commands.describe(task_id="Bingo Task Number")
@app_commands.checks.has_role(Constants.BINGO_ADMIN_ROLE_ID)
@app_commands.guilds(Constants.GUILD)
async def task(interaction: discord.Interaction, task_id: int) -> None:
    """
    Displays bingo task information.
    param interaction: Discord Interaction instance
    param task_id: int - bingo task number
    return: None
    """
    await interaction.response.send_message(f"Task # {task_id}: {Constants.TASK_DESCRIPTION_MAP.get(task_id)}", ephemeral=True)
    bot_logger.info(f"/task used by -> {interaction.user.display_name}")


# ? # ? # ? # ? #


@bot.tree.command(description="Kill the bot.")
@app_commands.guilds(Constants.GUILD)
@commands.is_owner()
async def kill(interaction: discord.Interaction) -> None:
    """
    Closes the bot.
    param interaction: Discord Interaction instance
    return: None
    """
    await interaction.response.send_message("Later nerds.")
    bot_logger.info(f"/kill used by -> {interaction.user.display_name}")
    await bot.close()


# ? # ? # ? # ? #


@bot.tree.command(description="Set day of bingo.")
@app_commands.describe(day="Day of bingo")
@app_commands.checks.has_role(Constants.BINGO_ADMIN_ROLE_ID)
@app_commands.guilds(Constants.GUILD)
async def day(interaction: discord.Interaction, day: int) -> None:
    """
    Updates the current day of the bingo.
    param interaction: Discord Interaction instance
    param day: int - day of bingo
    return: None
    """
    await interaction.response.defer()
    async with QueryTool() as tool:
        day = await tool.update_day(day)
    await interaction.followup.send(f"Day of bingo updated to: {day}")
    bot_logger.info(f"/day used by -> {interaction.user.display_name}")


# ? # ? # ? # ? #


@bot.tree.command(description="Opens tool for reviewing active bingo submissions.")
@app_commands.checks.has_role(Constants.BINGO_ADMIN_ROLE_ID)
@app_commands.guilds(Constants.GUILD)
async def approve(interaction: discord.Interaction) -> None:
    """
    Opens tool for reviewing active bingo submissions.
    param interaction: Discord Interaction instance
    return: None
    """
    # is this admin channel?
    if interaction.channel_id != Constants.TEST_ADMIN_CHANNEL_ID:
        await interaction.response.send_message("This command can only be used in the admin channel.", ephemeral=True)
        return
    await interaction.response.defer()
    approve_tool = ApproveTool(interaction, bot)
    await approve_tool.create_approve_embed()
    bot_logger.info(f"/approve used by -> {interaction.user.display_name}")


# * # * # USER COMMANDS # * # * #


@bot.tree.command(description="Displays bot help menu.")
@app_commands.guilds(Constants.GUILD)
async def help(interaction: discord.Interaction) -> None:
    """
    Shows help menu for normal users.
    param interaction: Discord Interaction instance
    return: None
    """
    help_embed = discord.Embed(title="Foki Bot Bingo Commands", color=0xFFFF00)
    help_embed.set_thumbnail(url=bot.user.avatar.url)
    help_embed.add_field(name="/help", value="Displays this help menu.", inline=True)
    help_embed.add_field(name="!bingosubmit X", value="Submit bingo task X to bingo admin team.", inline=True)
    help_embed.add_field(name="", value="", inline=True)
    help_embed.add_field(name="/bonus", value="Submit a bonus task for the Twisted Joe award.", inline=True)
    help_embed.add_field(name="/butt", value="Bingo butt!", inline=True)
    help_embed.add_field(name="", value="", inline=True)
    help_embed.add_field(name="/ranch", value="Ram Ranch really rocks!", inline=True)

    await interaction.response.send_message(embed=help_embed)
    bot_logger.info(f"/help used by -> {interaction.user.display_name}")


# ? # ? # ? # ? #


@bot.tree.command(description="Bingo butt!")
@app_commands.guilds(Constants.GUILD)
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
    bot_logger.info(f"/butt used by -> {interaction.user.display_name}")


# ? # ? # ? # ? #


@bot.tree.command(description="Ram Ranch really rocks!")
@app_commands.guilds(Constants.GUILD)
async def ranch(interaction: discord.Interaction) -> None:
    """
    Ping pong command as ram ranch image.  Custom command.
    param interaction: Discord Interaction instance
    return: None
    """
    await interaction.response.send_message("https://cdn.discordapp.com/attachments/1195577008973946890/1265373919788011540/Screenshot_2024-07-12_115957.jpg?ex=66a53b4b&is=66a3e9cb&hm=662036eb2d866fbf462af74a746926fdb5750e3a2022c8afa0b94b46b48fc0f7&")
    bot_logger.info(f"/ranch used by -> {interaction.user.display_name}")


# ? # ? # ? # ? #


@bot.tree.command(description="Submit a bingo task for approval.")
@app_commands.describe(day="What board is the task on?", task="Which task are you trying to complete?")
@app_commands.guilds(Constants.GUILD)
async def submit(interaction: discord.Interaction, day: int, task: int) -> None:
    """
    Submits bingo task to bingo team for approval.
    param interaction: Discord Interaction instance
    param day: int - Choice, bingo day
    param task: int - Choice, bingo task
    return: None
    """
    await interaction.response.defer()
    task_id = (day * 9) + (task - 9)
    bot_logger.info(f"/submit task_id -> {task_id}")

    await interaction.channel.send(f"Selected Task: {Constants.TASK_DESCRIPTION_MAP.get(task_id)}")
    bot_logger.info(f"/submit task -> {Constants.TASK_DESCRIPTION_MAP.get(task_id)}")
    team = Functions.get_user_team(interaction.user.roles)
    bot_logger.info(f"/submit team -> {team}")

    # is user in bingo?
    if not team:
        await interaction.followup.send("You are not authorized to use this command!", ephemeral=True)
        bot_logger.info("/submit failed -> user not in bingo")
        return

    # is this users submission channel?
    if interaction.channel_id != Constants.TEST_SUBMISSION_CHANNELS.get(team):
        await interaction.followup.send("This is not your teams submission channel!", ephemeral=True)
        bot_logger.info("/submit failed -> submission not in correct channel")
        return

    # get screenshots
    await interaction.channel.send("https://cdn.discordapp.com/attachments/1195577008973946890/1267326377259172010/submit.png?ex=66a8612a&is=66a70faa&hm=62156fc5695b715eeb1c46388aa96763d99fe96f82c4df146e6ff2125dd4c24e&", delete_after=20.0)
    message = await bot.wait_for("message", check=lambda m: m.author == interaction.user and m.channel == interaction.channel, timeout=60.0)
    bot_logger.info(f"/submit attachments message -> {message}")

    # are there screenshots?
    if not message.attachments:
        await interaction.followup.send("No attachments found. Please attach submission screenshots.", ephemeral=True)
        bot_logger.info(f"/submit failed -> no attachments sent")
        return

    # ok cool
    uuid_no = uuid.uuid1()
    bot_logger.info(f"/submit uuid -> {uuid_no}")
    # task_id = 999 # ! UNCOMMENT DURING LIVE CODE
    logs_channel = bot.get_channel(Constants.TEST_ADMIN_CHANNEL_ID)
    ctx = await bot.get_context(message)
    submit_tool = SubmitTool(ctx, message, logs_channel, team, uuid_no, task_id=task_id)
    await submit_tool.create_submit_tool_embed()
    bot_logger.info(f"/submit command used by -> {interaction.user.display_name}")


@submit.autocomplete("day")
async def auto_complete_day(interaction: discord.Interaction, current: str) -> List[Choice]:
    async with QueryTool() as tool:
        day = await tool.get_day()
    bot_logger.info(f"\nDay from database -> {day}")
    choices = [choice for choice in Choices.DAY_AND_BOARD if choice.value <= day]
    bot_logger.info(f"Auto-complete days options -> {choices}")
    return choices


@submit.autocomplete("task")
async def auto_complete_task(interaction: discord.Interaction, current: str) -> List[Choice]:
    opts = interaction.data.get("options")
    bot_logger.info(f"Task options -> {opts}")
    bot_logger.info(f"Interaction data -> {interaction.data}")

    if opts:
        day_option = opts[0]
        bot_logger.info(f"Day option -> {day_option}")
        if day_option:
            day = day_option.get("value")
            bot_logger.info(f"Day -> {day}, Day data type -> {type(day)}")
            if day in Choices.DAY_TASKS:
                choices = [task for task in Choices.DAY_TASKS[day]]
                bot_logger.info(f"Task choices -> {choices}")
                return choices
    return []


# ? # ? # ? # ? #


@bot.tree.command(description="Submit a bonus task for the Twisted Joe award.")
@app_commands.describe(purple="Which item was obtained?", date="Date from clan event plugin, format MM-DD-YY", time="Time from clan event plugin, format HH:MM (24-hr UTC)", player="Which player got the item?")
@app_commands.choices(purple=Choices.COX_PURPLES)
@app_commands.guilds(Constants.GUILD)
async def bonus(interaction: discord.Interaction, purple: Choice[int], date: str, time: str, player: discord.Member) -> None:
    """
    Submits a bonus task to bingo admins for approval.
    param interaction: Discord Interaction instance
    param purple: str - name of bonus item
    param date: str - date of submission
    param time: str - time of submission
    param player: Discord Member instance
    param submission: submission screenshot
    return: None
    """
    await interaction.response.defer()

    # is user in bingo?
    if not Functions.get_user_team(interaction.user.roles):
        await interaction.followup.send("You are not authorized to use this command!", ephemeral=True)
        return

    # is player in bingo?
    if not Functions.get_user_team(player.roles):
        await interaction.followup.send("Invalid player, they are either not in the bingo or are missing a team role.\n", ephemeral=True)
        return

    team = Functions.get_user_team(player.roles)

    # is this users submission channel?
    if interaction.channel_id != Constants.TEST_SUBMISSION_CHANNELS.get(team):
        await interaction.followup.send("This is not your teams submission channel!", ephemeral=True)
        return

    # validate date/time format
    if not await Functions.validate_data(interaction, date=date, time=time):
        await interaction.followup.send("Date/Time error!", ephemeral=True)
        return

    # get screenshots
    await interaction.channel.send("https://cdn.discordapp.com/attachments/1195577008973946890/1267326377259172010/submit.png?ex=66a8612a&is=66a70faa&hm=62156fc5695b715eeb1c46388aa96763d99fe96f82c4df146e6ff2125dd4c24e&", delete_after=20.0)
    try:
        message = await bot.wait_for("message", check=lambda m: m.author == interaction.user and m.channel == interaction.channel, timeout=30.0)
    except Exception as e:
        bot_logger.error(f'Error obtaining screenshots -> {e}')
        return

    # are there screenshots?
    if not message.attachments:
        await interaction.followup.send("No attachments found.  Please attach submission screenshots.", ephemeral=True)
        bot_logger.info(f"/bonus failed -> no attachments sent")
        return

    # ok cool

    uuid_no = uuid.uuid1()
    date = datetime.strptime(date, Constants.DATE_FORMAT).date()
    time = datetime.strptime(time, Constants.TIME_FORMAT).time()
    date_bonus = datetime.combine(date, time)
    logs_channel = bot.get_channel(Constants.TEST_ADMIN_CHANNEL_ID)
    ctx = await bot.get_context(message)
    # name, item, time
    submission = [player.display_name, purple.name, date_bonus]
    submit_tool = SubmitTool(ctx, message, logs_channel, team, uuid_no, bonus=submission)
    await submit_tool.create_submit_tool_embed()

    await interaction.followup.send("Your bonus submission has been sent to the bingo admin team.", ephemeral=True)
    bot_logger.info(f"/bonus used by -> {interaction.user.display_name}")


# ? # ? # ? # ? #


@bot.event
async def on_ready() -> None:
    """
    This code runs every time the bot boots up,
    return: None
    """

    await bot.get_channel(Constants.TEST_ADMIN_CHANNEL_ID).send("Foki Bot online!")
    print("Bingo Bot online.")
    bot_logger.info("Foki Bot online.")
    try:
        await bot.tree.sync(guild=Constants.GUILD)
        bot_logger.info("Command tree synced.")
    except Exception as e:
        bot_logger.error(f"Error syncing command tree -> {e}")


bot.run(DISCORD_TOKEN, log_handler=logging.FileHandler(filename="logs/discord.log", encoding="utf-8", mode="w"), log_level=logging.DEBUG)

# ? # ? # TEST CODE # ? # ? #


@bot.command()
async def teams(ctx: commands.Context) -> None:
    """
    Prints bingo teams and their info
    param: Discord Context object
    return: None
    """
    print(f"Teams command used by -> {ctx.author}")
    if not Functions.is_admin(ctx):
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
    team_options_tool = TeamOptionsTool.TeamOptionsTool(team)
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


# ? # ? # ? # ? #


@bot.tree.command(description="TEST")
@app_commands.guilds(Constants.GUILD)
async def test_game(interaction: discord.Interaction) -> None:
    await interaction.response.defer()

    p = Game.Player(x=7, y=10)
    game = Game(interaction, p)
    game.set_map(Game.game_map)
    await game.start()
