from pathlib import Path
from typing import List

from data_analytics.image import Image
from data_analytics.title import Title


def load_images(pathstr: str = "posts", exts=[".gif", ".jpg", ".png"]) -> List[Image]:
    images: List[Image] = []

    for path in Path(pathstr).rglob("*"):
        if path.suffix in exts:
            title = Title.parse(path)

            image = Image(
                date=title.date,
                ext=title.ext,
                indices=title.indices,
                path=path,
                type=title.type,
            )
            images.append(image)

    return images
