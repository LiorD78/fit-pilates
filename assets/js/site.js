/* Fit Pilates — site.js
 * Mobile burger menu, nav scroll state, smooth scroll
 * Last updated: 2026-04-29
 */
(function () {
  'use strict';

  // ─── Mobile burger menu ───
  function initBurger() {
    var burger = document.querySelector('.nav-burger');
    var overlay = document.getElementById('nav-overlay');
    if (!burger || !overlay) return;

    function open() {
      overlay.classList.add('open');
      burger.classList.add('open');
      burger.setAttribute('aria-expanded', 'true');
      document.body.style.overflow = 'hidden';
    }
    function close() {
      overlay.classList.remove('open');
      burger.classList.remove('open');
      burger.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    }
    function toggle() {
      if (overlay.classList.contains('open')) close();
      else open();
    }

    burger.addEventListener('click', toggle);

    // Close when clicking a link inside overlay
    overlay.addEventListener('click', function (e) {
      var t = e.target;
      if (t.tagName === 'A') close();
      // Click on overlay background (not on the menu content) = close
      if (t === overlay) close();
    });

    // Close on ESC
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && overlay.classList.contains('open')) close();
    });
  }

  // ─── Nav scroll state (already inline in some pages, but harmless to dedupe) ───
  function initNavScroll() {
    var nav = document.querySelector('nav');
    if (!nav) return;

    function update() {
      var scrolled = window.scrollY > 80;
      nav.classList.toggle('s', scrolled);
    }
    window.addEventListener('scroll', update, { passive: true });
    update();
  }

  // ─── Init ───
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      initBurger();
      initNavScroll();
    });
  } else {
    initBurger();
    initNavScroll();
  }
})();

/* ============================================================
   SITE-NAV: scroll state + burger toggle
   Aktualizováno: 17.5.2026 — liquid glass nav
   ============================================================ */
(function(){
  var nav = document.querySelector('.site-nav');
  if(!nav) return;

  function onScroll(){
    nav.classList.toggle('is-scrolled', window.scrollY > 40);
  }
  window.addEventListener('scroll', onScroll, {passive:true});
  onScroll();

  var burger = nav.querySelector('.site-nav__burger');
  var overlay = document.getElementById('siteNavOverlay');
  if(burger && overlay){
    function close(){
      overlay.classList.remove('is-open');
      overlay.setAttribute('hidden', '');
      burger.classList.remove('is-open');
      burger.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    }
    function open(){
      overlay.removeAttribute('hidden');
      overlay.classList.add('is-open');
      burger.classList.add('is-open');
      burger.setAttribute('aria-expanded', 'true');
      document.body.style.overflow = 'hidden';
    }
    burger.addEventListener('click', function(){
      if(overlay.classList.contains('is-open')) close(); else open();
    });
    overlay.addEventListener('click', function(e){
      if(e.target === overlay || e.target.tagName === 'A') close();
    });
    document.addEventListener('keydown', function(e){
      if(e.key === 'Escape' && overlay.classList.contains('is-open')) close();
    });
  }
})();

/* ============================================================
   Consent Mode v2 lišta + GA4 konverzní události + e-mail obfuskace
   Přidáno: 5.6.2026 — fitpilates analytics
   ============================================================ */
