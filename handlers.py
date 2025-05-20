from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from config import ADMIN_ID, SUBSCRIPTIONS
from keyboards import get_main_menu, get_subscription_menu, get_cancel_keyboard, get_confirm_keyboard, get_payment_keyboard
from states import OrderStates
from crypto_api import create_invoice, check_invoice_status
from database import get_subscription, save_subscription
from datetime import datetime

async def start_command(message: types.Message, state: FSMContext):
    await message.answer(
        "Добро пожаловать в сервис! Выберите действие:",
        reply_markup=get_main_menu()
    )
    await state.clear()

async def handle_menu(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)
    subscription_id, end_date = get_subscription(user_id)

    if message.text == "Профиль":
        user = message.from_user
        sub_info = f"Подписка: {SUBSCRIPTIONS[subscription_id]['name']}\nИстекает: {end_date}" if subscription_id else "Подписка: Отсутствует"
        await message.answer(
            f"**Информация о пользователе:**\n"
            f"ID: {user.id}\n"
            f"Имя: {user.full_name}\n"
            f"Юзернейм: @{user.username or 'Не указан'}\n"
            f"Дата регистрации: Не доступна\n"
            f"{sub_info}\n"
            f"Статус белого списка: Не в белом списке",
            reply_markup=get_main_menu()
        )
    elif message.text == "Снести аккаунт":
        if subscription_id:
            await message.answer(
                "Пожалуйста, напишите юзернейм или отправьте ссылку на канал:",
                reply_markup=get_cancel_keyboard()
            )
            await state.set_state(OrderStates.ENTER_TARGET)
        else:
            await message.answer(
                "Для использования этой функции нужна активная подписка. Купите подписку!",
                reply_markup=get_main_menu()
            )
    elif message.text == "Купить подписку":
        await message.answer(
            "Выберите тариф подписки:",
            reply_markup=get_subscription_menu()
        )
        await state.set_state(OrderStates.SELECT_SUBSCRIPTION)
    elif message.text == "Доступ к информации":
        await message.answer(
            "**Информация о сервисе:**\n"
            "Название сервиса: Снос аккаунтов\n"
            "Это сервис для удаления аккаунтов в Telegram. Как это работает:\n"
            "1. Вы покупаете тариф на определенное количество дней.\n"
            "2. Указываете аккаунт, который нужно снести.\n"
            "3. Наши боты отправляют множество жалоб на целевой аккаунт.\n"
            "Обратите внимание: массовые жалобы могут привести к временным ограничениям. "
            "Мы не гарантируем блокировку аккаунта.\n"
            "По вопросам обращайтесь в поддержку.",
            reply_markup=get_main_menu()
        )
    else:
        await message.answer("Пожалуйста, выберите действие из меню.", reply_markup=get_main_menu())

