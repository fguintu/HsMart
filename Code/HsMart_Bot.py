import discord
from discord.ext import commands
import aiohttp
from bs4 import BeautifulSoup

intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

bot = commands.Bot(command_prefix='!', intents=intents)

CHANNEL_ID = 123  # Replace with your channel ID
PAGE_URL = "https://www.hmart.com/weekly-ads/georgia"  # Page URL to scrape

async def fetch_image_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                html = await resp.text()
                soup = BeautifulSoup(html, 'html.parser')
                # Adjust the selector according to the actual HTML structure
                image_tag = soup.find('img', {'class': 'hmartus-store-theme-1-x-mainImage'})
                if image_tag:
                    return image_tag['src']
    return None

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command()
async def weekly_ad(ctx):
    image_url = await fetch_image_url(PAGE_URL)
    if image_url:
        await ctx.send(f"Weekly Ad Georgia English: {image_url}")
    else:
        await ctx.send("Failed to fetch the weekly ad image.")


bot.run('bot_token')  # Replace with your bot token