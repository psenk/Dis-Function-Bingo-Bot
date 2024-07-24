import datetime
import discord

import discord.ext
import discord.ext.commands

from QueryTool import QueryTool
from SheetsTool import SheetsTool
import Util

# GUILD_ID = 741153043776667658 # ! LIVE CODE
TEST_GUILD_ID = 969399636995493899
TEST_SUBMISSION_CHANNEL = {
    "Test Bingo Team": 986537383250001940, 
    "Starship Enterprise": 986537383250001940, 
    "Cheese Cape": 986537383250001940,
    "Sasa Loves Bingo": 986537383250001940,
    "Drunk Chinchompa": 986537383250001940,
    }


class ApproveTool(discord.ui.View):
    def __init__(self, ctx: discord.ext.commands.Context, bot: discord.ext.commands.Bot):
        """
        param: Discord Context object
        description: ApprovalTool Constructor
        return: None
        """
        super().__init__(timeout=None)
        self.ctx = ctx
        self.bot = bot
        # submission_id, task_id, player, team, uuid_no, jump_url, message_id, date_submitted
        self.submissions = []
        self.page = 0

    async def create_approve_embed(self) -> None:
        """
        description: Creates initial embed
        return: None
        """
        self.submissions = await QueryTool.get_submissions()
        if len(self.submissions) == 0:
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
        approve_tool = discord.Embed(
            title=f"Submission Approval Tool",
            color=0x0000FF,
            description=f"ID # {submission.get('uuid')[:8]}",
        )
        approve_tool.add_field(
            name="Submission:",
            value=f"[HERE]({submission.get('jump_url')})",
            inline=True,
        )
        approve_tool.add_field(name="Player:", value=f"{submission.get('player')}", inline=True)
        approve_tool.add_field(name="", value="", inline=True)
        approve_tool.add_field(name="Team:", value=f"{submission.get('team')}", inline=True)
        approve_tool.add_field(
            name="Date Submitted:",
            value=f"{submission.get('date_submitted').strftime('%Y-%m-%d at %H:%M:%S')}",
            inline=True,
        )
        approve_tool.add_field(name="", value="", inline=True)
        approve_tool.add_field(name="Task ID:", value=f"{submission.get('task_id')}", inline=True)
        approve_tool.add_field(name="Task:", value=f"{Util.task_number_dict[submission.get('task_id')]}", inline=True)
        approve_tool.add_field(name="", value="", inline=True)

        return approve_tool

    def update_buttons(self) -> None:
        """
        description: Updates button states
        return: None
        """
        # left_button, approve_button, reject_button, right_button = ApproveTool.buttons[0], ApproveTool.buttons[1], ApproveTool.buttons[2], ApproveTool.buttons[3]
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
        await interaction.followup.edit_message(embed=new_embed, view=self, message_id=interaction.message.id)

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green, custom_id="approve_task")
    async def approve_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        submission = self.submissions[self.page]
        task_id = submission.get("task_id")
        await interaction.response.defer()
        await self.ctx.send(f"Submission for Task #{task_id}: {Util.task_number_dict.get(task_id)} has been approved!")
        msg = await ApproveTool.get_message(self.bot, submission.get("message_id"), submission.get("team"))
        await msg.add_reaction("✅")
        self.submissions.pop(self.page)
        if self.page >= len(self.submissions):
            self.page -= 1
        self.update_buttons()
        await QueryTool.delete_submission(task_id, submission.get("team"))
        sheets_tool = SheetsTool(submission.get("team"), submission.get("date_submitted"), submission.get("player"), submission.get("task_id"))
        sheets_tool.update_sheets()
        if self.submissions:
            new_embed = await self.populate_embed()
            await interaction.followup.edit_message(embed=new_embed, view=self, message_id=interaction.message.id)
        else:
            await interaction.followup.edit_message(content="No more submissions to review.", embed=None, view=None, message_id=interaction.message.id)

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.red, custom_id="reject_task")
    async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        submission = self.submissions[self.page]
        task_id = submission.get("task_id")
        await interaction.response.defer()
        await self.ctx.send(f"Submission for Task #{task_id}: {Util.task_number_dict.get(task_id)} has been rejected.")
        msg = await ApproveTool.get_message(self.bot, submission.get("message_id"), submission.get("team"))
        await msg.add_reaction("❌")
        self.submissions.pop(self.page)
        if self.page >= len(self.submissions):
            self.page -= 1
        self.update_buttons()
        await QueryTool.delete_submission(task_id, submission.get("team"))
        if self.submissions:
            new_embed = await self.populate_embed()
            await interaction.followup.edit_message(embed=new_embed, view=self)
        else:
            await interaction.followup.edit_message(content="No more submissions to review.", embed=None, view=None)

    @discord.ui.button(label=">", style=discord.ButtonStyle.blurple, custom_id="right_task")
    async def right_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        self.page += 1
        new_embed = await self.populate_embed()
        self.update_buttons()
        await interaction.followup.edit_message(embed=new_embed, view=self, message_id=interaction.message.id)

    async def get_message(bot: discord.ext.commands.Bot, message_id: int, team: str) -> discord.Message:
        """
        param: Discord Bot object
        param int: Discord message id
        param str: Bingo team name
        description: retrieves specific message from team channel
        return: Discord Message object
        """
        guild = bot.get_guild(TEST_GUILD_ID)
        ch = guild.get_channel(TEST_SUBMISSION_CHANNEL.get(team))
        msg = await ch.fetch_message(message_id)
        return msg
