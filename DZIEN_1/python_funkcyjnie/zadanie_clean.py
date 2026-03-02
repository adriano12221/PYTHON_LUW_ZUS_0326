
# =========================
# 1) FABRYKA FUNKCJI (closure)
# =========================
def make_scoring(base_points):

    def score(time):
        return base_points - time
    return score


# =========================
# 2) FUNKCJA PRZETWARZAJĄCA DANE (strategy pattern)
# =========================
def evaluate(results, scoring_function):
    evaluated = []

    for row in results:
        time = row["time"]
        points = scoring_function(time)
        new_row = {**row, "score": points}
        evaluated.append(new_row)
    return evaluated


# =========================
# 3) TEST NA DANYCH Z ZADANIA
# =========================
if __name__ == "__main__":
    results = [
        {"name": "Anna", "time": 280},
        {"name": "Jan", "time": 310},
        {"name": "Maria", "time": 295},
    ]

    # Tworzymy dwie strategie punktacji (dwie różne funkcje score).
    elite_scoring = make_scoring(500)
    amateur_scoring = make_scoring(400)

    # Liczymy wyniki dla obu strategii.
    elite_scores = evaluate(results, elite_scoring)
    amateur_scores = evaluate(results, amateur_scoring)

    # Drukujemy porównanie.
    print("=== ELITE (base_points=500) ===")
    for r in elite_scores:
        print(r)

    print("\n=== AMATEUR (base_points=400) ===")
    for r in amateur_scores:
        print(r)


