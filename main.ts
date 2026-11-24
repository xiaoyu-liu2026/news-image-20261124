// 24 November World News in One Image — entry program
//
// Competition: make.fun "Sum up 24 November's world news in one image"
//   slug: news-image-20261124
//
// The entry image lives in this repository as entry.png, drawn by
// make_image.py from the day's verified headlines:
//   - Ukraine sinks Russian warship off Libya (Benghazi, naval drones)
//   - Nvidia reinstates Jensen Huang as CEO; shares +31%, markets rally
//   - Three tankers hit mines in the Strait of Hormuz (Iran)
//   - NATO vows space defence after Russian nuclear-satellite reports
//   - COP31 climate summit ends without a deal
//   - Ticker: Gaza strikes, Indonesia factory fire, landmine casualties
//
// This program copies entry.png, byte for byte, to /output/entry.png.
// It runs with no network and no dependencies, and two runs always
// produce identical bytes because the source file never changes.
//
// Runs on Node 22.18+:
//   node main.ts
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
// /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const MAX_BYTES = 1_048_576; // the gate: at most 1 MiB
const MAX_SIDE = 1024; // the gate: at most 1024 x 1024 pixels
const SOURCE = new URL("./entry.png", import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

const size = statSync(SOURCE).size;
if (size === 0 || size > MAX_BYTES) {
  throw new Error(`entry.png must be 1..${MAX_BYTES} bytes, got ${size}`);
}

// Verify the PNG header before copying: signature, then the IHDR
// width and height, so an oversize or corrupt image fails loudly
// here instead of at the gate.
const head = readFileSync(SOURCE).subarray(0, 24);
const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
if (!PNG_SIGNATURE.every((byte, i) => head[i] === byte)) {
  throw new Error("entry.png does not start with the PNG signature");
}
const width = head.readUInt32BE(16);
const height = head.readUInt32BE(20);
if (width > MAX_SIDE || height > MAX_SIDE) {
  throw new Error(`entry.png is ${width}x${height}, over ${MAX_SIDE}x${MAX_SIDE}`);
}

copyFileSync(SOURCE, target);
console.log(`wrote ${size} bytes (${width}x${height}) to ${target}`);
