from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from keyboards.faq import get_faq_main_keyboard, get_faq_questions_keyboard, get_faq_back_keyboard
from data.faq_data import FAQ_DATA  # ← Импорт из отдельного файла

faq_router = Router()

@faq_router.message(Command("faq"))
@faq_router.message(F.text == "❓ FAQ")
async def show_faq_menu(message: Message):
    """Показывает главное меню FAQ"""
    await message.answer(
        "❓ Часто задаваемые вопросы:\nВыберите раздел:",
        reply_markup=get_faq_main_keyboard()
    )

@faq_router.callback_query(F.data == "faq_menu")
async def back_to_faq_menu(callback: CallbackQuery):
    """Возврат в главное меню FAQ"""
    await callback.message.edit_text(
        "❓ Часто задаваемые вопросы:\nВыберите раздел:",
        reply_markup=get_faq_main_keyboard()
    )
    await callback.answer()

@faq_router.callback_query(F.data == "faq_back")
async def back_to_faq_main(callback: CallbackQuery):
    """Возврат из ответа в меню FAQ"""
    await callback.message.edit_text(
        "❓ Часто задаваемые вопросы:\nВыберите раздел:",
        reply_markup=get_faq_main_keyboard()
    )
    await callback.answer()

@faq_router.callback_query(F.data.startswith("faq_"))
async def process_faq_category(callback: CallbackQuery):
    """Обрабатывает выбор категории FAQ"""
    # Убираем префикс "faq_"
    category = callback.data[4:]  # Берем все после "faq_"
    
    # Проверяем специальные случаи
    if category in ["menu", "back"]:
        await callback.answer()
        return
    
    if category in FAQ_DATA:
        section = FAQ_DATA[category]
        
        await callback.message.edit_text(
            f"{section['title']}:\nВыберите вопрос:",
            reply_markup=get_faq_questions_keyboard(category, section["questions"])
        )
    
    await callback.answer()

@faq_router.callback_query(F.data.startswith("faq_answer_"))
async def show_faq_answer(callback: CallbackQuery):
    """Показывает ответ на вопрос FAQ"""
    # Разбираем callback_data: faq_answer_{category}_{q_id}
    parts = callback.data.split("_")
    
    if len(parts) >= 4:
        category = parts[2]
        q_id = parts[3]
        
        if category in FAQ_DATA and q_id in FAQ_DATA[category]["questions"]:
            question_data = FAQ_DATA[category]["questions"][q_id]
            
            answer_text = question_data["answer"]
            if not answer_text:
                answer_text = "⚠️ Ответ на этот вопрос пока не заполнен. Обратитесь к организаторам."
            
            await callback.message.edit_text(
                f"❓ Вопрос: {question_data['question']}\n\n"
                f"💡 Ответ: {answer_text}",
                reply_markup=get_faq_back_keyboard(category)
            )
    
    await callback.answer()