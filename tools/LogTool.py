import datetime
import uuid

import discord
import discord.ext
import discord.ext.commands

from utils import Constants, Functions


class LogTool(discord.ui.View):
    def __init__(self, ctx: discord.ext.commands.Context, logs_channel: discord.TextChannel, team: str, timestamp: datetime.datetime, uuid_no: uuid.UUID, task_id: int = None) -> None:
        """
        LogTool Constructor
        param ctx: Discord Context instance
        param logs_channel: Discord TextChannel
        param multi: bool - multiple submissions
        param team: str - bingo team name
        param timestamp: timestamp of submission
        param uuid_no: UUID number of submission
        param task_id: int - optional, bingo task number
        return: None
        """
        super().__init__(timeout=None)
        self.logger = Functions.create_logger('tools')
        self.ctx = ctx
        self.logs_channel = logs_channel
        self.team = team
        self.task_id = task_id
        self.timestamp = timestamp
        self.uuid_no = uuid_no
        self.message = None

    async def create_log_embed(self) -> None:
        """
        Creates and posts submission log embed.
        return: None
        """

        log_embed = discord.Embed(title='Submission Received', color=0xFFFF00)
        log_embed.set_author(name='Link to Submission', url=self.ctx.message.jump_url)

        log_embed.add_field(name='Team', value=self.team, inline=True)
        log_embed.add_field(name='Player', value=self.ctx.author.display_name, inline=True)
        log_embed.add_field(name='', value='', inline=True)
        log_embed.add_field(name='Task', value=f'{Constants.TASK_DESCRIPTION_MAP.get(self.task_id) if self.task_id else "Bonus"}')
        log_embed.add_field(name='Submitted on', value=self.timestamp, inline=True)
        log_embed.add_field(name='', value='', inline=True)
        log_embed.set_footer(text=self.uuid_no)

        self.message = await self.logs_channel.send(embed=log_embed, view=self)
        self.logger.info('create_log_embed finished.')
