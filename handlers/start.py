from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

# Импортируем напрямую из файла
from keyboards.main_menu import get_main_keyboard

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Добро пожаловать на финал олимпиады! 🎓\n"
        "Выберите нужный раздел:",
        reply_markup=get_main_keyboard()
    )

@start_router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer(
        "Главное меню:",
        reply_markup=get_main_keyboard()
    )

@start_router.message(F.text == "📞 Контакты")
async def show_contacts(message: Message):
    await message.answer(
        "📞 Контакты организаторов:\n\n"
        "📧 Email: olymp@ulstu.ru\n"
        "📱 Телефон: +7 (8422) 123-45-67\n"
        "📍 Адрес: г. Ульяновск, ул. Северный Венец, 32"
    )

@start_router.message(F.text == "👤 Профиль")
async def show_profile(message: Message):
    await message.answer("Раздел профиля в разработке...")