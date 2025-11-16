from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Event:
    date: str
    start_time: str
    end_time: str
    location: str
    title: str
    event_type: str
    color: Optional[str] = None

@dataclass
class Schedule:
    events: List[Event]
    last_updated: str

@dataclass
class User:
    telegram_id: int
    name: str
    olymp_id: Optional[str] = None
    discipline: Optional[str] = None