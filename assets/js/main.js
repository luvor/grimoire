/* ═══════════════════════════════════════════════════════
   GRIMOIRE — Main JavaScript
   Scroll animations, card interactions
   ═══════════════════════════════════════════════════════ */

(function () {
  'use strict';

  // ── Nav Scroll Effect ────────────────────────────── //
  function handleNavScroll() {
    const nav = document.querySelector('.site-nav');
    if (!nav) return;

    let ticking = false;
    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          nav.classList.toggle('scrolled', window.scrollY > 80);
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });
  }

  // ── Intersection Observer for Scroll Animations ──── //
  function initScrollAnimations() {
    const observerOptions = {
      root: null,
      rootMargin: '0px 0px -60px 0px',
      threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);

    // Observe article cards
    document.querySelectorAll('.article-card').forEach((card, i) => {
      card.style.transitionDelay = `${i * 100}ms`;
      observer.observe(card);
    });

    // Observe other animated elements
    document.querySelectorAll('[data-animate]').forEach(el => {
      observer.observe(el);
    });
  }

  // ── Card Tilt Effect ─────────────────────────────── //
  function initCardEffects() {
    document.querySelectorAll('.card-inner').forEach(card => {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width;
        const y = (e.clientY - rect.top) / rect.height;

        const glowX = x * 100;
        const glowY = y * 100;

        card.style.setProperty('--glow-x', `${glowX}%`);
        card.style.setProperty('--glow-y', `${glowY}%`);
      });
    });
  }

  // ── Article Count / Stats ────────────────────────── //
  function updateStats() {
    const cards = document.querySelectorAll('.article-card');
    const countEl = document.querySelector('[data-article-count]');
    if (countEl) {
      countEl.textContent = cards.length;
    }
  }

  // ── Smooth Reveal on Page Load ───────────────────── //
  function initPageReveal() {
    document.body.classList.add('loaded');
  }

  // ── Initialize ───────────────────────────────────── //
  document.addEventListener('DOMContentLoaded', () => {
    handleNavScroll();
    initScrollAnimations();
    initCardEffects();
    updateStats();

    // Delayed reveal for smooth load
    requestAnimationFrame(() => {
      requestAnimationFrame(initPageReveal);
    });
  });
})();
