import discord
import Util


class BonusTool(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=60.0)
        self.purp = None
        dropdown = BonusToolDropdown(self)
        self.add_item(dropdown)

    def add_purp(self, purp: str) -> None:
        self.purp = purp
        self.stop()

class BonusToolDropdown(discord.ui.Select):
    
    def __init__(self, parent: discord.ui.View):
        self.parent = parent
        options = [discord.SelectOption(label=p, value=p) for p in Util.COX_PURPLES]
        super().__init__(placeholder="Purple", options=options, min_values=1, max_values=1)
    
    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        self.parent.add_purp(self.values[0])
        
    async def on_timeout(self) -> None:
        print("Selecting purple menu timed out.")
        return await super().on_timeout()