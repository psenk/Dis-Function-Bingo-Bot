import datetime
import discord
import discord.ext
import discord.ext.commands
import Util
import uuid


class LogTool(discord.ui.View):
    
    def __init__(self):
        super().__init__(timeout=None)
        
        
async def create_log_embed(ctx: discord.ext.commands.Context, logs_channel: discord.TextChannel, multi: bool, team: str, task_id: int, timestamp: datetime.datetime, uuid_no: uuid.UUID):
    if multi:
        log_embed = discord.Embed(title="Dis Function's Bingo Bonanza", color=0x0000FF)
        log_embed.set_author(name=f"Submission Received (multiple images)", url=ctx.message.jump_url)
    else:
        log_embed = discord.Embed(title="Dis Function's Bingo Bonanza", color=0x0000FF)
        log_embed.set_author(name=f"Submission Received", url=ctx.message.jump_url)
        
    #log_embed(name="Submission Link", url=ctx.message.jump_url)
    log_embed.set_thumbnail(url=ctx.message.attachments[0].url)
    log_embed.set_footer(text=uuid_no)
    log_embed.add_field(name="Team:", value=team, inline=True)
    log_embed.add_field(name="", value="", inline=True)
    log_embed.add_field(name="Player:", value=ctx.author.display_name, inline=True)
    log_embed.add_field(name="Task:", value=Util.task_number_dict.get(task_id)) # ! LIVE CODE CHANGE FOR PUBLIC TESTING
    #log_embed.add_field(name="Task:", value=Util.task_number_dict.get(999), inline=True)
    log_embed.add_field(name="", value="", inline=True)
    log_embed.add_field(name="Submitted on:", value=timestamp, inline=True)
    
    # Buttons
    class ApproveButtons(discord.ui.View):

        @discord.ui.button(label="Approve", style=discord.ButtonStyle.green)
        async def approve_button(
            self, interaction: discord.Interaction, button: discord.ui.Button
        ) -> None:
            await ctx.send(f"Submission for Task #{task_id}: {Util.task_number_dict.get(task_id)} approved!")
            await message.add_reaction("✅")
            await ctx.message.add_reaction("✅")
            # send logs
            await interaction.response.edit_message(view=None)

        @discord.ui.button(label="Reject", style=discord.ButtonStyle.red)
        async def reject_button(
            self, interaction: discord.Interaction, button: discord.ui.Button
        ) -> None:
            await ctx.send(f"Submission for Task #{task_id}: {Util.task_number_dict.get(task_id)} rejected!")
            await message.add_reaction("❌")
            await ctx.message.add_reaction("❌")
            await interaction.response.edit_message(view=None)
    
    message = await logs_channel.send(embed=log_embed, view=ApproveButtons())