import re
from pathlib import Path
from typing import List

from data_analytics.post import Post

import mistletoe
import lxml.html

from data_analytics.title import Title

ENCRYPTED_FILE_DATES = ["2022-09-14"]
EXTERNAL_FILE_PATHS = ["shared"]


def _strip_github_metadata_tags(md: str) -> str:
    # Match tags non-greedily.
    return re.sub(r"---\n.*?\n---", "", md, count=1, flags=re.S).strip()


def load_posts(pathstr: str = "posts", ext: str = "*.md") -> List[Post]:
    """
    Sources:
      - https://scrapeops.io/python-web-scraping-playbook/best-python-html-parsing-libraries/
      - https://stackoverflow.com/a/11946195/
    """
    posts: List[Post] = []

    for path in Path(pathstr).rglob(ext):
        title = Title.parse(path)

        with open(path, encoding="utf-8", mode="r") as f:
            content = f.read()
            # Optional, comment out to include GitHub metadata tags in corpus.
            stripped = _strip_github_metadata_tags(content)

            html = mistletoe.markdown(stripped)
            document = lxml.html.document_fromstring(html)
            text = document.text_content()

            post = Post(
                content=content,
                date=title.date,
                encrypted=any(f in path.name for f in ENCRYPTED_FILE_DATES),
                ext=title.ext,
                external=any(f in path.parent.name for f in EXTERNAL_FILE_PATHS),
                indices=title.indices,
                path=path,
                slug=title.slug,
                text=text,
                type=title.type,
            )
            posts.append(post)

    return posts
