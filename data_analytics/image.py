import datetime
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class Image:
    date: datetime.date
    ext: str
    indices: List[int]
    path: Path
    # Post type
    type: str
