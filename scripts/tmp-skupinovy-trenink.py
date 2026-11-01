# -*- coding: utf-8 -*-
"""Sjednocení webu: nový Skupinový trénink (590 Kč, max. 6 osob) + reformer skupina jen Čt 19:00."""
import pathlib, re, sys

ROOT = pathlib.Path(".")
TERMINY = "Po a Út 18:00, St a Čt 16:00, Pá 14:00"
errors = []

def rep(path, old, new, count=1):
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    n = s.count(old)
    if n != count:
        errors.append(f"{path}: očekáváno {count}×, nalezeno {n}× → {old[:70]!r}")
        return
    p.write_text(s.replace(old, new), encoding="utf-8")

# 1) „další lekce od 790 Kč“ → od 590 Kč (všude)
for p in ROOT.rglob("*.html"):
    s = p.read_text(encoding="utf-8")
    if "další lekce od 790 Kč" in s:
        p.write_text(s.replace("další lekce od 790 Kč", "další lekce od 590 Kč"), encoding="utf-8")

# 2) index.html – prostřední karta ceníku
rep("index.html", """        <span class="p-name">Skupinová lekce</span>
        <div class="p-num">790</div>
        <div class="p-per">Kč · 60 min · max 3 osoby</div>
        <div class="p-per" style="margin-top:-22px;">Po 18:00 &middot; Čt 19:00</div>
        <div class="p-div"></div>
        <ul class="p-list">
          <li>Pondělí 18:00 a čtvrtek 19:00</li>
          <li>Pilates, fitness nebo box</li>
          <li>Max 3 osoby = skutečný osobní přístup</li>
          <li>Permanentka 10× = 6 990 Kč</li>
          <li>Platnost permanentky 4 měsíce</li>
        </ul>""", """        <span class="p-name">Skupinový trénink</span>
        <div class="p-num">590</div>
        <div class="p-per">Kč · 60 min · max 6 osob</div>
        <div class="p-div"></div>
        <ul class="p-list">
          <li>Po a Út 18:00 &middot; St a Čt 16:00 &middot; Pá 14:00</li>
          <li>Kondiční a funkční trénink, pilates na podložkách</li>
          <li>Max 6 osob = trenér vidí každého</li>
          <li>Skupina na reformerech: Čt 19:00, max 3 osoby, 790 Kč</li>
          <li>Permanentka 10× na reformeru = 6 990 Kč</li>
        </ul>""")

# 3) rezervace – meta + prostřední karta
rep("rezervace/index.html", "Vstupní lekce 590 Kč, skupinová 790 Kč, individuální 1 290 Kč.",
    "Vstupní lekce 590 Kč, skupinový trénink 590 Kč, individuální 1 290 Kč.")
rep("rezervace/index.html", 'alt="Skupinová lekce pilates pro maximálně 3 osoby v Praze 10"',
    'alt="Skupinový trénink v malé skupině do 6 osob ve studiu Fit Pilates v Praze 10"')
rep("rezervace/index.html", """        <div class="prog-name">Skupinová lekce</div>
        <div class="prog-en">Malá skupina</div>
        <div class="res-meta">
          <span>60 min</span>
          <span>Max 3 osoby</span>
          <span>Po 18:00 &middot; Čt 19:00</span>
        </div>
        <div class="res-price">790 Kč <em>/ lekce</em></div>
        <p class="prog-desc">Sdílená lekce s osobním přístupem. Tři reformery, tři lidé, jeden trenér. Dostatek prostoru i pozornosti — žádné davy, žádný ruch.</p>
        <div class="prog-tags">
          <span class="prog-tag">Pokročilejší</span>
          <span class="prog-tag">Allegro</span>
          <span class="prog-tag">Skupina</span>
        </div>
        <div class="prog-link">Rezervovat skupinovou</div>""", """        <div class="prog-name">Skupinový trénink</div>
        <div class="prog-en">Malá skupina</div>
        <div class="res-meta">
          <span>60 min</span>
          <span>Max 6 osob</span>
          <span>Po a Út 18:00 &middot; St a Čt 16:00 &middot; Pá 14:00</span>
        </div>
        <div class="res-price">590 Kč <em>/ lekce</em></div>
        <p class="prog-desc">Kondiční a funkční trénink a pilates na podložkách v malé skupině do šesti lidí, vede Štefan. Na reformerech cvičí skupina nejvýš tří lidí ve čtvrtek v 19:00 (790 Kč).</p>
        <div class="prog-tags">
          <span class="prog-tag">Začátečníci</span>
          <span class="prog-tag">Kondice</span>
          <span class="prog-tag">Skupina</span>
        </div>
        <div class="prog-link">Rezervovat skupinový trénink</div>""")

