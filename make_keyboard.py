
import telebot


def make_keyboard(message, markup, buttons, row_w):

    k = 0
    l: int = len(buttons)-1
    while k + row_w <= l:
        b1 = telebot.types.InlineKeyboardButton(buttons[k], callback_data=buttons[k])
        b2 = telebot.types.InlineKeyboardButton(buttons[k+1], callback_data=buttons[k+1])
        b3 = telebot.types.InlineKeyboardButton(buttons[k+2], callback_data=buttons[k+2])
        markup.add(b1, b2, b3)
        k = k+row_w

    if l-k == 2:
        b1 = telebot.types.InlineKeyboardButton(buttons[k], callback_data=buttons[k])
        b2 = telebot.types.InlineKeyboardButton(buttons[k+1], callback_data=buttons[k+1])
        markup.add(b1, b2)
    elif l-k == 1:
        b1 = telebot.types.InlineKeyboardButton(buttons[k], callback_data=buttons[k])
        markup.add(b1)

    return markup
