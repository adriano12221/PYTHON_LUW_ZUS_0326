"""dataclasses_examples.py

4 przykłady dataclasses od podstaw.
Uruchom:
    python dataclasses_examples.py
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
import json
import math
import datetime as dt


# ============================================================
# 1) Najprostsza dataclass: przechowuje dane + ma metodę
# ============================================================

@dataclass
class User:
    username: str
    email: str
    is_active: bool = True

    def contact_card(self) -> str:
        return f"{self.username} <{self.email}> | active={self.is_active}"


# ============================================================
# 2) Defaulty, default_factory i "mutable defaults"
#    (lista/słownik ZAWSZE przez field(default_factory=...))
# ============================================================

@dataclass
class ShoppingCart:
    owner: str
    items: List[str] = field(default_factory=list)
    discounts: Dict[str, float] = field(default_factory=dict)

    def add(self, item: str) -> None:
        self.items.append(item)

    def add_discount(self, code: str, percent: float) -> None:
        if not (0.0 < percent < 100.0):
            raise ValueError("percent must be in (0, 100)")
        self.discounts[code] = percent

    def summary(self) -> str:
        return f"Cart(owner={self.owner}, items={len(self.items)}, discounts={len(self.discounts)})"


# ============================================================
# 3) Frozen + ordering: niemutowalny obiekt, sortowanie, hash
# ============================================================

@dataclass(frozen=True, order=True, slots=True)
class Money:
    """Prosty value object: kwota w groszach + waluta.

    - frozen=True: niemutowalne (bez przypadkowych zmian)
    - order=True: można sortować (wg pól w kolejności definicji)
    - slots=True: mniejszy narzut pamięci (dla wielu obiektów)
    """
    cents: int
    currency: str = "PLN"

    def __post_init__(self) -> None:
        # W frozen dataclass nie możemy przypisywać normalnie,
        # ale walidować możemy, a ewentualną normalizację robi się przez object.__setattr__.
        if self.cents < 0:
            raise ValueError("cents cannot be negative")
        cur = self.currency.strip().upper()
        if not cur:
            raise ValueError("currency cannot be empty")
        object.__setattr__(self, "currency", cur)

    @property
    def value(self) -> float:
        return self.cents / 100.0

    def __str__(self) -> str:
        return f"{self.value:.2f} {self.currency}"


# ============================================================
# 4) Kompozycja + walidacja w __post_init__ + serializacja
#    (dataclass w dataclass, oraz asdict/json)
# ============================================================

@dataclass(slots=True)
class Point:
    x: float
    y: float

    def distance_to(self, other: Point) -> float:
        return math.hypot(self.x - other.x, self.y - other.y)


@dataclass(slots=True)
class RunSession:
    """Przykład 'obiektu domenowego' dla biegacza.

    - points: trasa jako lista punktów GPS (tu uproszczona 2D)
    - start_time: data/czas startu
    - note: opcjonalna notatka
    """
    athlete: str
    points: List[Point] = field(default_factory=list)
    start_time: dt.datetime = field(default_factory=lambda: dt.datetime.now(dt.timezone.utc))
    note: Optional[str] = None

    def __post_init__(self) -> None:
        # Walidacja domenowa
        if not self.athlete.strip():
            raise ValueError("athlete cannot be empty")
        if self.note is not None and len(self.note) > 200:
            raise ValueError("note too long (max 200 chars)")

    def add_point(self, x: float, y: float) -> None:
        self.points.append(Point(x, y))

    @property
    def distance(self) -> float:
        """Całkowita długość trasy (sumaryczna odległość między punktami)."""
        if len(self.points) < 2:
            return 0.0
        return sum(self.points[i].distance_to(self.points[i + 1]) for i in range(len(self.points) - 1))

    def to_json(self) -> str:
        """Serializacja do JSON (dataclasses -> dict -> JSON)."""
        payload = asdict(self)
        # asdict zamieni Point na dict automatycznie, ale datetime trzeba ujednolicić:
        payload["start_time"] = self.start_time.isoformat()
        return json.dumps(payload, ensure_ascii=False, indent=2)

    @staticmethod
    def from_json(data: str) -> RunSession:
        """Deserializacja z JSON do obiektu."""
        raw = json.loads(data)
        session = RunSession(
            athlete=raw["athlete"],
            start_time=dt.datetime.fromisoformat(raw["start_time"]),
            note=raw.get("note"),
        )
        for p in raw.get("points", []):
            session.points.append(Point(p["x"], p["y"]))
        return session


# ============================================================
# DEMO / MAIN
# ============================================================

def demo_1_user() -> None:
    print("\n[1] User")
    u = User("marcin", "marcin@example.com")
    print(u)
    print(u.contact_card())


def demo_2_cart() -> None:
    print("\n[2] ShoppingCart")
    cart = ShoppingCart("marcin")
    cart.add("coffee")
    cart.add("protein_bar")
    cart.add_discount("SPRING10", 10.0)
    print(cart.summary())
    print("items:", cart.items)
    print("discounts:", cart.discounts)


def demo_3_money() -> None:
    print("\n[3] Money (frozen + ordering + slots)")
    a = Money(12345, "pln")
    b = Money(500, "EUR")
    c = Money(999, "pln")
    print("a:", a, "| cents:", a.cents, "| currency:", a.currency)
    print("sorted:", [str(x) for x in sorted([a, b, c])])

    # a.cents = 1  # <- odkomentuj, żeby zobaczyć błąd (frozen dataclass)


def demo_4_runsession() -> None:
    print("\n[4] RunSession (kompozycja + __post_init__ + JSON)")
    s = RunSession("Marcin", note="lekki bieg regeneracyjny")
    # dodajemy kilka punktów (udawana trasa 2D)
    s.add_point(0.0, 0.0)
    s.add_point(1.0, 0.0)
    s.add_point(1.0, 1.0)
    s.add_point(2.0, 1.0)

    print("distance:", round(s.distance, 3))
    js = s.to_json()
    print("json:\n", js)

    restored = RunSession.from_json(js)
    print("restored distance:", round(restored.distance, 3))
    print("restored start_time:", restored.start_time.isoformat())


if __name__ == "__main__":
    demo_1_user()
    demo_2_cart()
    demo_3_money()
    demo_4_runsession()
