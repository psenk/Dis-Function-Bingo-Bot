import datetime
import uuid

import discord
import discord.ext
import discord.ext.commands

import Util


class LogTool(discord.ui.View):
    def __init__(self, ctx: discord.ext.commands.Context, logs_channel: discord.TextChannel, multi: bool, team: str, timestamp: datetime.datetime, uuid_no: uuid.UUID, task_id: int = None):
        """
        LogTool Constructor
        param ctx: Discord Context instance
        param logs_channel: Discord TextChannel 
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
        
        log_embed = discord.Embed(title=f"Submission Received{' (multiple images)' if self.multi else ''}", color=0x0000FF)
        log_embed.set_author(name=f"Submission", url=self.ctx.message.jump_url)

        log_embed.add_field(name="Team", value=self.team, inline=True)
        log_embed.add_field(name="Player", value=self.ctx.author.display_name, inline=True)
        log_embed.add_field(name="", value="", inline=True)
        log_embed.add_field(name="Task", value=f"{'Bonus' if self.multi else Util.TASK_NUMBER_DICT.get(self.task_id)}")
        log_embed.add_field(name="Submitted on", value=self.timestamp, inline=True)
        log_embed.add_field(name="", value="", inline=True)
        log_embed.set_footer(text=self.uuid_no)

        self.message = await self.logs_channel.send(embed=log_embed, view=self)