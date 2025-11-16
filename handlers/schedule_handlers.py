from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
import os

from services.schedule_service import schedule_service
from keyboards.schedule import get_schedule_main_keyboard, get_schedule_back_keyboard

schedule_router = Router()

@schedule_router.message(Command("schedule"))
@schedule_router.message(F.text == "📅 Расписание")
async def show_schedule_menu(message: Message):
    """Показывает меню расписания"""
    await message.answer(
        "📅 Выберите вариант расписания:",
        reply_markup=get_schedule_main_keyboard()
    )

@schedule_router.callback_query(F.data.startswith("schedule_"))
async def handle_schedule_request(callback: CallbackQuery):
    """Обрабатывает запросы на расписание"""
    action = callback.data
    
    await callback.answer()
    
    if action == "schedule_back":
        # Удаляем предыдущее сообщение и отправляем новое
        try:
            await callback.message.delete()
        except:
            pass  # Игнорируем ошибки удаления
        
        await callback.message.answer(
            "📅 Выберите вариант расписания:",
            reply_markup=get_schedule_main_keyboard()
        )
        return
    
    # Показываем "Генерируем..."
    generating_msg = await callback.message.answer("🔄 Генерируем расписание...")
    
    image_path = None
    
    if action == "schedule_18.11":
        image_path = await schedule_service.generate_daily_schedule_image("18.11")
        caption = "📅 Расписание на 18 ноября"
    
    elif action == "schedule_19.11":
        image_path = await schedule_service.generate_daily_schedule_image("19.11")
        caption = "📅 Расписание на 19 ноября"
    
    elif action == "schedule_20.11":
        image_path = await schedule_service.generate_daily_schedule_image("20.11")
        caption = "📅 Расписание на 20 ноября"
    
    elif action == "schedule_overview":
        image_path = await schedule_service.generate_overview_image()
        caption = "📊 Обзорное расписание на все дни"
    
    elif action == "schedule_volga_it":
        image_path = await schedule_service.generate_volga_it_image()
        caption = "🎯 Расписание финала Волга-IT"
    
    # Удаляем сообщение "Генерируем..."
    try:
        await generating_msg.delete()
    except:
        pass
    
    if image_path and os.path.exists(image_path):
        # Отправляем PNG файл
        photo = FSInputFile(image_path)
        await callback.message.answer_photo(
            photo=photo,
            caption=caption,
            reply_markup=get_schedule_back_keyboard()
        )
    else:
        await callback.message.answer(
            "❌ Не удалось сгенерировать расписание. Попробуйте позже.",
            reply_markup=get_schedule_back_keyboard()
        )

@schedule_router.callback_query(F.data == "main_menu")
async def back_to_main_menu(callback: CallbackQuery):
    await callback.answer()
    try:
        await callback.message.delete()
    except:
        pass
    
    from keyboards.main_menu import get_main_keyboard
    await callback.message.answer(
        "Главное меню:",
        reply_markup=get_main_keyboard()
    )