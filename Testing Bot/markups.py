from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def summ_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 8
    markup.add(InlineKeyboardButton("On", callback_data="summ_on"), InlineKeyboardButton("Off", callback_data="summ_off"))
    return markup


def len_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 8
    markup.add(InlineKeyboardButton("Yes", callback_data="len_yes"), InlineKeyboardButton("No", callback_data="len_no"))
    return markup