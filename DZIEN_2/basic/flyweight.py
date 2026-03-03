from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar, Dict, Tuple


class Money(int):
    """
    Money to niemutowalny typ oparty o int, przechowuje kwotę w groszach (cents).
    Używamy __new__ bo int jest niemutowalny: wartość trzeba ustawić podczas tworzenia obiektu.
    
    Dodatkowo:
    - normalizujemy walutę do uppercase
    - cache'ujemy obiekty (flyweight), żeby te same wartości zwracały ten sam obiekt
    """

    _cache: ClassVar[Dict[Tuple[int, str], "Money"]] = {}

    def __new__(cls, cents: int, currency: str = "PLN"):
        # 1) Walidacja i normalizacja zanim obiekt powstanie
        if not isinstance(cents, int):
            raise TypeError("cents musi być int (kwota w groszach)")
        if cents < 0:
            raise ValueError("cents nie może być ujemne")

        if not isinstance(currency, str) or not currency.strip():
            raise ValueError("currency musi być niepustym stringiem")
        currency_norm = currency.strip().upper()

        key = (cents, currency_norm)

        # 2) Flyweight: jeśli już istnieje, zwróć istniejący obiekt
        if key in cls._cache:
            return cls._cache[key]

        # 3) Realne utworzenie obiektu int: tu powstaje obiekt
        obj = super().__new__(cls, cents)

        # 4) Doczepiamy dodatkowy atrybut (int normalnie go nie ma)
        obj.currency = currency_norm

        # 5) Zapis do cache
        cls._cache[key] = obj
        return obj

    def __repr__(self) -> str:
        return f"Money({int(self)} cents, {self.currency})"

    @property
    def zl(self) -> float:
        """Wygodny podgląd w złotówkach."""
        return int(self) / 100.0


# --- Demo ---
m1 = Money(12345, "pln")
m2 = Money(12345, "PLN")
m3 = Money(500, "eur")

print(m1)              # Money(12345 cents, PLN)
print(m1.zl)           # 123.45
print(m3)              # Money(500 cents, EUR)

print(m1 is m2)        # True  (cache)
print(int(m1) + 55)    # 12400  (bo to jest też int)
