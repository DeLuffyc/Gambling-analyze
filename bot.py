from pathlib import Path
import time
from aiogram.types import ContentType, ReplyKeyboardMarkup, KeyboardButton
from aiogram.exceptions import TelegramBadRequest
import asyncio
from aiogram.filters import Command
import os
import json
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
# Обработчик нажатий на кнопки
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from aiogram import F
from scriptss.config import load_credentials, DB_CREDENTIALS, TGRM_BOT_CREDENTIALS, OPENAI_API
import logging
import pandas as pd
from aiogram.client.default import DefaultBotProperties
from request_llm import perplexity
from handlers.llm_system_prompts import system_prompt_il_v1


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Создаем обработчик для вывода в консоль
#console_handler = logging.StreamHandler()
#console_handler.setLevel(logging.INFO)

# Добавляем обработчик к логгеру
#logger.addHandler(console_handler)

# Объект бота
creds = load_credentials(TGRM_BOT_CREDENTIALS)
#TOKEN = creds['tg_prod']
# TOKEN = creds['tg_test']
TOKEN = os.environ.get('tg_prod')
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

# Диспетчер
dp = Dispatcher()

logger.info("This is an informational message")
print("This is a print statement")

from datetime import datetime
current_datetime_for_log = datetime.now()
log_dt_now = current_datetime_for_log.strftime('%Y-%m-%d %H:%M:%S')

class UserSession:
    def __init__(self):
        self.state = 'start'
        self.json_user = ''
        self.flow_language = 'ru'
        self.start_args = ''


user_sessions = {}

def get_user_session(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = UserSession()
    return user_sessions[user_id]


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    command_text = message.text
    user_id = message.from_user.id
    user_session = get_user_session(user_id)
    start_message = "Привет! Назови команды и дату матча"
    # Отправка стартового сообщения
    await message.answer(start_message)

    user_session.state = 'start_match'


@dp.message()  # content_types=[types.ContentType.TEXT, types.ContentType.VOICE])
async def process_message(message: types.Message):
    try:
        user_id = message.from_user.id
        user_session = get_user_session(user_id)
        f = message.content_type
        message_text = message.text

        logging.info(f"Стадия: {user_session.state} --- Сообщение: {message_text}")

        if user_session.state == 'start_match':

            await message.answer('Получили информацию, дай нам 30 секунд')
            res, status = perplexity(message_text, system_prompt_il_v1)
            if status == 0:
                await message.answer('Произошла ошибка, попробуйте попозже')
                logging.info(f"Стадия: {user_session.state} --- Сообщение: {message_text}, {res}")
            else:
                await message.answer(res)


        elif user_session.state == 'start':
            await message.answer('Начини заново /start')
            logger.info(f"Стадия: {user_session.state} --- Упал на тексте от {user_id}, {message_text}, {f}", exc_info=True)


        else:
            await message.answer(
                "Упс. Где-то что-то упало)")
            logger.error(f"Стадия: {user_session.state} --- Упал на тексте от {user_id}, {message_text}", exc_info=True)
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {message.text}: {e}", exc_info=True)
        await message.answer(
            "Извините, произошла ошибка при обработке вашего сообщения. Попробуйте еще раз или начните заново /start.")


# Запуск процесса поллинга новых апдейтов
async def main():
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Критическая ошибка в main(): {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
