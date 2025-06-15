lang = "eng"

if lang == "eng":
    CATEGORIES = [
        (150, "Brilliant: A move of exceptional precision and rare depth"),
        (90,  "Excellent: A non-obvious decision with strong strategic effect"),
        (50,  "Great: One of the best options in the position"),
        (20,  "Good: A solid move that strengthens the position"),
        (5,   "OK: Safe, but passive"),
        (0,   "Reasonable: Doesn’t improve or worsen the situation"),
        (-50, "Inaccuracy: A missed opportunity"),
        (-150, "Mistake: A significant oversight"),
        (-1000, "Blunder: A critical mistake")
    ]
elif lang == "rus":
    CATEGORIES = [
        (150, "Блестяще: Ход исключительной точности и редкой глубины"),
        (90,  "Выдающийся: Неочевидное решение с сильным стратегическим эффектом"),
        (50,  "Сильный: Один из лучших вариантов в позиции"),
        (20,  "Хороший: Грамотный ход, укрепляющий позиции"),
        (5,   "Приемлемый: Безопасно, но пассивно"),
        (0,   "Нейтральный: Не улучшает и не ухудшает ситуацию"),
        (-50, "Неточность: Упущенная возможность"),
        (-150, "Ошибка: Существенный просчёт"),
        (-1000, "Промах: Критическая ошибка")
    ]

def categorize(score_diff):
    for threshold, category in CATEGORIES:
        if score_diff >= threshold:
            return category
    return CATEGORIES[-1][1]
