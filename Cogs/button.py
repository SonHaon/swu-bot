from typing import Any, Coroutine, Optional, Union
import discord
from discord import ButtonStyle, app_commands
import time
from discord.emoji import Emoji
from discord.enums import ButtonStyle

from discord.interactions import Interaction
from discord.partial_emoji import PartialEmoji
from discord.ui.item import Item
from .fonction import fields,recup_card,trad_card,fields_fr

embed_vide=discord.Embed(title="...")

class buttons_confirm(discord.ui.View):
    def __init__(self,message:discord.Message):
        self.message = message
        super().__init__(timeout=None)
    
    @discord.ui.button(
        style=ButtonStyle.gray,
        emoji="✅",
        custom_id="yes",
        row=0
    )
    async def yes(self,interaction:discord.Interaction,button:discord.ui.Button):
        await interaction.response.edit_message(content="le message est supprimé")
        await self.message.edit(embeds=[embed_vide])
        await interaction.delete_original_response()
        await self.message.delete()

    @discord.ui.button(
        style=ButtonStyle.gray,
        emoji="❌",
        custom_id="no",
        row=0
    )
    async def no(self,interaction:discord.Interaction,button:discord.ui.Button):
        await interaction.response.edit_message(content="Vous avez annulé la suppression")
        time.sleep(0.5)
        await interaction.delete_original_response()


class button_delete(discord.ui.Button):
    def __init__(self):
        super().__init__(style=ButtonStyle.red,label="supprimer",custom_id="delete")

    async def callback(self, interaction: Interaction) -> Any:
        await interaction.response.send_message("Voulez vous vraiment supprimer le message ?",ephemeral=True,view=buttons_confirm(interaction.message))
        
class button_image(discord.ui.Button):
    def __init__(self,view,set,number,trad):
        self.set=set
        self.number=number
        self.view2:discord.ui.View = view
        self.trad=trad
        super().__init__(style=ButtonStyle.blurple,label="Image",custom_id="image")

    async def callback(self, interaction: Interaction) -> Coroutine[Any, Any, Any]:
        await interaction.response.defer(ephemeral=True)
        embed=discord.Embed(title=interaction.message.embeds[0].title)
        card=recup_card(self.set,self.number)
        embed.set_image(url=card["FrontArt"])
        embed.set_author(name=interaction.message.embeds[0].author.name,icon_url=interaction.message.embeds[0].author.icon_url)
        self.view2.clear_items()
        self.view2.add_item(button_delete())
        self.view2.add_item(button_info(self.view2,self.set,self.number,self.trad))
        if "BackArt" in card:
            embed_image=discord.Embed().set_image(url=card["BackArt"])
            await interaction.message.edit(embeds=[embed,embed_image],view=self.view2)
        else:
            await interaction.message.edit(embeds=[embed],view=self.view2)

class button_info(discord.ui.Button):
    def __init__(self,view,set,number,trad):
        self.set=set
        self.number=number
        self.view2:discord.ui.View = view
        self.trad=trad
        super().__init__(style=ButtonStyle.blurple,label="Info",custom_id="info")

    async def callback(self, interaction: Interaction) -> Coroutine[Any, Any, Any]:
        await interaction.response.defer(ephemeral=True)
        embed=discord.Embed(title=interaction.message.embeds[0].title)
        card=recup_card(self.set,self.number)
        embed=fields(embed,card)
        embed.set_author(name=interaction.message.embeds[0].author.name,icon_url=interaction.message.embeds[0].author.icon_url)
        self.view2.clear_items()
        self.view2.add_item(button_delete())
        self.view2.add_item(button_image(self.view2,self.set,self.number,self.trad))
        self.view2.add_item(button_info_fr(self.view2,self.set,self.number,self.trad))
        await interaction.message.edit(embed=embed,view=self.view2)

class button_info_fr(discord.ui.Button):
    def __init__(self,view,set,number,trad):
        self.set=set
        self.number=number
        self.view2:discord.ui.View = view
        self.trad=trad
        super().__init__(style=ButtonStyle.blurple,label="Français",custom_id="français")

    async def callback(self, interaction: Interaction) -> Coroutine[Any, Any, Any]:
        await interaction.response.defer(ephemeral=True)
        embed=discord.Embed(title="<a:loading:1144766942100598855> Traduction en cours <a:loading:1144766942100598855>")
        await interaction.message.edit(embed=embed)
        embed=discord.Embed(title=interaction.message.embeds[0].title)
        card=trad_card(recup_card(self.set,self.number),self.trad)
        embed=fields_fr(embed,card,self.trad)
        embed.set_author(name=interaction.message.embeds[0].author.name,icon_url=interaction.message.embeds[0].author.icon_url)
        self.view2.clear_items()
        self.view2.add_item(button_delete())
        self.view2.add_item(button_image(self.view2,self.set,self.number,self.trad))
        self.view2.add_item(button_info(self.view2,self.set,self.number,self.trad))
        await interaction.message.edit(embed=embed,view=self.view2)

class buttons_switch(discord.ui.View):
    def __init__(self,):
        super().__init__(timeout=None)

    async def interaction_check(self, interaction: Interaction) -> Coroutine[Any, Any, bool]:
        if not interaction.message.embeds[0].author.name==interaction.user.display_name:
            raise
        else:
            return True
    async def on_error(self, interaction: Interaction, error: Exception, item: Item[Any]) -> None:
        await interaction.response.send_message(content="Désolé vous ne pouvez pas faire ça",ephemeral=True)
 
class buttons_card(discord.ui.View):
    def __init__(self,type,set,number,trad):
        super().__init__(timeout=None)
        self.add_item(button_delete())
        self.set=set
        self.number=number
        self.trad=trad
        if type=="image":
            self.add_item(button_info(self,set,number,trad))
        if type=="info":
            self.add_item(button_image(self,set,number,trad))
            self.add_item(button_info_fr(self,set,number,trad))

    async def interaction_check(self, interaction: Interaction) -> Coroutine[Any, Any, bool]:
        if not interaction.message.embeds[0].author.name==interaction.user.display_name:
            try:
                await interaction.response.send_message(content="Désolé vous ne pouvez pas faire ça",ephemeral=True)
            except:
                await interaction.edit_original_response(content="Désolé vous ne pouvez pas faire ça")
        else:
            return True
    async def on_error(self, interaction: Interaction, error: Exception, item: Item[Any]) -> None:
        raise error


class button_rules(discord.ui.View):
    def __init__(self,role:discord.Role):
        self.role=role
        super().__init__(timeout=None)
    
    @discord.ui.button(
        style=ButtonStyle.green,
        emoji="✅",
        custom_id="accept",
        row=0
    )
    async def accept(self,interaction:discord.Interaction,button:discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        await interaction.user.add_roles(roles=[self.role],reason="acceptation des règles")
        await interaction.edit_original_response(content="Merci d'avoir lu et accepté les règles,\nVous avez maintenant accès a l'entièreté du serveur")