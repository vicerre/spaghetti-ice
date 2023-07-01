import { validate } from "./validate";
import { find, loadPathed } from "./files";
import path from "node:path";
import { AssetExt, AssetType, PostExt, PostType } from "./schema";
import _ from "lodash";
import { isExternal } from "./hrefs";

const main = async () => {
  const files = await find("posts");

  const parsed = await Promise.all(files.map((f) => loadPathed(f)));
  const parseIssues = parsed.flatMap((p) =>
    p.validationResult.isValid ? ([] as const) : p.validationResult.issues
  );
  const valids = parsed.flatMap((p) =>
    p.validationResult.isValid && p.value ? p.value : ([] as const)
  );

  const assets = valids.filter((p) =>
    Object.values<string>(AssetExt).includes(p.ext)
  );
  const posts = valids.filter((p) =>
    Object.values<string>(PostExt).includes(p.ext)
  );

  const assetIssues = validate({
    exts: Object.values(AssetExt),
    posts: assets,
    types: Object.values(AssetType),
  });

  const postIssues = validate({
    exts: Object.values(PostExt),
    posts: posts,
    types: Object.values(PostType),
  });

  const assetNames = assets.map((p) => p.name);
  const postAssetNames = posts.flatMap(({ dir, doc }) => {
    const hrefNames = Array.from(doc.getElementsByTagName("a")).flatMap(
      ({ href }) => {
        if (isExternal(href)) {
          return [];
        }
        const f = path.resolve(dir, href);
        return path.parse(f).name;
      }
    );
    const imgNames = Array.from(doc.getElementsByTagName("img")).map(
      ({ src }) => {
        const f = path.resolve(dir, src);
        return path.parse(f).name;
      }
    );
    return [...hrefNames, ...imgNames];
  });
  const usageIssues = _.difference(assetNames, postAssetNames).map(
    (f: string) => `Asset ${f} is not used in any posts.`
  );

  const issues = [
    ...parseIssues,
    ...assetIssues,
    ...postIssues,
    ...usageIssues,
  ];

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
