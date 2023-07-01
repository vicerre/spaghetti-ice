import { validate } from "./validate";
import { find, loadPathed } from "./files";

const ASSET_EXTS = [".gif", ".jpg", ".png"];
const ASSET_TYPES = ["fanimage", "image", "oldimage"];
const POST_EXTS = [".md"];
const POST_TYPES = [
  "elucidation",
  "fanart",
  "icebreaker",
  "illustration",
  "meta",
  "rendition",
  "vestige",
  "vignette",
];

const main = async () => {
  const files = await find("posts");

  const parsed = await Promise.all(files.map((f) => loadPathed(f)));
  const parseIssues = parsed.flatMap((p) =>
    p.validationResult.isValid ? ([] as const) : p.validationResult.issues
  );
  const posts = parsed.flatMap((p) =>
    p.validationResult.isValid && p.value ? p.value : ([] as const)
  );

  const assetIssues = validate({
    exts: ASSET_EXTS,
    posts: posts.filter((p) => ASSET_EXTS.includes(p.ext)),
    types: ASSET_TYPES,
  });

  const postIssues = validate({
    exts: POST_EXTS,
    posts: posts.filter((p) => POST_EXTS.includes(p.ext)),
    types: POST_TYPES,
  });

  const issues = [...parseIssues, ...assetIssues, ...postIssues];

  if (issues.length === 0) {
    process.exit(0);
  } else {
    console.warn("Validation issues:");
    for (const issue of issues) {
      console.warn(issue);
    }
    process.exit(1);
  }
};

main();
