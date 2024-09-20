from aiogram.types import ReplyKeyboardMarkup

# Translated messages
back_message = '👈 Back'
confirm_message = '✅ Confirm order'
all_right_message = '✅ All correct'
cancel_message = '🚫 Cancel'

# Markup for confirming the order
def confirm_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(confirm_message)
    markup.add(back_message)

    return markup

# Markup with only a back button
def back_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(back_message)

    return markup

# Markup with options to go back or confirm everything is correct
def check_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row(back_message, all_right_message)

    return markup

# Markup with options to cancel or confirm everything is correct
def submit_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row(cancel_message, all_right_message)

    return markup