# 4) reformer-pilates-praha-10
f = "reformer-pilates-praha-10/index.html"
rep(f, '"name": "Skupinová lekce (max 3 osoby)",', '"name": "Skupinová lekce na reformeru (max 3 osoby)",')
old_faq = "Pravidelné termíny jsou pondělí od 18:00 a čtvrtek od 19:00. Lekce trvá 60 minut a probíhá ve studiu Fit Pilates na adrese U Trati 886/52, Praha 10 – Strašnice. Místo je potřeba rezervovat předem, protože kapacita jsou tři lidé."
new_faq = f"Skupinová lekce na reformeru probíhá každý čtvrtek od 19:00, trvá 60 minut a kapacita jsou tři lidé, proto je potřeba místo rezervovat předem. Kromě ní vedeme skupinový trénink bez strojů pro nejvýš šest lidí ({TERMINY}, 590 Kč). Obojí probíhá ve studiu Fit Pilates na adrese U Trati 886/52, Praha 10 – Strašnice."
rep(f, old_faq, new_faq, count=2)
rep(f, "Pravidelné termíny: <strong>pondělí 18:00</strong> a <strong>čtvrtek 19:00</strong>.",
    "Pravidelný termín: <strong>čtvrtek 19:00</strong>.")
rep(f, """  <p><a href="/rezervace/">Rezervovat skupinovou lekci</a></p>
</div>""", f"""  <p><a href="/rezervace/">Rezervovat skupinovou lekci</a></p>
</div>
<p>Bez strojů vedeme také <strong>skupinový trénink</strong> pro nejvýš šest lidí – kondiční a funkční cvičení a pilates na podložkách, 60 minut za 590 Kč. Termíny: {TERMINY}.</p>""")
rep(f, "<li><strong>Pravidelné termíny:</strong> pondělí 18:00, čtvrtek 19:00</li>",
    "<li><strong>Pravidelný termín:</strong> čtvrtek 19:00</li>")
old_cena = "Jedna skupinová lekce stojí 790 Kč, balíček deseti skupinových lekcí 6 990 Kč."
new_cena = "Jedna skupinová lekce na reformeru stojí 790 Kč, balíček deseti lekcí 6 990 Kč. Skupinový trénink bez strojů (max. 6 osob) stojí 590 Kč."
rep(f, old_cena, new_cena, count=2)

# 5) pilates-praha-10
f = "pilates-praha-10/index.html"
rep(f, "Skupinové lekce (max. 3 osoby) vycházejí na 790 Kč za 60 minut, individuální lekce na 1 290 Kč.",
    "Skupinové lekce na reformeru (max. 3 osoby) vycházejí na 790 Kč, skupinový trénink (max. 6 osob) na 590 Kč a individuální lekce na 1 290 Kč, vždy za 60 minut.")
rep(f, "Skupinové lekce (max. 3 osoby) vycházejí na <strong>790 Kč za 60 minut</strong>, individuální",
    "Skupinové lekce na reformeru (max. 3 osoby) vycházejí na <strong>790 Kč za 60 minut</strong>, skupinový trénink (max. 6 osob) na <strong>590 Kč</strong>, individuální")
rep(f, "<li>Skupinové lekce maximálně pro 3 osoby</li>",
    "<li>Malé skupiny – na reformerech nejvýš 3 osoby, skupinový trénink nejvýš 6</li>")
rep(f, "<p>Skupinové lekce mají maximálně 3 účastníky –", "<p>Skupinové lekce na reformeru mají maximálně 3 účastníky –")
rep(f, "díky maximálně tříčlenným skupinám se dostanete k individuálnímu vedení i v ceně skupinové lekce.",
    "díky malým skupinám (na reformeru nejvýš tři, ve skupinovém tréninku nejvýš šest lidí) se dostanete k osobnímu vedení i v ceně skupinové lekce.")
rep(f, "vycházejí na <strong>790 Kč za 60 minut</strong>. <a href=\"/individualni-reformer-pilates-praha/\">",
    f"vycházejí na <strong>790 Kč za 60 minut</strong> (čtvrtek 19:00). Skupinový trénink bez strojů pro nejvýš 6 osob stojí <strong>590 Kč</strong> ({TERMINY}). <a href=\"/individualni-reformer-pilates-praha/\">")

# 6) individualni-reformer-pilates-praha
f = "individualni-reformer-pilates-praha/index.html"
rep(f, '"name": "Skupinová lekce (max 3 osoby)",', '"name": "Skupinová lekce na reformeru (max 3 osoby)",')
rep(f, "Skupinová lekce probíhá v pevných termínech pro maximálně tři klienty;",
    "Skupinová lekce na reformeru probíhá v pevném termínu pro maximálně tři klienty, skupinový trénink bez strojů pro nejvýš šest;", count=2)
