import json
import os
import random
from exercices.base import BaseExercise


class DescriptionExercise(BaseExercise):
    """Упражнение на описание предмета"""

    def __init__(self):
        file_path = os.path.join(os.path.dirname(__file__), "..", "data", "texts.json")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            subjects = data.get("subjects", [])
        except:
            pass
        super().__init__(
            name="Описание предмета",
            description="Опишите предмет за 1-1.5 минуты",
            experience=25
        )
        self.subject = random.choice(subjects)

    async def execute(self, **kwargs):
        instructions = (
            f"🎯 *Упражнение: Описание предмета*\n\n"
            f"*Задание:* Опишите предмет: *{self.subject}*\n\n"
            f"*Требования:*\n"
            f"1. Перечислите все плюсы и минусы\n"
            f"2. Ваша речь должна длиться 1-1.5 минуты\n"
            f"3. Говорите четко и структурированно\n"
            f"4. Используйте связные предложения\n\n"
            f"*Цель:* Развить логику речи и способность импровизировать"
        )
        return {
            "text": instructions,
            "expect_voice": True,
            "data": {"subject": self.subject}
        }

    async def validate(self, voice_message) -> bool:
        # Проверяем, что речь длится от 50 до 100 секунд
        return 50 <= voice_message.duration <= 100