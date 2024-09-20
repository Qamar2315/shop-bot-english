from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from keyboards.default.markups import all_right_message, cancel_message, submit_markup
from aiogram.types import Message
from states import SosState
from filters import IsUser
from loader import dp, db

@dp.message_handler(commands='sos')
async def cmd_sos(message: Message):
    await SosState.question.set()
    await message.answer('What is the issue? Describe it as detailed as possible, and the administrator will get back to you.', reply_markup=ReplyKeyboardRemove())

@dp.message_handler(state=SosState.question)
async def process_question(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['question'] = message.text

    await message.answer('Make sure everything is correct.', reply_markup=submit_markup())
    await SosState.next()

@dp.message_handler(lambda message: message.text not in [cancel_message, all_right_message], state=SosState.submit)
async def process_invalid_choice(message: Message):
    await message.answer('This option was not available.')

@dp.message_handler(text=cancel_message, state=SosState.submit)
async def process_cancel(message: Message, state: FSMContext):
    await message.answer('Cancelled!', reply_markup=ReplyKeyboardRemove())
    await state.finish()

@dp.message_handler(text=all_right_message, state=SosState.submit)
async def process_submit(message: Message, state: FSMContext):

    cid = message.chat.id

    if db.fetchone('SELECT * FROM questions WHERE cid=?', (cid,)) is None:

        async with state.proxy() as data:
            db.query('INSERT INTO questions VALUES (?, ?)',
                     (cid, data['question']))

        await message.answer('Sent!', reply_markup=ReplyKeyboardRemove())

    else:
        await message.answer('The question submission limit has been exceeded.', reply_markup=ReplyKeyboardRemove())

    await state.finish()
