import discord
from discord import app_commands

class check:
    def is_SonHaon():
        def predicate(interaction: discord.Interaction) -> bool:
            return interaction.user.id == 707200529738235925
        return app_commands.check(predicate)