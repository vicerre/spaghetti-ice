/*
 * All file processing should be performed in this file.
 */

import { Parsed } from "./parsed";
import { Post } from "./post";
import { Posts } from "./posts";
import fs from "fs/promises";
import path from "path";

// Optimally, we should pass files in as CLI arguments from an external source
// such as `find posts -type f`. However, we can't do this in Windows, as we
// hit the max CLI argument length limit of 8192 characters. As a workaround,
// find all relevant files in Node.
export const find = async (dir: string) => {
  const entries = await fs.readdir(dir, {
    withFileTypes: true,
  });
  const results: string[][] = await Promise.all(
    entries.map(async (e) => {
      const pathed = path.join(dir, e.name);
      if (e.isDirectory()) {
        const found = await find(pathed);
        return found;
      }
      if (e.isFile()) {
        return [pathed];
      }
      return [];
    })
  );
  return results.flat();
};
export const loadPathed = async (pathed: string): Promise<Parsed<Post>> => {
  const content = await fs.readFile(pathed, "utf8");
  try {
    const post = Posts.parse({ content, pathed });
    return Parsed.of(post);
  } catch (e) {
    return Parsed.issues([`Could not parse ${pathed}. Issue: ${e.message}`]);
  }
};
