import dataclasses
import re
from itertools import accumulate, pairwise
from typing import overload, List, Dict

from data_analytics.image import Image
from data_analytics.post import Post
from data_analytics.postkey import PostKey, KeyDiff
from data_analytics.posttitle import PostTitle, TitleDiff
from data_analytics.replacements import Replacements


@overload
def get_keymap(images: List[Image]) -> Dict[str, str]: ...


@overload
def get_keymap(posts: List[Post]) -> Dict[str, str]: ...


def get_keymap(posts: List[Image] | List[Post]) -> Dict[str, str]:
    # Get current ordering
    beforekeys: List[PostKey] = []
    for post in posts:
        beforekey = PostKey(indices=post.indices, type=post.type)
        beforekeys.append(beforekey)

    # Determine updated ordering
    endindices = list(accumulate(len(key.indices) for key in beforekeys))
    ranges = [[0, endindices[0]], *pairwise(endindices)] if (endindices) else []
    indices = [list(range(start + 1, end + 1)) for start, end in ranges]

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


@overload
def get_titlemap(images: List[Image]) -> Dict[str, str]: ...


@overload
def get_titlemap(posts: List[Post]) -> Dict[str, str]: ...


def get_titlemap(posts: List[Image] | List[Post]) -> Dict[str, str]:
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


@overload
def get_rekeyed(image: Image, keyreplacements: Replacements) -> Image: ...


@overload
def get_rekeyed(post: Post, keyreplacements: Replacements) -> Post: ...


def get_rekeyed(post: Image | Post, keyreplacements: Replacements) -> Image | Post:
    afterpath = post.path.parent / keyreplacements.multikeyreplace(post.path.name)

    return dataclasses.replace(post, path=afterpath)


def get_retitled(
    post: Post, keyreplacements: Replacements, titlereplacements: Replacements
) -> Post:
    aftercontent = post.content
    aftercontent = keyreplacements.multikeyreplace(aftercontent)
    aftercontent = titlereplacements.multititlereplace(aftercontent)

    return dataclasses.replace(post, content=aftercontent)
