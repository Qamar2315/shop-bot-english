import os
import handlers
from aiogram import executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from data import config
from loader import dp, db, bot
import filters
import logging

filters.setup(dp)

user_message = 'User'
admin_message = 'Admin'


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):

    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row(user_message, admin_message)

    await message.answer('''Hello! 👋

🤖 I am a shop bot for selling products of any category.

🛍️ To view the catalog and select products, use the /menu command.

💰 You can top up your account via Yandex.Money, Sberbank, or Qiwi.

❓ Have questions? No problem! Use the /sos command to contact admins, who will respond as quickly as possible.

🤝 Want a similar bot? Contact the developer <a href="https://t.me/NikolaySimakov">Nikolay Simakov</a>, he won't bite)))
    ''', reply_markup=markup)


@dp.message_handler(text=user_message)
async def user_mode(message: types.Message):

    cid = message.chat.id
    if cid in config.ADMINS:
        config.ADMINS.remove(cid)

    await message.answer('User mode enabled.', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(text=admin_message)
async def admin_mode(message: types.Message):

    cid = message.chat.id
    if cid not in config.ADMINS:
        config.ADMINS.append(cid)

    await message.answer('Admin mode enabled.', reply_markup=ReplyKeyboardRemove())


async def on_startup(dp):
    logging.basicConfig(level=logging.INFO)
    db.create_tables()

    await bot.delete_webhook()  # This is not required for local polling but ensures clean startup


async def on_shutdown():
    logging.warning("Shutting down..")
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Bot has been shut down")


if __name__ == '__main__':

    # Since you are running locally, only use polling mode
    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
