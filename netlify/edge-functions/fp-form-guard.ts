/* Fit Pilates — serverová kontrola odeslaných formulářů (Netlify Forms)
 * Přidáno: 20.10.2026
 *
 * Proč: 20. 10. 2026 v 15:50 přišla Štefanovi „poptávka“ úplně prázdná
 * (vyplněné jen skryté pole stranka=homepage). Povinná pole (required) hlídá
 * jen prohlížeč — robot, který pošle POST rovnou na server, je obejde,
 * a honeypot bot-field nechytí robota, který nevyplní nic.
 *
 * Co dělá: před zpracováním v Netlify Forms zkontroluje odeslání formulářů
 * „poptavka“ a „vstupni-lekce“. Když chybí jméno nebo kontakt (e-mail
 * či telefon), nebo je vyplněný honeypot, odeslání zahodí — do Netlify Forms
 * ani do e-mailu se nedostane. Odesílatel dostane přesměrování na /dekujeme/
 * (robot nepozná, že neuspěl). Zahozené odeslání se anonymně započte
 * do počítadla (událost „form_blocked“, viz /api/fp-stats).
 *
 * Skutečný návštěvník se sem nedostane: prohlížeč ho bez jména a kontaktu
 * odeslat nepustí (atributy required + kontrola checkValidity v JS).
 * Ostatní formuláře a požadavky propouští beze změny.
 */
import type { Config, Context } from "@netlify/edge-functions";
import { inBackground, record } from "../lib/fp-attr.ts";

const GUARDED_FORMS = new Set(["poptavka", "vstupni-lekce"]);
const MAX_BODY_BYTES = 100_000;

function clean(v: FormDataEntryValue | null): string {
  return typeof v === "string" ? v.trim() : "";
}

function hasEmail(v: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
}

function hasPhone(v: string): boolean {
  return v.replace(/\D/g, "").length >= 9;
}

/* Vrací důvod zahození, nebo null, když je odeslání v pořádku */
function rejectReason(data: FormData): string | null {
  if (clean(data.get("bot-field"))) return "honeypot";
  if (clean(data.get("jmeno")).length < 2) return "bez-jmena";
  const email = clean(data.get("email"));
  const telefon = clean(data.get("telefon"));
  if (!hasEmail(email) && !hasPhone(telefon)) return "bez-kontaktu";
  return null;
}

export default async (req: Request, context: Context) => {
  if (req.method !== "POST") return;

  const type = (req.headers.get("content-type") || "").toLowerCase();
  if (!type.includes("application/x-www-form-urlencoded") && !type.includes("multipart/form-data")) return;

  const len = Number(req.headers.get("content-length") || "0");
  if (len > MAX_BODY_BYTES) return;

  let data: FormData;
  try {
    data = await req.clone().formData();
  } catch (_) {
    return; // nečitelné tělo → nech rozhodnout Netlify
  }

  const formName = clean(data.get("form-name"));
  if (!GUARDED_FORMS.has(formName)) return;

  const reason = rejectReason(data);
  if (!reason) return; // v pořádku → Netlify Forms zpracuje původní požadavek

  await inBackground(context, record("form_blocked", { src: "web", camp: reason }, formName));

  return new Response(null, {
    status: 303,
    headers: {
      "location": "/dekujeme/",
      "cache-control": "no-store",
      "x-robots-tag": "noindex, nofollow",
      "x-fp-form-guard": "blocked",
    },
  });
};

export const config: Config = {
  path: "/*",
  method: ["POST"],
  excludedPath: ["/.netlify/*", "/api/*", "/go/*"],
  onError: "bypass",
};
