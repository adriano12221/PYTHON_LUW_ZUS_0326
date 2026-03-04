class InvalidFuelAmountError(Exception):
    """Gdy ilość paliwa (w litrach) jest <= 0."""
    pass


class TankOverflowError(Exception):
    """Gdy próbujemy zatankować więcej niż wolne miejsce w baku."""
    pass


class InvalidCommandError(Exception):
    """Gdy komenda ma zły format (np. 'pln' bez kwoty)."""
    pass


def parse_command(raw: str, price_per_liter: float) -> float:
    """
    Zwraca liczbę litrów do zatankowania na podstawie wpisu użytkownika.

    Obsługiwane formaty:
    - "10.5"        -> 10.5 litra
    - "pln 100"     -> (100 / cena) litrów

    Rzuca:
    - ValueError (gdy nie da się sparsować liczby)
    - InvalidCommandError (gdy format komendy jest niepoprawny)
    """
    raw = raw.strip()

    if not raw:
        raise InvalidCommandError("Pusty input. Podaj liczbę litrów lub 'pln <kwota>' albo 'exit'.")

    parts = raw.split()

    # tryb "pln <kwota>"
    if parts[0].lower() == "pln":
        if len(parts) != 2:
            raise InvalidCommandError("Format: 'pln <kwota>', np. 'pln 100'.")
        amount_pln = float(parts[1])  # może rzucić ValueError
        liters = amount_pln / price_per_liter
        return liters

    # tryb "liczba litrów"
    if len(parts) == 1:
        return float(parts[0])  # może rzucić ValueError

    raise InvalidCommandError("Nieznany format. Podaj np. '12.5' albo 'pln 100' albo 'exit'.")


def main():
    capacity = 50.0
    fuel = 12.5
    price_per_liter = 6.49

    print("=== STACJA PALIW ===")
    print("Komendy:")
    print("  - wpisz liczbę litrów, np. 10.5")
    print("  - albo wpisz 'pln <kwota>', np. pln 100")
    print("  - zakończ: exit\n")

    while True:
        free_space = capacity - fuel

        print(f"\nPojemność baku: {capacity:.1f} L")
        print(f"Aktualny stan:  {fuel:.1f} L")
        print(f"Wolne miejsce:  {free_space:.1f} L")
        print(f"Cena paliwa:    {price_per_liter:.2f} PLN/L")

        raw = input("\nIle tankujesz? ").strip()

        if raw.lower() == "exit":
            print("Koniec. Szerokiej drogi!")
            break

        liters = None

        try:
            liters = parse_command(raw, price_per_liter)

            if liters <= 0:
                raise InvalidFuelAmountError("Ilość paliwa musi być większa od zera.")

            if liters > free_space:
                raise TankOverflowError(
                    f"Za dużo paliwa. Maksymalnie możesz dolać: {free_space:.1f} L."
                )

        except ValueError:
            print("Błąd: podaj liczbę w formacie np. 10.5 albo komendę 'pln 100'.")

        except InvalidCommandError as e:
            print("Błąd:", e)

        except InvalidFuelAmountError as e:
            print("Błąd:", e)

        except TankOverflowError as e:
            print("Błąd:", e)

        else:
            fuel += liters
            cost = liters * price_per_liter

            print("\nTankowanie zakończone")
            print(f"Zatankowano:    {liters:.2f} L")
            print(f"Koszt:          {cost:.2f} PLN")
            print(f"Nowy stan baku: {fuel:.2f} L")

        finally:
            print("Operacja zakończona.")


if __name__ == "__main__":
    main()
