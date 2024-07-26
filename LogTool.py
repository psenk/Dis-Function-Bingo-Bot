import datetime
import uuid

import discord
import discord.ext
import discord.ext.commands

import Util


class LogTool(discord.ui.View):
    def __init__(self, ctx: discord.ext.commands.Context, logs_channel: discord.TextChannel, multi: bool, team: str, task_id: int, timestamp: datetime.datetime, uuid_no: uuid.UUID):
        """
        param: Discord Context object
        param: Discord TextChannel object
        param boolean: multiple submissions
        param string: bingo team name
        param int: bingo task number
        param datetime: timestamp of submission
        param uuid: UUID number of submission
        description: Constructor for LogTool
        return: None
        """
        super().__init__(timeout=None)
        self.ctx = ctx
        self.logs_channel = logs_channel
        self.multi = multi
        self.team = team
        self.task_id = task_id
        self.timestamp = timestamp
        self.uuid_no = uuid_no
        self.message = None

    async def create_log_embed(self) -> None:
        """
        param: Discord context object
        param: Discord TextChannel object
        param boolean: multiple submissions
        param string: name of bingo team
        param int: id # of bingo task
        param datetime: timestamp of submission
        param: UUID object
        description: posts log embed to logs channel
        return: None
        """
        if self.multi:
            log_embed = discord.Embed(title="Dis Function's Bingo Bonanza", color=0x0000FF)
            log_embed.set_author(name=f"Submission Received (multiple images)", url=self.ctx.message.jump_url)
        else:
            log_embed = discord.Embed(title="Dis Function's Bingo Bonanza", color=0x0000FF)
            log_embed.set_author(name=f"Submission Received", url=self.ctx.message.jump_url)

        # log_embed(name="Submission Link", url=ctx.message.jump_url)
        log_embed.set_thumbnail(url=self.ctx.message.attachments[0].url)
        log_embed.add_field(name="Team:", value=self.team, inline=True)
        log_embed.add_field(name="", value="", inline=True)
        log_embed.add_field(name="Player:", value=self.ctx.author.display_name, inline=True)
        log_embed.add_field(name="Task:", value=Util.TASK_NUMBER_DICT.get(self.task_id))
        log_embed.add_field(name="", value="", inline=True)
        log_embed.add_field(name="Submitted on:", value=self.timestamp, inline=True)
        log_embed.set_footer(text=self.uuid_no)

        self.message = await self.logs_channel.send(embed=log_embed, view=self)

    # log tool buttons
    # add to constructor: purple: str, player: str
    """
    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green)
    async def approve_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        await self.ctx.send(f"Submission for Task #{self.task_id}: {Util.TASK_NUMBER_DICT.get(self.task_id)} has been approved!")
        await self.message.add_reaction("✅")
        await self.ctx.message.add_reaction("✅")
        if self.task_id == 998:
            sheets_tool = SheetsTool(self.team, self.timestamp, self.ctx.author.display_name, self.task_id, self.purple)
            sheets_tool.add_purple(self.player)
        else:
            sheets_tool = SheetsTool(self.team, self.timestamp, self.ctx.author.display_name, self.task_id)
            sheets_tool.update_sheets()
        await QueryTool.delete_submission(self.uuid_no.__str__())
        print(f"Task {self.uuid_no.__str__()[:6]} has been approved by the bingo admins.")
        await interaction.message.edit(view=None)

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.red)
    async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        await self.ctx.send(f"Submission for Task #{self.task_id}: {Util.TASK_NUMBER_DICT.get(self.task_id)} has been rejected!")
        await self.message.add_reaction("❌")
        await self.ctx.message.add_reaction("❌")
        await QueryTool.delete_submission(self.uuid_no.__str__())
        print(f"Task {self.uuid_no.__str__()[:6]} has been rejected by the bingo admins.")
        await interaction.message.edit(view=None)
    """
