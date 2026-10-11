/* Fit Pilates — anonymní počítadlo příchodů z kampaní a kliků na rezervaci
 * Přidáno: 11.10.2026
 *
 * Proč: GA4 vidí jen návštěvníky, kteří přijmou cookies (u nás ~25 % příchodů
 * z reklam). Tohle počítadlo běží na serveru (Netlify Edge) jako obdoba
 * serverového logu: nic neukládá do prohlížeče, nečte cookies, neukládá IP,
 * user-agent ani ID kliknutí. Ukládá jen agregovatelný záznam
 * „den / zdroj / událost / kampaň / stránka“.
 *
 * Klíč záznamu v Netlify Blobs (store „fp-attribution“):
 *   YYYY-MM-DD/<zdroj>/<udalost>/<kampan>/<stranka>/<nahodny-suffix>
 * Obsah záznamu je prázdný — všechno podstatné je v klíči, takže statistiky
 * stačí spočítat z výpisu klíčů a nevzniká souběh při zápisu.
 */

import { getStore } from "@netlify/blobs";

export const STORE_NAME = "fp-attribution";
export const SITE_HOST = "fitpilates.cz";

export type Attribution = { src: string; camp: string };

/* Parametry, podle kterých poznáme placený nebo kampaňový příchod */
export const CAMPAIGN_PARAMS = [
  "gclid", "gbraid", "wbraid", "fbclid",
  "utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term",
];

const PAID_MEDIUMS = /^(cpc|ppc|paid|paidsocial|paid_social|paid-social|ads?|display|cpm)$/;
const META_SOURCES = /^(facebook|fb|instagram|ig|meta|messenger|audience_network)$/;

/* Bezpečný krátký slug: bez diakritiky, jen a-z 0-9 a pomlčky */
export function slug(input: string | null | undefined, max = 48): string {
  if (!input) return "";
  return input
    .normalize("NFD").replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, max)
    .replace(/-+$/g, "");
}

/* Stránka z cesty: "/" → "home", "/pilates-na-strojich/" → "pilates-na-strojich" */
export function pageSlug(pathname: string): string {
  const s = slug(pathname.replace(/\/index\.html$/, "/"), 60);
  return s || "home";
}

/* Z parametrů URL určí zdroj a kampaň. Vrací null, když nejde o kampaňový příchod. */
export function classify(params: URLSearchParams): Attribution | null {
  const source = slug(params.get("utm_source"), 32);
  const medium = slug(params.get("utm_medium"), 32);
  const campaign = slug(params.get("utm_campaign")) || slug(params.get("utm_content"));
  const hasGoogleClick = params.has("gclid") || params.has("gbraid") || params.has("wbraid");
  const hasFbClick = params.has("fbclid");

  if (hasGoogleClick || (source === "google" && PAID_MEDIUMS.test(medium))) {
    return { src: "google-ads", camp: campaign || "auto" };
  }
  if (META_SOURCES.test(source)) {
    return { src: PAID_MEDIUMS.test(medium) ? "meta" : "meta-organic", camp: campaign || "-" };
  }
  if (source) {
    return { src: source, camp: campaign || "-" };
  }
  if (hasFbClick) {
    /* fbclid bez UTM = sdílený odkaz z Facebooku/Instagramu, ne naše reklama */
    return { src: "meta-organic", camp: "-" };
  }
  return null;
}

/* Boti, náhledy odkazů a přednačítání se nepočítají */
const BOT_UA = /bot|crawl|spider|slurp|facebookexternalhit|facebookcatalog|meta-externalagent|preview|headless|lighthouse|pagespeed|inspectiontool|adsbot|mediapartners|curl|wget|python|httpclient|java\//i;

export function isNoise(req: Request): boolean {
  const ua = req.headers.get("user-agent") || "";
  if (!ua || BOT_UA.test(ua)) return true;
  const purpose = [
    req.headers.get("sec-purpose"),
    req.headers.get("purpose"),
    req.headers.get("x-purpose"),
    req.headers.get("x-moz"),
  ].join(" ").toLowerCase();
  return /prefetch|prerender|preview/.test(purpose);
}

/* Datum v pražském čase (YYYY-MM-DD) */
export function pragueDate(d = new Date()): string {
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: "Europe/Prague", year: "numeric", month: "2-digit", day: "2-digit",
  }).format(d);
}

export function recordKey(event: string, a: Attribution, page: string, d = new Date()): string {
  const rnd = Math.random().toString(36).slice(2, 8);
  return [pragueDate(d), a.src || "-", event, a.camp || "-", page || "-", d.getTime().toString(36) + rnd].join("/");
}

export async function record(event: string, a: Attribution, page: string): Promise<void> {
  try {
    const store = getStore(STORE_NAME);
    await store.set(recordKey(event, a, page), "");
  } catch (err) {
    console.error("fp-attr record failed", err);
  }
}

/* Nechá zápis doběhnout po odeslání odpovědi, aby návštěvník nečekal */
export function inBackground(context: { waitUntil?: (p: Promise<unknown>) => void }, p: Promise<unknown>): Promise<unknown> | undefined {
  if (context && typeof context.waitUntil === "function") {
    context.waitUntil(p);
    return undefined;
  }
  return p;
}

/* Rozpad klíče zpět na položky (pro statistiky) */
export function parseKey(key: string): { date: string; src: string; event: string; camp: string; page: string } | null {
  const parts = key.split("/");
  if (parts.length < 6) return null;
  const [date, src, event, camp, page] = parts;
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) return null;
  return { date, src, event, camp, page };
}
