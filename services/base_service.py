from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

class BaseService(ABC):
    """Абстрактный базовый сервис"""
    
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        pass
    
    @abstractmethod
    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def update(self, id: int, data: Dict[str, Any]) -> bool:
        pass