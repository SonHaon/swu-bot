import asyncio
from pathlib import Path
import discord
from discord.ext import commands
from discord import app_commands, Locale
from discord.ui import *
import random
import os
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image,ImageFont,ImageDraw,ImageOps
import logging
import logging.handlers
import deepl
from discord.app_commands import Translator, locale_str, TranslationContext, TranslationContextLocation
from Cogs_sommaire import *
from Cogs.button import buttons_card

load_dotenv(".env")
TOKEN = os.getenv("TOKEN")
guild = discord.Object(id=1105547376690745426)
guild_test = discord.Object(id=916617095876337664)
translator = deepl.Translator("b2f44de3-fa00-9598-36ba-effea8104e2b:fx") 

class MyTranslator(Translator):
    async def translate(
        self,
        string: locale_str,
        locale: Locale,
        context: TranslationContext
        ):
#        if context!= None:
#            print(str(context.location).removeprefix("TranslationContextLocation."), string.extras)
#        else:
#            print(string.extras)
        if locale is Locale.french:
            try:
                return string.extras["fr"]
            except:
                return None
        else:
            try:
                return string.extras["en"]
            except:
                return None
        return None 
    

class bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(intents = intents,command_prefix="%µ¨£%£µ%",help_command=None)
        
    async def setup_hook(self):
        self.trad=translator
        # set le traducteur
        await self.tree.set_translator(MyTranslator())
        # commande
        await self.add_cog(ping(self),guilds=[guild,guild_test])
        await self.add_cog(card(self),guild=guild)
        await self.add_cog(reboot(self),guilds=[guild,guild_test])
        await self.add_cog(member_join(self),guild=guild)

        await self.tree.sync(guild=guild)
        await self.tree.sync()


    async def on_ready(self):
        await self.wait_until_ready()
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.custom,name="essaie /carte"))

SonHaon_Bot = bot()
tree = SonHaon_Bot.tree

@tree.error
async def on_app_command_error(interaction:discord.Interaction,error):
    if isinstance(error,app_commands.BotMissingPermissions):
        try:
            await interaction.response.send_message(content="je n'ai pas les permissions de faire ça",ephemeral=True)
        except:
            await interaction.edit_original_response(content="je n'ai pas les permissions de faire ça")
    elif isinstance(error, app_commands.MissingPermissions or app_commands.MissingRole or app_commands.MissingAnyRole):
        try:
            await interaction.response.send_message(content="vous ne pouvez pas faire ça",ephemeral=True)
        except:
            await interaction.edit_original_response(content="vous ne pouvez pas faire ça")
    elif isinstance(error,app_commands.CheckFailure):
        try:
            await interaction.response.send_message(content="vous ne pouvez pas faire ça",ephemeral=True)
        except:
            await interaction.edit_original_response(content="vous ne pouvez pas faire ça")
    else:
        embed=discord.Embed(title="Une erreur inattendue est survenue",description=f"""```{error}```""")
        try:
            await interaction.response.send_message(embed=embed,ephemeral=True)
        except:
            await interaction.edit_original_response(embed=embed)
        raise error


SonHaon_Bot.run(TOKEN)