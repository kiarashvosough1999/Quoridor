from dataclasses import dataclass, field
from typing import Any


@dataclass(order=True)
class PriorityQueueItem:
    priority: int
    move_array_tuple: Any = field(compare=False)
