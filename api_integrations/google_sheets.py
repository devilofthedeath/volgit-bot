import gspread
from decouple import config

class GoogleSheetsIntegration:
    """Альтернативный источник расписания"""
    
    def __init__(self):
        self.gc = gspread.service_account(filename='credentials.json')
    
    async def get_schedule_from_sheets(self, sheet_url: str) -> list:
        """Получить расписание из Google Sheets"""
        sheet = self.gc.open_by_url(sheet_url)
        worksheet = sheet.sheet1
        return worksheet.get_all_records()