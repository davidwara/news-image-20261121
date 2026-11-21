/**
 * News in One Image — 21 Nov 2026.
 *
 * Runs draw_image.py (Pillow) to render the day's world news as one
 * 1024x1024 PNG, validates the result, and writes it to
 * $MAKEFUN_OUTPUT_DIR/entry.png. If drawing fails, falls back to the
 * entry.png committed in this repository.
 */
import { spawnSync } from "node:child_process";
import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = dirname(fileURLToPath(import.meta.url));
const DRAW = join(ROOT, "draw_image.py");
const COMMITTED = join(ROOT, "entry.png");

function fail(message: string): never {
  console.error(`[news-image] ERROR: ${message}`);
  process.exit(1);
}

function pngSize(buf: Buffer): { width: number; height: number } {
  if (buf.length < 24 || buf.subarray(0, 8).toString("hex") !== "89504e470d0a1a0a") {
    fail("not a PNG file");
  }
  return {
    width: buf.readUInt32BE(16),
    height: buf.readUInt32BE(20),
  };
}

function validate(path: string): void {
  if (!existsSync(path)) fail(`missing file: ${path}`);
  const size = statSync(path).size;
  if (size > 1048576) fail(`entry.png is ${size} bytes, over the 1 MiB limit`);
  const { width, height } = pngSize(readFileSync(path));
  if (width !== 1024 || height !== 1024) {
    fail(`entry.png is ${width}x${height}, expected 1024x1024`);
  }
  console.log(`[news-image] validated ${path}: 1024x1024, ${size} bytes`);
}

function main(): void {
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? join(ROOT, "output");
  mkdirSync(outDir, { recursive: true });
  const target = join(outDir, "entry.png");

  const run = spawnSync("python3", [DRAW], { stdio: "inherit" });
  if (run.status === 0 && existsSync(COMMITTED)) {
    validate(COMMITTED);
    copyFileSync(COMMITTED, target);
    validate(target);
    console.log(`[news-image] wrote ${target}`);
    return;
  }

  console.error(
    `[news-image] draw failed (status ${run.status}); ` +
      "falling back to the committed entry.png",
  );
  if (!existsSync(COMMITTED)) fail("no committed entry.png to fall back to");
  validate(COMMITTED);
  copyFileSync(COMMITTED, target);
  validate(target);
  console.log(`[news-image] wrote ${target} (fallback)`);
}

main();
