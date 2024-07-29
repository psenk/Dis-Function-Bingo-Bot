import discord

from utils import Functions

class YesNoTool(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=60.0)
        self.logger = Functions.create_logger("tools")
        self.response = None
        dropdown = YesNoDropdown(self)
        self.add_item(dropdown)

    def add_response(self, response: str) -> None:
        self.response = response
        self.stop()
        self.logger.info("Response added.")

class YesNoDropdown(discord.ui.Select):
    
    def __init__(self, parent: discord.ui.View):
        self.parent = parent
        options = [discord.SelectOption(label="Yes", value="Yes", emoji="👍"), discord.SelectOption(label="No", value="No", emoji="👎")]
        super().__init__(placeholder="Select", options=options, min_values=1, max_values=1)
    
    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        self.parent.add_response(self.values[0])
        self.parent.logger.info(f"Response selected: {self.values[0]}")