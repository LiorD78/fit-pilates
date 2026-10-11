/* Fit Pilates — souhrn anonymního počítadla kampaní
 * Přidáno: 11.10.2026
 * GET /api/fp-stats?k=<FP_STATS_KEY>&days=30
 *   nebo  &from=2026-10-01&to=2026-10-31
 * Vrací JSON: součty podle zdroje / události / kampaně / stránky a po dnech.
 * Klíč FP_STATS_KEY je v proměnných prostředí Netlify (není v repozitáři).
 */
import type { Config } from "@netlify/edge-functions";
import { getStore } from "@netlify/blobs";
import { parseKey, pragueDate, STORE_NAME } from "../lib/fp-attr.ts";

declare const Netlify: { env: { get(name: string): string | undefined } };

function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body, null, 2), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
      "x-robots-tag": "noindex, nofollow",
    },
  });
}

function safeEqual(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

function bump(obj: Record<string, number>, key: string) {
  obj[key] = (obj[key] || 0) + 1;
}

export default async (req: Request) => {
  const expected = Netlify.env.get("FP_STATS_KEY") || "";
  const url = new URL(req.url);
  if (!expected) return json({ error: "FP_STATS_KEY není nastavený" }, 503);
  if (!safeEqual(url.searchParams.get("k") || "", expected)) return json({ error: "unauthorized" }, 401);

  const isDate = (s: string | null) => !!s && /^\d{4}-\d{2}-\d{2}$/.test(s);
  const days = Math.min(Math.max(parseInt(url.searchParams.get("days") || "30", 10) || 30, 1), 400);
  const to = isDate(url.searchParams.get("to")) ? url.searchParams.get("to")! : pragueDate();
  const from = isDate(url.searchParams.get("from"))
    ? url.searchParams.get("from")!
    : pragueDate(new Date(Date.now() - (days - 1) * 86400000));

  const store = getStore({ name: STORE_NAME, consistency: "strong" });
  const totals: Record<string, Record<string, number>> = {};
  const bySource: Record<string, Record<string, number>> = {};
  const byCampaign: Record<string, Record<string, number>> = {};
  const byPage: Record<string, Record<string, number>> = {};
  const daily: Record<string, Record<string, number>> = {};
  let count = 0;

  for await (const page of store.list({ paginate: true })) {
    for (const b of page.blobs) {
      const k = parseKey(b.key);
      if (!k || k.date < from || k.date > to) continue;
      count++;
      totals[k.event] ??= {};
      bump(totals[k.event], "celkem");
      bySource[k.src] ??= {};
      bump(bySource[k.src], k.event);
      byCampaign[`${k.src} / ${k.camp}`] ??= {};
      bump(byCampaign[`${k.src} / ${k.camp}`], k.event);
      byPage[k.page] ??= {};
      bump(byPage[k.page], k.event);
      daily[k.date] ??= {};
      bump(daily[k.date], `${k.src}:${k.event}`);
    }
  }

  const sortedDaily = Object.fromEntries(Object.entries(daily).sort(([a], [b]) => a.localeCompare(b)));
  return json({
    obdobi: { od: from, do: to },
    zaznamu: count,
    souhrn: totals,
    vysvetlivky: {
      landing: "příchod na web z odkazu s kampaňovými parametry (gclid, fbclid, utm_*)",
      booking: "klik na rezervaci přes /go/rezervace; zdroj podle stránky, ze které klik přišel",
      "web": "klik na rezervaci ze stránky bez kampaňových parametrů (organika, přímý vstup…)",
    },
    podle_zdroje: bySource,
    podle_kampane: byCampaign,
    podle_stranky: byPage,
    po_dnech: sortedDaily,
  });
};

export const config: Config = {
  path: "/api/fp-stats",
  onError: "bypass",
};
