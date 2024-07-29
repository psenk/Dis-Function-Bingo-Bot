import uuid
from datetime import datetime

import discord
import discord.ext
import discord.ext.commands

import Util
from LogTool import LogTool
from QueryTool import QueryTool


class SubmitTool(discord.ui.View):
    def __init__(self, ctx: discord.ext.commands.Context, attachments: list, logs_channel: discord.TextChannel, task_id: int, team: str, uuid_no: uuid.UUID) -> None:
        """
        SubmitTool Constructor
        param attachments: list - list of attachments
        param logs_channel: Discord TextChannel instance
        param task_id: int - bingo task number
        param team: str - bingo team name
        param uuid_no: uuid number of submission
        return: None
        """
        super().__init__(timeout=None)
        self.ctx = ctx
        self.attachments = attachments
        self.logs_channel = logs_channel
        self.task_id = task_id
        self.team = team
        self.uuid_no = uuid_no
        self.message = None

    async def create_submit_tool_embed(self) -> None:
        """
        Creates submission tool embed.
        return: None
        """
        description = f"""You are attempting to submit: **Task #{self.task_id}\n{Util.TASK_NUMBER_DICT.get(self.task_id)}**
        for the Team: **{self.team}**.\nIs this correct?\n
        Please ensure your submission contains:
        o  The bingo codeword plugin
        o  The key item in view
        
        Screenshots of entire RuneLite window preferred!"""

        submit_tool = discord.Embed(title=f"Bingo Tile Submission Tool", color=0xFFFF00, description=description)
        submit_tool.set_image(url=self.attachments[0].url)
        submit_tool.set_author(name="Dis Function's Bingo Bonanza")
        submit_tool.set_footer(text=self.uuid_no)

        self.message = await self.ctx.send(embed=submit_tool, view=self)

    @discord.ui.button(label="Submit", style=discord.ButtonStyle.green)
    async def submit_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        d = datetime.now()
        await interaction.followup.send(f"Submission for Bingo Task {self.task_id}: **{Util.TASK_NUMBER_DICT.get(self.task_id)}** was sent by {interaction.user.display_name} on {d.strftime('%Y-%m-%d at %H:%M:%S')}.")
        
        async with QueryTool() as query_tool:
            await query_tool.submit_task(interaction.user.display_name, self.team, self.uuid_no, self.ctx.message.jump_url, str(self.ctx.message.id), task_id=self.task_id)
        log_tool = LogTool(self.ctx, self.logs_channel, self.team, d, self.uuid_no, task_id=self.task_id)
        await log_tool.create_log_embed()
        # await interaction.response.edit_message(view=None)
        await self.message.delete()
        print(f"{self.interaction.user.display_name} has submitted a task -> UUID {self.uuid_no.__str__()[:6]}.")

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.send_message("Submission cancelled.", delete_after=5.0)
        await self.message.delete()