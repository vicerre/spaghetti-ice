export interface Post {
  content: string;
  date: Date;
  dir: string;
  doc: Document | null;
  ext: string;
  indices: number[];
  name: string;
  slug: string;
  tags: string[];
  type: string;
}
