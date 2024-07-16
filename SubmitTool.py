import discord
from discord.interactions import Interaction

class SubmitTool(discord.ui.View):
    
    def __init__(self, task_id: int, team: str):
        super().__init__(timeout=None)
        self.task_id: int = task_id
        self.team: str = team
        
    @discord.ui.button(label="Submit", style=discord.ButtonStyle.green)
    async def submit_button(self):
        pass
    
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel_button(self):
        pass
    
    
async def create_submit_tool_embed(ctx, task_id: int, team: str) -> None:
    
    description = f"""You are attempting to submit Task #{task_id} for the group {team}. Is this correct?\n
    Please ensure your submission contains:\n
    1. The bingo codeword\n2. The key item in view\n3. Chat notification (if applicable)"""
    
    submit_tool = discord.Embed(
        title=f"Send Users Bingo Moments Instantly Tool (SUBMIT)", color=0x0000FF, description=description
    )
    submit_tool.set_author(name="Dis Function's Bingo Bonanza")
    submit_tool.set_image(url=ctx.message.attachments[0])
    
    await ctx.send(embed=submit_tool)