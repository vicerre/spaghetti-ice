import jsdom from "jsdom";
import marked from "marked";
import path from "path";
import yaml from "yaml";
import { Post } from "./post";
import { PostExt } from "./schema";

// Approximates the behavior of C library's sscanf() function.
const patternMatch = (str: string, regExp: RegExp): string[] => {
  const match = [...str.matchAll(regExp)][0];
  if (match === undefined) {
    throw Error(`Could not match ${str} to pattern ${regExp}.`);
  }
  return match.slice(1).map((s) => s);
};

const toDate = (str: string): Date => {
  const [year, month, day] = patternMatch(
    str,
    /^(\d{4})-(\d{2})-(\d{2})$/g
  ).map((s) => Number(s));
  return new Date(year, month - 1, day);
};

const toDocument = (str: string): Document => {
  const html = marked.parse(str) as string;
  const { window } = new jsdom.JSDOM(html);
  return window.document;
};

const toKey = (str: string) => {
  const [type, ...strindices] = str.split("-");

  return {
    indices: strindices.map((strindex) => Number(strindex)),
    type,
  };
};

const toTags = (str: string): string[] => {
  const [header] = patternMatch(str, /(?<!-)---(.*?)---(?!-)/gs);
  const metadata = yaml.parse(header);
  return metadata.tags;
};

const parse = ({
  content,
  pathed,
}: {
  content: string;
  pathed: string;
}): Post => {
  const { dir, ext, name } = path.parse(pathed);
  const [yyyyMmDd, key, slug = ""] = name.split(/[._]/);
  const date = toDate(yyyyMmDd);
  const doc = ext === PostExt.Markdown ? toDocument(content) : null;
  const { indices, type } = toKey(key);
  const tags = ext === PostExt.Markdown ? toTags(content) : [];

  return {
    content,
    date,
    dir,
    doc,
    ext,
    indices,
    name,
    slug,
    tags,
    type,
  };
};

export const Posts = {
  parse,
};
