import asyncio
import logging
from create_bot import bot, dp, scheduler

# роутеры
from handlers.start import start_router
from handlers.faq import faq_router
from handlers.schedule import schedule_router
from handlers.navigation import navigation_router
from handlers.schedule_handlers import schedule_router

# сервисы
from services import schedule_service
from services.schedule_service import ScheduleService
from utils.file_manager import ensure_directories

async def main():
    ensure_directories()

    await schedule_service.initialize()

    # Регистрируем роутеры
    dp.include_router(start_router)
    dp.include_router(faq_router)
    dp.include_router(schedule_router)
    dp.include_router(navigation_router)
    scheduler.start()
    
    print("Бот запущен!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")