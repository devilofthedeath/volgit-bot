from db_handler.db_class import PostgresHandler
from api_integrations.olympiad_api import OlympiadAPI

class UserService:
    def __init__(self, db: PostgresHandler, olympiad_api: OlympiadAPI):
        self.db = db
        self.api = olympiad_api
    
    async def get_user_profile(self, telegram_id: int) -> dict:
        """Получить профиль пользователя (из БД + API)"""
        # 1. Ищем в локальной БД
        user_data = await self.db.get_user(telegram_id)
        
        # 2. Если есть olymp_id, дополняем данными с сайта
        if user_data and user_data.get('olymp_id'):
            olymp_data = await self.api.get_participant_data(user_data['olymp_id'])
            user_data.update(olymp_data)
        
        return user_data
    
    async def link_olymp_id(self, telegram_id: int, olymp_id: str) -> bool:
        """Привязать ID участника олимпиады"""
        # Валидация через API сайта
        is_valid = await self.api.validate_olymp_id(olymp_id)
        if is_valid:
            return await self.db.update_user_olymp_id(telegram_id, olymp_id)
        return False