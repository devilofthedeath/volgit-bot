class PostgresHandler:
    async def log_user_query(self, user_id: int, query_type: str, query_text: str):
        """Логирование статистики запросов"""
        await self.execute(
            "INSERT INTO user_queries (user_id, query_type, query_text) VALUES ($1, $2, $3)",
            user_id, query_type, query_text
        )
    
    async def get_popular_questions(self, limit: int = 10) -> list:
        """Какие вопросы задают чаще (для аналитики)"""
        return await self.fetch(
            "SELECT query_text, COUNT(*) as count FROM user_queries "
            "WHERE query_type = 'faq' GROUP BY query_text ORDER BY count DESC LIMIT $1",
            limit
        )