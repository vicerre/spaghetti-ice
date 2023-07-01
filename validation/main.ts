import { validate } from "./validate";
import { find, loadPathed } from "./files";
import { AssetExt, AssetType, PostExt, PostType } from "./schema";

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
    exts: Object.values(AssetExt),
    posts: posts.filter((p) => Object.values<string>(AssetExt).includes(p.ext)),
    types: Object.values(AssetType),
  });

  const postIssues = validate({
    exts: Object.values(PostExt),
    posts: posts.filter((p) => Object.values<string>(PostExt).includes(p.ext)),
    types: Object.values(PostType),
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
