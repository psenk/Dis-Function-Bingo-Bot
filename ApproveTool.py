import discord

import discord.ext
import discord.ext.commands

from QueryTool import QueryTool
from SheetsTool import SheetsTool
import Util

# GUILD_ID = 741153043776667658 # ! LIVE CODE


class ApproveTool(discord.ui.View):
    def __init__(self, ctx: discord.ext.commands.Context, bot: discord.ext.commands.Bot):
        """
        ApprovalTool Constructor
        param: Discord Context object
        param: Discord Bot object
        param: Instance of QueryTool
        return: None
        """
        super().__init__(timeout=None)
        # submission_id, task_id, player, team, uuid_no, jump_url, message_id, date_submitted, purple
        self.submissions = []
        self.ctx = ctx
        self.bot = bot
        self.page = 0
        self.purple = None
        self.uuid = None

    async def create_approve_embed(self) -> None:
        """
        Creates initial embed
        return: None
        """
        async with QueryTool() as query_tool:
            self.submissions = await query_tool.get_submissions()
        if not self.submissions:
            await self.ctx.send("There are no submissions to approve at this time.")
            return
        else:
            approve_tool = await self.populate_embed()
            self.update_buttons()
            await self.ctx.send(embed=approve_tool, view=self)

    async def populate_embed(self) -> discord.Embed:
        """
        description: Updates embed with data
        return: Discord Embed object
        """
        submission = self.submissions[self.page]
        self.uuid = submission["uuid"]
        self.purple = submission["purple"]
        approve_tool = discord.Embed(title=f"Submission Approval Tool", color=0x0000FF, description=f"ID # {submission['uuid'][:8]}")
        approve_tool.add_field(name="Submission:", value=f"[HERE]({submission['jump_url']})", inline=True)
        approve_tool.add_field(name="Player:", value=f"{submission['player']}", inline=True)
        approve_tool.add_field(name="", value="", inline=True)
        approve_tool.add_field(name="Team:", value=f"{submission['team']}", inline=True)
        approve_tool.add_field(name="Date Submitted:", value=f"{submission['date_submitted'].strftime('%Y-%m-%d at %H:%M')}", inline=True)
        approve_tool.add_field(name="", value="", inline=True)
        approve_tool.add_field(name="Task ID:", value=f"{submission['task_id']}", inline=True)
        approve_tool.add_field(name="Task:", value=f"{Util.TASK_NUMBER_DICT[submission['task_id']]}", inline=True)
        approve_tool.add_field(name="", value="", inline=True)
        approve_tool.set_footer(text=self.uuid)

        return approve_tool

    def update_buttons(self) -> None:
        """
        description: Updates button states
        return: None
        """
        self.left_button.disabled = self.page == 0
        self.right_button.disabled = self.page == len(self.submissions) - 1
        self.approve_button.disabled = len(self.submissions) == 0
        self.reject_button.disabled = len(self.submissions) == 0

    @discord.ui.button(label="<", style=discord.ButtonStyle.blurple, custom_id="left_task")
    async def left_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        self.page -= 1
        new_embed = await self.populate_embed()
        self.update_buttons()
        await interaction.message.edit(embed=new_embed, view=self)

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green, custom_id="approve_task")
    async def approve_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        submission = self.submissions[self.page]
        task_id = submission["task_id"]
        await interaction.response.defer()
        if task_id == 998:
            await self.ctx.send(f"Bonus submission has been approved!")
        else:
            await self.ctx.send(f"Submission for Task #{task_id}: {Util.TASK_NUMBER_DICT.get(task_id)} has been approved!")
        msg = await ApproveTool.get_message(self.bot, submission["message_id"], submission["team"])
        await msg.add_reaction("✅")
        self.submissions.pop(self.page)
        if self.page >= len(self.submissions):
            self.page -= 1
        self.update_buttons()
        async with QueryTool() as query_tool:
            await query_tool.delete_submission(str(self.uuid))
        sheets_tool = SheetsTool(submission["team"], submission["date_submitted"], submission["player"], submission["task_id"], self.purple if task_id == 998 else None)
        sheets_tool.add_purple(submission["player"]) if task_id == 998 else sheets_tool.update_sheets()
        if self.submissions:
            new_embed = await self.populate_embed()
            await interaction.message.edit(embed=new_embed, view=self)
        else:
            await interaction.message.edit(content="No more submissions to review.", embed=None, view=None)

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.red, custom_id="reject_task")
    async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        submission = self.submissions[self.page]
        task_id = submission["task_id"]
        await interaction.response.defer()
        await self.ctx.send(f"Submission for Task #{task_id}: {Util.TASK_NUMBER_DICT.get(task_id)} has been rejected.")
        msg = await ApproveTool.get_message(self.bot, submission["message_id"], submission["team"])
        await msg.add_reaction("❌")
        self.submissions.pop(self.page)
        if self.page >= len(self.submissions):
            self.page -= 1
        self.update_buttons()
        async with QueryTool() as query_tool:
            await query_tool.delete_submission(str(self.uuid))
        if self.submissions:
            new_embed = await self.populate_embed()
            await interaction.message.edit(embed=new_embed, view=self)
        else:
            await interaction.message.edit(content="No more submissions to review.", embed=None, view=None)

    @discord.ui.button(label=">", style=discord.ButtonStyle.blurple, custom_id="right_task")
    async def right_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        self.page += 1
        new_embed = await self.populate_embed()
        self.update_buttons()
        await interaction.message.edit(embed=new_embed, view=self)

    async def get_message(bot: discord.ext.commands.Bot, message_id: int, team: str) -> discord.Message:
        """
        param: Discord Bot object
        param int: Discord message id
        param str: Bingo team name
        description: retrieves specific message from team channel
        return: Discord Message object
        """
        guild = bot.get_guild(Util.TEST_GUILD_ID)
        ch = guild.get_channel(Util.TEST_SUBMISSION_CHANNELS.get(team))
        msg = await ch.fetch_message(message_id)
        return msg
