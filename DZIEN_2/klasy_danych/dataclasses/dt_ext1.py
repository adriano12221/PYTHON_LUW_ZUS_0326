from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
import json
import math
import datetime as dt

@dataclass
class User:
    username: str
    email: str
    is_active: bool = True

    def contact_card(self) -> str:
        return f"{self.username} <{self.email}> | active={self.is_active}"
