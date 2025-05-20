from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import SUBSCRIPTIONS

def get_main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Профиль"))
    keyboard.add(KeyboardButton("Снести аккаунт"))
    keyboard.add(KeyboardButton("Купить подписку"))
    keyboard.add(KeyboardButton("Доступ к информации"))
    return keyboard

def get_subscription_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for sub_id, sub in SUBSCRIPTIONS.items():
        keyboard.add(KeyboardButton(f"{sub['name']} ({sub['price']} {sub['currency']})"))
    keyboard.add(KeyboardButton("Отмена"))
    return keyboard

def get_cancel_keyboard():
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[[KeyboardButton("Отмена")]]
    )

def get_confirm_keyboard():
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[[KeyboardButton("Подтвердить"), KeyboardButton("Отмена")]]
    )

def get_payment_keyboard():
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[[KeyboardButton("Проверить оплату"), KeyboardButton("Отмена")]]
    )