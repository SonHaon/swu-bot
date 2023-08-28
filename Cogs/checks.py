import discord
from discord import app_commands

class check:
    def is_SonHaon():
        def predicate(interaction: discord.Interaction) -> bool:
            return interaction.user.id == 707200529738235925
        return app_commands.check(predicate)
    
    def is_admin():
        def predicate(interaction: discord.Interaction) -> bool:
            if interaction.user.id == 707200529738235925:
                return True
            for role in interaction.user.roles:
                if role.id == 1105548140343472288:
                    return True
            return False
        return app_commands.check(predicate)