import os
import discord
from discord import app_commands
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN environment variable is missing.")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s).")
    except Exception as error:
        print(f"Command sync failed: {error}")
    print(f"Logged in as {bot.user} — nickname bot is online!")

@bot.tree.command(name="nick", description="Change a member's server nickname")
@app_commands.describe(member="Member whose nickname you want to change", nickname="New nickname")
@app_commands.checks.has_permissions(manage_nicknames=True)
async def nick(interaction: discord.Interaction, member: discord.Member, nickname: str):
    if len(nickname) > 32:
        await interaction.response.send_message(
            "Nickname must be 32 characters or fewer.", ephemeral=True
        )
        return
    try:
        await member.edit(nick=nickname, reason=f"Nickname changed by {interaction.user}")
        await interaction.response.send_message(
            f"✅ {member.mention}'s nickname changed to **{discord.utils.escape_markdown(nickname)}**."
        )
    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ I can't change that member's nickname. Check my Manage Nicknames permission and role position.",
            ephemeral=True
        )
    except discord.HTTPException:
        await interaction.response.send_message(
            "❌ Discord couldn't update that nickname. Please try again.", ephemeral=True
        )

@bot.tree.command(name="resetnick", description="Reset a member's server nickname")
@app_commands.describe(member="Member whose nickname you want to reset")
@app_commands.checks.has_permissions(manage_nicknames=True)
async def resetnick(interaction: discord.Interaction, member: discord.Member):
    try:
        await member.edit(nick=None, reason=f"Nickname reset by {interaction.user}")
        await interaction.response.send_message(
            f"✅ {member.mention}'s nickname has been reset."
        )
    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ I can't reset that member's nickname. Check my Manage Nicknames permission and role position.",
            ephemeral=True
        )
    except discord.HTTPException:
        await interaction.response.send_message(
            "❌ Discord couldn't reset that nickname. Please try again.", ephemeral=True
        )

@nick.error
@resetnick.error
async def nickname_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        message = "❌ You need the **Manage Nicknames** permission to use this command."
    else:
        message = "❌ Something went wrong while running that command."
    if interaction.response.is_done():
        await interaction.followup.send(message, ephemeral=True)
    else:
        await interaction.response.send_message(message, ephemeral=True)

bot.run(TOKEN)
