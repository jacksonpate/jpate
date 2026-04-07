#!/usr/bin/env node
/**
 * Obsidian Local REST API — MCP Server
 * Bridges Claude to the Obsidian Local REST API plugin running on localhost.
 *
 * Required env vars:
 *   OBSIDIAN_API_KEY   — API key from Obsidian plugin settings
 *   OBSIDIAN_HOST      — default: 127.0.0.1
 *   OBSIDIAN_PORT      — default: 27124
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import https from "https";

// ── Config ───────────────────────────────────────────────────────────────────

const API_KEY = process.env.OBSIDIAN_API_KEY;
const HOST    = process.env.OBSIDIAN_HOST || "127.0.0.1";
const PORT    = process.env.OBSIDIAN_PORT || "27124";
const BASE    = `https://${HOST}:${PORT}`;

if (!API_KEY) {
  process.stderr.write("OBSIDIAN_API_KEY is not set\n");
  process.exit(1);
}

// Obsidian plugin uses a self-signed cert — safe to bypass on localhost
const agent = new https.Agent({ rejectUnauthorized: false });

// ── HTTP helper ──────────────────────────────────────────────────────────────

async function api(method, path, body = null) {
  const url = `${BASE}${path}`;
  const headers = {
    Authorization: `Bearer ${API_KEY}`,
    "Content-Type": "application/json",
  };

  const res = await fetch(url, {
    method,
    headers,
    body: body !== null ? JSON.stringify(body) : undefined,
    // Node 18+ fetch doesn't support custom agents natively;
    // NODE_TLS_REJECT_UNAUTHORIZED=0 is set in the MCP env config
  });

  const text = await res.text();
  if (!res.ok) {
    throw new Error(`Obsidian API ${res.status}: ${text}`);
  }

  try {
    return JSON.parse(text);
  } catch {
    return text; // plain text response (note content)
  }
}

// ── Tool definitions ─────────────────────────────────────────────────────────

const TOOLS = [
  {
    name: "obsidian_read_note",
    description: "Read the full content of a note by its vault path (e.g. 'Core/identity.md')",
    inputSchema: {
      type: "object",
      properties: {
        path: { type: "string", description: "Vault-relative path to the note" },
      },
      required: ["path"],
    },
  },
  {
    name: "obsidian_write_note",
    description: "Create or fully overwrite a note at the given path",
    inputSchema: {
      type: "object",
      properties: {
        path:    { type: "string", description: "Vault-relative path to the note" },
        content: { type: "string", description: "Full markdown content to write" },
      },
      required: ["path", "content"],
    },
  },
  {
    name: "obsidian_append_note",
    description: "Append text to the end of an existing note",
    inputSchema: {
      type: "object",
      properties: {
        path:    { type: "string", description: "Vault-relative path to the note" },
        content: { type: "string", description: "Text to append" },
      },
      required: ["path", "content"],
    },
  },
  {
    name: "obsidian_search",
    description: "Full-text search across the entire Obsidian vault. Returns matching file paths and context snippets.",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string", description: "Search query" },
      },
      required: ["query"],
    },
  },
  {
    name: "obsidian_list",
    description: "List files and folders at a vault path. Use '/' for the vault root.",
    inputSchema: {
      type: "object",
      properties: {
        path: {
          type: "string",
          description: "Vault-relative directory path (e.g. '/', 'Core/', 'Memory/')",
          default: "/",
        },
      },
    },
  },
  {
    name: "obsidian_delete_note",
    description: "Permanently delete a note from the vault",
    inputSchema: {
      type: "object",
      properties: {
        path: { type: "string", description: "Vault-relative path to the note" },
      },
      required: ["path"],
    },
  },
  {
    name: "obsidian_active_note",
    description: "Get the content of the note currently open in Obsidian",
    inputSchema: {
      type: "object",
      properties: {},
    },
  },
];

// ── Tool handlers ─────────────────────────────────────────────────────────────

async function handleTool(name, args) {
  switch (name) {
    case "obsidian_read_note": {
      const content = await api("GET", `/vault/${encodeURIComponent(args.path)}`);
      return { content: [{ type: "text", text: typeof content === "string" ? content : JSON.stringify(content) }] };
    }

    case "obsidian_write_note": {
      await fetch(`${BASE}/vault/${encodeURIComponent(args.path)}`, {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${API_KEY}`,
          "Content-Type": "text/markdown",
        },
        body: args.content,
      });
      return { content: [{ type: "text", text: `Written: ${args.path}` }] };
    }

    case "obsidian_append_note": {
      await fetch(`${BASE}/vault/${encodeURIComponent(args.path)}`, {
        method: "PATCH",
        headers: {
          Authorization: `Bearer ${API_KEY}`,
          "Content-Type": "text/markdown",
        },
        body: args.content,
      });
      return { content: [{ type: "text", text: `Appended to: ${args.path}` }] };
    }

    case "obsidian_search": {
      const results = await api("POST", `/search/simple/?query=${encodeURIComponent(args.query)}`);
      if (!Array.isArray(results) || results.length === 0) {
        return { content: [{ type: "text", text: "No results found." }] };
      }
      const formatted = results.slice(0, 20).map(r => {
        const snippets = (r.matches || []).slice(0, 2).map(m => m.context?.trim()).filter(Boolean).join("\n…\n");
        return `**${r.filename}** (score: ${r.score?.toFixed(1)})\n${snippets}`;
      }).join("\n\n---\n\n");
      return { content: [{ type: "text", text: formatted }] };
    }

    case "obsidian_list": {
      const dirPath = args.path || "/";
      const normalized = dirPath === "/" ? "" : dirPath.replace(/\/?$/, "/");
      const result = await api("GET", `/vault/${normalized}`);
      const files = result.files || [];
      return { content: [{ type: "text", text: files.join("\n") || "(empty)" }] };
    }

    case "obsidian_delete_note": {
      await api("DELETE", `/vault/${encodeURIComponent(args.path)}`);
      return { content: [{ type: "text", text: `Deleted: ${args.path}` }] };
    }

    case "obsidian_active_note": {
      const content = await api("GET", "/active/");
      return { content: [{ type: "text", text: typeof content === "string" ? content : JSON.stringify(content) }] };
    }

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
}

// ── Server setup ──────────────────────────────────────────────────────────────

const server = new Server(
  { name: "obsidian-local-rest-api", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools: TOOLS }));

server.setRequestHandler(CallToolRequestSchema, async (req) => {
  const { name, arguments: args } = req.params;
  try {
    return await handleTool(name, args ?? {});
  } catch (err) {
    return {
      content: [{ type: "text", text: `Error: ${err.message}` }],
      isError: true,
    };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
