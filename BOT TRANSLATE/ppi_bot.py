import discord
from discord.ext import tasks, commands
from discord.utils import get
from dotenv import load_dotenv
import asyncio
import os
import googletrans 
from discord import Embed

translator = googletrans.Translator()

# Create a dictionary of flag emojis and their corresponding language codes
flag_emoji_dict = {
"🇺🇸": "en",
"🇩🇪": "de",
"🇫🇷": "fr",
"🇪🇸": "es",
"🇮🇹": "it",
"🇵🇹": "pt",
"🇷🇺": "ru",
"🇦🇱": "sq",
"🇸🇦": "ar",
"🇧🇦": "bs",
"🇧🇬": "bg",
"🇨🇳": "zh-CN",
"🇭🇷": "hr",
"🇨🇿": "cs",
"🇩🇰": "da",
"🇪🇪": "et",
"🇫🇮": "fi",
"🇬🇷": "el",
"🇭🇺": "hu",
"🇮🇩": "id",
"🇮🇳": "hi",
"🇮🇪": "ga",
"🇮🇸": "is",
"🇮🇱": "he",
"🇯🇵": "ja",
"🇰🇷": "ko",
"🇱🇻": "lv",
"🇱🇹": "lt",
"🇲🇹": "mt",
"🇲🇪": "sr",
"🇳🇱": "nl",
"🇳🇴": "no",
"🇵🇰": "ur",
"🇵🇱": "pl",
"🇵🇹": "pt",
"🇷🇴": "ro",
"🇷🇸": "sr",
"🇸🇦": "ar",
"🇸🇰": "sk",
"🇸🇮": "sl",
"🇸🇬": "sv",
"🇹🇭": "th",
"🇹🇷": "tr",
"🇹🇼": "zh-TW",
"🇺🇦": "uk",
"🇻🇦": "la"
}

#For a more secure, we loaded the .env file and assign the token value to a variable 
load_dotenv(".env")
TOKEN = os.getenv("TOKEN")

#Intents are permissions for the bot that are enabled based on the features necessary to run the bot.
intents=discord.Intents.all()

#Comman prefix is setup here, this is what you have to type to issue a command to the bot
prefix = './'
bot = commands.Bot(command_prefix=prefix, intents=intents)

#------------------------------------------------Events------------------------------------------------------#

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.emoji in flag_emoji_dict:
        lang_code = flag_emoji_dict[reaction.emoji]
        message = reaction.message
        detected_lang = translator.detect(message.content)
        
        if detected_lang:
            translated_message = message.content
            pronunciation_message = message.content
        else:
            translated_message = "Tidak dapat mendeteksi bahasa"
            pronunciation_message = "Tidak tersedia"
        
        embed = Embed(title='Translated Text', description=f'{translated_message}', color=0x00ff00)
        embed.add_field(name="Original Text", value=message.content, inline=False)
        
        if detected_lang:
            embed.add_field(name="Translated from:", value=f'{detected_lang.lang.capitalize()} ({detected_lang.confidence*100:.2f}%)')
        else:
            embed.add_field(name="Translated from:", value="Tidak dapat mendeteksi bahasa")
        
        embed.add_field(name="Pronunciation:", value=pronunciation_message, inline=False)
        try:
            await reaction.message.channel.send(content=f'{user.mention}', embed=embed)
        except Exception as e:
            print(f"An error occurred: {str(e)}")

#Run the bot
bot.run(TOKEN)