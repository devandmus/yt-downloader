#!/usr/bin/env node
/**
 * YouTube MP3 Downloader - MCP Server
 *
 * Exposes a single tool: download_audio(url)
 * Downloads YouTube audio as MP3 to ~/Downloads/yt-downloader/ via yt-dlp.
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { spawnSync } from "child_process";
import { existsSync, mkdirSync, readdirSync, statSync } from "fs";
import { join } from "path";
import { homedir } from "os";
import { execFileSync } from "child_process";

// ---------------------------------------------------------------------------
// Resolve yt-dlp binary
// ---------------------------------------------------------------------------

function resolveYtDlp() {
  // Try to locate yt-dlp from the shell (handles nvm, brew, pyenv, etc.)
  try {
    const result = execFileSync("/bin/zsh", ["-lc", "which yt-dlp"], {
      encoding: "utf8",
      timeout: 5000,
    }).trim();
    if (result && existsSync(result)) return result;
  } catch (_) {
    // fall through
  }

  // Fallback: common brew locations
  const candidates = [
    "/opt/homebrew/bin/yt-dlp",
    "/usr/local/bin/yt-dlp",
    "/usr/bin/yt-dlp",
  ];
  for (const p of candidates) {
    if (existsSync(p)) return p;
  }

  return null;
}

const YT_DLP_PATH = resolveYtDlp();

// ---------------------------------------------------------------------------
// URL cleaning  (mirrors the Python clean_youtube_url logic)
// ---------------------------------------------------------------------------

function cleanYouTubeUrl(raw) {
  try {
    const parsed = new URL(raw);

    // Only touch YouTube domains
    if (!parsed.hostname.includes("youtube.com") && !parsed.hostname.includes("youtu.be")) {
      return raw;
    }

    // youtu.be/VIDEO_ID  →  youtube.com/watch?v=VIDEO_ID
    if (parsed.hostname.includes("youtu.be")) {
      const videoId = parsed.pathname.replace(/^\//, "");
      if (!videoId) return raw;
      return `https://www.youtube.com/watch?v=${videoId}`;
    }

    // youtube.com/watch?v=ID&...  →  keep only ?v=ID
    if (parsed.pathname === "/watch") {
      const videoId = parsed.searchParams.get("v");
      if (!videoId) return raw;
      return `https://www.youtube.com/watch?v=${videoId}`;
    }

    // Any other YouTube path (e.g. /shorts/ID) — return as-is
    return raw;
  } catch (_) {
    // If URL parsing fails, pass through unchanged
    return raw;
  }
}

// ---------------------------------------------------------------------------
// Output directory
// ---------------------------------------------------------------------------

const OUTPUT_DIR = join(homedir(), "Downloads", "yt-downloader");

function ensureOutputDir() {
  if (!existsSync(OUTPUT_DIR)) {
    mkdirSync(OUTPUT_DIR, { recursive: true });
  }
}

// ---------------------------------------------------------------------------
// Download implementation
// ---------------------------------------------------------------------------

/**
 * Runs yt-dlp synchronously and returns { title, filePath } on success.
 * Throws an Error with a descriptive message on failure.
 */
function downloadAudioMp3(cleanUrl) {
  if (!YT_DLP_PATH) {
    throw new Error(
      "yt-dlp binary not found. Install it with: brew install yt-dlp"
    );
  }

  ensureOutputDir();

  // Capture the video title before downloading so we can report it back.
  // --print title is fast and does not download.
  const titleResult = spawnSync(
    YT_DLP_PATH,
    ["--print", "title", "--no-playlist", cleanUrl],
    { encoding: "utf8", timeout: 30_000 }
  );

  const title =
    titleResult.status === 0
      ? titleResult.stdout.trim()
      : "Unknown title";

  // Snapshot files already in the output dir so we can find the new one after download
  const before = new Set(
    readdirSync(OUTPUT_DIR).map((f) => join(OUTPUT_DIR, f))
  );

  // Run yt-dlp:
  //   -x                extract audio
  //   --audio-format mp3
  //   --audio-quality 192K
  //   --no-playlist      single video only
  //   -o <template>      output path template
  const args = [
    "-x",
    "--audio-format", "mp3",
    "--audio-quality", "192K",
    "--no-playlist",
    "-o", join(OUTPUT_DIR, "%(title)s.%(ext)s"),
    cleanUrl,
  ];

  const result = spawnSync(YT_DLP_PATH, args, {
    encoding: "utf8",
    timeout: 300_000, // 5-minute cap for large files
  });

  if (result.status !== 0) {
    const stderr = (result.stderr || "").trim();
    const stdout = (result.stdout || "").trim();
    const detail = stderr || stdout || "yt-dlp exited with status " + result.status;
    throw new Error(`Download failed: ${detail}`);
  }

  // Find the newly created file
  const after = readdirSync(OUTPUT_DIR).map((f) => join(OUTPUT_DIR, f));
  const newFiles = after.filter((f) => !before.has(f) && f.endsWith(".mp3"));

  // Pick the most recently modified if somehow more than one appeared
  let filePath = newFiles[0] ?? null;
  if (newFiles.length > 1) {
    filePath = newFiles.sort(
      (a, b) => statSync(b).mtimeMs - statSync(a).mtimeMs
    )[0];
  }

  if (!filePath) {
    // yt-dlp succeeded but we couldn't pin down the file — report the dir
    return { title, filePath: OUTPUT_DIR };
  }

  return { title, filePath };
}

// ---------------------------------------------------------------------------
// MCP server setup
// ---------------------------------------------------------------------------

const server = new McpServer({
  name: "yt-downloader",
  version: "1.0.0",
});

server.tool(
  "download_audio",
  "Download a YouTube video as an MP3 file to ~/Downloads/yt-downloader/",
  {
    url: z.string().describe("YouTube URL (youtube.com/watch or youtu.be short link)"),
  },
  async ({ url }) => {
    const cleanUrl = cleanYouTubeUrl(url.trim());

    try {
      const { title, filePath } = downloadAudioMp3(cleanUrl);
      return {
        content: [
          {
            type: "text",
            text: [
              `Downloaded successfully.`,
              `Title: ${title}`,
              `File:  ${filePath}`,
            ].join("\n"),
          },
        ],
      };
    } catch (err) {
      return {
        content: [
          {
            type: "text",
            text: `Error: ${err.message}`,
          },
        ],
        isError: true,
      };
    }
  }
);

// ---------------------------------------------------------------------------
// Start
// ---------------------------------------------------------------------------

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  // Intentionally no console.log — stdout is reserved for the MCP protocol
}

main().catch((err) => {
  process.stderr.write(`Fatal: ${err.message}\n`);
  process.exit(1);
});
