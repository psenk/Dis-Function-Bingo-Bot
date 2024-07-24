import discord


class ConfirmTool(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=60.0)
        self.confirm = None
        dropdown = ConfirmDropdown(self)
        self.add_item(dropdown)

    def add_confirm(self, confirm: str) -> None:
        self.confirm = confirm
        self.stop()

class ConfirmDropdown(discord.ui.Select):
    
    def __init__(self, parent: discord.ui.View):
        self.parent = parent
        options = [discord.SelectOption(label="Yes", value="Yes"), discord.SelectOption(label="No", value="No")]
        super().__init__(placeholder="Select", options=options, min_values=1, max_values=1)
    
    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        self.parent.add_confirm(self.values[0])
        
    async def on_timeout(self) -> None:
        print("Selecting purple menu timed out.")
        return await super().on_timeout()