import datetime
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class Post:
    # Raw post content
    content: str
    date: datetime.date
    # Are post contents encrypted
    encrypted: bool
    ext: str
    # Are post contents from external sources
    external: bool
    indices: List[int]
    path: Path
    slug: str
    # Actual rendered text
    text: str
    # Post type
    type: str
