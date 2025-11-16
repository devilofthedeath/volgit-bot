from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

def get_schedule_main_keyboard():
    """Главное меню расписания"""
    builder = InlineKeyboardBuilder()
    builder.button(text="📅 Расписание на 18.11", callback_data="schedule_18.11")
    builder.button(text="📅 Расписание на 19.11", callback_data="schedule_19.11")
    builder.button(text="📅 Расписание на 20.11", callback_data="schedule_20.11")
    builder.button(text="🔙 Назад", callback_data="main_menu")
    builder.adjust(2)
    return builder.as_markup()

def get_schedule_back_keyboard():
    """Кнопка назад в расписании"""
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Назад в расписание", callback_data="schedule_back")
    return builder.as_markup()