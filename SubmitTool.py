import datetime
import uuid
import discord
from discord.interactions import Interaction
import LogTool
import Util

class SubmitTool(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)


async def create_submit_tool_embed(ctx, logs_channel: discord.TextChannel, task_id: int, team: str, multi: bool, uuid_no: uuid.UUID) -> None:
    
    # Embed
    description: str = f"""You are attempting to submit Task #{task_id}: {Util.task_number_dict.get(task_id)} for the Team: {team}. Is this correct?\n
    Please ensure your submission contains:\n
    1. The bingo codeword\n2. The key item in view\n3. Chat notification (if applicable)"""

    submit_tool = discord.Embed(
        title=f"Bingo Tile Submission Tool",
        color=0x0000FF,
        description=description
    )
    submit_tool.set_author(name="Dis Function's Bingo Bonanza")
    submit_tool.set_image(url=ctx.message.attachments[0].url)
    submit_tool.set_footer(text=uuid_no)

    # Buttons
    class SubmissionButtons(discord.ui.View):

        @discord.ui.button(label="Submit", style=discord.ButtonStyle.green)
        async def submit_button(
            self, interaction: discord.Interaction, button: discord.ui.Button
        ) -> None:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d at %H:%M:%S")
            await ctx.send("Sending submission to bingo admins...", delete_after=3.0)
            await ctx.send(f"Submission for Task #{task_id}: {Util.task_number_dict.get(task_id)} sent by {ctx.author.display_name} on {timestamp}.")
            # send logs
            await LogTool.create_log_embed(ctx, logs_channel, multi, team, task_id, timestamp, uuid_no)
            await interaction.response.edit_message(view=None)
            await message.delete()

        @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
        async def cancel_button(
            self, interaction: discord.Interaction, button: discord.ui.Button
        ) -> None:
            await ctx.send("Submission cancelled.", delete_after=3.0)
            await interaction.response.defer()
            await message.delete()

    message = await ctx.send(embed=submit_tool, view=SubmissionButtons())