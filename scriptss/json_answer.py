import json
import re
from ast import literal_eval

def text_json_answer(text_with_json: str) -> str:
    json_match = re.search(r'\{[\s\S]*\}', text_with_json)
    if not json_match:
        return 0, 0

    json_raw = json_match.group(0)

    try:
        data = json.loads(json_raw)
    except json.JSONDecodeError:
        try:
            data = literal_eval(json_raw)
        except Exception:
            return 0, 0

    if isinstance(data, dict) and "error" in data:
        return f"⚠️ {data['error']}", 1

    try:
        lines = []
        lines.append(f"🏆 <b>Матч:</b> {data['teams']}")
        lines.append("\n📊 <b>Форма команд:</b>")
        for team, form in data["form"].items():
            lines.append(f"- {team}: {form}")

        lines.append("\n📈 <b>Статистика:</b>")
        for team, stats in data["stats"].items():
            lines.append(f"- {team}: {stats}")

        lines.append("\n🧑‍💼 <b>Ключевые игроки и состав:</b>")
        for team, info in data["key_players"].items():
            lines.append(f"- {team}: {info}")

        lines.append(f"\n🤝 <b>Личные встречи:</b>\n{data['head_to_head']}")
        lines.append(f"\n🌍 <b>Контекст матча:</b>\n{data['context']}")
        lines.append(f"\n💸 <b>Тренды ставок:</b>\n{data['betting_trends']}")

        lines.append("\n✅ <b>Рекомендуемые ставки:</b>")
        for bet in data["recommended_bets"]:
            lines.append(f"- {bet}")

        lines.append(f"\n⚠️ <b>Потенциальные риски:</b>\n{data['risks']}")

        prediction = data["prediction"]
        lines.append("\n📌 <b>Прогноз:</b>")
        lines.append(f"- Победитель: {prediction['winner']}")
        lines.append(f"- Уверенность: {prediction['confidence']}")
        lines.append(f"- Обоснование: {prediction['reason']}")

        return "\n".join(lines), 1

    except Exception as e:
        return f"❌ Ошибка при обработке JSON: {e}", 0

