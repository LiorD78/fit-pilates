/* Fit Pilates — přesměrování na rezervace s anonymním započtením kliku
 * Přidáno: 11.10.2026
 * /go/rezervace → https://fitpilates.isportsystem.cz/
 * Zdroj kliku se určí z adresy stránky, ze které návštěvník přišel
 * (hlavička Referer; web posílá v rámci vlastní domény celou URL).
 */
import type { Config, Context } from "@netlify/edge-functions";
import { classify, inBackground, isNoise, pageSlug, record, SITE_HOST } from "../lib/fp-attr.ts";

const BOOKING_ORIGIN = "https://fitpilates.isportsystem.cz";

/* Volitelná cílová cesta v rámci iSportu (?p=/neco); cokoli jiného → úvodní stránka rezervací */
function target(url: URL): string {
  const p = url.searchParams.get("p") || "/";
  return /^\/[A-Za-z0-9\/_.=&?%-]*$/.test(p) && !p.startsWith("//") ? BOOKING_ORIGIN + p : BOOKING_ORIGIN + "/";
}

export default async (req: Request, context: Context) => {
  const url = new URL(req.url);
  const location = target(url);

  if (req.method === "GET" && !isNoise(req)) {
    let src = { src: "web", camp: "-" };
    let page = "-";
    const ref = req.headers.get("referer");
    if (ref) {
      try {
        const r = new URL(ref);
        const host = r.hostname.replace(/^www\./, "");
        if (host === SITE_HOST || host.endsWith(".netlify.app")) {
          page = pageSlug(r.pathname);
          src = classify(r.searchParams) || src;
        } else {
          src = { src: "externi", camp: "-" };
        }
      } catch (_) { /* neplatný Referer → počítá se jako web */ }
    }
    await inBackground(context, record("booking", src, page));
  }

  return new Response(null, {
    status: 302,
    headers: {
      "location": location,
      "cache-control": "no-store",
      "x-robots-tag": "noindex, nofollow",
      "referrer-policy": "strict-origin-when-cross-origin",
    },
  });
};

export const config: Config = {
  path: "/go/rezervace",
  onError: "bypass",
};
