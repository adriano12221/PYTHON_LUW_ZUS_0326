class InvalidFuelAmountError(Exception):
    """Gdy ilość paliwa jest <= 0."""
    pass


class TankOverflowError(Exception):
    """Gdy próbujemy zatankować więcej niż wolne miejsce w baku."""
    pass


def main():
    capacity = 50.0
    fuel = 12.5
    price_per_liter = 6.49

    free_space = capacity - fuel

    print("=== STACJA PALIW ===")
    print(f"Pojemność baku: {capacity:.1f} L")
    print(f"Aktualny stan:  {fuel:.1f} L")
    print(f"Wolne miejsce:  {free_space:.1f} L")
    print(f"Cena paliwa:    {price_per_liter:.2f} PLN/L\n")

    liters = None

    try:
        raw = input("Podaj ile litrów chcesz zatankować: ").strip()
        liters = float(raw)  # może rzucić ValueError

        if liters <= 0:
            raise InvalidFuelAmountError("Ilość paliwa musi być większa od zera.")

        if liters > free_space:
            raise TankOverflowError(
                f"Za dużo paliwa. Maksymalnie możesz dolać: {free_space:.1f} L."
            )

    except ValueError:
        print("Błąd: podaj liczbę w formacie np. 10.5")

    except InvalidFuelAmountError as e:
        print("Błąd:", e)

    except TankOverflowError as e:
        print("Błąd:", e)

    else:
        # wykona się tylko jeśli nie było żadnego wyjątku
        fuel += liters
        cost = liters * price_per_liter

        print("\nTankowanie zakończone")
        print(f"Zatankowano:   {liters:.1f} L")
        print(f"Koszt:         {cost:.2f} PLN")
        print(f"Nowy stan baku:{fuel:.1f} L")

    finally:
        # wykona się zawsze, nawet przy błędzie
        print("\nOperacja zakończona.")


if __name__ == "__main__":
    main()
