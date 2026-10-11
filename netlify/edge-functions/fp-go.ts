/* Fit Pilates — přesměrování s anonymním započtením kliku
 * Přidáno: 11.10.2026
 *   /go/rezervace → https://fitpilates.isportsystem.cz/   (událost „booking“)
 *   /go/whatsapp  → https://wa.me/420604925249?text=…      (událost „whatsapp“)
 * Zdroj kliku se určí z adresy stránky, ze které návštěvník přišel
 * (hlavička Referer; web posílá v rámci vlastní domény celou URL).
 */
import type { Config, Context } from "@netlify/edge-functions";
import { classify, inBackground, isNoise, pageSlug, record, SITE_HOST } from "../lib/fp-attr.ts";

const BOOKING_ORIGIN = "https://fitpilates.isportsystem.cz";
const WHATSAPP_NUMBER = "420604925249";
const WHATSAPP_DEFAULT_TEXT = "Dobrý den, mám zájem o vstupní lekci za 590 Kč ve Fit Pilates. Můžeme domluvit termín?";

/* Rezervace: volitelná cílová cesta v rámci iSportu (?p=/neco); cokoli jiného → úvodní stránka */
function bookingTarget(url: URL): string {
  const p = url.searchParams.get("p") || "/";
  return /^\/[A-Za-z0-9\/_.=&?%-]*$/.test(p) && !p.startsWith("//") ? BOOKING_ORIGIN + p : BOOKING_ORIGIN + "/";
}

/* WhatsApp: vždy jen na Štefanovo číslo; předvyplněný text (?t=…) zkrácený na rozumnou délku */
function whatsappTarget(url: URL): string {
  const raw = (url.searchParams.get("t") || "").replace(/[\u0000-\u001f\u007f]/g, " ").trim();
  const text = (raw || WHATSAPP_DEFAULT_TEXT).slice(0, 400);
  return `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(text)}`;
}

export default async (req: Request, context: Context) => {
  const url = new URL(req.url);
  const isWhatsapp = url.pathname.replace(/\/+$/, "") === "/go/whatsapp";
  const location = isWhatsapp ? whatsappTarget(url) : bookingTarget(url);
  const event = isWhatsapp ? "whatsapp" : "booking";

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
    await inBackground(context, record(event, src, page));
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
  path: ["/go/rezervace", "/go/whatsapp"],
  onError: "bypass",
};