rep(f, "<p>Skupinové lekce ve Strašnicích — maximálně tři klienti, pevné termíny a průběh lekce.</p>",
    "<p>Skupinové lekce na reformeru ve Strašnicích — maximálně tři klienti, pevný termín a průběh lekce.</p>")

# 7) o-stefanovi
rep("o-stefanovi/index.html", "<p>Pracuji primárně 1:1. Malé skupiny (max. 3 osoby) jen pro klienty s podobnými cíli, vždy s individuálním plánem.</p>",
    "<p>Pracuji primárně 1:1. Na reformerech vedu malé skupiny nejvýš tří lidí, skupinový trénink bez strojů nejvýš pro šest – i tam znám každého jménem a hlídám jeho techniku.</p>")

# 8) bolest-zad-praha
f = "bolest-zad-praha/index.html"
rep(f, "Skupinové lekce mají maximálně 3 osoby.", "Skupinové lekce na reformeru mají maximálně 3 osoby, skupinový trénink bez strojů maximálně 6.", count=2)
rep(f, "<h3>Balíček 10 skupinových lekcí</h3>", "<h3>Balíček 10 skupinových lekcí na reformeru</h3>")

# 9) podminky
f = "podminky/index.html"
rep(f, "      <tr><td>Skupinová lekce (nejvýš 3 osoby)</td><td>790 Kč</td></tr>",
    "      <tr><td>Skupinový trénink (nejvýš 6 osob)</td><td>590 Kč</td></tr>\n      <tr><td>Skupinová lekce na reformeru (nejvýš 3 osoby)</td><td>790 Kč</td></tr>")
rep(f, "<tr><td>Permanentka 10 skupinových lekcí</td>", "<tr><td>Permanentka 10 skupinových lekcí na reformeru</td>")
rep(f, "Studio má na lekci nejvýš tři místa a termín drží jen pro vás.", "Lekce mají jen pár míst a termín držíme jen pro vás.")

# 10) vstupni-lekce
f = "vstupni-lekce/index.html"
rep(f, "Další lekce od 790 Kč (skupinka max. 3 osob) nebo 1 290 Kč individuálně.",
    "Další lekce od 590 Kč (skupinový trénink, max. 6 osob), 790 Kč (skupinka na reformeru, max. 3 osoby) nebo 1 290 Kč individuálně.")
rep(f, "      <div><dt>Lekce ve skupince (max. 3 osoby)</dt><dd>790 Kč</dd></div>",
    "      <div><dt>Skupinový trénink (max. 6 osob)</dt><dd>590 Kč</dd></div>\n      <div><dt>Lekce ve skupince na reformeru (max. 3 osoby)</dt><dd>790 Kč</dd></div>")
rep(f, "<dt>10 lekcí ve skupince / individuálně</dt>", "<dt>10 lekcí na reformeru ve skupince / individuálně</dt>")

# 11) osobni-trener-praha-10
f = "osobni-trener-praha-10/index.html"
rep(f, "vždy ve formátu 1:1 nebo maximálně 3 osoby, nikdy v anonymním davu.", "vždy 1:1 nebo v malé skupině, nikdy v anonymním davu.")
rep(f, "vždy ve formátu 1:1 nebo maximálně 3 osoby.</p>", "vždy 1:1 nebo v malé skupině (na reformerech nejvýš 3, ve skupinovém tréninku nejvýš 6 osob).</p>")
rep(f, "Skupinový balíček 10 lekcí (max. 3 osoby) stojí 6 990 Kč.", "Balíček 10 skupinových lekcí na reformeru (max. 3 osoby) stojí 6 990 Kč, skupinový trénink bez strojů (max. 6 osob) 590 Kč za lekci.")
rep(f, "✦ Formát 1:1 nebo max. 3 osoby", "✦ Formát 1:1 nebo malá skupina")
rep(f, "ve dvojici nebo v malé skupině max. 3 osob, bez publika.", "ve dvojici nebo v malé skupině, bez publika.")
rep(f, "<td>Balíček 10 lekcí — skupinový (max. 3 osoby)</td>", "<td>Balíček 10 lekcí — skupinový na reformeru (max. 3 osoby)</td>")
rep(f, "skupinový balíček 10 lekcí (max. 3 osoby) na 6 990 Kč", "skupinový balíček 10 lekcí na reformeru (max. 3 osoby) na 6 990 Kč, skupinový trénink (max. 6 osob) na 590 Kč za lekci")

