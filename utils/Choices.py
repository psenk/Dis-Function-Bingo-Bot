import discord

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

DAY_AND_BOARD = [
    discord.app_commands.Choice(name="Day One: Chambers of Xeric", value=1),
    discord.app_commands.Choice(name="Day Two: Wilderness and PvP", value=2),
    discord.app_commands.Choice(name="Day Three: Slayer", value=3),
    discord.app_commands.Choice(name="Day Four: Tombs of Amascut", value=4),
    discord.app_commands.Choice(name="Day Five: Skilling", value=5),
    discord.app_commands.Choice(name="Day Six: Player versus Monster", value=6),
    discord.app_commands.Choice(name="Day Seven: Theatre of Blood", value=7),
]

DAY_ONE = [
    discord.app_commands.Choice(name="Get any good purple (No Prayer Scrolls)", value=1),
    discord.app_commands.Choice(name="Get 5 Prayer Scrolls", value=2),
    discord.app_commands.Choice(name='Complete the "Kill it with Fire" Combat Task', value=3),
    discord.app_commands.Choice(name='Complete the "Perfect Olm" Combat Task', value=4),
    discord.app_commands.Choice(name="Obtain a complete set of Ancestral", value=5),
    discord.app_commands.Choice(name="Make a Kodai Wand from scratch", value=6),
    discord.app_commands.Choice(name="Complete a 5-Scale Challenge Mode in 25 minutes or less", value=7),
    discord.app_commands.Choice(name="Get a Twisted Recolor Kit", value=8),
    discord.app_commands.Choice(name="Get the Metamorphic Dust", value=9),
]

DAY_TWO = [
    discord.app_commands.Choice(name="Get a 5m+ PK at the Chaos Altar", value=1),
    discord.app_commands.Choice(name="Complete 100 Laps of the Wildy Agility Course in 1 session, without banking", value=2),
    discord.app_commands.Choice(name="Win a game of LMS", value=3),
    discord.app_commands.Choice(name="Obtain and redeem 5 Loot Keys in 1 trip", value=4),
    discord.app_commands.Choice(name="Get a PK at Callisto, Vet'ion, AND Venenatis", value=5),
    discord.app_commands.Choice(name="Obtain all of the Wilderness Rings", value=6),
    discord.app_commands.Choice(name="Complete the Malediction or Odium Ward from scratch", value=7),
    discord.app_commands.Choice(name="Obtain a Chaos Elemental pet", value=8),
    discord.app_commands.Choice(name="Obtain a Revenant Weapon drop", value=9)
]

DAY_THREE = [
    discord.app_commands.Choice(name="Obtain 5 Abby Whips", value=1),
    discord.app_commands.Choice(name="Obtain a Kraken Tentacle and a Trident of the Seas", value=2),
    discord.app_commands.Choice(name="Kill the Abyssal Sire 200 Times as a team", value=3),
    discord.app_commands.Choice(name="Obtain a Dark Bow", value=4),
    discord.app_commands.Choice(name="Obtain a Dragon Chainbody", value=5),
    discord.app_commands.Choice(name="Obtain a Hydra Fang", value=6),
    discord.app_commands.Choice(name="Obtain a Drake Tooth or Claw", value=7),
    discord.app_commands.Choice(name="Obtain at least 2 different Cerberus uniques", value=8),
    discord.app_commands.Choice(name="Obtain any Slayer Boss Jar", value=9)
]

DAY_FOUR = [
    discord.app_commands.Choice(name="Get a good purple (No Ring, No Ward)", value=1),
    discord.app_commands.Choice(name="Have all 6 books in 1 person's inventory in the Chest Room", value=2),
    discord.app_commands.Choice(name="Upgrade a Icthlarin's Shroud (Min level 2, must be an upgrade, not a first obtain)", value=3),
    discord.app_commands.Choice(name="Obtain Any Pet Transmog", value=4),
    discord.app_commands.Choice(name="Obtain a complete set of Masori", value=5),
    discord.app_commands.Choice(name="Get at least 2 of the Combat Tasks: Perfect Ba-Ba, Kephri, Akkha, Zebak", value=6),
    discord.app_commands.Choice(name='Complete the "Chompington" Combat Task', value=7),
    discord.app_commands.Choice(name="Complete a 300+ Invo TOA within 18 minutes at any group size", value=8),
    discord.app_commands.Choice(name="Complete a deathless 500 with a group of at least 3 teammates", value=9)
]

DAY_FIVE = [
    discord.app_commands.Choice(name="Get any 3 different Wintertodt uniques", value=1),
    discord.app_commands.Choice(name="Max out your Monkey Backpack! (1 Player must do 2000 new laps of Ape Atoll Agility and get the Princely Monkey)", value=2),
    discord.app_commands.Choice(name="Open 10 of each tier of Clue Casket (Must obtain and complete the clue during bingo)", value=3),
    discord.app_commands.Choice(name="Obtain a Zalcano Shard", value=4),
    discord.app_commands.Choice(name="Get 13,034,431 Runecrafting XP as a team", value=5),
    discord.app_commands.Choice(name="Complete 1,000 Expert/Master Hunter Rumors", value=6),
    discord.app_commands.Choice(name="Have a player on your team get a first clear at the Inferno", value=7),
    discord.app_commands.Choice(name="Complete 350 rounds each of Wintertodt, Tempoross, and Zalcano", value=8),
    discord.app_commands.Choice(name="Get ANY Skilling Pet (Includes Skilling Bosses, i.e. Tiny Tempor, Abyssal Protector, etc)", value=9)
]

DAY_SIX = [
    discord.app_commands.Choice(name="Get a Zulrah unique", value=1),
    discord.app_commands.Choice(name="Get all 4 Dagannoth Kings' Rings", value=2),
    discord.app_commands.Choice(name="Obtain a Curved Bone", value=3),
    discord.app_commands.Choice(name="Obtain any full set of Barrows Armor", value=4),
    discord.app_commands.Choice(name="Get a Sigil from the Corporeal Beast", value=5),
    discord.app_commands.Choice(name="Complete the Fight Caves in 26:30 or less", value=6),
    discord.app_commands.Choice(name="Obtain a Draconic, Skeletal, or Wyvern Visage", value=7),
    discord.app_commands.Choice(name="Get 1 unique from each of the 4 God Wars Generals (No Sword Shards)", value=8),
    discord.app_commands.Choice(name="Complete A Voidwaker from scratch", value=9)
]

DAY_SEVEN = [
    discord.app_commands.Choice(name="Complete a Hard Mode In the Grandmaster Time Limit - 3 Scale - 23 Min - 4 Scale - 21 Min - 5 Scale - 19 Min", value=1),
    discord.app_commands.Choice(name="Get a purple!", value=2),
    discord.app_commands.Choice(name='Complete the "Back in my Day" Combat Task', value=3),
    discord.app_commands.Choice(name="Bring a learner through a first clear Hard Mode", value=4),
    discord.app_commands.Choice(name="Obtain a complete set of Justiciar", value=5),
    discord.app_commands.Choice(name="Complete a deathless Hard Mode with at least 5 team members", value=6),
    discord.app_commands.Choice(name='Complete the "Personal Space" Combat Achievement', value=7),
    discord.app_commands.Choice(name="Obtain a Holy Ornament Kit and a Sanguine Ornament Kit", value=8),
    discord.app_commands.Choice(name="Get Lil' Zik", value=9)
]

DAY_TASKS = {
    1: DAY_ONE,
    2: DAY_TWO,
    3: DAY_THREE,
    4: DAY_FOUR,
    5: DAY_FIVE,
    6: DAY_SIX,
    7: DAY_SEVEN
}