from __future__ import annotations

from functools import reduce, partial
from typing import Callable, Dict, Any, Iterable, List


# ============================================================
# 1) FABRYKA FUNKCJI (closure) – WERSJA ROZSZERZONA (BONUS)
# ============================================================
def make_scoring(base_points: int, penalty_threshold: int = 300) -> Callable[[int], int]:
    """
    Zwraca funkcję score(time) wyliczającą punkty z czasu.

    Reguła:
    - jeśli time <= penalty_threshold:
        points = base_points - time
    - jeśli time > penalty_threshold:
        nadwyżka ponad próg karana podwójnie

      points_at_threshold = base_points - penalty_threshold
      points = points_at_threshold - 2 * (time - penalty_threshold)
    """

    def score(time: int) -> int:
        if time <= penalty_threshold:
            return base_points - time

        extra = time - penalty_threshold
        points_at_threshold = base_points - penalty_threshold
        return points_at_threshold - 2 * extra

    return score


# ============================================================
# 2) KOMPOZYCJA / PIPELINE
# ============================================================
def pipe(data: Any, *steps: Callable[[Any], Any]) -> Any:
    """
    Przepuszcza data przez kolejne kroki (funkcje) od lewej do prawej.

    pipe(x, f, g, h)  ==  h(g(f(x)))

    Dzięki temu mamy czytelny "pipeline" przetwarzania.
    """
    return reduce(lambda acc, fn: fn(acc), steps, data)


# ============================================================
# 3) MAŁE, CZYSTE KROKI PIPELINE
# ============================================================
def add_score(scoring: Callable[[int], int], row: Dict[str, Any]) -> Dict[str, Any]:
    """
    Zwraca NOWY rekord z dodanym polem 'score'.
    Nie mutuje row.
    """
    return {**row, "score": scoring(row["time"])}


def evaluate(scoring: Callable[[int], int], rows: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Funkcyjna wersja evaluate: mapujemy add_score po wszystkich rekordach.
    """
    return list(map(partial(add_score, scoring), rows))


def sort_by_score_desc(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Zwraca nową listę posortowaną malejąco po score.
    """
    return sorted(rows, key=lambda r: r["score"], reverse=True)


def format_table(rows: List[Dict[str, Any]]) -> str:
    """
    Prosta tabelka tekstowa do natychmiastowego pokazania wyniku.
    """
    if not rows:
        return "(brak danych)"

    name_w = max(len(r["name"]) for r in rows)
    header = f"{'NAME'.ljust(name_w)} | TIME | SCORE"
    line = "-" * len(header)

    body = "\n".join(
        f"{r['name'].ljust(name_w)} | {str(r['time']).rjust(4)} | {str(r['score']).rjust(5)}"
        for r in rows
    )

    return f"{header}\n{line}\n{body}"


# ============================================================
# 4) DEMO / TESTY
# ============================================================
if __name__ == "__main__":
    # Dane wejściowe (jak w zadaniu)
    results = [
        {"name": "Anna", "time": 280},
        {"name": "Jan", "time": 310},
        {"name": "Maria", "time": 295},
    ]

    # Strategie punktacji (closure)
    elite_scoring = make_scoring(base_points=500, penalty_threshold=300)
    amateur_scoring = make_scoring(base_points=400, penalty_threshold=300)

    # PIPELINE: dane -> evaluate -> sort -> format
    elite_report = pipe(
        results,
        partial(evaluate, elite_scoring),
        sort_by_score_desc,
        format_table,
    )

    amateur_report = pipe(
        results,
        partial(evaluate, amateur_scoring),
        sort_by_score_desc,
        format_table,
    )

    print("=== ELITE (base=500, threshold=300, double penalty above) ===")
    print(elite_report)

    print("\n=== AMATEUR (base=400, threshold=300, double penalty above) ===")
    print(amateur_report)

    # Mini-testy (assert) – super na szkoleniu
    elite_scored = evaluate(elite_scoring, results)
    expected_elite = {"Anna": 220, "Maria": 205, "Jan": 180}
    assert {r["name"]: r["score"] for r in elite_scored} == expected_elite

    amateur_scored = evaluate(amateur_scoring, results)
    expected_amateur = {"Anna": 120, "Maria": 105, "Jan": 80}
    assert {r["name"]: r["score"] for r in amateur_scored} == expected_amateur

    print("\nTesty przeszły (assert).")
