import _ from "lodash";
import path from "path";
import { KnownExt, Post } from "./posts";

// Legacy checks:
//
// - `...` -> `----`
// - No "tmblr.co" or "vicerre.tumblr.com" URLs

const INDEX_LENGTH = 3;

const validatePost = (
  { content, dir, ext, indices, name, slug, tags, type }: Post,
  { exts, types }: { exts: string[]; types: string[] }
) => {
  const normalizedContent = content
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
  const pathed = path.join(dir, name);

  // General checks
  const validChecks = {
    [`${pathed} has incorrect extension ${ext}.`]: exts.includes(ext),
    [`${pathed} has incorrect type ${type}.`]: types.includes(type),
    [`${pathed} is missing indices.`]: indices.length > 0,
    [`${pathed} tags are not sorted.`]: _.isEqual(tags, tags.sort()),
  };

  // File-specific checks
  const mdValidChecks =
    ext === KnownExt.Markdown
      ? {
          [`${pathed} does not contain all expected top-level headers.`]:
            indices.every((index) => {
              const padded = `${index}`.padStart(INDEX_LENGTH, "0");
              const pattern = new RegExp(
                `^# ${type.slice(0, 1).toUpperCase()}${type.slice(
                  1
                )} ${padded}`,
                "m"
              );
              return pattern.test(content);
            }),
          [`${pathed} slug should be in post.`]: slug
            .toLowerCase()
            .split("-")
            .every((s) => normalizedContent.includes(s)),
        }
      : {};
  const mdInvalidChecks =
    ext === KnownExt.Markdown
      ? {
          [`${pathed} contains smart quotes. These should be replaced with straight quotes.`]:
            /[‘’“”]/.test(content),
          [`${pathed} contains the string "--". This should be replaced with "—".`]:
            /\b--\b/.test(content),
          [`${pathed} contains the string " - ". This should be replaced with "–".`]:
            /\b - \b/.test(content),
          [`${pathed} should not contain any TODOs.`]: /\btodo\b/i.test(
            content
          ),
          [`${pathed} contains the string "Pokemon". This should be replaced with "Pokémon".`]:
            /\bpokemon\b/i.test(content),
          [`${pathed} is missing tags.`]: tags.length === 0,
        }
      : {};

  // Type-specific checks
  const elucidationInterludeMetaValidChecks =
    type === "elucidation" || type === "interlude" || type === "meta"
      ? {
          [`${pathed} should have multiple indices or a slug.`]:
            (indices.length === 1 && slug.length > 0) ||
            (indices.length > 1 && slug.length === 0),
        }
      : {};
  const fanartValidChecks =
    type === "fanart"
      ? {
          [`${pathed} should be tagged with one of "art trade", "commission", or "gift art".`]:
            ["art trade", "commission", "gift art"].flatMap((s) =>
              content.includes(`- Type: ${s}`) ? 1 : []
            ).length === 1,
          [`${pathed} should have all of the following fields: Artist, Subject(s), Type`]:
            ["Artist", "Subject", "Type"].every((s) =>
              content.includes(`- ${s}:`)
            ),
          [`${pathed} should have an image.`]: /\bsrc\b/.test(content),
        }
      : {};
  const icebreakerValidChecks =
    type === "icebreaker"
      ? {
          [`${pathed} should not have a slug.`]: slug === "",
        }
      : {};
  const illustrationValidChecks =
    type === "illustration"
      ? {
          [`${pathed} should have an image.`]: /\bsrc\b/.test(content),
          [`${pathed} should have an "Overview" section.`]:
            /^## Overview$/m.test(content),
        }
      : {};
  const interludeValidChecks =
    type === "interlude"
      ? {
          [`${pathed} should include location.`]: content.includes("location:"),
          [`${pathed} should include POV.`]: content.includes("pov:"),
        }
      : {};

  return [
    ...Object.entries({
      ...elucidationInterludeMetaValidChecks,
      ...fanartValidChecks,
      ...icebreakerValidChecks,
      ...illustrationValidChecks,
      ...interludeValidChecks,
      ...mdValidChecks,
      ...validChecks,
    }).flatMap(([issue, good]) => (good ? [] : issue)),
    ...Object.entries(mdInvalidChecks).flatMap(([issue, bad]) =>
      bad ? issue : []
    ),
  ];
};

export const validate = ({
  exts,
  posts,
  types,
}: {
  exts: string[];
  posts: Post[];
  types: string[];
}): string[] => {
  const postIssues = posts.flatMap((post) =>
    validatePost(post, {
      exts,
      types,
    })
  );
  const typeIssues = types.flatMap((type) => {
    const typeIndices = posts
      .flatMap((post) => (post.type === type ? post.indices : ([] as const)))
      .sort((i1, i2) => i1 - i2);
    const expectedTypeIndices = _.range(1, typeIndices.length + 1);
    return _.isEqual(typeIndices, expectedTypeIndices)
      ? ([] as const)
      : `Files with extension ${type} are not properly ordered. Expected ${expectedTypeIndices}, instead saw ${typeIndices}.`;
  });

  return [...postIssues, ...typeIssues];
};
