import discord


class Game(discord.ui.View):
    game_map = [
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
            '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
            '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
            '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
            '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
            '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
            '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
            '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
            '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
            '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
            '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
            '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
            '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
            '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    ]

    class Player:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.icon = 'X'

        def up(self):
            self.x = max(0, self.x - 1)

        def dn(self):
            self.x = min(len(Game.game_map) - 1, self.x + 1)

        def lt(self):
            self.y = max(0, self.y - 1)

        def rt(self):
            self.y = min(len(Game.game_map[0]) - 1, self.y + 1)

    def __init__(self, interaction: discord.Interaction, player=None):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.player = player
        self.game_map = None
        self.instance = None

    async def start(self):
        self.instance = await self.interaction.channel.send(self.draw_map(), view=self)

    async def update(self):
        if self.instance:
            await self.instance.edit(content=self.draw_map(), view=self)

    def set_map(self, m):
        self.game_map = m

    def set_player(self, p):
        self.player = p

    def get_player_loc(self):
        return [self.player.x, self.player.y]

    def draw_map(self) -> str:
        map_copy = [row[:] for row in self.game_map]
        p = self.get_player_loc()
        map_copy[p[0]][p[1]] = self.player.icon

        map_str = ''
        for row in map_copy:
            for col in row:
                map_str += col
            map_str += '\n'
        return map_str

    @discord.ui.button(custom_id='left', emoji='⏪')
    async def left_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        self.player.lt()
        await self.update()

    @discord.ui.button(custom_id='up', emoji='⏫')
    async def up_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        self.player.up()
        await self.update()

    @discord.ui.button(custom_id='down', emoji='⏬')
    async def down_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        self.player.dn()
        await self.update()

    @discord.ui.button(custom_id='right', emoji='⏩')
    async def right_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        self.player.rt()
        await self.update()
