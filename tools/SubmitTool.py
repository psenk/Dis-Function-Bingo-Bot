import uuid
from datetime import datetime

import discord
import discord.ext
import discord.ext.commands

from tools.LogTool import LogTool
from tools.QueryTool import QueryTool
from utils import Constants, Functions


class SubmitTool(discord.ui.View):
    def __init__(self, ctx: discord.ext.commands.Context, message: discord.Message, logs_channel: discord.TextChannel, team: str, uuid_no: uuid.UUID, task_id: int = None, bonus: list = None) -> None:
        """
        SubmitTool Constructor
        param ctx: Discord Context instance
        param message: Discord Message instance
        param logs_channel: Discord TextChannel instance
        param team: str - bingo team name
        param uuid_no: uuid number of submission
        param task_id: int - optional, bingo task number
        param bonus: list- optional, bonus info
        return: None
        """
        super().__init__(timeout=None)
        self.logger = Functions.create_logger("tools")
        self.ctx = ctx
        self.message = message
        self.logs_channel = logs_channel
        self.team = team
        self.uuid_no = uuid_no
        self.task_id = task_id
        self.bonus = bonus
        self.msg = None

    async def create_submit_tool_embed(self) -> None:
        """
        Creates submission tool embed.
        return: None
        """
        submit_text = f"**Task #{self.task_id}\n{Constants.TASK_DESCRIPTION_MAP.get(self.task_id)}**" if self.task_id else f"**{self.bonus[1]}**"
        description = f"""You are attempting to submit: {submit_text}
        for the team: **{self.team}**.\nIs this correct?\n
        Please ensure your submission contains:
        -  The bingo codeword plugin
        -  The key item in view
        
        Screenshots of entire RuneLite window preferred!"""

        submit_tool = discord.Embed(title=f"Bingo Tile Submission Tool", color=0xFFFF00, description=description)
        submit_tool.set_image(url=self.message.attachments[0].url)
        submit_tool.set_author(name="Dis Function's Bingo Bonanza")
        submit_tool.set_footer(text=str(self.uuid_no))

        self.msg = await self.ctx.send(embed=submit_tool, view=self)
        self.logger.info("create_submit_tool_embed finished.")

    @discord.ui.button(label="Submit", style=discord.ButtonStyle.green)
    async def submit_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        d = datetime.now()
        response = f"# {self.task_id}: **{Constants.TASK_DESCRIPTION_MAP.get(self.task_id)}**" if self.task_id else f"**{self.bonus[1]}**"
        await interaction.followup.send(f"Submission for Task {response} sent by {interaction.user.display_name} on {d.strftime('%Y-%m-%d at %H:%M')}.")

        async with QueryTool() as tool:
            if self.task_id:
                await tool.submit_task(interaction.user.display_name, self.team, self.uuid_no, self.message.attachments[0].jump_url, str(self.message.id), task_id=self.task_id)
            else:
                await tool.submit_task(self.bonus[0], self.team, self.uuid_no, self.message.attachments[0].jump_url, str(self.message.id), purple=self.bonus[1], d=self.bonus[2])

        log_tool = LogTool(self.ctx, self.logs_channel, self.team, d, self.uuid_no, task_id=self.task_id)
        await log_tool.create_log_embed()
        await self.msg.delete()
        self.logger.info("submit_button finished.")

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.send_message("Submission canceled.", delete_after=5.0)
        await self.msg.delete()
        self.logger.info("cancel_button finished.")
