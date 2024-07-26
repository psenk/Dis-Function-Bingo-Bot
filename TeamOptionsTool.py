import discord

class TeamOptionsTool(discord.ui.View):
    def __init__(self, option: str) -> None:
        super().__init__(timeout=60.0)
        self.option = None
        dropdown = TeamOptionsDropdown(self)
        self.add_item(dropdown)
        
    def add_option(self, option: str) -> None:
        self.option = option
        self.stop()
    
class TeamOptionsDropdown(discord.ui.Select):
    
    def __init__(self, parent: discord.ui.View) -> None:
        self.parent = parent
        options = []
        options.append(discord.SelectOption(label="Update team name", value="0"))
        options.append(discord.SelectOption(label="Update team captain", value="1"))
        options.append(discord.SelectOption(label="Update role ID", value="2"))
        options.append(discord.SelectOption(label="Update submission channel ID", value="3"))
        super().__init__(placeholder="Select an option", options=options, min_values=1, max_values=1)

    
    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        self.parent.add_option(self.values[0])
        
    async def on_timeout(self) -> None:
        print("Selecting purple menu timed out.")
        return await super().on_timeout()