(function(){
  'use strict';
  function gtag(){ (window.dataLayer=window.dataLayer||[]).push(arguments); }
  var KEY='fp-consent';
  var GRANT={ad_storage:'granted',ad_user_data:'granted',ad_personalization:'granted',analytics_storage:'granted'};

  // Sklik slot — aktivuje se po marketingovém souhlasu (doplní se s první kampaní)
  function loadSklik(){
    if(window.__fpSklik) return; window.__fpSklik=true;
    /* TODO Sklik: až poběží kampaň, sem retargeting/měřící kód (c.seznam.cz/js/rc.js) */
  }
  function applyGranted(){ gtag('consent','update',GRANT); loadSklik(); }

  // ─── Konverzní události (booking/phone/email) ───
  function track(name, params){ gtag('event', name, params||{}); /* Sklik konverze slot */ }
  function initEvents(){
    document.addEventListener('click', function(e){
      var a=e.target && e.target.closest ? e.target.closest('a') : null;
      if(!a) return;
      var href=a.getAttribute('href')||'';
      if(/reservio\.com|isportsystem\.cz/i.test(href)) track('booking_click',{link_url:href});
      else if(href.indexOf('tel:')===0) track('phone_click');
      else if(href.indexOf('mailto:')===0 || (a.classList&&a.classList.contains('fp-email'))) track('email_click');
    }, true);
  }

  // ─── E-mail obfuskace: postav mailto z data-u/data-d (varianta 2) ───
  function initEmail(){
    var nodes=document.querySelectorAll('a.fp-email');
    for(var i=0;i<nodes.length;i++){
      var a=nodes[i], u=a.getAttribute('data-u'), d=a.getAttribute('data-d');
      if(u&&d) a.setAttribute('href','mailto:'+u+'@'+d);
    }
  }

  // ─── Cookie lišta ───
  function buildBanner(){
    var saved=null; try{ saved=localStorage.getItem(KEY); }catch(_){}
    if(saved){ if(saved==='granted') applyGranted(); return; }
    var css='.fp-cc{position:fixed;left:16px;right:16px;bottom:16px;z-index:99999;max-width:560px;margin:0 auto;background:#0f1115;color:#f3f3f0;border:1px solid rgba(196,154,60,.45);border-radius:14px;padding:18px 20px;box-shadow:0 12px 44px rgba(0,0,0,.5);font-family:Inter,system-ui,sans-serif;font-size:14px;line-height:1.55}.fp-cc p{margin:0 0 12px}.fp-cc a{color:#c49a3c}.fp-cc__row{display:flex;gap:10px;flex-wrap:wrap}.fp-cc button{flex:1;min-width:130px;padding:11px 16px;border-radius:999px;border:0;font-weight:600;font-size:14px;cursor:pointer;font-family:inherit}.fp-cc__ok{background:#c49a3c;color:#1a1a1a}.fp-cc__no{background:transparent;color:#f3f3f0;border:1px solid rgba(243,243,240,.35)}';
    var st=document.createElement('style'); st.textContent=css; document.head.appendChild(st);
    var box=document.createElement('div'); box.className='fp-cc';
    box.setAttribute('role','dialog'); box.setAttribute('aria-label','Souhlas s cookies');
    box.innerHTML='<p>Používáme cookies pro anonymní měření návštěvnosti a marketing. Více v <a href="/gdpr.html">zásadách ochrany údajů</a>.</p><div class="fp-cc__row"><button class="fp-cc__ok" type="button">Přijmout</button><button class="fp-cc__no" type="button">Odmítnout</button></div>';
    document.body.appendChild(box);
    box.querySelector('.fp-cc__ok').addEventListener('click',function(){ try{localStorage.setItem(KEY,'granted');}catch(_){} applyGranted(); box.parentNode&&box.parentNode.removeChild(box); });
    box.querySelector('.fp-cc__no').addEventListener('click',function(){ try{localStorage.setItem(KEY,'denied');}catch(_){} box.parentNode&&box.parentNode.removeChild(box); });
  }

  function init(){ initEvents(); initEmail(); buildBanner(); }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();

/* ============================================================
   Sticky mobilní CTA lišta + WhatsApp prefill + měření
   Přidáno: 14.8.2026 — mobilní konverzní trychtýř
   ============================================================ */
(function(){
  'use strict';
  var TEL   = '+420604925249';
  var WA    = '420604925249';
  var BOOK  = 'https://fitpilates.isportsystem.cz/';

  function gtag(){ (window.dataLayer=window.dataLayer||[]).push(arguments); }
  function track(name, params){ gtag('event', name, params||{}); }

  /* ── Předvyplněná WhatsApp zpráva podle stránky ── */
  var WA_TEXTS = {
    '/bolest-zad-praha/': 'Dobrý den, řeším bolesti zad ze sedavé práce a zajímá mě úvodní konzultace. Můžeme domluvit termín?',
    '/restart-po-40/':    'Dobrý den, po delší pauze bych se rád(a) vrátil(a) k pohybu. Zajímá mě úvodní konzultace.',
    '/pilates-na-strojich/': 'Dobrý den, zajímá mě pilates na strojích. Rád(a) bych domluvil(a) úvodní konzultaci.',
    '/pilates-allegro/':  'Dobrý den, zajímá mě reformer pilates. Můžeme domluvit úvodní konzultaci?',
    '/silovy-trenink/':   'Dobrý den, zajímá mě silový a funkční trénink. Můžeme domluvit úvodní konzultaci?',
    '/kondicni-box/':     'Dobrý den, zajímá mě kondiční box. Můžeme domluvit úvodní konzultaci?',
    '/osobni-trener-praha-10/': 'Dobrý den, hledám osobního trenéra v Praze 10. Zajímá mě úvodní konzultace.'
  };
  function waText(){
    return WA_TEXTS[location.pathname] ||
      'Dobrý den, mám zájem o úvodní konzultaci ve Fit Pilates. Můžeme domluvit termín?';
  }
  function waHref(){ return 'https://wa.me/' + WA + '?text=' + encodeURIComponent(waText()); }

  /* Doplní prefill do všech existujících wa.me odkazů bez ?text= */
  function initWaPrefill(){
    var links = document.querySelectorAll('a[href*="wa.me/"]');
    for (var i=0;i<links.length;i++){
      var h = links[i].getAttribute('href') || '';
      if (h.indexOf('text=') === -1) links[i].setAttribute('href', waHref());
    }
  }

  /* ── Měření: WhatsApp + odeslání formuláře ── */
  function initExtraEvents(){
    document.addEventListener('click', function(e){
      var a = e.target && e.target.closest ? e.target.closest('a') : null;
      if (!a) return;
      var href = a.getAttribute('href') || '';
      if (href.indexOf('wa.me/') > -1){
        track('whatsapp_click', { placement: a.getAttribute('data-fp-place') || 'inline' });
      }
    }, true);

    var form = document.getElementById('fp-form');
    if (form) form.addEventListener('submit', function(){
      track('form_submit', { form_name: form.getAttribute('name') || 'poptavka' });
    });
  }

  /* ── Sticky CTA lišta ── */
  function initSticky(){
    if (document.querySelector('.fp-sticky')) return;

    var bar = document.createElement('div');
    bar.className = 'fp-sticky';
    bar.innerHTML =
      '<a class="fp-sticky__main" data-fp-place="sticky" href="' + BOOK + '" target="_blank" rel="noopener">Rezervovat konzultaci</a>' +
      '<a class="fp-sticky__icon" data-fp-place="sticky" href="tel:' + TEL + '" aria-label="Zavolat Štefanovi">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>' +
      '</a>' +
      '<a class="fp-sticky__icon" data-fp-place="sticky" href="' + waHref() + '" target="_blank" rel="noopener" aria-label="Napsat na WhatsApp">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>' +
      '</a>';
    document.body.appendChild(bar);
    document.body.classList.add('has-sticky-cta');

    /* Skryje se u kontaktního formuláře a patičky, ať nepřekrývá obsah */
    var stop = document.getElementById('kontakt') || document.querySelector('footer');
    var forced = false;
    if (stop && 'IntersectionObserver' in window){
      new IntersectionObserver(function(entries){
        forced = entries[0].isIntersecting;
        bar.classList.toggle('is-visible', !forced);
      }, { rootMargin: '0px 0px -40% 0px' }).observe(stop);
    }
    requestAnimationFrame(function(){ if(!forced) bar.classList.add('is-visible'); });
  }

  /* Lišta se vytvoří i odstraní podle šířky okna za běhu (bez reloadu) */
  function syncSticky(){
    var narrow = !window.matchMedia || window.matchMedia('(max-width:900px)').matches;
    if (narrow) { initSticky(); return; }
    var bar = document.querySelector('.fp-sticky');
    if (bar) { bar.remove(); document.body.classList.remove('has-sticky-cta'); }
  }

  function initStickyWatcher(){
    if (!window.matchMedia) { syncSticky(); return; }
    var mq = window.matchMedia('(max-width:900px)');
    if (mq.addEventListener) mq.addEventListener('change', syncSticky);
    else if (mq.addListener) mq.addListener(syncSticky);
    syncSticky();
  }

  function init(){ initWaPrefill(); initExtraEvents(); initStickyWatcher(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
