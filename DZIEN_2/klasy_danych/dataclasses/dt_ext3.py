from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
import json
import math
import datetime as dt

@dataclass
class ShoppingCart:a
    owner: str
    items: List[str] = field(default_factory=list)
    discounts: Dict[str, float] = field(default_factory=dict)

    def add(self, item: str) -> None:
        self.items.append(item)

    def add_discount(self, code: str, percent: float) -> None:
        if not (0.0 < percent < 40.0):
            raise ValueError("percent must be in (0, 40)")
        self.discounts[code] = percent

    def summary(self) -> str:
        return f"Cart(owner={self.owner}, items={len(self.items)}, discounts={len(self.discounts)})"
