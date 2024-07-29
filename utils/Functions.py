from datetime import datetime
import logging

import discord
import discord.ext
import discord.ext.commands

from utils import Constants

@staticmethod
def check_task_id(task_no: int) -> bool:
    """
    Validates task ID.
    param task_no: int - bingo task number
    return: bool - is valid task number?
    """
    if task_no <= 0:
        print("ERROR: Task submission failed, task id out of bounds. (less than zero)")
        return False
    elif task_no > len(Constants.TASK_DESCRIPTION_MAP):
        print("ERROR: Task submission failed, task id out of bounds. (number too high)")
        return False
    else:
        return True

@staticmethod
def get_user_team(roles: list) -> str:
    """
    Gets users bingo team.
    param roles: list - list of users roles
    return: str - bingo team name
    """
    for team_id in Constants.BINGO_TEAM_IDS_LIST:
        for role in roles:
            if team_id == role.id:
                return role.name
    return None

@staticmethod
def is_admin(member: discord.Member) -> bool:
    """
    Checks if member has admin role.
    param member: Discord Member instance
    return: bool - is member an admin?
    """
    roles = []
    for role in member.roles:
        roles.append(role.id)
    if Constants.BINGO_ADMIN_ROLE_ID not in roles:
        return False
    return True

@staticmethod
async def validate_data(interaction: discord.Interaction, date: str, time: str) -> bool:
    """
    Validates format of input date or time.
    param interaction: Discord Interaction instance
    param date: str - date input
    param time: str - time input
    return: bool - is format good?
    """
    try:
        if date:
            datetime.strptime(date, Constants.DATE_FORMAT)
        if time:
            datetime.strptime(time, Constants.TIME_FORMAT)
    except ValueError as e:
        if date and "does not match format" in str(e):
            await interaction.channel.send("Invalid **date** format. Use format: MM-DD-YY")
        if time and "does not match format" in str(e):
            await interaction.channel.send("Invalid **time** format. Use format: HH:MM")
        return False
    return True

def create_logger(filename: str) -> logging.Logger:
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        handler = logging.FileHandler(filename=f"logs/{filename}.log", encoding="utf-8", mode="w")
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger