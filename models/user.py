from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from datetime import datetime, date


@dataclass
class User:
    user_id: int
    username: str
    first_name: str
    last_name: str
    registered_at: str
    last_active: str
    streak_days: int = 0
    total_experience: int = 0
    completed_today: bool = False
    last_completed_date: Optional[str] = None
    notification_times: List[str] = None
    notifications_enabled: bool = True
    current_course: str = "speech"
    course_experience: Dict[str, int] = None

    def __post_init__(self):
        if self.notification_times is None:
            self.notification_times = ["09:00", "13:00", "19:00"]
        if self.course_experience is None:
            self.course_experience = {"speech": 0}

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def check_streak_update(self):
        """Обновляет серию дней"""
        today = date.today().isoformat()

        if self.last_completed_date == today:
            return False

        if self.last_completed_date:
            last_date = date.fromisoformat(self.last_completed_date)
            days_diff = (date.today() - last_date).days

            if days_diff == 1:
                self.streak_days += 1
            elif days_diff > 1:
                self.streak_days = 1
            else:
                return False
        else:
            self.streak_days = 1

        self.last_completed_date = today
        self.completed_today = True
        return True