from typing import Callable, List, Dict, Any

# =========================
# 1) FABRYKA FUNKCJI (closure)
# =========================
def make_scoring(base_points: int) -> Callable[[int], int]:
    """
    Funkcja wyższego rzędu: tworzy i zwraca funkcję punktującą.

    Parametry:
        base_points (int): bazowa liczba punktów (np. 500 dla elity)

    Zwraca:
        score(time: int) -> int:
            Funkcja, która dla podanego czasu (w minutach) wylicza punkty.

    Ważne:
    - make_scoring NIE liczy punktów sama.
    - Ona tworzy funkcję score, która "zapamiętuje" base_points (to jest closure).
    """

    def score(time: int) -> int:
        """
        Funkcja punktująca (czysta): na podstawie czasu wylicza wynik.

        Reguła podstawowa:
            punkty = base_points - time

        Dla zadania głównego nie ma tu żadnych efektów ubocznych:
        - nie ma printów
        - nie modyfikuje globali
        - zawsze zwraca wynik zależny tylko od wejścia
        """
        return base_points - time

    # Zwracamy funkcję score (nie wywołujemy jej tutaj!)
    return score


# =========================
# 2) FUNKCJA PRZETWARZAJĄCA DANE (strategy pattern)
# =========================
def evaluate(results: List[Dict[str, Any]], scoring_function: Callable[[int], int]) -> List[Dict[str, Any]]:
    """
    Funkcja przyjmuje:
    - results: listę słowników z danymi zawodników
    - scoring_function: funkcję, która umie policzyć punkty z czasu

    Zwraca:
    - NOWĄ listę słowników, gdzie każdy słownik ma dodane pole 'score'

    Cel:
    - oddzielić logikę "jak liczyć punkty" (scoring_function)
      od logiki "jak przetwarzać listę wyników" (evaluate)
    """

    evaluated: List[Dict[str, Any]] = []

    for row in results:
        # Wyciągamy czas zawodnika z bieżącego rekordu.
        time = row["time"]

        # Liczymy punkty używając przekazanej strategii (funkcji).
        points = scoring_function(time)

        # Tworzymy nowy słownik, żeby NIE mutować oryginalnych danych wejściowych.
        # Dzięki temu evaluate jest bezpieczne i przewidywalne.
        new_row = {**row, "score": points}

        # Dodajemy do listy wynikowej.
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