# 12) restart-po-40
f = "restart-po-40/index.html"
rep(f, "Balíček deseti skupinových lekcí (max. 3 osoby).", "Balíček deseti skupinových lekcí na reformeru (max. 3 osoby).")
rep(f, "i malou skupinku nejvýš tří lidí (790 Kč).", "i malé skupiny – na reformeru nejvýš tři lidé (790 Kč), skupinový trénink nejvýš šest (590 Kč).")

# 13) blog
rep("blog/co-je-reformer-pilates/index.html", "Skupinová lekce (max 3 osoby) stojí 790 Kč,", "Skupinová lekce na reformeru (max 3 osoby) stojí 790 Kč, skupinový trénink bez strojů (max 6 osob) 590 Kč,")
rep("blog/co-je-reformer-pilates/index.html", "Skupinové lekce ve Fit Pilates mají maximálně 3 osoby,", "Skupinové lekce na reformeru ve Fit Pilates mají maximálně 3 osoby,")
rep("blog/pilates-apparatus-stroje/index.html", "Skupinová lekce (max. 3 osoby) stojí 790 Kč,", "Skupinová lekce na reformeru (max. 3 osoby) stojí 790 Kč,")
rep("blog/reformer-pilates-praha/index.html", "Pravidelné skupinové lekce stojí 790 Kč ve skupince max. 3 lidí", "Pravidelné skupinové lekce na reformeru stojí 790 Kč ve skupince max. 3 lidí")

# 14) llms.txt
f = "llms.txt"
rep(f, "Individuální lekce 1:1 i malé skupiny max. 3 osob.", "Individuální lekce 1:1, skupiny na reformerech max. 3 osob a skupinový trénink max. 6 osob.")
rep(f, "- **Formáty:** individuální lekce 1:1 (60 min) a skupinová lekce max. 3 osoby",
    "- **Formáty:** individuální lekce 1:1, skupinová lekce na reformeru (max. 3 osoby) a skupinový trénink bez strojů (max. 6 osob); vše 60 min")
rep(f, "- **Pravidelné skupinové termíny:** pondělí 18:00 a čtvrtek 19:00",
    f"- **Skupinový trénink (max. 6 osob):** {TERMINY}\n- **Skupinová lekce na reformeru (max. 3 osoby):** čtvrtek 19:00")
rep(f, "- Skupinová lekce (max. 3 osoby): **790 Kč**\n- Balíček 10 skupinových lekcí: **6 990 Kč**",
    "- Skupinový trénink (max. 6 osob): **590 Kč**\n- Skupinová lekce na reformeru (max. 3 osoby): **790 Kč**\n- Balíček 10 skupinových lekcí na reformeru: **6 990 Kč**")
rep(f, "Individuální lekce 1:1 i skupinové lekce max. 3 osob ve Strašnicích", "Individuální lekce 1:1 i skupinové lekce na reformeru (max. 3 osoby) ve Strašnicích")
rep(f, "skupinová lekce (max. 3 osoby) 790 Kč. Balíčky 10 lekcí: 11 490 Kč individuální, 6 990 Kč skupinové.",
    "skupinová lekce na reformeru (max. 3 osoby) 790 Kč, skupinový trénink (max. 6 osob) 590 Kč. Balíčky 10 lekcí: 11 490 Kč individuální, 6 990 Kč skupinové na reformeru.")
rep(f, "Ano, v malých skupinách max. 3 osob – pravidelně v pondělí 18:00 a ve čtvrtek 19:00. Díky malému počtu lektor koriguje techniku každého účastníka.",
    f"Ano. Skupinový trénink bez strojů pro max. 6 osob ({TERMINY}, 590 Kč) a skupinová lekce na reformeru pro max. 3 osoby (čtvrtek 19:00, 790 Kč). Díky malému počtu lektor koriguje techniku každého účastníka.")

# 15) CLAUDE.md ceník
rep("CLAUDE.md", "- Skupinová lekce (max 3 osoby): 790 Kč\n", f"- Skupinový trénink (max 6 osob, bez strojů): 590 Kč — {TERMINY}\n- Skupinová lekce na reformeru (max 3 osoby): 790 Kč — Čt 19:00\n")
rep("CLAUDE.md", "- Balíček 10 lekcí skupinový: 6 990 Kč", "- Balíček 10 lekcí skupinový (reformer): 6 990 Kč")

# 16) pilates-praha-10 – FAQ pro začátečníky
rep("pilates-praha-10/index.html", "je díky maximálně tříčlenným skupinám a 24leté praxi",
    "je díky malým skupinám (na reformeru nejvýš tři, ve skupinovém tréninku nejvýš šest lidí) a 24leté praxi")

if errors:
    print("CHYBY:"); print("\n".join(errors)); sys.exit(1)
print("OK – všechny náhrady provedeny")
