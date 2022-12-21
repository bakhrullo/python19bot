import logging
import aiogram.types.base
import converter
from converter import text_to_mp3, mp3_to_text
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputFile
import pathlib
import os

user = {}
API_TOKEN = ''

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\n i am converter bot.\n Send me text or audio and you will see the magic.\n Bot creator @Fatkhullaev_b")



@dp.message_handler(content_types=('text'))
async def echo(message: types.Message):
    print(message.text)
    print(message.from_user)
    msg = message.text
    aud = message.from_user.first_name
    aud = (aud + '.mp3')

    converter.text_to_mp3(msg, aud)
    cat = InputFile(aud)
    await bot.send_audio(chat_id=message.chat.id, audio=cat, reply_to_message_id=message.message_id)
    file_delete = pathlib.Path(str(aud))
    file_delete.unlink()
    


@dp.message_handler(content_types=('voice'))
async def voice(message):
    print(message)
    file = message.voice.file_unique_id + '.mp3'
    cos = message.voice.file_unique_id
    await message.voice.download(file)
    res = await converter.mp3_to_text(file, cos)
    await bot.send_message(message.chat.id, res, reply_to_message_id=message.message_id)
    file_delete = pathlib.Path(str(file))
    file_delete.unlink()
    
    
@dp.message_handler(content_types=('audio'))
async def aud(message):
    print(message)
    file = message.audio.file_unique_id + '.mp3'
    cos = message.audio.file_unique_id
    await message.audio.download(file)
    res = await converter.mp3_to_text(file, cos)
    await bot.send_message(message.chat.id, res, reply_to_message_id=message.message_id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
