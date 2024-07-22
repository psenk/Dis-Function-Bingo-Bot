import datetime
import uuid
import discord
import discord.ext.commands
from LogTool import LogTool
from QueryTool import QueryTool
import Util
import discord.ext


class SubmitTool(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def create_submit_tool_embed(ctx: discord.ext.commands.Context, logs_channel: discord.TextChannel, task_id: int, team: str, multi: bool, uuid_no: uuid.UUID) -> None:
        """
        param: Discord Context object
        param: Discord TextChannel object
        param int: id # of bingo task
        param string: name of bingo team
        param boolean: multiple submissions
        param: UUID of task
        description: posts submission tool embed
        return: None
        """
        description: str = f"""You are attempting to submit Task #{task_id}: {Util.task_number_dict.get(task_id)} for the Team: {team}. Is this correct?\n
        Please ensure your submission contains:\n
        1. The bingo codeword\n2. The key item in view\n3. Chat notification (if applicable)"""

        submit_tool = discord.Embed(title=f"Bingo Tile Submission Tool", color=0x0000FF, description=description)
        submit_tool.set_author(name="Dis Function's Bingo Bonanza")
        submit_tool.set_image(url=ctx.message.attachments[0].url)
        submit_tool.set_footer(text=uuid_no)

        # Buttons
        class SubmissionButtons(discord.ui.View):
            @discord.ui.button(label="Submit", style=discord.ButtonStyle.green)
            async def submit_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d at %H:%M:%S")
                await ctx.send("Sending submission to bingo admins...", delete_after=3.0)
                await ctx.send(f"Submission for Task #{task_id}: {Util.task_number_dict.get(task_id)} sent by {ctx.author.display_name} on {timestamp}.")
                await QueryTool.submit_task(task_id, ctx.author.display_name, team, uuid_no, ctx.message.jump_url, ctx.message.id)
                await LogTool.create_log_embed(ctx, logs_channel, multi, team, task_id, timestamp, uuid_no)
                await interaction.response.edit_message(view=None)
                await message.delete()
                print(f"{ctx.author.display_name} has submitted a task, UUID {uuid_no[:6]}.")

            @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
            async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
                await ctx.send("Submission cancelled.", delete_after=3.0)
                await interaction.response.defer()
                await message.delete()

        message = await ctx.send(embed=submit_tool, view=SubmissionButtons())
