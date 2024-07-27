from datetime import datetime
from enum import Enum

import discord
import discord.ext
import discord.ext.commands

import Util

BINGO_ADMIN_ROLE_ID = 1265728711731183759  # ! REPLACE WHEN MOVING TO SITH SERVER
BINGO_TEAM_IDS_LIST = [1262935908777332757]  # ! REPLACE WHEN MOVED TO SITH SERVER, TEAM ROLES HAVE BEEN CREATED
BINGO_TEAM_NAMES_LIST = ["Sasa Loves Bingo", "Godopka Team Name Pending", "Starship Enterprise", "Cheese Cape", "Drunk Chinchompa"]  # ! REPLACE WHEN HAVE ACTUAL TEAM NAME
BINGO_TEAM_SUBMISSION_CHANNEL_IDS_LIST = []

TEST_ADMIN_CHANNEL_ID = 1194488938480537740  # ! SWAP DURING LIVE BINGO
TEST_GUILD_ID = 969399636995493899
TEST_SUBMISSION_CHANNELS = {
    "Godopka Team Name Pending": 1266581710657814599,
    "Starship Enterprise": 1266581710657814599,
    "Cheese Cape": 1266581710657814599,
    "Sasa Loves Bingo": 1266581710657814599,
    "Drunk Chinchompa": 1266581710657814599,
}



COX_PURPLES = [
    discord.app_commands.Choice(name="Dexterous prayer scroll", value=1),
    discord.app_commands.Choice(name="Arcane prayer scroll", value=2),
    discord.app_commands.Choice(name="Twisted buckler", value=3),
    discord.app_commands.Choice(name="Dragon hunter crossbow", value=4),
    discord.app_commands.Choice(name="Dinh's bulwark", value=5),
    discord.app_commands.Choice(name="Ancestral hat", value=6),
    discord.app_commands.Choice(name="Ancestral robe top", value=7),
    discord.app_commands.Choice(name="Ancestral robe bottom", value=8),
    discord.app_commands.Choice(name="Dragon claws", value=9),
    discord.app_commands.Choice(name="Elder maul", value=10),
    discord.app_commands.Choice(name="Kodai insignia", value=11),
    discord.app_commands.Choice(name="Twisted bow", value=12)
    ]

DATE_FORMAT = "%m-%d-%y"
TIME_FORMAT = "%H:%M"

TASK_NUMBER_DICT = {
    1: "Get any good purple (No Prayer Scrolls)",
    2: "Get 5 Prayer Scrolls",
    3: 'Complete the "Kill it with Fire" Combat Task',
    4: 'Complete the "Perfect Olm" Combat Task',
    5: "Obtain a complete set of Ancestral",
    6: "Make a Kodai Wand from scratch",
    7: "Complete a 5-Scale Challenge Mode in 25 minutes or less",
    8: "Get a Twisted Recolor Kit",
    9: "Get the Metamorphic Dust",
    10: "Get a 5m+ PK at the Chaos Altar",
    11: "Complete 100 Laps of the Wildy Agility Course in 1 session, without banking",
    12: "Win a game of LMS",
    13: "Obtain and redeem 5 Loot Keys in 1 trip",
    14: "Get a PK at Callisto, Vet'ion, AND Venenatis",
    15: "Obtain all of the Wilderness Rings",
    16: "Complete the Malediction or Odium Ward from scratch",
    17: "Obtain a Chaos Elemental pet",
    18: "Obtain a Revenant Weapon drop",
    19: "Obtain 5 Abby Whips",
    20: "Obtain a Kraken Tentacle and a Trident of the Seas",
    21: "Kill the Abyssal Sire 200 Times as a team",
    22: "Obtain a Dark Bow",
    23: "Obtain a Dragon Chainbody",
    24: "Obtain a Hydra Fang",
    25: "Obtain a Drake Tooth or Claw",
    26: "Obtain at least 2 different Cerberus uniques",
    27: "Obtain any Slayer Boss Jar",
    28: "Get a good purple (No Ring, No Ward)",
    29: "Have all 6 books in 1 person's inventory in the Chest Room",
    30: "Upgrade a Icthlarin's Shroud (Min level 2, must be an upgrade, not a first obtain)",
    31: "Obtain Any Pet Transmog",
    32: "Obtain a complete set of Masori",
    33: "Get at least 2 of the Combat Tasks: Perfect Ba-Ba, Kephri, Akkha, Zebak",
    34: 'Complete the "Chompington" Combat Task',
    35: "Complete a 300+ Invo TOA within 18 minutes at any group size",
    36: "Complete a deathless 500 with a group of at least 3 teammates",
    37: "Get any 3 different Wintertodt uniques",
    38: "Max out your Monkey Backpack! (1 Player must do 2000 new laps of Ape Atoll Agility and get the Princely Monkey)",
    39: "Open 10 of each tier of Clue Casket (Must obtain and complete the clue during bingo)",
    40: "Obtain a Zalcano Shard",
    41: "Get 13,034,431 Runecrafting XP as a team",
    42: "Complete 1,000 Expert/Master Hunter Rumors",
    43: "Have a player on your team get a first clear at the Inferno",
    44: "Complete 350 rounds each of Wintertodt, Tempoross, and Zalcano",
    45: "Get ANY Skilling Pet (Includes Skilling Bosses, i.e. Tiny Tempor, Abyssal Protector, etc)",
    46: "Get a Zulrah unique",
    47: "Get all 4 Dagannoth Kings' Rings",
    48: "Obtain a Curved Bone",
    49: "Obtain any full set of Barrows Armor",
    50: "Get a Sigil from the Corporeal Beast",
    51: "Complete the Fight Caves in 26:30 or less",
    52: "Obtain a Draconic, Skeletal, or Wyvern Visage",
    53: "Get 1 unique from each of the 4 God Wars Generals (No Sword Shards)",
    54: "Complete A Voidwaker from scratch",
    55: "Complete a Hard Mode In the Grandmaster Time Limit - 3 Scale - 23 Min - 4 Scale - 21 Min - 5 Scale - 19 Min",
    56: "Get a purple!",
    57: 'Complete the "Back in my Day" Combat Task',
    58: "Bring a learner through a first clear Hard Mode",
    59: "Obtain a complete set of Justiciar",
    60: "Complete a deathless Hard Mode with at least 5 team members",
    61: 'Complete the "Personal Space" Combat Achievement',
    62: "Obtain a Holy Ornament Kit and a Sanguine Ornament Kit",
    63: "Get Lil' Zik",
    998: "Bonus Task",
    999: "Test Task",
}

