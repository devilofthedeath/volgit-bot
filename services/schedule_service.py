import os
from typing import List, Optional
from core.models import Event
from parsers.xlsx_parser import WorkingParser
from visualizers.schedule_visualizer import ScheduleVisualizer
from visualizers.schedule_visualizer import ScheduleVisualizer  # ← Импорт из правильной папки

class ScheduleService:
    def __init__(self):
        self.parser = WorkingParser()
        self.visualizer = ScheduleVisualizer()
        self.events: List[Event] = []
        self.schedule_file = "schedule.xlsx"
        
    async def initialize(self):
        """Инициализация при старте бота"""
        if os.path.exists(self.schedule_file):
            self.events = self.parser.parse_file(self.schedule_file)
            print("✅ Расписание загружено")
        else:
            print("❌ Файл расписания не найден")
    
    async def get_events_by_date(self, date: str) -> List[Event]:
        """События по дате"""
        return [e for e in self.events if e.date == date]
    
    async def get_events_by_type(self, event_type: str) -> List[Event]:
        """События по типу"""
        return [e for e in self.events if e.event_type == event_type]
    
    async def generate_daily_schedule_image(self, date: str) -> Optional[str]:
        """Генерирует PNG для даты"""
        try:
            output_path = f"schedule_images/schedule_{date.replace('.', '')}.png"
            self.visualizer.create_daily_schedule(self.events, date, output_path)
            return output_path
        except Exception as e:
            print(f"❌ Ошибка генерации расписания: {e}")
            return None
    
    async def generate_overview_image(self) -> Optional[str]:
        """Генерирует обзорное PNG"""
        try:
            output_path = "schedule_images/schedule_overview.png"
            self.visualizer.create_overview_schedule(self.events, output_path)
            return output_path
        except Exception as e:
            print(f"❌ Ошибка генерации обзора: {e}")
            return None
    
    async def generate_volga_it_image(self) -> Optional[str]:
        """Генерирует PNG только Волга-IT"""
        try:
            output_path = "schedule_images/schedule_volga_it.png"
            self.visualizer.create_volga_it_schedule(self.events, output_path)
            return output_path
        except Exception as e:
            print(f"❌ Ошибка генерации Волга-IT: {e}")
            return None
        
schedule_service = ScheduleService()