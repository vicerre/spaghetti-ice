import dataclasses
import datetime
import unittest
from pathlib import Path

from data_analytics import reindex
from data_analytics.post import Post

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

KEYMAP = {
    "meta-001": "meta-001",
    "meta-000": "meta-002",
    "meta-002-003": "meta-003-004",
}
TITLEMAP = {
    "Meta 001": "Meta 001",
    "Meta 000": "Meta 002",
    "Meta 002": "Meta 003",
    "Meta 003": "Meta 004",
}


class ReindexTest(unittest.TestCase):
    def test_get_keymap(self):
        actual = reindex.get_keymap(POSTS)
        expected = KEYMAP
        self.assertEqual(actual, expected)

    def test_get_titlemap(self):
        actual = reindex.get_titlemap(POSTS)
        expected = TITLEMAP
        self.assertEqual(actual, expected)

    def test_get_rekeyed_noop(self):
        post = POST1
        keymap = KEYMAP
        actual = reindex.get_rekeyed(post, keymap)
        expected = POST1
        self.assertEqual(actual, expected)

    def test_get_rekeyed_single(self):
        post = POST0
        keymap = KEYMAP
        actual = reindex.get_rekeyed(post, keymap)
        expected = dataclasses.replace(
            post, path=Path("a/b/c/1980-01-01_meta-002_test.md")
        )
        self.assertEqual(actual, expected)

    def test_get_rekeyed_multiple(self):
        post = POST2
        keymap = KEYMAP
        actual = reindex.get_rekeyed(post, keymap)
        expected = dataclasses.replace(
            post, path=Path("a/b/c/1980-01-01_meta-003-004.md")
        )
        self.assertEqual(actual, expected)

    def test_get_retitled_noop(self):
        post = POST1
        keymap = KEYMAP
        titlemap = TITLEMAP
        actual = reindex.get_retitled(post, keymap, titlemap)
        expected = dataclasses.replace(post, content="Meta 001")
        self.assertEqual(actual, expected)

    def test_get_retitled_single(self):
        post = POST0
        keymap = KEYMAP
        titlemap = TITLEMAP
        actual = reindex.get_retitled(post, keymap, titlemap)
        expected = dataclasses.replace(post, content="Meta 002")
        self.assertEqual(actual, expected)

    def test_get_retitled_multiple(self):
        post = POST2
        keymap = KEYMAP
        titlemap = TITLEMAP
        actual = reindex.get_retitled(post, keymap, titlemap)
        expected = dataclasses.replace(post, content="Meta 003 Meta 004")
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
