from aiogram.types import ReplyKeyboardMarkup, aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import SUBSCRIPTIONS

def get_main_menu():
    keyboard = ReplyKeyboardMarkup KeyboardButton
from config import SUBSCRIPTIONS

def get_main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Профиль"))
    keyboard.add((resize_keyboard=True)
    keyboard.add(KeyboardButton("Профиль"))
    keyboard.add(KeyboardButton("Снести акKeyboardButton("Снести аккаунт"))
каунт"))
    keyboard.add(KeyboardButton("Куп    keyboard.add(KeyboardButton("Купить подить подписку"))
    keyboard.addписку"))
    keyboard.add(KeyboardButton("Доступ(KeyboardButton("Доступ к информации"))
    return keyboard

 к информации"))
    return keyboard

def get_subscription_menudef get_subscription_menu():
    keyboard():
    keyboard = ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
    for sub(resize_keyboard=True)
    for sub_id, sub_id, sub in SUBSCRIPTIONS in SUBSCRIPTIONS.items():
        keyboard.add.items():
        keyboard.add((KeyboardButton(f"{sub['KeyboardButton(fname']} ({"{sub['name']} ({sub['pricesub['price']} {sub['currency']']} {sub['currency']})"))
    keyboard})"))
    keyboard.add(Keyboard.add(KeyboardButton("ОтButton("Отмена"))
    return keyboard

мена"))
    return keyboard

def get_cancel_keyboard():
    return Replydef get_cancel_keyboard():
    return ReplyKeyboardMarkup(
        resizeKeyboardMarkup(
        resize_keyboard=True,
        keyboard_keyboard=True,
        keyboard=[[Keyboard=[[KeyboardButton("ОтButton("Отмена")]]
    )

defмена")]]
    )

def get_confirm_keyboard get_confirm_keyboard():
    return():
    return ReplyKeyboardMarkup(
        resize ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard_keyboard=True,
        keyboard=[[Keyboard=[[KeyboardButton("ПодButton("Подтвердтвердить"), Keyboardить"), KeyboardButton("ОтButton("Отмена")]]
   мена")]]
    )

def )

def get_payment_keyboard():
 get_payment_keyboard():
    return ReplyKeyboard    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboardMarkup(
        resize_keyboard=True,
        keyboard=[[KeyboardButton("П=[[KeyboardButton("Проверить оплроверить оплату"), Keyboardату"), KeyboardButton("ОтButton("Отмена")]]
   мена")]]
    )
