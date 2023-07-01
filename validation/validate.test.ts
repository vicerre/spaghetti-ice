import { validate } from "./validate";

import { Post } from "./post";

const getPost = (post: Partial<Post> = {}): Post => {
  return {
    content: "# Meta 001 – Hello World",
    date: new Date(2021, 5, 28),
    dir: "posts",
    ext: ".md",
    indices: [1],
    name: "2023-06-28_meta-001_hello-world.md",
    slug: "hello-world",
    tags: ["meta"],
    type: "meta",
    ...post,
  };
};

test("icebreaker slug post", () => {
  const post = getPost({
    ext: ".md",
    name: "2023-06-28_icebreaker-001_hello-world.md",
    slug: "hello-world",
    type: "icebreaker",
  });
  const result = validate({
    exts: [".md"],
    posts: [post],
    types: ["icebreaker"],
  });
  expect(result.length).toBeGreaterThan(0);
});

test("invalid post", () => {
  const post = getPost({
    ext: ".png",
    type: "image",
  });
  const result = validate({
    exts: [".md"],
    posts: [post],
    types: ["meta"],
  });
  expect(result.length).toBeGreaterThan(0);
});

test("linked post", () => {
  const post = getPost({
    content: "# Meta 001 – Hello World\n[Link](http://example.com)",
    ext: ".md",
    indices: [1],
    slug: "hello-world",
    type: "meta",
  });
  const result = validate({
    exts: [".md"],
    posts: [post],
    types: ["meta"],
  });
  expect(result.length).toBe(0);
});

test("locally linked post", () => {
  const post = getPost({
    content: "# Meta 001 – Hello World\n[Link](../validation/validate.test.ts)",
    ext: ".md",
    indices: [1],
    slug: "hello-world",
    type: "meta",
  });
  const result = validate({
    exts: [".md"],
    posts: [post],
    types: ["meta"],
  });
  expect(result.length).toBe(0);
});

test("missing index", () => {
  const post1 = getPost({
    content: "# Meta 001 – Hello World",
    ext: ".md",
    indices: [1],
    slug: "hello-world",
    type: "meta",
  });
  const post2 = getPost({
    content: "# Meta 003 – Hello World",
    ext: ".md",
    indices: [3],
    slug: "hello-world",
    type: "meta",
  });
  const result = validate({
    exts: [".md"],
    posts: [post1, post2],
    types: ["meta"],
  });
  expect(result.length).toBe(1);
});

test("missing subtitle", () => {
  const post = getPost({
    content: "# Meta 001\n## Design notes",
    ext: ".md",
    type: "meta",
  });
  const result = validate({
    exts: [".md"],
    posts: [post],
    types: ["meta"],
  });
  expect(result.length).toBe(1);
});

test("missing title", () => {
  const post = getPost({
    content: "# Meta 001",
    ext: ".md",
    indices: [1],
    slug: "hello-world",
  });
  const result = validate({
    exts: [".md"],
    posts: [post],
    types: ["meta"],
  });
  expect(result.length).toBe(1);
});

test("multi-index post", () => {
  const post = getPost({
    content: "# Meta 001\n# Meta 002\n# Meta 003",
    ext: ".md",
    indices: [1, 2, 3],
    name: "2023-06-28_meta-001-002-003.md",
    slug: "",
    type: "meta",
  });
  const result = validate({
    exts: [".md"],
    posts: [post],
    types: ["meta"],
  });
  expect(result).toHaveLength(0);
});

test("slugless post", () => {
  const post = getPost({
    content: "# Meta 001",
    ext: ".md",
    indices: [1],
    name: "2023-06-28_meta-001.md",
    slug: "",
    type: "meta",
  });
  const result = validate({
    exts: [".md"],
    posts: [post],
    types: ["meta"],
  });
  expect(result.length).toBeGreaterThan(0);
});

test("valid post", () => {
  const post = getPost({
    ext: ".md",
    type: "meta",
  });
  const result = validate({
    exts: [".md"],
    posts: [post],
    types: ["meta"],
  });
  expect(result).toHaveLength(0);
});
