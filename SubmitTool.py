import datetime
import uuid
import discord
import discord.ext.commands
from LogTool import LogTool
from QueryTool import QueryTool
import Util
import discord.ext


class SubmitTool(discord.ui.View):
    def __init__(self, ctx: discord.ext.commands.Context, logs_channel: discord.TextChannel, task_id: int, team: str, multi: bool, uuid_no: uuid.UUID):
        """
        param: Discord Context object
        param: Discord TextChannel object
        param int: bingo task number
        param string: bingo team name
        param boolean: multiple submissions
        param uuid: uuid number of submission
        description: Constructor for SubmitTool
        return: None
        """
        super().__init__(timeout=None)
        self.ctx = ctx
        self.logs_channel = logs_channel
        self.task_id = task_id
        self.team = team
        self.multi = multi
        self.uuid_no = uuid_no
        self.message = None
        self.query_tool = QueryTool()

    async def create_submit_tool_embed(self) -> None:
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
        description: str = f"""You are attempting to submit: **Task #{self.task_id}\n{Util.TASK_NUMBER_DICT.get(self.task_id)}**\nfor the Team: **{self.team}**.\nIs this correct?\n
        Please ensure your submission contains:\n
        1. The bingo codeword\n2. The key item in view\n3. Chat notification (if applicable)"""

        submit_tool = discord.Embed(title=f"Bingo Tile Submission Tool", color=0x0000FF, description=description)
        submit_tool.set_author(name="Dis Function's Bingo Bonanza")
        submit_tool.set_image(url=self.ctx.message.attachments[0].url)
        submit_tool.set_footer(text=self.uuid_no)
        
        self.message = await self.ctx.send(embed=submit_tool, view=self)


    @discord.ui.button(label="Submit", style=discord.ButtonStyle.green)
    async def submit_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        d = datetime.datetime.now()
        timestamp = d.strftime("%Y-%m-%d at %H:%M:%S")
        await self.ctx.send("Sending submission to bingo admins...", delete_after=3.0)
        await self.ctx.send(f"Submission for Task #{self.task_id}: {Util.TASK_NUMBER_DICT.get(self.task_id)} sent by {self.ctx.author.display_name} on {timestamp}.")
        await self.query_tool.submit_task(self.task_id, self.ctx.author.display_name, self.team, self.uuid_no, self.ctx.message.jump_url, self.ctx.message.id)
        log_tool = LogTool(self.ctx, self.logs_channel, self.multi, self.team, self.task_id, d, self.uuid_no)
        await log_tool.create_log_embed()
        await interaction.response.edit_message(view=None)
        await self.message.delete()
        print(f"{self.ctx.author.display_name} has submitted a task, UUID {self.uuid_no.__str__()[:6]}.")

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self.ctx.send("Submission cancelled.", delete_after=3.0)
        await interaction.response.defer()
        await self.message.delete()

