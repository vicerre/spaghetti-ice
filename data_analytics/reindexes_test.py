import dataclasses
import datetime
import unittest
from pathlib import Path

from data_analytics import reindexes
from data_analytics.image import Image
from data_analytics.post import Post
from data_analytics.replacements import Replacements

IMAGE_BASE = Image(
    date=datetime.datetime.fromtimestamp(0).date(),
    ext="",
    indices=[],
    path=Path(""),
    type="",
)
IMAGE0 = dataclasses.replace(
    IMAGE_BASE,
    indices=[0],
    path=Path("a/b/c/1980-01-01_image-000.png"),
    type="image",
)
IMAGE1 = dataclasses.replace(
    IMAGE_BASE,
    indices=[1],
    path=Path("a/b/c/1980-01-01_image-001.png"),
    type="image",
)
IMAGES = [IMAGE1, IMAGE0]

POST_BASE = Post(
    content="",
    date=datetime.datetime.fromtimestamp(0).date(),
    encrypted=False,
    external=False,
    ext="",
    indices=[],
    path=Path(""),
    slug="",
    text="",
    type="",
)
POST0 = dataclasses.replace(
    POST_BASE,
    content="Meta 000",
    indices=[0],
    path=Path("a/b/c/1980-01-01_meta-000_test.md"),
    type="meta",
)
POST1 = dataclasses.replace(
    POST_BASE,
    content="Meta 001",
    indices=[1],
    path=Path("a/b/c/1980-01-01_meta-001_test.md"),
    type="meta",
)
POST2 = dataclasses.replace(
    POST_BASE,
    content="Meta 002 Meta 003",
    indices=[2, 3],
    path=Path("a/b/c/1980-01-01_meta-002-003.md"),
    type="meta",
)
POSTS = [POST1, POST0, POST2]

IMAGEKEYMAP = {
    "image-001": "image-001",
    "image-000": "image-002",
}
IMAGETITLEMAP = {
    "Image 001": "Image 001",
    "Image 000": "Image 002",
}
POSTKEYMAP = {
    "meta-001": "meta-001",
    "meta-000": "meta-002",
    "meta-002-003": "meta-003-004",
}
POSTTITLEMAP = {
    "Meta 001": "Meta 001",
    "Meta 000": "Meta 002",
    "Meta 002": "Meta 003",
    "Meta 003": "Meta 004",
}


class ReindexTest(unittest.TestCase):

    def test_get_keymap_images(self):
        actual = reindexes.get_keymap(IMAGES)
        expected = IMAGEKEYMAP
        self.assertEqual(actual, expected)

    def test_get_keymap_posts(self):
        actual = reindexes.get_keymap(POSTS)
        expected = POSTKEYMAP
        self.assertEqual(actual, expected)

    def test_get_titlemap_images(self):
        actual = reindexes.get_titlemap(IMAGES)
        expected = IMAGETITLEMAP
        self.assertEqual(actual, expected)

    def test_get_titlemap_posts(self):
        actual = reindexes.get_titlemap(POSTS)
        expected = POSTTITLEMAP
        self.assertEqual(actual, expected)

    def test_get_rekeyed_empty(self):
        post = POST1
        keyreplacements = Replacements.from_dict({})
        actual = reindexes.get_rekeyed(post, keyreplacements)
        expected = POST1
        self.assertEqual(actual, expected)

    def test_get_rekeyed_noop(self):
        post = POST1
        keyreplacements = Replacements.from_dict(POSTKEYMAP)
        actual = reindexes.get_rekeyed(post, keyreplacements)
        expected = POST1
        self.assertEqual(actual, expected)

    def test_get_rekeyed_single(self):
        post = POST0
        keyreplacements = Replacements.from_dict(POSTKEYMAP)
        actual = reindexes.get_rekeyed(post, keyreplacements)
        expected = dataclasses.replace(
            post, path=Path("a/b/c/1980-01-01_meta-002_test.md")
        )
        self.assertEqual(actual, expected)

    def test_get_rekeyed_multiple(self):
        post = POST2
        keyreplacements = Replacements.from_dict(POSTKEYMAP)
        actual = reindexes.get_rekeyed(post, keyreplacements)
        expected = dataclasses.replace(
            post, path=Path("a/b/c/1980-01-01_meta-003-004.md")
        )
        self.assertEqual(actual, expected)

    def test_get_retitled_empty(self):
        post = POST1
        keyreplacements = Replacements.from_dict({})
        titlereplacements = Replacements.from_dict({})
        actual = reindexes.get_retitled(post, keyreplacements, titlereplacements)
        expected = POST1
        self.assertEqual(actual, expected)

    def test_get_retitled_noop(self):
        post = POST1
        keyreplacements = Replacements.from_dict(POSTKEYMAP)
        titlereplacements = Replacements.from_dict(POSTTITLEMAP)
        actual = reindexes.get_retitled(post, keyreplacements, titlereplacements)
        expected = POST1
        self.assertEqual(actual, expected)

    def test_get_retitled_single(self):
        post = POST0
        keyreplacements = Replacements.from_dict(POSTKEYMAP)
        titlereplacements = Replacements.from_dict(POSTTITLEMAP)
        actual = reindexes.get_retitled(post, keyreplacements, titlereplacements)
        expected = dataclasses.replace(post, content="Meta 002")
        self.assertEqual(actual, expected)

    def test_get_retitled_multiple(self):
        post = POST2
        keyreplacements = Replacements.from_dict(POSTKEYMAP)
        titlereplacements = Replacements.from_dict(POSTTITLEMAP)
        actual = reindexes.get_retitled(post, keyreplacements, titlereplacements)
        expected = dataclasses.replace(post, content="Meta 003 Meta 004")
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