TASK_POINTS_DICT = {
    1: 1,
    2: 1,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 2,
    8: 2,
    9: 3,
    10: 1,
    11: 1,
    12: 1,
    13: 1,
    14: 2,
    15: 2,
    16: 2,
    17: 2,
    18: 3,
    19: 1,
    20: 1,
    21: 1,
    22: 1,
    23: 2,
    24: 2,
    25: 2,
    26: 2,
    27: 3,
    28: 1,
    29: 1,
    30: 1,
    31: 1,
    32: 2,
    33: 2,
    34: 2,
    35: 2,
    36: 3,
    37: 1,
    38: 1,
    39: 1,
    40: 1,
    41: 2,
    42: 2,
    43: 2,
    44: 2,
    45: 3,
    46: 1,
    47: 1,
    48: 1,
    49: 1,
    50: 2,
    51: 2,
    52: 2,
    53: 2,
    54: 3,
    55: 1,
    56: 1,
    57: 1,
    58: 1,
    59: 2,
    60: 2,
    61: 2,
    62: 2,
    63: 3,
}

TEAMS_SHEETS_COLUMN_DICT = {
    # value must be int, not char
    "Godopka Team Name Pending": 6,
    "Cheese Cape": 7,
    "Sasa Loves Bingo": 8,
    "Drunk Chinchompa": 9,
    "Starship Enterprise": 10,
}


# Checks if task id is out of bounds (1 <= task_id <= num_tasks)
# Tested good 16 Jul 2024
def check_task_id(task_no: int) -> bool:
    if task_no <= 0:
        print("ERROR: Task submission failed, task id out of bounds. (less than zero)")
        return False
    elif task_no > len(TASK_NUMBER_DICT):
        print("ERROR: Task submission failed, task id out of bounds. (number too high)")
        return False
    else:
        return True


def check_screenshots(screenshots) -> bool:
    pass


# Gets users bingo team
# Tested good 19 Jul 2024
def get_user_team(roles: list) -> str:
    for team_id in BINGO_TEAM_IDS_LIST:
        for role in roles:
            if team_id == role.id:
                return role.name
    return None


def is_admin(member: discord.Member) -> bool:
    roles = []
    for role in member.roles:
        roles.append(role.id)
    if BINGO_ADMIN_ROLE_ID not in roles:
        return False
    return True


async def validate_data(interaction: discord.Interaction, date: str = None, time: str = None) -> bool:
    try:
        if date:
            datetime.strptime(date, Util.DATE_FORMAT)
        if time:
            datetime.strptime(time, Util.TIME_FORMAT)
    except ValueError:
        if date:
            await interaction.channel.send("Invalid **date* format. Use format: MM-DD-YY")
        if time:
            await interaction.channel.send("Invalid *time* format. Use format: HH:MM")
        return False
    return True
