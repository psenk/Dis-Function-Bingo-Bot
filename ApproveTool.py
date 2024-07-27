import discord

import discord.ext
import discord.ext.commands

from QueryTool import QueryTool
from SheetsTool import SheetsTool
import Util

# GUILD_ID = 741153043776667658 # ! LIVE CODE


class ApproveTool(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, bot: discord.ext.commands.Bot) -> None:
        """
        ApproveTool Constructor
        param interaction: Discord Interaction instance
        param bot: Discord Bot instance
        return: None
        """
        super().__init__(timeout=None)
        # submission_id, task_id, player, team, uuid_no, jump_url, message_id, date_submitted, purple
        self.submissions = []
        self.interaction = interaction
        self.message = None
        self.bot = bot
        self.page = 0
        self.purple = None
        self.uuid = None

    async def create_approve_embed(self) -> None:
        """
        Creates initial approve tool embed.
        return: None
        """
        async with QueryTool() as query_tool:
            self.submissions = await query_tool.get_submissions()
        if not self.submissions:
            await self.interaction.response.send_message("There are no submissions to approve at this time.")
            return
        else:
            approve_tool = await self.populate_embed()
            self.update_buttons()
            self.message = await self.interaction.response.send_message(embed=approve_tool, view=self)

    async def populate_embed(self) -> discord.Embed:
        """
        Updates approve tool embed with new data.
        return: Discord Embed instance
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

    @discord.ui.button(label="<", style=discord.ButtonStyle.blurple, custom_id="left_task")
    async def left_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        await self.next_page(interaction, right=False)

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green, custom_id="approve_task")
    async def approve_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        submission = self.submissions[self.page]
        task_id = submission["task_id"]
        sheets_tool = SheetsTool(submission["team"], submission["date_submitted"], submission["player"], submission["task_id"], self.purple if task_id == 998 else None)
        if task_id == 998:
            await self.react_and_refresh(task_id, submission, bonus=True)
            sheets_tool.add_purple(submission["player"])
        else:
            await self.react_and_refresh(task_id, submission, approve=True)
            sheets_tool.update_sheets()

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.red, custom_id="reject_task")
    async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        submission = self.submissions[self.page]
        task_id = submission["task_id"]
        await self.react_and_refresh(task_id, submission)

    @discord.ui.button(label=">", style=discord.ButtonStyle.blurple, custom_id="right_task")
    async def right_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        await ApproveTool.next_page(self, interaction, True)

    def update_buttons(self) -> None:
        """
        Updates states of approve tool buttons.
        return: None
        """
        self.left_button.disabled = self.page == 0
        self.right_button.disabled = self.page == len(self.submissions) - 1
        self.approve_button.disabled = len(self.submissions) == 0
        self.reject_button.disabled = len(self.submissions) == 0

    async def get_message(self, message_id: int, team: str) -> discord.Message:
        """
        Retrieves a specific message from teams bingo channel.
        param message_id: int - id of desired message
        param team: str - bingo team name
        return: Discord Message instance
        """

        ch = self.bot.get_channel(Util.TEST_SUBMISSION_CHANNELS.get(team))
        msg = await ch.fetch_message(message_id)
        return msg

    async def react_and_refresh(self, task_id: int, submission: list, bonus: bool = False, approve: bool = False) -> None:
        """
        Button event.  Reacts to submission with emoji, sends message to team submission channel.  Refreshes self.
        param task_id: int - bingo task number
        param submission: list - submission receiving reaction
        param bonus: bool - is it a bonus submission?  default to False # ! TODO: UPDATE THIS AFTER BONUS COMMAND WORK DONE
        param approve: bool - approve submission?  default to False (reject)
        return: None
        """
        if bonus:
            await self.interaction.channel.send(f"{submission['purple']} bonus submission has been approved!")
            return
        else:
            await self.interaction.channel.send(f"Submission for Task #{task_id}: [{Util.TASK_NUMBER_DICT.get(task_id)}]({submission['jump_url']}) has been **{'approved' if approve else 'rejected'}**!")
            msg = await self.get_message(submission["message_id"], submission["team"])
            await msg.add_reaction(f"{'✅' if approve else '❌'}")
            await msg.channel.send(f"Submission for Task #{task_id}: [{Util.TASK_NUMBER_DICT.get(task_id)}]({submission['jump_url']}) has been **{'approved' if approve else 'rejected'}**!")
        await self.refresh()

    async def refresh(self) -> None:
        """
        Deletes current submission, updates buttons, refreshes embed tool data.
        return: None
        """
        self.submissions.pop(self.page)
        if self.page >= len(self.submissions):
            self.page -= 1
        self.update_buttons()
        async with QueryTool() as query_tool:
            await query_tool.delete_submission(str(self.uuid))
        if self.submissions:
            new_embed = await self.populate_embed()
            await self.interaction.edit_original_response(embed=new_embed, view=self)
        else:
            await self.interaction.edit_original_response(content="No more submissions to review.", embed=None, view=None)

    async def next_page(self, interaction: discord.Interaction, right: bool = False) -> None:
        """
        Pages submissions left or right.
        param interaction: Discord Interaction instance
        param right: bool - are we turning right?  default False (left)
        return: None
        """
        self.page = (self.page + 1) if right else (self.page - 1)
        new_embed = await self.populate_embed()
        self.update_buttons()
        await interaction.message.edit(embed=new_embed, view=self)
