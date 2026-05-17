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
