/** In-page helper: list visible text whose colour barely differs from its background. */
export function lowContrastText(threshold) {
  const parse = (value) => {
    const m = value.match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const [r, g, b, a = 1] = m[1].split(/[ ,/]+/).filter(Boolean).map(Number);
    return { r, g, b, a };
  };
  const lum = ({ r, g, b }) => {
    const f = (c) => {
      c /= 255;
      return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
    };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  };
  const ratio = (x, y) => {
    const [a, b] = [lum(x), lum(y)].sort((p, q) => q - p);
    return (a + 0.05) / (b + 0.05);
  };
  let owner;
  const background = (el) => {
    for (let node = el; node && node.nodeType === 1; node = node.parentElement) {
      const style = getComputedStyle(node);
      if (style.backgroundImage !== "none" && node.tagName !== "BODY") return null;
      const c = parse(style.backgroundColor);
      owner = node;
      if (c && c.a > 0.5) return c;
    }
    owner = document.body;
    return parse(getComputedStyle(document.body).backgroundColor);
  };
  const failures = [];
  const seen = new Set();
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let text; (text = walker.nextNode()); ) {
    const el = text.parentElement;
    if (!text.data.trim() || seen.has(el)) continue;
    seen.add(el);
    // SVG text sits on shapes this helper cannot see; only check HTML text.
    if (el.closest("svg,noscript,script,style,video,audio,.katex-mathml,.sr-only")) continue;
    const rects = el.getClientRects();
    if (!rects.length || getComputedStyle(el).visibility === "hidden") continue;
    const style = getComputedStyle(el);
    if (Number(style.opacity) === 0 || parseFloat(style.fontSize) === 0) continue;
    const fg = parse(style.color),
      bg = background(el);
    if (!fg || !bg) continue;
    const value = ratio(fg, bg);
    if (value < threshold)
      failures.push(
        `${value.toFixed(2)} [on ${owner.tagName.toLowerCase()}.${[...owner.classList].join(".")}] ${el.tagName.toLowerCase()}.${[...el.classList].join(".")} "${text.data.trim().slice(0, 30)}"`,
      );
  }
  return failures;
}
