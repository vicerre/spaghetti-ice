export const isExternal = (str: string) => {
  return (
    str.startsWith("...") || // placeholder links
    str.startsWith("http://") ||
    str.startsWith("https://") ||
    str.startsWith("mailto:")
  );
};
