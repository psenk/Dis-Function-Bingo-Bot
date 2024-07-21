import discord

import discord.ext
import discord.ext.commands

from QueryTool import QueryTool


class ApproveTool(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    async def create_approve_embed(ctx: discord.ext.commands.Context) -> None:
        # submission_id, task_id, player, team, jump_url, message_id, date_submitted
        submissions = await QueryTool.get_submissions()
        i = 0
        approve_tool = discord.Embed(title=f"Submission Approval Tool", color=0x0000FF, description="pee pee poo poo my name is blepe")
        approve_tool.add_field(name="Submission:", value=f"[HERE]({submissions[i].get('jump_url')})", inline=True)
        approve_tool.add_field(name="Player:", value=f"{submissions[i].get('player')}", inline=True)
        approve_tool.add_field(name="", value="", inline=True)
        approve_tool.add_field(name="Team:", value=f"{submissions[i].get('team')}", inline=True)
        approve_tool.add_field(name="Date Submitted:", value=f"{submissions[i].get('date_submitted')}", inline=True)
        approve_tool.add_field(name="", value="", inline=True)

        class ApprovalButtons(discord.ui.View):

            @discord.ui.button(label="<", style=discord.ButtonStyle.blurple)
            async def left_button(
                self, interaction: discord.Interaction, button: discord.ui.Button
            ) -> None:
                await interaction.response.defer()

            @discord.ui.button(label="Approve", style=discord.ButtonStyle.green)
            async def approve_button(
                self, interaction: discord.Interaction, button: discord.ui.Button
            ) -> None:
                await interaction.response.defer()

            @discord.ui.button(label="Reject", style=discord.ButtonStyle.red)
            async def reject_button(
                self, interaction: discord.Interaction, button: discord.ui.Button
            ) -> None:
                await interaction.response.defer()

            @discord.ui.button(label=">", style=discord.ButtonStyle.blurple)
            async def right_button(
                self, interaction: discord.Interaction, button: discord.ui.Button
            ) -> None:
                await interaction.response.defer()

        message = await ctx.send(embed=approve_tool, view=ApprovalButtons())

    async def update_buttons(self, data):
        if len(data) == 0:
            self.prev_button.disabled = True
            self.submit_button.disabled = True
            self.deny_button.disabled = True
            self.next_button.disabled = True
        elif len(data) == 1:
            self.prev_button.disabled = True
            self.next_button.disabled = True
        elif self.current_page == 1:
            self.prev_button.disabled = True
            self.next_button.disabled = False
        elif self.current_page == len(data):
            self.next_button.disabled = True
            self.prev_button.disabled = False
        else:
            self.prev_button.disabled = False
            self.submit_button.disabled = False
            self.deny_button.disabled = False
            self.next_button.disabled = False