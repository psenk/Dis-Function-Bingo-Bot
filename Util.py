import datetime
import discord

import discord.ext
import discord.ext.commands

task_number_dict = {
    1: "Complete a Hard Mode In the Grandmaster Time Limit - 3 Scale - 23 Min - 4 Scale - 21 Min - 5 Scale - 19 Min",
    2: "Get a Purple!",
    3: "Complete the Back in my Day Combat Task",
    4: "Obtain a Holy Ornament Kit AND a Sanguine Ornament Kit",
    5: "Complete a set of Justicar",
    6: "Complete a Deathless Hard Mode with at least 5 Team Members",
    7: "Complete the Personal Space Combat Achievement",
    8: "Bring a Learner through a first Clear Hard Mode",
    9: "Get Lil'Zik",
    10: "Get a 5m+ PK at the Chaos Altar",
    11: "Complete 100 Laps of the WIldy Agility Course in 1 session, without banking",
    12: "Win a game of LMS",
    13: "Obtain and Redeem 5 Loot Keys in 1 Trip",
    14: "Get a PK at Calisto, Vet’ion, AND Venenatis",
    15: "Obtain all of the Wilderness Rings",
    16: "Complete the Malediction or Odium Ward from Scratch",
    17: "Obtain a Chaos Elemental pet",
    18: "Obtain a Revenant Weapon Drop",
    19: "Obtain 5 Abby Whips",
    20: "Obtain a Kraken Tentacle and a Trident of the Seas",
    21: "Kill the Abyssal Sire 200 Times as a Team",
    22: "Obtain a Dark Bow",
    23: "Obtain a Dragon Chainbody",
    24: "Obtain a Hydra Fang",
    25: "Obtain a Drake Tooth or Claw",
    26: "Obtain at least 2 different Cerberus Unique",
    27: "Obtain any Slayer Boss Jar",
    28: "Get a Good Purple (No Ring, No Ward)",
    29: "Exit The Raid with All 6 Books in 1 Players Inventory",
    30: "Upgrade a Icthalrin’s Shroud (Min level 2, must be an upgrade, not a first obtain)",
    31: "Obtain Any Pet Transmog",
    32: "Complete a set of Masori",
    33: "Get at least 2 of the Tasks: Prefect Ba-Ba, Kephri, Akkha, Zebak",
    34: "Defeat Zebak using only melee attacks and without dying yourself. (Chompington)",
    35: "Complete a 300+ Invo TOA within 18 minutes at any Group Size",
    36: "Complete a deathless 500 with a group of at least 3",
    37: "Get any 3 Different Wintertodt Uniques",
    38: "Max Out Your Monkey Backpack! (1 Player must do 2000 new laps of Ape Atol Agility and get the Princely monkey)",
    39: "Open 10 Of Each Tier of Clue Casket (Must obtain and complete the clue during bingo)",
    40: "Obtain a Zalcano Shard",
    41: "13,034,431 Runecrafting XP (Whole team)",
    42: "Complete 1,000 Expert/Master Hunter Rumors",
    43: "Have a player on your team get a First Clear at the Inferno (any funny business, i.e. buying capes, or logging in to other players account will forfeit the entire days points)",
    44: "Complete 350 rounds each of Wintertodt, Tempoross, and Zalcano",
    45: "Get ANY Skilling Pet (Includes Skilling Bosses, i.e. Tiny Tempor, Abyssal Protector, etc)",
    46: "Get a Zulrah Unique",
    47: "Get all 4 Dagannoth Kings' Rings",
    48: "Obtain a Curved Bone",
    49: "Obtain any Full Set of Barrows Armor",
    50: "Get A Sigil From Corporeal Beast",
    51: "Complete the Fight Caves in 26:30 or less",
    52: "Obtain a Draconic, Skeletal, or Wyvern Visage",
    53: "Get 1 Unique from each of the 4 God Wars Generals (No Sword Shards)",
    54: "Complete A Voidwaker from Scratch",
    55: "Get Any Good Purple (No Prayer Scrolls)",
    56: "Get 5 Prayer Scrolls",
    57: "Complete the Kill it with Fire Combat Task",
    58: "Complete the Perfect Olm Combat Task",
    59: "Get a Complete set of Ancestral",
    60: "Make a Kodai Wand from scratch",
    61: "Complete a 5-Scale Challenge Mode in 25 minutes or less",
    62: "Get a Twisted Recolor Kit",
    63: "Get the Metamorphic Dust",
    999: "Test Task"
}

task_points_dict = {
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

# Discord role IDs
bingo_teams = [1262935908777332757]


# Checks if task id is out of bounds (1 <= task_id <= num_tasks)
# Tested good 16 Jul 2024
def check_task_id(task_no) -> bool:
    if task_no <= 0:
        print("ERROR: Task submission failed, task id out of bounds. (less than zero)")
        return False
    elif task_no > len(task_number_dict):
        print("ERROR: Task submission failed, task id out of bounds. (number too high)")
        return False
    else:
        return True


def check_screenshots(screenshots) -> bool:
    pass


# Gets users bingo team
# Tested good 19 Jul 2024
def get_user_team(roles: list) -> str:
    for team_id in bingo_teams:
        for role in roles:
            if team_id == role.id:
                return role.name
