import discord

import discord.ext
import discord.ext.commands

from QueryTool import QueryTool
import Util


class ApproveTool(discord.ui.View):
    def __init__(self, ctx: discord.ext.commands.Context):
        super().__init__(timeout=None)
        self.ctx = ctx
        # submission_id, task_id, player, team, uuid_no, jump_url, message_id, date_submitted
        self.submissons = []
        self.page = 0

    async def create_approve_embed(self) -> None:
        self.submissions = await QueryTool.get_submissions()
        if len(self.submissions) == 0:
            self.ctx.send("There are no submissions to approve at this time.")
            return
        else:
            approve_tool = await self.populate_embed()
            self.update_buttons()
            await self.ctx.send(embed=approve_tool, view=self)

    async def populate_embed(self) -> discord.Embed:
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
            value=f"{submission.get('date_submitted')}",
            inline=True,
        )
        approve_tool.add_field(name="", value="", inline=True)

        return approve_tool

    def update_buttons(self) -> None:
        # left_button, approve_button, reject_button, right_button = ApproveTool.buttons[0], ApproveTool.buttons[1], ApproveTool.buttons[2], ApproveTool.buttons[3]
        self.left_button.disabled = self.page == 0
        self.right_button.disabled = self.page == len(self.submissions) - 1
        self.approve_button.disabled = len(self.submissions) == 0
        self.reject_button.disabled = len(self.submissions) == 0

    @discord.ui.button(label="<", style=discord.ButtonStyle.blurple, custom_id="left_task")
    async def left_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.page -= 1
        new_embed = await self.populate_embed()
        self.update_buttons()
        await interaction.response.edit_message(embed=new_embed, view=self)

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green, custom_id="approve_task")
    async def approve_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        submission = self.submissions[self.page]
        task_id = submission.get("task_id")
        await self.ctx.send(f"Submission for Task #{task_id}: {Util.task_number_dict.get(task_id)} has been approved!")
        await self.ctx.fetch_message(submission.get("message_id")).add_reaction("✅")
        self.submissions.pop(self.page)
        if self.page >= len(self.submissions):
            self.page -= 1
        if self.submissions:
            new_embed = await self.populate_embed()
        self.update_buttons()
        # ! TODO: delete from submissions
        if new_embed:
            await interaction.response.edit_message(embed=new_embed, view=self)
        else:
            await interaction.response.edit_message(content="No more submissions to review.", embed=None, view=None)
    @discord.ui.button(label="Reject", style=discord.ButtonStyle.red, custom_id="reject_task")
    async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        submission = self.submissions[self.page]
        task_id = submission.get("task_id")
        await self.ctx.send(f"Submission for Task #{task_id}: {Util.task_number_dict.get(task_id)} has been rejected.")
        await self.ctx.fetch_message(submission.get("message_id")).add_reaction("❌")
        self.submissions.pop(self.page)
        if self.page >= len(self.submissions):
            self.page -= 1
        if self.submissions:
            new_embed = await self.populate_embed()
        self.update_buttons()
        # ! TODO: delete from submissions
        if new_embed:
            await interaction.response.edit_message(embed=new_embed, view=self)
        else:
            await interaction.response.edit_message(content="No more submissions to review.", embed=None, view=None)

    @discord.ui.button(label=">", style=discord.ButtonStyle.blurple, custom_id="right_task")
    async def right_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.page += 1
        new_embed = await self.populate_embed()
        self.update_buttons()
        await interaction.response.edit_message(embed=new_embed, view=self)
