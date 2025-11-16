import os
import sys
from .xlsx_parser import XLSXParser

def main():
    """Главная функция для тестирования парсера"""
    print("🚀 Запуск XLSX парсера расписания")
    print("=" * 50)
    
    # Путь к файлу (поместите ваш schedule.xlsx в эту папку)
    file_path = "schedule.xlsx"
    
    if not os.path.exists(file_path):
        print(f"❌ Файл {file_path} не найден!")
        print("Поместите ваш schedule.xlsx в папку с парсером")
        return
    
    # Создаем парсер и парсим файл
    parser = XLSXParser()
    schedule = parser.parse_file(file_path)
    
    # Показываем результаты
    print("\n" + "=" * 50)
    print("📊 РЕЗУЛЬТАТЫ ПАРСИНГА:")
    print("=" * 50)
    
    # Показываем события по датам
    for date in ["18.11", "19.11", "20.11"]:
        date_events = [e for e in schedule.events if e.date == date]
        print(f"\n📅 {date}: {len(date_events)} событий")
        for event in date_events[:3]:  # Показываем первые 3 события каждой даты
            print(f"   • {event.start_time} | {event.location} | {event.title}")
        if len(date_events) > 3:
            print(f"   ... и еще {len(date_events) - 3} событий")
    
    # Статистика по типам событий
    print(f"\n📈 СТАТИСТИКА:")
    event_types = {}
    for event in schedule.events:
        event_types[event.event_type] = event_types.get(event.event_type, 0) + 1
    
    for event_type, count in event_types.items():
        print(f"   {event_type}: {count} событий")

if __name__ == "__main__":
    main()