export interface Post {
  content: string;
  date: Date;
  dir: string;
  ext: string;
  indices: number[];
  name: string;
  slug: string;
  tags: string[];
  type: string;
}
