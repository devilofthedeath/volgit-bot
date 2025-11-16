from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_navigation_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🗺️ Карта кампуса", callback_data="nav_campus_map")
    builder.button(text="🚶 Пеший маршрут", callback_data="nav_walking_route")
    builder.button(text="🚌 На транспорте", callback_data="nav_transport_route")
    builder.button(text="🚗 На автомобиле", callback_data="nav_driving_route")
    builder.button(text="🔙 Назад", callback_data="main_menu")
    builder.adjust(2)
    return builder.as_markup()