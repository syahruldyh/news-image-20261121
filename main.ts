// "The World on One Page" — entrypoint for news-image-20261121.
//
// The entry itself is a single finished newspaper front page, entry.png,
// stored beside this file. All this program has to do is deliver that
// page, byte for byte, to the directory the harness names through
// MAKEFUN_OUTPUT_DIR (or /output when the variable is not set).

import { createHash } from "node:crypto";
import { copyFileSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const pageFile = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

// Sanity-check the page before delivering it: the competition gate only
// accepts a whole PNG of at most 1 MiB, so fail loudly here rather than
// hand over a truncated or oversized file.
const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
const bytes = readFileSync(pageFile);
if (bytes.length > 1_048_576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}
if (!PNG_SIGNATURE.every((b, i) => bytes[i] === b)) {
  throw new Error("entry.png does not start with a PNG signature");
}

copyFileSync(pageFile, join(outDir, "entry.png"));

const digest = createHash("sha256").update(bytes).digest("hex");
console.log(`delivered entry.png: ${bytes.length} bytes, sha256 ${digest}`);
