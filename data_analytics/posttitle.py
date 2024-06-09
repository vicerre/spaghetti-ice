from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class PostTitle:
    type: str
    index: int

    INDEX_LENGTH = 3

    def format(self):
        keystr = f"{self.index:0{self.INDEX_LENGTH}}"
        return f"{self.type.capitalize()} {keystr}"


@dataclass(frozen=True)
class TitleDiff:
    before: PostTitle
    after: PostTitle
