/* Fit Pilates — počítání příchodů z kampaní (serverově, bez cookies)
 * Přidáno: 11.10.2026
 * Počítá jen načtení HTML stránky, jejíž URL nese kampaňové parametry
 * (gclid, fbclid, utm_*). Ostatní požadavky propouští beze změny.
 */
import type { Config, Context } from "@netlify/edge-functions";
import { classify, inBackground, isNoise, pageSlug, record } from "../lib/fp-attr.ts";

export default async (req: Request, context: Context) => {
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (!url.search) return;
  const accept = req.headers.get("accept") || "";
  if (!accept.includes("text/html")) return;
  if (isNoise(req)) return;

  const a = classify(url.searchParams);
  if (!a) return;

  await inBackground(context, record("landing", a, pageSlug(url.pathname)));
  // nic nevracíme → Netlify doručí stránku jako obvykle
};

export const config: Config = {
  path: "/*",
  excludedPath: [
    "/assets/*", "/images/*", "/media/*", "/api/*", "/go/*", "/.netlify/*",
    "/*.css", "/*.js", "/*.png", "/*.jpg", "/*.jpeg", "/*.webp", "/*.avif", "/*.svg",
    "/*.ico", "/*.xml", "/*.txt", "/*.json", "/*.webmanifest", "/*.mp4", "/*.pdf",
  ],
  onError: "bypass",
};
