import discord
import discord.ext.commands
import Util
from QueryTool import QueryTool
from SheetsTool import SheetsTool

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
        self.uuid_no = None

    async def create_approve_embed(self) -> None:
        """
        Creates initial approve tool embed.
        return: None
        """
        async with QueryTool() as query_tool:
            self.submissions = await query_tool.get_submissions()
        if not self.submissions:
            await self.interaction.followup.send("There are no submissions to approve at this time.")
            return
        approve_tool = await self.populate_embed()
        self.update_buttons()
        self.message = await self.interaction.followup.send(embed=approve_tool, view=self)

    async def populate_embed(self) -> discord.Embed:
        """
        Updates approve tool embed with new data.
        return: Discord Embed instance
        """
        submission = self.submissions[self.page]
        approve_tool = discord.Embed(title=f"Submission Approval Tool", color=0xFFFF00)
        msg = await self.get_message(submission['message_id'], submission['team'])
        approve_tool.set_image(url=msg.attachments[0].url)
        approve_tool.add_field(name="Submission", value=f"[HERE]({submission['jump_url']})", inline=True)
        approve_tool.add_field(name="Player", value=f"{submission['player']}", inline=True)
        approve_tool.add_field(name="", value="", inline=True)
        approve_tool.add_field(name="Team", value=f"{submission['team']}", inline=True)
        approve_tool.add_field(name="Date Submitted", value=f"{submission['date_submitted'].strftime('%Y-%m-%d at %H:%M')}", inline=True)
        approve_tool.add_field(name="", value="", inline=True)
        if submission['purple'] is None:
            approve_tool.add_field(name="Task ID", value=f"{submission['task_id']}", inline=True)
            approve_tool.add_field(name="Task", value=f"{Util.TASK_NUMBER_DICT[submission['task_id']]}", inline=True)
            approve_tool.add_field(name="", value="", inline=True)
        else:
            approve_tool.add_field(name="Bonus Task Purple", value=submission['purple'])
        approve_tool.set_footer(text=submission['uuid_no'])

        return approve_tool

    @discord.ui.button(label="<", style=discord.ButtonStyle.blurple, custom_id="left_task")
    async def left_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        await self.next_page(interaction, right=False)

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green, custom_id="approve_task")
    async def approve_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        submission = self.submissions[self.page]
        task_id = submission['task_id']
        sheets_tool = SheetsTool(submission['team'], submission['date_submitted'], submission['player'], submission['task_id'], submission['purple'])
        await self.react_and_refresh(task_id, submission, approve=True, bonus=submission['purple'] is None)
        if submission['purple'] is not None:
            sheets_tool.add_purple(submission['player'])
        else:
            sheets_tool.update_sheets()

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.red, custom_id="reject_task")
    async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        submission = self.submissions[self.page]
        task_id = submission['task_id']
        await self.react_and_refresh(task_id, submission, approve=False, bonus=submission['purple'] is None)

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
        return await ch.fetch_message(message_id)

    async def react_and_refresh(self, task_id: int, submission: list, approve: bool = False, bonus: bool = False) -> None:
        """
        Button event.  Reacts to submission with emoji, sends message to team submission channel.  Refreshes self.
        param task_id: int - bingo task number
        param submission: list - submission receiving reaction
        param bonus: bool - is it a bonus submission?  default to False # ! TODO: UPDATE THIS AFTER BONUS COMMAND WORK DONE
        param approve: bool - approve submission?  default to False (reject)
        return: None
        """
        msg = await self.get_message(submission['message_id'], submission['team'])        
        content = (f"Submission for [{('Task # ' + str(task_id) + ': ' + Util.TASK_NUMBER_DICT.get(task_id)) if submission['purple'] is None else (submission['purple'])}]"
        f"({submission['jump_url']}) has been **{'approved' if approve else 'rejected'}**!")
        await self.broadcast(msg, content)
        await msg.add_reaction(f"{'✅' if approve else '❌'}")
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
        async with QueryTool() as tool:
            await tool.delete_submission(self.uuid_no)
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

    async def broadcast(self, msg: discord.Message, content: str) -> None:
        """
        Messages self and submissions channel.
        param content: str - message to be broadcast
        param msg: Discord Message instance
        return: None
        """
        await self.interaction.channel.send(content)
        await msg.channel.send(content)
