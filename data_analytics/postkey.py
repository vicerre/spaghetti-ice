from dataclasses import dataclass
from typing import List


@dataclass(frozen=True, order=True)
class PostKey:
    type: str
    indices: List[int]

    INDEX_LENGTH = 3

    def format(self):
        keystrs = [f"{index:0{self.INDEX_LENGTH}}" for index in self.indices]
        keystr = "-".join(keystrs)
        return f"{self.type}-{keystr}"


@dataclass(frozen=True)
class KeyDiff:
    before: PostKey
    after: PostKey
