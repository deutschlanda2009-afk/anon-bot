
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging

# =========================
# НАСТРОЙКИ
# =========================

TOKEN = 8738376027:AAHLsCBy0GWHO8XOIj1R7CDi21uFhJegs8Y
OWNER_ID = 7116697287

# =========================

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


start_kb = InlineKeyboardMarkup(row_width=1)
start_kb.add(
    InlineKeyboardButton(
        "📩 Отправить анонимное сообщение",
        callback_data="send_anon"
    )
)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):

    me = await bot.get_me()

    text = (
        "🖤 Анонимный бот\n\n"
        "Отправь сообщение полностью анонимно."
    )

    if message.from_user.id == OWNER_ID:
        text += (
            f"\n\n🔗 Твоя ссылка для анонимных сообщений:\n"
            f"https://t.me/{me.username}"
        )

    await message.answer(text, reply_markup=start_kb)


@dp.callback_query_handler(text="send_anon")
async def send_anon(callback: types.CallbackQuery):

    await callback.message.answer(
        "✍️ Напиши сообщение, которое хочешь отправить анонимно."
    )

    await callback.answer()


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def messages(message: types.Message):

    if message.from_user.id == OWNER_ID:
        return

    sender = message.from_user

    text = (
        "📨 Новое анонимное сообщение\n\n"
        f"{message.text}"
    )

    await bot.send_message(OWNER_ID, text)

    await message.reply("✅ Сообщение отправлено анонимно.")


@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def photos(message: types.Message):

    if message.from_user.id == OWNER_ID:
        return

    caption = message.caption if message.caption else "📷 Фото без подписи"

    await bot.send_photo(
        OWNER_ID,
        photo=message.photo[-1].file_id,
        caption=f"📨 Анонимное фото\n\n{caption}"
    )

    await message.reply("✅ Фото отправлено анонимно.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
