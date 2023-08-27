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
from .fonction import recup_card, fields
from .button import buttons_card
from requests import get
import json
import time


class card(commands.Cog): 
    def __init__(self,bot:commands.Bot) -> None: 
        self.bot = bot 
        super().__init__()

    groupe=app_commands.Group(name=_t("card",fr="carte",en="card"),description="...")

    @groupe.command(
        name=_t(
            "info",
            fr="info",
            en="info"
        ),
        description=_t(
            "description",
            fr="recherche une carte avec l'id et affiche les infos",
            en="search a card with id and show informations"
        )
    )
    @app_commands.choices(set=[
        app_commands.Choice(name="SOR (Spark of Rebellion)",value="sor")
        ]
    )
    async def info(self,interaction:discord.Interaction,number:int,set:str="sor"):
        await interaction.response.defer(ephemeral=False)
        card=recup_card(set,number)
        try:
            if card["message"]=="Internal server error":
                await interaction.edit_original_response(content="Cette carte n'existe pas ou n'est pas dans la base de donnée")
                time.sleep(2)
                await interaction.delete_original_response()
                return
        except:
            pass
        embed=discord.Embed(title=f"{card['Name']}")
        embed.set_author(name=interaction.user.display_name,icon_url=interaction.user.display_avatar)
        embed=fields(embed,card)
        await interaction.edit_original_response(embeds=[embed],view=buttons_card("info",card["Set"],card["Number"],self.bot.trad))

    @app_commands.command(
        name=_t(
            "card2",
            fr="carte",
            en="card"
        ),
        description=_t(
            "description",
            fr="recherche une carte avec l'id et affiche l'image",
            en="search a card with id and show image"
        )
    )
    @app_commands.choices(set=[
        app_commands.Choice(name="SOR (Spark of Rebellion)",value="sor")
        ]
    )
    async def carte(self,interaction:discord.Interaction,number:int,set:str="sor"):
        await interaction.response.defer(ephemeral=False)
        card=recup_card(set,number)
        try:
            if card["message"]=="Internal server error":
                await interaction.edit_original_response(content="Cette carte n'existe pas ou n'est pas dans la base de donnée")
                time.sleep(2)
                await interaction.delete_original_response()
                return
        except:
            pass
        embed=discord.Embed(title=f"{card['Name']}")
        embed.set_author(name=interaction.user.display_name,icon_url=interaction.user.display_avatar)
        embed.set_image(url=card["FrontArt"])
        if "BackArt" in card:
            embed_image=discord.Embed().set_image(url=card["BackArt"])
            await interaction.edit_original_response(embeds=[embed,embed_image],view=buttons_card("image",card["Set"],card["Number"],self.bot.trad))
        else:
            await interaction.edit_original_response(embeds=[embed],view=buttons_card("image",card["Set"],card["Number"],self.bot.trad))