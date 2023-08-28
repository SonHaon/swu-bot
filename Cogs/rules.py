import asyncio
from datetime import datetime
import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import locale_str as _t
from discord.ui import *
import random
import os
from io import BytesIO
from PIL import Image,ImageFont,ImageDraw,ImageOps
import logging

from .button import button_rules
from .checks import check

class rules(commands.GroupCog,name=_t(
            "rules",
            fr="règles",
            en="rules"
        )):
    def __init__(self,bot:commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name=_t(
            "create",
            fr="créer",
            en="create"
        ),
        description=_t(
            "description",
            fr="créer le message de règle",
            en="create rule message"
        )
    )
    @check.is_admin()
    async def create(self,interaction:discord.Interaction,role:discord.Role):
        await interaction.response.defer(ephemeral=True)
        embed=discord.Embed(title="__**Règles**__",description="Bienvenue dans la section des règles de notre serveur discord,\nVoici les règles standards du serveur pour que tout le monde se plaise ici, merci de les accepter avec une petite :white_check_mark: \n\n- On est respectueux avec tout le monde, pas de trashtalk, on reste cool\n- Pas de propos racistes, homophobes ou n’importe quoi d’autre qui pourrait offenser \n- Pas d’image NSFW …\n- Si vous voulez partager dans les liens communautaires vos vidéos, blogs ou chaines, n'hésitez pas à @Conseil Jedi ou à nous envoyez un MP ! \n- Au moindre problème, n'hésitez pas à contacter un membre du staff.",colour=discord.Colour.dark_grey())
        embed.set_footer(text="Clique sur le bouton ✅ pour accéder à l'entièreté du serveur")
        embed.set_author(name=interaction.guild.name,icon_url=interaction.guild.icon.url)
        await interaction.channel.send(embed=embed,view=button_rules(role))
        await interaction.edit_original_response(content=f"le message de règles a bien été créé")
