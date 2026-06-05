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
