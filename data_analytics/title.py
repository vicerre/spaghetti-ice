import datetime
from dataclasses import dataclass
from pathlib import Path
from typing import List

DATE_FORMAT = "%Y-%m-%d"


@dataclass
class Title:
    date: datetime.date
    ext: str
    indices: List[int]
    slug: str
    type: str

    INDEX_LENGTH = 3

    def format(self):
        datestr = self.date.strftime(DATE_FORMAT)

        strindices = [f"{index:0{self.INDEX_LENGTH}}" for index in self.indices]
        key = "-".join([self.type, *strindices])
        stem = "_".join([datestr, key, *self.slug])

        return f"{stem}{self.ext}"

    @staticmethod
    def parse(path: Path):
        (datestr, key, *slug) = path.stem.split("_")
        (posttype, *strindices) = key.split("-")
        indices = [int(strindex) for strindex in strindices]

        date = datetime.datetime.strptime(datestr, DATE_FORMAT)

        return Title(
            date=date,
            ext=path.suffix,
            indices=indices,
            slug=slug,
            type=posttype,
        )
