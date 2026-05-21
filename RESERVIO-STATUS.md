# Reservio setup — stav 21.5.2026

## Hotovo dnes ✅

### Account konfigurace
- Otevírací hodiny: Po–Pá 7–11 + 14–20, So+Ne zavřeno
- Zaměstnanec: Štefan Bitto (staffId `0410219e-d929-447a-a43b-6a071cd894c3`)
- 3 typy lekcí:
  - Individuální (serviceId `6b8b05de-12c0-4694-8e31-65c26486354e`), kapacita 1, 60min, 1290 Kč
  - Zkušební (serviceId `91c83beb-fe3b-4186-bd3f-75046f573dd9`), kapacita 1, 60min, 590 Kč
  - Skupinová (jiný serviceId, viz Reservio admin), kapacita 3, 60min, 790 Kč

### Zkušební lekce — popis upraven
> **Pouze pro první návštěvu.** Vstupní konzultace, analýza držení těla a plně vedená lekce na reformeru. 60 minut. Pro stávající klienty zvolte Individuální (1 290 Kč) nebo Skupinovou (790 Kč) lekci.

Premium positioning + jasná hranice. Štefan manuálně čistí případné duplicitní zneužití (Reservio neumí "first booking only" per service).

### Recurring eventy — Individuální Po 25.5.2026
Vytvořeno **7 eventů**, vše opakování Týdně Pondělí, 12 krát (= do 17.8.2026):
- Po 7:00–8:00
- Po 8:00–9:00
- Po 9:00–10:00
- Po 10:00–11:00
- Po 14:00–15:00
- Po 15:00–16:00
- Po 16:00–17:00

= **84 jednotlivých termínů v kalendáři**

### Booking page status
Klient na https://fit-pilates2.reservio.com/?week=2026-05-25 vidí v Po 25.5. všech 7 termínů jako "Individuální lekce, 1 dostupné místo". Štefan zaplňuje kalendář, klient si vybírá.

---

## Zbývá dotáhnout ⏳

### Individuální lekce — zbytek týdne
**3 sloty pro Po (zbývají):**
- Po 17:00–18:00
- Po 18:00–19:00
- Po 19:00–20:00

**10 slotů × 4 dny pro Út–Pá = 40 eventů:**
- Út 26.5., St 27.5., Čt 28.5., Pá 29.5.
- Časy: 7, 8, 9, 10, 14, 15, 16, 17, 18, 19

**Celkem: 43 Individuálních eventů**

### Zkušební lekce — celý týden
50 eventů (5 dní × 10 slotů). Stejný workflow, jen jiný serviceId.

### Skupinová lekce — strategicky
Štefan ji vypisuje individuálně (1 termín týdně, časem). Není potřeba vytvořit teď.

---

## Reservio limity a rozhodnutí 💰

### Aktuální stav
- **Pro trial vyprší 28.5.2026** (7 dní)
- Po vypršení: Free plán s **limit 40 rezervací/30 dní**
- Limit 40 narazí — po 40 klient rezervuje, ale Štefan **neuvidí kontakt** = nepoužitelné

### Plány (199 Kč/měs+)
- **Starter 199 Kč/měs**: 200 rezervací/30 dní, payment fee 1.89% + ~63 Kč, Google/iCal sync
- **Standard ~399 Kč/měs**: 500 rezervací/30 dní
- **Pro ~599 Kč/měs**: unlimited

### Doporučení pro Štefana
**Zaplatit Starter (199 Kč/měs)** ihned po Pro trialu — 200 rezervací bohatě stačí, payment fee nízký, Google sync pomůže Štefanovi vidět své lekce v telefonu.

---

## Workflow pro vytvoření dalšího recurring eventu

### URL navigation
```
https://app.reservio.com/business/6ed3d57e-2755-43b6-84be-0b9bfaa3291d/create?what=class&serviceId={SERVICE_ID}&staffId=0410219e-d929-447a-a43b-6a071cd894c3
```

### Service IDs
- Individuální: `6b8b05de-12c0-4694-8e31-65c26486354e`
- Zkušební: zatím není ověřeno z URL (jiné than 91c83beb-... — tot je class detail, ne create URL)
- Skupinová: neznámé

### JS injection (form fill)
```js
function setInputValue(input, value) {
  const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
  setter.call(input, value);
  input.dispatchEvent(new Event('input', { bubbles: true }));
  input.dispatchEvent(new Event('change', { bubbles: true }));
}
setInputValue(document.querySelector('input[name="startDate"]'), '2026-05-25');
setInputValue(document.querySelector('input[name="startTime"]'), 'HH:00');
setInputValue(document.querySelector('input[name="endDate"]'), '2026-05-25');
setInputValue(document.querySelector('input[name="endTime"]'), '(HH+1):00');
```

### Klikání
1. Klik na "Opakování" dropdown (souřadnice ~339, 516)
2. Klik na "Týdně" (souřadnice ~339, 664)
3. JS: nastav `input[name="repeatEndsAfter"]` na 12
4. Klik na "Uložit a pokračovat" (souřadnice ~1286, 270)
5. Wait 6s (save + redirect)
6. Klik "Pokračovat ve zkušební verzi" (souřadnice ~748, 471)

### Známé problémy
1. **Reservio rate-limit** po ~7-10 eventech rychle za sebou — app zamrzne na bílém screenu. Řešení: F5 reload, počkat 10-15s.
2. **Datum auto-shift** — pokud nastavíš jen startDate a Reservio si pamatuje předchozí den, **uloží na předchozí den**. Vždy ověř v kalendáři po save.
3. **Konflikt dvou eventů ve stejný čas** — Reservio NEzabráňuje overlap mezi Class eventy stejného Štefana. Když dáš Individuální Po 7:00 + Zkušební Po 7:00, oba se uloží. Pojďme **NEdávat všechny 3 typy lekcí do stejného slotu** — udělat jen Individuální + Zkušební, Skupinovou nech Štefana vypisovat manuálně.

---

## Příští kroky (po session se Štefanem)

1. **Štefan zaplatí Starter** (199 Kč/měs) — pak má smysl pokračovat
2. **Dotáhnout 43 Individuálních eventů** pro Po-Pá (~25 min)
3. **Vytvořit 50 Zkušebních eventů** pro Po-Pá (~30 min)
4. **Nechat Skupinovou ručně** — Štefan vypisuje 1 termín týdně podle poptávky
5. **Test rezervace** — udělat fake rezervaci jako klient, ověřit:
   - Email notifikace přijde Štefanovi
   - Klient dostane confirm
   - Kalendář ukazuje (1/1) místo (0/1)
6. **Vrátit embed iframe** zpět do `/rezervace/` — když je booking page plná termínů, iframe má smysl (ne prázdný kalendář)
