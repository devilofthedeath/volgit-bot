import os
import shutil

def ensure_directories():
    """Создает необходимые директории"""
    os.makedirs("schedule_images", exist_ok=True)

def cleanup_old_files():
    """Очищает старые файлы расписаний"""
    if os.path.exists("schedule_images"):
        shutil.rmtree("schedule_images")
    ensure_directories()