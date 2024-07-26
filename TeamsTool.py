import discord

class TeamsTool(discord.ui.View):
    def __init__(self, teams: list) -> None:
        super().__init__(timeout=60.0)
        self.team = None
        dropdown = TeamsDropdown(self, teams)
        self.add_item(dropdown)
        
    def add_team(self, team: str) -> None:
        self.team = team
        self.stop()
    
class TeamsDropdown(discord.ui.Select):
    
    def __init__(self, parent: discord.ui.View, teams: list) -> None:
        self.parent = parent
        teams = [discord.SelectOption(label=team['team_name'], value=team['team_name']) for team in teams]
        super().__init__(placeholder="Select a team", options=teams, min_values=1, max_values=1)

    
    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        self.parent.add_team(self.values[0])
        
    async def on_timeout(self) -> None:
        print("Selecting purple menu timed out.")
        return await super().on_timeout()