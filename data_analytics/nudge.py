import functools
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Callable

from data_analytics.post import Post
from data_analytics.posts import load_posts
from data_analytics.title import Title


@dataclass(frozen=True)
class PostKey:
    index: int
    type: str

    INDEX_LENGTH = 3

    # E.g., meta-001
    def formatkey(self):
        return f"{self.type}-{self.index:0{self.INDEX_LENGTH}}"

    # E.g., Meta 001
    def formattitle(self):
        return f"{self.type.capitalize()} {self.index:0{self.INDEX_LENGTH}}"

    @staticmethod
    def parse(s: str):
        (indexstr, posttype) = s.split("-")
        return PostKey(
            index=int(indexstr),
            type=posttype,
        )


@dataclass(frozen=True)
class Nudge:
    before: PostKey
    after: PostKey


@dataclass(frozen=True)
class PostChange:
    content: str
    path: Path


@dataclass(frozen=True)
class PostDiff:
    before: PostChange
    after: PostChange


def _get_nudges(posts: List[Post], key: PostKey, increment_size: int) -> List[Nudge]:
    nudges: List[Nudge] = []

    for post in posts:
        if post.type == key.type:
            for index in post.indices:
                if index > key.index:
                    before = PostKey(type=post.type, index=index)
                    after = PostKey(type=post.type, index=index + increment_size)
                    nudge = Nudge(before=before, after=after)
                    nudges.append(nudge)

    return nudges


def _get_diffs(
    posts: List[PostChange], fn: Callable[[PostChange], PostChange]
) -> List[PostDiff]:
    """
    Given a list of posts and a function that edits the post, produces a mapping
    from original posts to changed posts. Any post that is unchanged is excluded
    from the diff.
    """

    result: List[PostDiff] = []

    for post in posts:
        before = PostChange(
            content=post.content,
            path=post.path,
        )
        after = fn(before)

        if before != after:
            result.append(PostDiff(before=before, after=after))

    return result


def _get_filename_diff(
    nudgemap: Dict[PostKey, PostKey],
    diff: PostChange,
) -> PostChange:
    title = Title.parse(diff.path)
    nudged_indices = []

    for index in title.indices:
        before = PostKey(type=title.type, index=index)
        after = nudgemap.get(before, before)
        nudged_indices.append(after.index)

    nudged_title = Title(
        date=title.date,
        ext=title.ext,
        indices=nudged_indices,
        slug=title.slug,
        type=title.type,
    )

    return PostChange(
        content=diff.content, path=diff.path.parent / nudged_title.format()
    )


def _get_filename_diffs(diffs: List[PostChange], nudges: List[Nudge]):
    nudgemap = {nudge.before: nudge.after for nudge in nudges}
    return _get_diffs(diffs, functools.partial(_get_filename_diff, nudgemap))


def _get_title_diff(
    nudgestrs: Dict[str, str],
    diff: PostChange,
):
    # https://stackoverflow.com/a/73948462
    nudged_content = re.sub(
        "|".join(nudgestrs.keys()),
        lambda match: nudgestrs[match.group(0)],
        diff.content,
    )

    return PostChange(
        content=nudged_content,
        path=diff.path,
    )


def _get_title_diffs(changes: List[PostChange], nudges: List[Nudge]):
    nudgestrs = {
        nudge.before.formattitle(): nudge.after.formattitle() for nudge in nudges
    }
    return _get_diffs(changes, functools.partial(_get_title_diff, nudgestrs))


def _get_reference_diff(
    nudgerefs: Dict[str, str],
    diff: PostChange,
) -> PostChange:
    # https://stackoverflow.com/a/73948462
    nudged_content = re.sub(
        "|".join(nudgerefs.keys()),
        lambda match: nudgerefs[match.group(0)],
        diff.content,
    )

    return PostChange(
        content=nudged_content,
        path=diff.path,
    )


def _get_reference_diffs(changes: List[PostChange], diffs: List[PostDiff]):
    nudgerefs = {diff.before.path.stem: diff.after.path.stem for diff in diffs}

    return _get_diffs(changes, functools.partial(_get_reference_diff, nudgerefs))


def nudge_rest(key: PostKey, increment_size: int, *, dry_run=True):
    """
    Upon changing a post from one post type to another, updates all other
    posts to preserve post ordering and hyperlinks.
    """

    posts = load_posts()
    nudges = _get_nudges(posts, key, increment_size)

    # Update nudged files

    posts = load_posts()
    changes = [PostChange(content=post.content, path=post.path) for post in posts]

    title_diffs = _get_title_diffs(changes, nudges)

    if dry_run:
        print(f"Dry run, not updating {len(title_diffs)} titles.")
    else:
        print(f"Updating {len(title_diffs)} titles...")
        for diff in title_diffs:
            with open(diff.after.path, encoding="utf-8", mode="w") as f:
                f.write(diff.after.content)

    # Move nudged files

    posts = load_posts()  # Fetch latest posts after previous write
    changes = [PostChange(content=post.content, path=post.path) for post in posts]

    filename_diffs = _get_filename_diffs(changes, nudges)

    if dry_run:
        print(f"Dry run, not moving {len(filename_diffs)} files.")
    else:
        print(f"Moving {len(filename_diffs)} files...")
        for diff in filename_diffs:
            os.rename(diff.before.path, diff.after.path)

    # Update file references after move

    posts = load_posts()  # Fetch latest posts after write
    changes = [PostChange(content=post.content, path=post.path) for post in posts]

    reference_diffs = _get_reference_diffs(changes, filename_diffs)

    if dry_run:
        print(f"Dry run, not updating {len(reference_diffs)} references.")
    else:
        print(f"Updating {len(reference_diffs)} references...")
        for diff in reference_diffs:
            with open(diff.after.path, encoding="utf-8", mode="w") as f:
                f.write(diff.after.content)


if __name__ == "__main__":
    input_key = PostKey(type="illustration", index=24)
    # Apply -1 to index to nudge post at existing key.
    output_key = PostKey(type="meta", index=5 - 1)

    nudge_rest(input_key, increment_size=-1)
    nudge_rest(output_key, increment_size=1)
