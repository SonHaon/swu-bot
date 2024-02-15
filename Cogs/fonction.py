from requests import get
import json
import discord
import deepl
from datetime import datetime
from PIL import Image,ImageDraw,ImageFont
import numpy as np
from io import BytesIO
import aiohttp
import os,logging

logger = logging.getLogger('discord.artichauds')
path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

blacklist=["FrontArt","BackArt","DoubleSided"]
card_fields_leader=["Name","Subtitle","Type","Aspects","Traits","Arenas","Cost","Power","HP","FrontText","EpicAction","BackText","Rarity","Unique","Artist","Set","Number",None]
card_fields_unit=["Name","Type",None,"Aspects","Traits","Arenas","Cost","Power","HP","FrontText","Rarity","Unique","Artist","Set","Number",None]
card_fields_event=["Name","Type",None,"Aspects","Traits",None,"Cost",None,None,"FrontText","Rarity","Unique","Artist","Set","Number",None]
card_fields_upgrade=["Name","Type",None,"Aspects","Traits",None,"Cost","Power","HP","FrontText","Rarity","Unique","Artist","Set","Number",None]
card_fields_base=["Name","Subtitle","Type","Aspects",None,"HP","FrontText","Rarity","Unique","Artist","Set","Number",None]
card_fields={
    "leader":card_fields_leader,
    "unit":card_fields_unit,
    "event":card_fields_event,
    "upgrade":card_fields_upgrade,
    "base":card_fields_base
}
emoji={
    "Exhaust":"<:incline2:1144604589337874534>",
    "Villainy":"<:villainy:1143830118159093842>",
    "Agression":"<:agression:1143830119169921068>",
    "Vigilance":"<:vigilance:1143830124840628314>",
    "Command":"<:command:1143830115470545026>",
    "Cunning":"<:cunning:1143830121048981505>",
    "Heroism":"<:heroism:1143830123490070588>"
}
card_not_inline=["FrontText","EpicAction","BackText"]

def trad_card(card:dict,translator:deepl.Translator):
    with open("Cogs/glossaire.json") as glossaire:
        glossaire=json.load(glossaire)
    glossaire_id=translator.create_glossary(name="SWU",source_lang="EN",target_lang="FR",entries=glossaire).glossary_id
    logger.info(card)
    for name in card:
        if name=="Type_EN":
            pass
        elif type(card[name])==type(list()):
            liste=[]
            for each in card[name]:
                logger.info(translator.translate_text(str(each),source_lang="EN",target_lang="FR",glossary=glossaire_id))
                liste.append(translator.translate_text(each,source_lang="EN",target_lang="FR",glossary=glossaire_id).text)
            card[name]=liste
        elif type(card[name])==type(bool()):
            logger.info(translator.translate_text(str(card[name]),source_lang="EN",target_lang="FR",glossary=glossaire_id))
            card[name]=translator.translate_text(str(card[name]),source_lang="EN",target_lang="FR",glossary=glossaire_id).text
        else:
            logger.info(translator.translate_text(str(card[name]),source_lang="EN",target_lang="FR",glossary=glossaire_id))
            card[name]=translator.translate_text(card[name],source_lang="EN",target_lang="FR",glossary=glossaire_id).text
    return card 

def recup_card(set,number):
    card=json.loads(get(f"https://api.swu-db.com/cards/{set}/{str(number)}").content)
    card["Type_EN"]=card["Type"]
    for each in emoji:
        card["FrontText"]=card["FrontText"].replace(each,emoji[each])
    card["FrontText"]=card["FrontText"].replace("{","")
    card["FrontText"]=card["FrontText"].replace("}","")
    return card

def fields(embed:discord.Embed,card:dict):
    for name in card_fields[card["Type_EN"].lower()]:
        try:
            if name==None:
                embed.add_field(name=f" ",value=" ",inline= True)
            elif name in card_not_inline:
                embed.add_field(name=f"**__{name}__**",value=card[name],inline= False)
            elif type(card[name]) == type(list()):
                embed.add_field(name=f"**__{name}__**",value=", ".join(card[name]),inline= True)
            else:
                embed.add_field(name=f"**__{name}__**",value=card[name],inline= True)
        except:
            print("une erreur dans les fields")
    return embed

def fields_fr(embed:discord.Embed,card:dict,translator:deepl.Translator):
    with open("Cogs/glossaire.json") as glossaire:
        glossaire=json.load(glossaire)
    glossaire_id=translator.create_glossary(name="SWU",source_lang="EN",target_lang="FR",entries=glossaire).glossary_id
    for name in card_fields[card["Type_EN"].lower()]:
        try:
            name_fr=translator.translate_text(str(name),source_lang='EN',target_lang='FR',glossary=glossaire_id).text
            if name==None:
                embed.add_field(name=f" ",value=" ",inline= True)
            elif name in card_not_inline:
                embed.add_field(name=f"**__{name_fr}__**",value=card[name],inline= False)
            elif type(card[name]) == type(list()):
                embed.add_field(name=f"**__{name_fr}__**",value=", ".join(card[name]),inline= True)
            else:
                embed.add_field(name=f"**__{name_fr}__**",value=card[name],inline= True)
        except:
            print("une erreur dans les fields")
    return embed

def circular_crowp(img):
    img=img.convert("RGB")
    npImage=np.array(img)
    h,w=img.size
    alpha = Image.new('L', img.size,0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0,0,h,w],0,360,fill=255)
    npAlpha=np.array(alpha)
    npImage=np.dstack((npImage,npAlpha))
    return Image.fromarray(npImage)

async def image_bienvenue(bot,member:discord.Member):
    user_pp_url = member.display_avatar.replace(size=256)
    user_pp_url = BytesIO(await user_pp_url.read())
    user_pp = Image.open(user_pp_url)
    user_pp = circular_crowp(user_pp)
    img = Image.open(f"{path}/joinimg.png")
    draw = ImageDraw.Draw(img)
    font= ImageFont.truetype(f"{path}/Quicksand_Bold.otf",50)
    draw.multiline_text((650,150),f"Bienvenue {member.display_name}\n\nsur notre serveur : \n\n{member.guild}", (255,255,255), anchor="mm",font=font,align="center")
    img.paste(user_pp, box=(22,22),mask=user_pp)
    img.save(f"{path}/{member.name}.png")
    channel_image=bot.get_channel(1009137943077724240)
    message = await channel_image.send(file=discord.File(f"{path}/{member.name}.png"))
    return message.attachments[0].url

async def member_count(guild:discord.Guild):
    counter_channel=guild.get_channel(1207325510418432010)
    await counter_channel.edit(name=f"Membres : {guild.member_count}")