import discord
from discord.ext import commands, tasks
import asyncio
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

CHANNEL_ID = 123456789  # Replace with your channel ID
MESSAGE_ID = None  # This will store the ID of the message we're updating
IMAGE_URL = "https://example.com/path/to/your/image.jpg"  # Replace with your image URL

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    update_image.start()

@tasks.loop(hours=168)  # 168 hours = 1 week
async def update_image():
    global MESSAGE_ID
    channel = bot.get_channel(CHANNEL_ID)
    
    if channel:
        if MESSAGE_ID is None:
            # If no message exists, send a new one
            message = await channel.send("Weekly Ad Georgia English", file=discord.File(IMAGE_URL))
            MESSAGE_ID = message.id
        else:
            # If a message exists, edit it
            try:
                message = await channel.fetch_message(MESSAGE_ID)
                await message.edit(content="Weekly Ad Georgia English", attachments=[discord.File(IMAGE_URL)])
            except discord.NotFound:
                # If the message was deleted, send a new one
                message = await channel.send("Weekly Ad Georgia English", file=discord.File(IMAGE_URL))
                MESSAGE_ID = message.id
    else:
        print(f"Channel with ID {CHANNEL_ID} not found.")

@update_image.before_loop
async def before_update_image():
    # Wait until the next Monday at 00:00
    now = datetime.now()
    next_monday = now + timedelta(days=(7 - now.weekday()))
    next_monday = next_monday.replace(hour=0, minute=0, second=0, microsecond=0)
    await discord.utils.sleep_until(next_monday)

bot.run('YOUR_BOT_TOKEN')  # Replace with your bot token