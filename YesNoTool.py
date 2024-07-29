import discord

class YesNoTool(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=60.0)
        self.response = None
        dropdown = YesNoDropdown(self)
        self.add_item(dropdown)

    def add_response(self, response: str) -> None:
        self.response = response
        self.stop()

class YesNoDropdown(discord.ui.Select):
    
    def __init__(self, parent: discord.ui.View):
        self.parent = parent
        options = [discord.SelectOption(label="Yes", value="Yes"), discord.SelectOption(label="No", value="No")]
        super().__init__(placeholder="Select", options=options, min_values=1, max_values=1)
    
    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        self.parent.add_response(self.values[0])