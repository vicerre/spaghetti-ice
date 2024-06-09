import os
from pathlib import Path
from typing import List, Dict

from data_analytics.image import Image
from data_analytics.images import load_images
from data_analytics.post import Post
from data_analytics.posts import load_posts
from data_analytics.reindexes import get_keymap, get_titlemap, get_rekeyed, get_retitled
from data_analytics.replacements import Replacements

ALT_PATH = "alt"


def escapepath(path: Path) -> Path:
    return path.parent / ALT_PATH / path.name


def unescapepath(path: Path) -> Path:
    return path.parent.parent / path.name


def rewrite(
    posts: List[Image] | List[Post],
    keyreplacements: Replacements,
    titlereplacements: Replacements,
    dryrun: bool = True,
) -> None:

    for post in posts:
        beforepost = post
        afterpost = post
        afterpost = get_rekeyed(afterpost, keyreplacements)
        if isinstance(afterpost, Post):
            afterpost = get_retitled(afterpost, keyreplacements, titlereplacements)
        beforepath = beforepost.path
        afterpath = afterpost.path

        # Handle name collisions
        if beforepath != afterpath and os.path.isfile(afterpath):
            afterpath = escapepath(afterpath)

        # Update paths
        if beforepath != afterpath:
            if dryrun:
                print("Dry run, not updating:")
                print(beforepath)
                print(afterpath)
            else:
                os.renames(beforepath, afterpath)

        # Update content
        if isinstance(beforepost, Post) and isinstance(afterpost, Post):
            if beforepost.content != afterpost.content:
                if dryrun:
                    print("Dry run, not updating:")
                    print(beforepost.content)
                    print(afterpost.content)
                else:
                    with open(afterpath, encoding="utf-8", mode="w") as f:
                        f.write(afterpost.content)


def remap(type: str, dryrun: bool = True) -> None:
    # Get posts
    images = load_images()
    posts = load_posts()

    typedimages = [image for image in images if image.type == type]
    typedposts = [post for post in posts if post.type == type]

    keymap = {
        **get_keymap(typedimages),
        **get_keymap(typedposts),
    }
    titlemap = {
        **get_titlemap(typedimages),
        **get_titlemap(typedposts),
    }
    keyreplacements = Replacements.from_dict(keymap)
    titlereplacements = Replacements.from_dict(titlemap)

    rewrite(images, keyreplacements, titlereplacements, dryrun)
    rewrite(posts, keyreplacements, titlereplacements, dryrun)

    # Resolve image name collisions
    updatedimages = load_images()

    for image in updatedimages:
        if image.path.parent.name == ALT_PATH:
            unescapedpath = unescapepath(image.path)
            if dryrun:
                print("Dry run, not updating:")
                print(image.path)
                print(unescapedpath)
            else:
                os.renames(image.path, unescapedpath)

    # Resolve image name collisions
    updatedposts = load_posts()

    for post in updatedposts:
        if post.path.parent.name == ALT_PATH:
            unescapedpath = unescapepath(post.path)
            if dryrun:
                print("Dry run, not updating:")
                print(post.path)
                print(unescapedpath)
            else:
                os.renames(post.path, unescapedpath)


def reindex(type: str, dryrun: bool = True) -> None:
    remap(type, dryrun)
    print("Done!")


if __name__ == "__main__":
    reindex(type="illustration", dryrun=False)
