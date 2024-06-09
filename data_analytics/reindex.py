import dataclasses
import os
import re
from dataclasses import dataclass
from itertools import accumulate, pairwise
from typing import List, Dict
from data_analytics.post import Post
from data_analytics.posts import load_posts


@dataclass(frozen=True, order=True)
class PostKey:
    type: str
    indices: List[int]

    INDEX_LENGTH = 3

    def format(self):
        keystrs = [f"{index:0{self.INDEX_LENGTH}}" for index in self.indices]
        keystr = "-".join(keystrs)
        return f"{self.type}-{keystr}"


@dataclass(frozen=True, order=True)
class PostTitle:
    type: str
    index: int

    INDEX_LENGTH = 3

    def format(self):
        keystr = f"{self.index:0{self.INDEX_LENGTH}}"
        return f"{self.type.capitalize()} {keystr}"


@dataclass(frozen=True)
class KeyDiff:
    before: PostKey
    after: PostKey


@dataclass(frozen=True)
class TitleDiff:
    before: PostTitle
    after: PostTitle


def get_keymap(posts: List[Post]) -> Dict[str, str]:
    # Get current ordering
    beforekeys: List[PostKey] = []
    for post in posts:
        beforekey = PostKey(indices=post.indices, type=post.type)
        beforekeys.append(beforekey)

    # Determine updated ordering
    endindices = list(accumulate(len(key.indices) for key in beforekeys))
    ranges = [[0, endindices[0]], *pairwise(endindices)]
    indices = [list(range(start + 1, end + 1, 1)) for start, end in ranges]

    afterkeys: List[PostKey] = []
    for indices, beforekey in zip(indices, beforekeys):
        afterkey = PostKey(indices=indices, type=beforekey.type)
        afterkeys.append(afterkey)

    # Get updates
    keydiffs: List[KeyDiff] = [
        KeyDiff(before=before, after=after)
        for before, after in zip(beforekeys, afterkeys)
    ]
    keymap: dict[str, str] = {
        diff.before.format(): diff.after.format() for diff in keydiffs
    }
    return keymap


def get_titlemap(posts: List[Post]) -> Dict[str, str]:
    # Get current ordering
    beforetitles: List[PostTitle] = []
    for post in posts:
        for index in post.indices:
            beforetitle = PostTitle(index=index, type=post.type)
            beforetitles.append(beforetitle)

    # Determine updated ordering
    aftertitles: List[PostTitle] = []
    for i, title in enumerate(beforetitles):
        aftertitle = PostTitle(index=i + 1, type=title.type)
        aftertitles.append(aftertitle)

    # Get updates
    titlediffs: List[TitleDiff] = [
        TitleDiff(before=before, after=after)
        for before, after in zip(beforetitles, aftertitles)
    ]
    titlemap: dict[str, str] = {
        diff.before.format(): diff.after.format() for diff in titlediffs
    }
    return titlemap


def multireplace(replacements: Dict[str, str], s: str) -> str:
    pattern = "|".join(replacements.keys())

    return re.sub(pattern, lambda match: replacements[match.group(0)], s)


def get_rekeyed(post: Post, keymap: Dict[str, str]) -> Post:
    afterpath = post.path.parent / multireplace(keymap, post.path.name)

    return dataclasses.replace(post, path=afterpath)


def get_retitled(post: Post, keymap: Dict[str, str], titlemap: Dict[str, str]) -> Post:
    aftercontent = post.content
    aftercontent = multireplace(keymap, aftercontent)
    aftercontent = multireplace(titlemap, aftercontent)

    return dataclasses.replace(post, content=aftercontent)


def remap(type: str, dryrun: bool = True) -> None:
    # Get posts
    posts = load_posts()

    typedposts = [post for post in posts if post.type == type]
    keymap = get_keymap(typedposts)
    titlemap = get_titlemap(typedposts)

    for post in posts:
        beforepost = post
        afterpost = post
        afterpost = get_rekeyed(afterpost, keymap)
        afterpost = get_retitled(afterpost, keymap, titlemap)

        if beforepost.path != afterpost.path:
            if dryrun:
                print("Dry run, not updating:")
                print(beforepost.path)
                print(afterpost.path)
            else:
                os.rename(beforepost.path, afterpost.path)
        if beforepost.content != afterpost.content:
            if dryrun:
                print("Dry run, not updating:")
                print(beforepost.content)
                print(afterpost.content)
            else:
                with open(afterpost.path, encoding="utf-8", mode="w") as f:
                    f.write(afterpost.content)


def reindex(type: str, dryrun: bool = True) -> None:
    remap(type, dryrun)
    print("Done!")


if __name__ == "__main__":
    reindex(type="vignette", dryrun=True)
