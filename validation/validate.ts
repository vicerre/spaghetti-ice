import _ from "lodash";
import path from "node:path";
import { PostExt, PostType } from "./schema";
import { Post } from "./post";
import fs from "node:fs";
import { isExternal } from "./hrefs";

// Legacy checks:
//
// - `...` -> `----`
// - No "tmblr.co" or "vicerre.tumblr.com" URLs

const ASSET_DIR = "assets";
const FANART_FIELDS = ["Artist", "Subject", "Type"];
const FANART_TYPES = [
  "art trade",
  "commission",
  "fanart",
  "gift art",
  "quickdraw",
];
const HEADER_LABELS = [
  "Bonus material",
  "Bonus passage",
  "Bonus sketch",
  "Design notes",
  "Explanation",
  "Game design notes",
  "Inspirations",
  "Miscellaneous notes",
  "References used",
  "Resources used",
  "Observations",
  "Option 1",
  "Option 2",
  "Overview",
  "Scrapped ideas",
  "Story notes",
  "WIPs",
  "Workflow",
];
const INDEX_LENGTH = 3;
const VIGNETTE_TAGS = ["location", "pov"];

const validatePost = (
  { content, dir, doc, ext, indices, name, slug, tags, type }: Post,
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
    ext === PostExt.Markdown
      ? {
          [`${pathed} does not contain all expected secondary-level headers.`]:
            type == PostType.Evergreen ||
            [...content.matchAll(/^## (.*)/gm)].every((match) =>
              HEADER_LABELS.some((label) => match[1].startsWith(label))
            ),
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
          [`${pathed} has broken links.`]: (() => {
            const hrefs = Array.from(doc.getElementsByTagName("a")).map(
              (e) => e.href
            );

            return hrefs
              .flatMap((href) =>
                isExternal(href) ? [] : path.resolve(dir, href)
              )
              .every((path) => fs.existsSync(path));
          })(),
          [`${pathed} slug should be in post.`]: slug
            .toLowerCase()
            .split("-")
            .every((s) => normalizedContent.includes(s)),
          [`${pathed} title should have exactly one of the following: a slug, multiple indices, type ${PostType.Icebreaker}.`]:
            [
              type === PostType.Icebreaker &&
                indices.length > 1 &&
                slug.length === 0,
              type === PostType.Icebreaker &&
                indices.length === 1 &&
                slug.length === 0,
              type !== PostType.Icebreaker &&
                indices.length === 1 &&
                slug.length > 0,
              type !== PostType.Icebreaker &&
                indices.length > 1 &&
                slug.length === 0,
            ].reduce((b1, b2) => b1 != b2),
        }
      : {};
  const mdInvalidChecks =
    ext === PostExt.Markdown
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
  const fanartValidChecks =
    type === PostType.Fanart
      ? {
          [`${pathed} should be tagged with exactly one of: ${FANART_TYPES.join(
            ", "
          )}`]:
            FANART_TYPES.flatMap((s) =>
              content.includes(`- Type: ${s}`) ? 1 : []
            ).length === 1,
          [`${pathed} should have all of the following fields: ${FANART_FIELDS.join(
            ", "
          )}`]: FANART_FIELDS.every((s) => content.includes(`- ${s}:`)),
          [`${pathed} should have an image.`]: /\bsrc\b/.test(content),
        }
      : {};
  const doodleIllustrationRenditionVestigeValidChecks =
    type === PostType.Doodle ||
    type === PostType.Illustration ||
    type === PostType.Rendition ||
    type === PostType.Vestige
      ? {
          [`${pathed} should have a date.`]: /\b\d{4}-\d{2}-\d{2}\b/.test(
            content
          ),
          [`${pathed} should have an image.`]: new RegExp(
            String.raw`\bsrc="${ASSET_DIR}\/.+"`
          ).test(content),
          [`${pathed} should have an "Overview" section.`]:
            /^## Overview$/m.test(content),
        }
      : {};
  const vignetteValidChecks =
    type === PostType.Vignette
      ? {
          [`${pathed} should include the following tags: ${VIGNETTE_TAGS.join(
            ", "
          )}.`]: VIGNETTE_TAGS.every((s) => content.includes(`${s}:`)),
        }
      : {};

  return [
    ...Object.entries({
      ...doodleIllustrationRenditionVestigeValidChecks,
      ...fanartValidChecks,
      ...mdValidChecks,
      ...validChecks,
      ...vignetteValidChecks,
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
