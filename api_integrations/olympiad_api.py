import aiohttp
from decouple import config

class OlympiadAPI:
    def __init__(self):
        self.base_url = config('OLYMPIAD_API_URL', 'https://volga-it.org/api')
        self.api_key = config('OLYMPIAD_API_KEY')
    
    async def get_participant_data(self, olymp_id: str) -> dict:
        """Получить данные участника с сайта олимпиады"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/participants/{olymp_id}",
                headers={"Authorization": f"Bearer {self.api_key}"}
            ) as response:
                if response.status == 200:
                    return await response.json()
                return {}
    
    async def get_schedule(self) -> dict:
        """Получить актуальное расписание"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/schedule") as response:
                return await response.json()