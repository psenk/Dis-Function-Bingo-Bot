-- DROP AND CREATE TEAM TABLES

DROP TABLE IF EXISTS settings CASCADE;
DROP TABLE IF EXISTS tasks CASCADE;

DROP TABLE IF EXISTS completions CASCADE;
DROP TABLE IF EXISTS submissions CASCADE;
DROP TABLE IF EXISTS teams;


--- BINGO TASKS

CREATE TABLE tasks (
	task_id SERIAL NOT NULL,
    point_value INT NOT NULL,
    task_name VARCHAR(500) NOT NULL,
    PRIMARY KEY (task_id)
);

INSERT INTO tasks VALUES 
	(1, 1, E'Get any good purple (No Prayer Scrolls)'),
	(2, 1, E'Get 5 Prayer Scrolls'),
	(3, 1, E'Complete the "Kill it with Fire" Combat Task'),
	(4, 1, E'Complete the "Perfect Olm" Combat Task'),
	(5, 2, E'Obtain a complete set of Ancestral'),
	(6, 2, E'Make a Kodai Wand from scratch'),
	(7, 2, E'Complete a 5-Scale Challenge Mode in 25 minutes or less'),
	(8, 2, E'Get a Twisted Recolor Kit'),
	(9, 3, E'Get the Metamorphic Dust'),
    (10, 1, E'Get a 5m+ PK at the Chaos Altar'),
    (11, 1, E'Complete 100 Laps of the Wildy Agility Course in 1 session, without banking'),
    (12, 1, E'Win a game of LMS'),
    (13, 1, E'Obtain and redeem 5 Loot Keys in 1 Trip'),
    (14, 2, E'Get a PK at Callisto, Vet''ion, AND Venenatis'),
    (15, 2, E'Obtain all of the Wilderness Rings'),
    (16, 2, E'Complete the Malediction or Odium Ward from scratch'),
    (17, 2, E'Obtain a Chaos Elemental pet'),
    (18, 3, E'Obtain a Revenant Weapon drop'),
    (19, 1, E'Obtain 5 Abby Whips'),
    (20, 1, E'Obtain a Kraken Tentacle and a Trident of the Seas'),
    (21, 1, E'Kill the Abyssal Sire 200 Times as a team'),
    (22, 1, E'Obtain a Dark Bow'),
    (23, 2, E'Obtain a Dragon Chainbody'),
    (24, 2, E'Obtain a Hydra Fang'),
    (25, 2, E'Obtain a Drake Tooth or Claw'),
    (26, 2, E'Obtain at least 2 different Cerberus uniques'),
    (27, 3, E'Obtain any Slayer Boss Jar'),
    (28, 1, E'Get a good purple (No Ring, No Ward)'),
    (29, 1, E'Have all 6 books in 1 person''s inventory in the Chest Room'),
    (30, 1, E'Upgrade a Icthlarin''s Shroud (Min level 2, must be an upgrade, not a first obtain)'),
    (31, 1, E'Obtain Any Pet Transmog'),
    (32, 2, E'Obtain a complete set of Masori'),
    (33, 2, E'Get at least 2 of the Combat Tasks: Perfect Ba-Ba, Kephri, Akkha, Zebak'),
    (34, 2, E'Complete the "Chompington" Combat Task'),
    (35, 2, E'Complete a 300+ Invo TOA within 18 minutes at any group size'),
    (36, 3, E'Complete a deathless 500 with a group of at least 3 teammates'),
    (37, 1, E'Get any 3 different Wintertodt uniques'),
    (38, 1, E'Max out your Monkey Backpack! (1 Player must do 2000 new laps of Ape Atoll Agility and get the Princely Monkey)'),
    (39, 1, E'Open 10 of each tier of Clue Casket (Must obtain and complete the clue during bingo)'),
    (40, 1, E'Obtain a Zalcano Shard'),
    (41, 2, E'Get 13,034,431 Runecrafting XP as a team'),
    (42, 2, E'Complete 1,000 Expert/Master Hunter Rumors'),
    (43, 2, E'Have a player on your team get a first clear at the Inferno'),
    (44, 2, E'Complete 350 rounds each of Wintertodt, Tempoross, and Zalcano'),
    (45, 3, E'Get ANY Skilling Pet (Includes Skilling Bosses, i.e. Tiny Tempor, Abyssal Protector, etc)'),
    (46, 1, E'Get a Zulrah unique'),
    (47, 1, E'Get all 4 Dagannoth Kings'' Rings'),
    (48, 1, E'Obtain a Curved Bone'),
    (49, 1, E'Obtain any full set of Barrows Armor'),
    (50, 2, E'Get a Sigil from the Corporeal Beast'),
    (51, 2, E'Complete the Fight Caves in 26:30 or less'),
    (52, 2, E'Obtain a Draconic, Skeletal, or Wyvern Visage'),
    (53, 2, E'Get 1 unique from each of the 4 God Wars Generals (No Sword Shards)'),
    (54, 3, E'Complete A Voidwaker from scratch'),
	(55, 1, E'Complete a Hard Mode In the Grandmaster Time Limit - 3 Scale - 23 Min - 4 Scale - 21 Min - 5 Scale - 19 Min'),
	(56, 1, E'Get a purple!'),
	(57, 1, E'Complete the "Back in my Day" Combat Task'),
	(58, 1, E'Bring a learner through a first clear Hard Mode'),
	(59, 2, E'Obtain a complete set of Justiciar'),
	(60, 2, E'omplete a deathless Hard Mode with at least 5 team members'),
	(61, 2, E'Complete the "Personal Space" Combat Achievement'),
	(62, 2, E'Obtain a Holy Ornament Kit and a Sanguine Ornament Kit'),
	(63, 3, E'Get Lil'' Zik'),
	(998, 998, E'Bonus Task'),
    (999, 999, E'Test Task');

--- BOT SETTINGS

CREATE TABLE settings (
	bingo_day INT
);

INSERT INTO settings VALUES (0);

--- team_id is the teams Discord submission channel id

CREATE TABLE teams (
	team_name VARCHAR(100) NOT NULL,
	captain VARCHAR(20) NOT NULL,
	role_id VARCHAR(50) NOT NULL,
	channel_id VARCHAR(50) NOT NULL
);

INSERT INTO teams VALUES
	(E'Team One', 'Captain', 'X', 'X'),
	(E'Team Two', 'Captain', 'X', 'X'),
	(E'Team Three', 'Captain', 'X', 'X'),
	(E'Team Four', 'Captain', 'X', 'X'),
	(E'Team Five', 'Captain', 'X', 'X');

CREATE TABLE completions (
	item_id SERIAL NOT NULL,
    team VARCHAR(100) NOT NULL,
    player VARCHAR(20) NOT NULL,
    task INT NOT NULL,
    completion_date TIMESTAMP NOT NULL,
    PRIMARY KEY (item_id),
    FOREIGN KEY (task) REFERENCES tasks(task_id)
);

CREATE TABLE submissions (
	submission_id SERIAL,
    task_id INT,
    player VARCHAR(100) NOT NULL,
    team VARCHAR(100) NOT NULL,
	uuid_no UUID NOT NULL,
    jump_url VARCHAR(500) NOT NULL,
    message_id VARCHAR(50) NOT NULL,
    date_submitted TIMESTAMP NOT NULL,
	purple VARCHAR(30),
    PRIMARY KEY (submission_id),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id)
);