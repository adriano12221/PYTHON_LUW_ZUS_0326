# Zadanie: dekorator, który zlicza wywołania i sumuje zwracane wyniki (jeśli są liczbami)

def accumulate_results(func):
    # Stan dekoratora (zamknięcie/closure):
    # Te zmienne będą "pamiętane" pomiędzy kolejnymi wywołaniami wrappera.
    call_count = 0
    total = 0.0

    def wrapper(*args, **kwargs):
        # nonlocal pozwala modyfikować zmienne zewnętrzne (z zakresu accumulate_results),
        # a nie tworzyć nowe lokalne o tych samych nazwach.
        nonlocal call_count, total

        # 1) Zwiększamy licznik wywołań
        call_count += 1

        # 2) Wywołujemy oryginalną funkcję z przekazanymi argumentami
        result = func(*args, **kwargs)

        # 3) Jeśli wynik jest liczbą, dodajemy do sumy
        if isinstance(result, (int, float)):
            total += float(result)

        # 4) Budujemy czytelny zapis argumentów do loga (opcjonalne, ale przydatne)
        args_str = ", ".join(map(str, args))  # argumenty pozycyjne
        kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())  # argumenty nazwane
        joined = ", ".join(x for x in (args_str, kwargs_str) if x)  # sklejamy, ignorując puste

        # 5) Wypisujemy informację po wywołaniu
        print(f"[CALL #{call_count}] {func.__name__}({joined}) -> {result} | total={total}")

        # 6) Zwracamy wynik bez zmian, żeby funkcja zachowała swoje działanie
        return result

    # Zwracamy funkcję-owijkę, która zastąpi oryginalną funkcję po dekoracji
    return wrapper


# Dwie funkcje do udekorowania

@accumulate_results
def vat(price, rate=0.23):
    """Zwraca kwotę VAT dla podanej ceny i stawki."""
    return price * rate


@accumulate_results
def discount(price, percent):
    """Zwraca cenę po rabacie procentowym."""
    return price * (1 - percent / 100)


# Testy (przykładowe wywołania)

vat(100)              # 23.0
vat(200)              # 46.0
discount(300, 10)      # 270.0
discount(120, 25)      # 90.0
vat(50, rate=0.08)     # 4.0
