import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
from datetime import datetime

class ScheduleVisualizer:
    def __init__(self):
        # Цвета для типов событий
        self.event_colors = {
            "Неделя инноваций": "#CCFFCC",      # зеленый
            "Волга-IT": "#CCFFFF",              # голубой
            "Студенческие СКБ": "#FFFFCC",      # желтый
            "Молодёжные метавселенные": "#CCCCFF",  # фиолетовый
            "Другое": "#F0F0F0"                 # серый
        }
        
        # Настройки внешнего вида
        self.cell_height = 0.8
        self.cell_width = 2.5

    def create_daily_schedule(self, events, date, output_path):
        """Создает расписание на один день"""
        # Фильтруем события по дате
        day_events = [e for e in events if e.date == date]
        
        if not day_events:
            print(f"❌ Нет событий для даты {date}")
            return False
        
        # Группируем события по времени и месту
        time_slots = sorted(set(e.start_time for e in day_events))
        locations = sorted(set(e.location for e in day_events))
        
        # Создаем figure
        fig, ax = plt.subplots(figsize=(max(16, len(locations) * 1.5), 12))
        
        # Заголовок
        title = f"Расписание на {date}"
        plt.suptitle(title, fontsize=16, fontweight='bold', y=0.95)
        
        # Сетка: время по вертикали, места по горизонтали
        for i, time_slot in enumerate(time_slots):
            y_pos = len(time_slots) - i - 1
            
            # Время
            ax.text(-0.5, y_pos, time_slot, ha='right', va='center', 
                   fontsize=10, fontweight='bold')
            
            for j, location in enumerate(locations):
                x_pos = j
                
                # Находим событие в этой ячейке
                cell_events = [e for e in day_events 
                             if e.start_time == time_slot and e.location == location]
                
                if cell_events:
                    event = cell_events[0]
                    color = self.event_colors.get(event.event_type, "#F0F0F0")
                    
                    # Рисуем ячейку
                    rect = patches.Rectangle(
                        (x_pos - 0.4, y_pos - 0.4), 
                        self.cell_width - 0.2, 
                        self.cell_height - 0.2,
                        linewidth=1, 
                        edgecolor='black',
                        facecolor=color,
                        alpha=0.8
                    )
                    ax.add_patch(rect)
                    
                    # Текст события (обрезаем если длинный)
                    event_text = self._wrap_text(event.title, 25)
                    ax.text(x_pos, y_pos, event_text, 
                           ha='center', va='center', fontsize=8, wrap=True)
                    
                    # Тип события маленьким шрифтом
                    ax.text(x_pos, y_pos - 0.25, event.event_type, 
                           ha='center', va='center', fontsize=6, color='gray', style='italic')
                else:
                    # Пустая ячейка
                    rect = patches.Rectangle(
                        (x_pos - 0.4, y_pos - 0.4), 
                        self.cell_width - 0.2, 
                        self.cell_height - 0.2,
                        linewidth=0.5, 
                        edgecolor='lightgray',
                        facecolor='white',
                        alpha=0.3
                    )
                    ax.add_patch(rect)
        
        # Настройка осей
        ax.set_xlim(-1, len(locations))
        ax.set_ylim(-1, len(time_slots))
        
        # Подписи мест
        ax.set_xticks(range(len(locations)))
        ax.set_xticklabels([self._wrap_text(loc, 15) for loc in locations], 
                          rotation=45, ha='right', fontsize=9)
        
        # Убираем цифры на оси Y (время уже подписано)
        ax.set_yticks(range(len(time_slots)))
        ax.set_yticklabels([])
        
        # Сетка
        ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
        
        # Легенда
        self._add_legend(ax)
        
        # Сохраняем
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close()
        
        print(f"✅ Создано расписание: {output_path}")
        return True

    def create_overview_schedule(self, events, output_path):
        """Создает обзорное расписание на все дни"""
        fig, axes = plt.subplots(1, 3, figsize=(24, 14))
        
        dates = ["18.11", "19.11", "20.11"]
        
        for idx, date in enumerate(dates):
            ax = axes[idx]
            day_events = [e for e in events if e.date == date]
            
            if not day_events:
                ax.text(0.5, 0.5, f"Нет событий\nна {date}", 
                       ha='center', va='center', fontsize=14, style='italic')
                ax.set_title(f"Расписание на {date}", fontsize=12, fontweight='bold')
                continue
            
            # Упрощенная версия для обзора - берем основные временные слоты
            all_times = sorted(set(e.start_time for e in day_events))
            time_slots = all_times[:10]  # первые 10 времен
            
            # Группируем события по времени
            for i, time_slot in enumerate(time_slots):
                y_pos = len(time_slots) - i - 1
                
                # Время
                ax.text(-1.5, y_pos, time_slot, ha='right', va='center', 
                       fontsize=9, fontweight='bold')
                
                time_events = [e for e in day_events if e.start_time == time_slot]
                
                for j, event in enumerate(time_events[:4]):  # первые 4 события в этом времени
                    x_pos = j * 3
                    color = self.event_colors.get(event.event_type, "#F0F0F0")
                    
                    # Упрощенный блок
                    rect = patches.Rectangle(
                        (x_pos, y_pos - 0.3), 2.8, 0.6,
                        linewidth=1, edgecolor='black', facecolor=color, alpha=0.8
                    )
                    ax.add_patch(rect)
                    
                    # Сокращенный текст
                    short_title = self._wrap_text(event.title, 25)
                    ax.text(x_pos + 1.4, y_pos, short_title, 
                           ha='center', va='center', fontsize=7, wrap=True)
                    
                    # Место проведения маленьким шрифтом
                    short_location = self._wrap_text(event.location, 20)
                    ax.text(x_pos + 1.4, y_pos - 0.15, short_location, 
                           ha='center', va='center', fontsize=5, color='gray')
            
            ax.set_title(f"Расписание на {date}\n({len(day_events)} событий)", 
                        fontsize=12, fontweight='bold')
            ax.set_xlim(-2, 12)
            ax.set_ylim(-1, len(time_slots))
            ax.grid(True, alpha=0.2)
        
        plt.suptitle("ОБЗОР РАСПИСАНИЯ - ВОЛГА-IT & НЕДЕЛЯ ИННОВАЦИЙ", 
                    fontsize=18, fontweight='bold', y=0.95)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Создан обзор: {output_path}")
        return True

    def create_volga_it_schedule(self, events, output_path):
        """Создает расписание только для событий Волга-IT"""
        volga_events = [e for e in events if e.event_type == "Волга-IT"]
        
        if not volga_events:
            print("❌ Нет событий Волга-IT")
            return False
        
        fig, axes = plt.subplots(1, 3, figsize=(20, 12))
        dates = ["18.11", "19.11", "20.11"]
        
        for idx, date in enumerate(dates):
            ax = axes[idx]
            day_events = [e for e in volga_events if e.date == date]
            
            if not day_events:
                ax.text(0.5, 0.5, f"Нет событий Волга-IT\nна {date}", 
                       ha='center', va='center', fontsize=12, style='italic')
                continue
            
            time_slots = sorted(set(e.start_time for e in day_events))
            
            for i, time_slot in enumerate(time_slots):
                y_pos = len(time_slots) - i - 1
                ax.text(-1, y_pos, time_slot, ha='right', va='center', 
                       fontsize=9, fontweight='bold')
                
                time_events = [e for e in day_events if e.start_time == time_slot]
                
                for j, event in enumerate(time_events):
                    x_pos = j * 4
                    color = "#CCFFFF"  # Голубой для Волга-IT
                    
                    rect = patches.Rectangle(
                        (x_pos, y_pos - 0.3), 3.8, 0.6,
                        linewidth=1, edgecolor='black', facecolor=color, alpha=0.8
                    )
                    ax.add_patch(rect)
                    
                    short_title = self._wrap_text(event.title, 30)
                    ax.text(x_pos + 1.9, y_pos, short_title, 
                           ha='center', va='center', fontsize=8, wrap=True)
                    
                    ax.text(x_pos + 1.9, y_pos - 0.15, event.location, 
                           ha='center', va='center', fontsize=6, color='gray')
            
            ax.set_title(f"Волга-IT на {date}\n({len(day_events)} событий)", 
                        fontsize=11, fontweight='bold')
            ax.set_xlim(-1.5, 16)
            ax.set_ylim(-1, len(time_slots))
        
        plt.suptitle("РАСПИСАНИЕ ФИНАЛА МЕЖДУНАРОДНОЙ ЦИФРОВОЙ ОЛИМПИАДЫ «ВОЛГА-IT»", 
                    fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Создано расписание Волга-IT: {output_path}")
        return True

    def _wrap_text(self, text, max_length):
        """Переносит длинный текст"""
        if len(text) <= max_length:
            return text
        
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= max_length:
                current_line += " " + word if current_line else word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
                if len(word) > max_length:
                    # Если слово слишком длинное, разбиваем его
                    current_line = word[:max_length-3] + "..."
        
        if current_line:
            lines.append(current_line)
        
        return "\n".join(lines)

    def _add_legend(self, ax):
        """Добавляет легенду"""
        legend_elements = []
        for event_type, color in self.event_colors.items():
            if event_type != "Другое":  # Показываем только основные типы
                legend_elements.append(
                    patches.Patch(facecolor=color, edgecolor='black', 
                                label=event_type, alpha=0.8)
                )
        
        ax.legend(handles=legend_elements, loc='upper left', 
                 bbox_to_anchor=(1, 1), fontsize=10, title="Типы событий",
                 title_fontsize=11)