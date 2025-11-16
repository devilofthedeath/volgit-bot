from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_faq_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🏆 Финал олимпиады", callback_data="faq_final")
    builder.button(text="📚 Дисциплины", callback_data="faq_disciplines")
    builder.button(text="📍 Локация", callback_data="faq_location") 
    builder.button(text="📋 Орг. вопросы", callback_data="faq_org")
    builder.button(text="🔙 Назад", callback_data="main_menu")
    builder.adjust(2)
    return builder.as_markup()

def get_faq_questions_keyboard(category: str, questions: dict):
    builder = InlineKeyboardBuilder()
    
    for q_id, q_data in questions.items():
        builder.button(text=q_data["question"], callback_data=f"faq_answer_{category}_{q_id}")
    
    builder.button(text="🔙 Назад", callback_data="faq_back")
    builder.adjust(1)
    return builder.as_markup()

def get_faq_back_keyboard(category: str = None):
    builder = InlineKeyboardBuilder()
    
    if category:
        builder.button(text="🔙 К вопросам", callback_data=f"faq_{category}")
    builder.button(text="📋 В меню FAQ", callback_data="faq_menu")
    
    return builder.as_markup()