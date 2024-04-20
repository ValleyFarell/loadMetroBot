import os
from pathlib import Path
from aiogram import Bot, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, File
from lexicon.lexicon_RU import ANSWERS_LEXICON
from aiogram import F
from services.recognition_services import voice_to_text
from services.data_generation import data_generation
from wordToNum.extractor import NumberExtractor
import requests

main_router: Router = Router()

@main_router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=ANSWERS_LEXICON['start'])


async def handle_file(file: File, file_name: str, path: str, bot: Bot):
    Path(f"{path}").mkdir(parents=True, exist_ok=True)

    await bot.download_file(file_path=file.file_path, destination=f"{path}/{file_name}")


@main_router.message(F.voice)
async def process_recognition_command(message: Message, bot: Bot):
    await message.reply('Чуть-чуть подождите...')
    voice_id = message.voice.file_id
    file = await bot.get_file(voice_id)

    path = "files/voices"

    await handle_file(file=file, file_name="voice.mp3", path=path, bot=bot)

    voice_to_text('files/voices/voice.mp3', 'files/voices/text.txt')
    text = ''.join(open('files/voices/text.txt', 'r').readlines())
    extractor = NumberExtractor()
    print(text)
    extext = extractor.replace_groups(text)
    data = data_generation(extext)
    os.remove('files/voices/text.txt')
    requests.post('http://127.0.0.1:8000/', data)
    if data['station'] == '':
        await message.answer('Пожалуйста, повторите запрос!' + '\n' + 'You said: ' + text)
    else:
        await message.answer(str(data) + '\n' + 'You said: ' + text)

@main_router.message()
async def process_message_command(message: Message):
    text = message.text
    extractor = NumberExtractor()
    text = extractor.replace_groups(text)
    data = data_generation(text)
    if data['station'] == '':
        await message.reply('Пожалуйста, повторите запрос!')
    else:
        await message.reply(str(data))






