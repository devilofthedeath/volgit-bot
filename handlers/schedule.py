from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from keyboards.schedule import get_schedule_main_keyboard, get_schedule_back_keyboard

schedule_router = Router()

# Пример данных расписания
SCHEDULE_DATA = {
    "day1": {
        "date": "2024-04-01",
        "events": [
            {"time": "09:00", "event": "Регистрация", "location": "Главный корпус, холл 1 этажа"},
            {"time": "10:00", "event": "Торжественное открытие", "location": "Актовый зал"},
            {"time": "11:00", "event": "Олимпиада по математике", "location": "Корпус А, ауд. 301"}
        ]
    },
    "day2": {
        "date": "2024-04-02", 
        "events": [
            {"time": "09:00", "event": "Олимпиада по физике", "location": "Корпус Б, ауд. 215"},
            {"time": "14:00", "event": "Мастер-классы", "location": "Научные лаборатории"}
        ]
    }
}

@schedule_router.message(Command("schedule"))
@schedule_router.message(F.text == "📅 Расписание")
async def show_schedule_menu(message: Message):
    await message.answer(
        "📅 Расписание мероприятий:\nВыберите опцию:",
        reply_markup=get_schedule_main_keyboard()
    )

@schedule_router.callback_query(F.data == "schedule_general")
async def show_general_schedule(callback: CallbackQuery):
    text = "📅 Общее расписание:\n\n"
    
    for day_id, day_data in SCHEDULE_DATA.items():
        text += f"📅 {day_data['date']}:\n"
        for event in day_data["events"]:
            text += f"⏰ {event['time']} - {event['event']}\n"
            text += f"📍 {event['location']}\n\n"
    
    await callback.message.edit_text(text, reply_markup=get_schedule_back_keyboard())
    await callback.answer()

@schedule_router.callback_query(F.data == "schedule_personal")
async def show_personal_schedule(callback: CallbackQuery):
    # Заглушка для персонального расписания
    await callback.message.edit_text(
        "👤 Функция персонального расписания будет доступна после привязки вашего ID участника.",
        reply_markup=get_schedule_back_keyboard()
    )
    await callback.answer()

@schedule_router.callback_query(F.data == "schedule_notifications")
async def show_notifications_settings(callback: CallbackQuery):
    # Заглушка для уведомлений
    await callback.message.edit_text(
        "🔔 Настройки уведомлений:\n\n"
        "Вы можете включить/выключить уведомления о:\n"
        "• Начале мероприятий\n"
        "• Изменениях в расписании\n"
        "• Важных объявлениях\n\n"
        "Функция в разработке...",
        reply_markup=get_schedule_back_keyboard()
    )
    await callback.answer()

@schedule_router.callback_query(F.data == "schedule_menu")
async def back_to_schedule_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "📅 Расписание мероприятий:\nВыберите опцию:",
        reply_markup=get_schedule_main_keyboard()
    )
    await callback.answer()