async def select_subscription(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await message.answer("Действие отменено.", reply_markup=get_main_menu())
        await state.clear()
        return
    selected_sub = None
    for sub_id, sub in SUBSCRIPTIONS.items():
        if message.text.startswith(sub["name"]):
            selected_sub = sub_id
            break
    if selected_sub:
        await state.update_data(subscription_id=selected_sub)
        await message.answer(
            f"Вы выбрали: {SUBSCRIPTIONS[selected_sub]['name']} ({SUBSCRIPTIONS[selected_sub]['price']} {SUBSCRIPTIONS[selected_sub]['currency']})\n"
            f"Подтвердите покупку:",
            reply_markup=get_confirm_keyboard()
        )
        await state.set_state(OrderStates.CONFIRM_ORDER)
    else:
        await message.answer("Пожалуйста, выберите тариф из списка.", reply_markup=get_subscription_menu())

async def confirm_order(message: types.Message, state: FSMContext, bot: types.Bot):
    if message.text == "Отмена":
        await message.answer("Действие отменено.", reply_markup=get_main_menu())
        await state.clear()
        return
    if message.text != "Подтвердить":
        await message.answer("Пожалуйста, подтвердите или отмените заказ.")
        return

    user_data = await state.get_data()
    subscription_id = user_data.get("subscription_id")
    target = user_data.get("target")

    if subscription_id:  # Покупка подписки
        description = f"Покупка подписки: {SUBSCRIPTIONS[subscription_id]['name']}"
        invoice_data = create_invoice(subscription_id, description)
        if invoice_data:
            invoice_id, invoice_url = invoice_data
            await state.update_data(invoice_id=invoice_id)
            await message.answer(
                f"Счет создан! Оплатите по ссылке:\n{invoice_url}\n"
                f"После оплаты нажмите 'Проверить оплату'.",
                reply_markup=get_payment_keyboard()
            )
            await state.set_state(OrderStates.CHECK_PAYMENT)

            # Уведомление администратора
            await bot.send_message(
                ADMIN_ID,
                f"Новый заказ подписки!\n"
                f"Пользователь: @{message.from_user.username or message.from_user.full_name}\n"
                f"Подписка: {SUBSCRIPTIONS[subscription_id]['name']}\n"
                f"Счет: {invoice_url}"
            )
        else:
            await message.answer("Ошибка при создании счета. Попробуйте позже.")
            await state.clear()
    elif target:  # Заказ сноса аккаунта
        await bot.send_message(
            ADMIN_ID,
            f"Новый заказ сноса!\n"
            f"Пользователь: @{message.from_user.username or message.from_user.full_name}\n"
            f"Цель: {target}"
        )
        await message.answer(
            "Заказ принят! Он передан в обработку.",
            reply_markup=get_main_menu()
        )
        await state.clear()

async def check_payment(message: types.Message, state: FSMContext, bot: types.Bot):
    if message.text == "Отмена":
        await message.answer("Действие отменено.", reply_markup=get_main_menu())
        await state.clear()
        return
    if message.text != "Проверить оплату":
        await message.answer("Пожалуйста, проверьте оплату или отмените заказ.")
        return

    user_data = await state.get_data()
    invoice_id = user_data["invoice_id"]
    subscription_id = user_data["subscription_id"]

    # Проверка статуса оплаты
    status, invoice_url = check_invoice_status(invoice_id)
    if status == "paid":
        save_subscription(str(message.from_user.id), subscription_id)
        await message.answer(
            f"Оплата подтверждена! Подписка {SUBSCRIPTIONS[subscription_id]['name']} активирована.",
            reply_markup=get_main_menu()
        )
        await bot.send_message(
            ADMIN_ID,
            f"Оплата подтверждена!\n"
            f"Пользователь: @{message.from_user.username or message.from_user.full_name}\n"
            f"Подписка: {SUBSCRIPTIONS[subscription_id]['name']}\n"
            f"Счет: {invoice_url}"
        )
        await state.clear()
    elif status:
        await message.answer(
            "Оплата еще не подтверждена. Попробуйте позже.",
            reply_markup=get_payment_keyboard()
        )
    else:
        await message.answer("Ошибка при проверке оплаты. Попробуйте позже.")

def setup_handlers(dp: Dispatcher):
    dp.message.register(start_command, Command("start"))
    dp.message.register(select_subscription, OrderStates.SELECT_SUBSCRIPTION)
    dp.message.register(enter_target, OrderStates.ENTER_TARGET)
    dp.message.register(lambda message, state, bot=dp.bot: confirm_order(message, state, bot), OrderStates.CONFIRM_ORDER)
    dp.message.register(lambda message, state, bot=dp.bot: check_payment(message, state, bot), OrderStates.CHECK_PAYMENT)
    dp.message.register(handle_menu)  # Обработчик для всех остальных сообщений

async def enter_target(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await message.answer("Действие отменено.", reply_markup=get_main_menu())
        await state.clear()
        return
    await state.update_data(target=message.text)
    await message.answer(
        f"Вы хотите снести аккаунт/канал: {message.text}\n"
        f"Подтвердите заказ:",
        reply_markup=get_confirm_keyboard()
    )
    await state.set_state(OrderStates.CONFIRM_ORDER)