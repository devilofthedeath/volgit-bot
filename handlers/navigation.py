from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from decouple import config
from data.navigation_data import LOCATIONS, ULSTU_COORDS
from keyboards.navigation import get_navigation_keyboard

navigation_router = Router()

def generate_yandex_map_url(start_coords: str, end_coords: str, route_type: str = "pd") -> str:
    base_url = "https://yandex.ru/maps/"
    
    if route_type == "pd":  # Пешком
        url = f"{base_url}?rtext={start_coords}~{end_coords}&rtt=pd"
    elif route_type == "mt":  # Общественный транспорт
        url = f"{base_url}?rtext={start_coords}~{end_coords}&rtt=mt"
    elif route_type == "auto":  # Автомобиль
        url = f"{base_url}?rtext={start_coords}~{end_coords}&rtt=auto"
    else:
        url = f"{base_url}?rtext={start_coords}~{end_coords}"
    
    return url

def generate_campus_map_url() -> str:
    return f"https://yandex.ru/maps/?ll={ULSTU_COORDS}&z=17&l=map&pt={ULSTU_COORDS}"

def generate_campus_map_url() -> str:
    """Генерирует ссылку на карту кампуса УлГТУ"""
    return "https://yandex.ru/maps/org/ulgtu/1075847905/?ll=48.397200%2C54.318500&z=17"

@navigation_router.message(Command("navigation"))
@navigation_router.message(F.text == "🗺️ Навигация")
async def show_navigation_menu(message: Message):
    await message.answer(
        "🗺️ Навигация по олимпиаде:\n\n"
        "Здесь вы можете построить маршрут до УлГТУ и посмотреть карту кампуса.",
        reply_markup=get_navigation_keyboard()
    )

@navigation_router.callback_query(F.data == "nav_campus_map")
async def show_campus_map(callback: CallbackQuery):
    map_url = generate_campus_map_url()
    
    await callback.message.edit_text(
        "🗺️ Карта кампуса УлГТУ:\n\n"
        "📍 Ключевые точки:\n"
        "• 🎯 Точка кипения (основная площадка)\n"
        "• 🏢 Главный корпус УлГТУ\n"
        "• 🏢 Корпус 2\n"
        "• 🍽️ Столовая\n"
        "• 🏠 Общежитие\n\n"
        f"📎 Ссылка на карту: {map_url}",
        reply_markup=get_navigation_keyboard()
    )
    await callback.answer()

@navigation_router.callback_query(F.data == "nav_walking_route")
async def show_walking_routes(callback: CallbackQuery):
    text = "🚶 Пешие маршруты:\n\n"
    
    # Маршрут от ж/д вокзала
    station_url = generate_yandex_map_url(
        LOCATIONS["train_station"]["coords"],
        LOCATIONS["main_building"]["coords"],
        "pd"
    )
    text += f"📍 От ж/д вокзала: {station_url}\n\n"
    
    # Маршрут от автовокзала  
    bus_url = generate_yandex_map_url(
        LOCATIONS["bus_station"]["coords"], 
        LOCATIONS["main_building"]["coords"],
        "pd"
    )
    text += f"📍 От автовокзала: {bus_url}\n\n"
    
    text += "💡 Совет: пешая прогулка займет 15-20 минут"

    await callback.message.edit_text(text, reply_markup=get_navigation_keyboard())
    await callback.answer()

@navigation_router.callback_query(F.data == "nav_transport_route")
async def show_transport_routes(callback: CallbackQuery):
    text = "🚌 Маршруты на общественном транспорте:\n\n"
    
    # От ж/д вокзала
    station_url = generate_yandex_map_url(
        LOCATIONS["train_station"]["coords"],
        LOCATIONS["main_building"]["coords"], 
        "mt"
    )
    text += f"📍 От ж/д вокзала: {station_url}\n\n"
    
    # От автовокзала
    bus_url = generate_yandex_map_url(
        LOCATIONS["bus_station"]["coords"],
        LOCATIONS["main_building"]["coords"],
        "mt" 
    )
    text += f"📍 От автовокзала: {bus_url}\n\n"
    
    text += "🚎 Рекомендуемые маршруты:\n"
    text += "• Автобусы: 1, 28, 59\n"
    text += "• Маршрутки: 4, 13, 31"

    await callback.message.edit_text(text, reply_markup=get_navigation_keyboard())
    await callback.answer()

@navigation_router.callback_query(F.data == "nav_driving_route")
async def show_driving_routes(callback: CallbackQuery):
    text = "🚗 Маршруты на автомобиле:\n\n"
    
    # Универсальный маршрут
    driving_url = generate_yandex_map_url(
        "",  # Пустые координаты - Яндекс определит текущее местоположение
        LOCATIONS["main_building"]["coords"],
        "auto"
    )
    
    text += f"📍 Маршрут от вашего местоположения: {driving_url}\n\n"
    text += "📍 Адрес для навигатора:\n"
    text += "г. Ульяновск, ул. Северный Венец, 32\n\n"
    text += "🅿️ Парковка: доступна на территории кампуса"

    await callback.message.edit_text(text, reply_markup=get_navigation_keyboard())
    await callback.answer()