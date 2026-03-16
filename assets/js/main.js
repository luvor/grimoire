/* ═══════════════════════════════════════════════════════
   GRIMOIRE — Main JavaScript
   Theme toggle, scroll animations, card interactions
   ═══════════════════════════════════════════════════════ */

(function () {
  'use strict';

  // ── Theme Management ─────────────────────────────── //
  const THEME_KEY = 'grimoire-theme';

  function getPreferredTheme() {
    const stored = localStorage.getItem(THEME_KEY);
    if (stored) return stored;
    return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  }

  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(THEME_KEY, theme);
    const toggle = document.querySelector('.theme-toggle');
    if (toggle) {
      toggle.setAttribute('aria-pressed', theme === 'light' ? 'true' : 'false');
    }
    // Update theme-color meta for browser chrome / PWA
    document.querySelectorAll('meta[name="theme-color"]').forEach(m => m.remove());
    const meta = document.createElement('meta');
    meta.name = 'theme-color';
    meta.content = theme === 'light' ? '#faf8f5' : '#0a0a0f';
    document.head.appendChild(meta);
  }

  // Apply theme immediately to prevent flash
  setTheme(getPreferredTheme());

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
    // Theme toggle
    const toggle = document.querySelector('.theme-toggle');
    if (toggle) {
      toggle.addEventListener('click', () => {
        const current = document.documentElement.getAttribute('data-theme') || 'dark';
        setTheme(current === 'dark' ? 'light' : 'dark');
      });
    }

    handleNavScroll();
    initScrollAnimations();
    initCardEffects();
    updateStats();

    // Delayed reveal for smooth load
    requestAnimationFrame(() => {
      requestAnimationFrame(initPageReveal);
    });
  });

  // Listen for system theme changes
  window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', (e) => {
    if (!localStorage.getItem(THEME_KEY)) {
      setTheme(e.matches ? 'light' : 'dark');
    }
  });
})();
