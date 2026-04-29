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
