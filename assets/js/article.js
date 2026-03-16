/* ═══════════════════════════════════════════════════════
   GRIMOIRE — Article Page JavaScript
   Reading progress, TOC generation, reading time, scroll
   ═══════════════════════════════════════════════════════ */

(function () {
  'use strict';

  // ── Reading Progress Bar ─────────────────────────── //
  function initReadingProgress() {
    const progressBar = document.querySelector('.reading-progress');
    const article = document.querySelector('.article-body');
    if (!progressBar || !article) return;

    let ticking = false;
    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          const rect = article.getBoundingClientRect();
          const articleTop = rect.top + window.scrollY;
          const articleHeight = rect.height;
          const scrolled = window.scrollY - articleTop;
          const progress = Math.max(0, Math.min(100, (scrolled / (articleHeight - window.innerHeight)) * 100));
          progressBar.style.width = `${progress}%`;
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });
  }

  // ── Table of Contents Generation ─────────────────── //
  function initTOC() {
    const article = document.querySelector('.article-body');
    const tocContainer = document.querySelector('.toc-list');
    const tocSidebar = document.querySelector('.toc-sidebar');
    if (!article || !tocContainer) return;

    const headings = article.querySelectorAll('h2, h3');
    if (headings.length < 3) {
      if (tocSidebar) tocSidebar.style.display = 'none';
      return;
    }

    headings.forEach((heading, i) => {
      // Generate ID if not present
      if (!heading.id) {
        heading.id = 'section-' + heading.textContent
          .toLowerCase()
          .replace(/[^\wа-яё]+/gi, '-')
          .replace(/^-+|-+$/g, '');
      }

      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = `#${heading.id}`;
      a.textContent = heading.textContent;
      a.classList.add(`toc-${heading.tagName.toLowerCase()}`);

      a.addEventListener('click', (e) => {
        e.preventDefault();
        heading.scrollIntoView({ behavior: 'smooth', block: 'start' });
        history.pushState(null, '', `#${heading.id}`);
      });

      li.appendChild(a);
      tocContainer.appendChild(li);
    });

    // Active heading tracking
    const tocLinks = tocContainer.querySelectorAll('a');

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            tocLinks.forEach(link => link.classList.remove('active'));
            const activeLink = tocContainer.querySelector(`a[href="#${entry.target.id}"]`);
            if (activeLink) activeLink.classList.add('active');
          }
        });
      },
      { rootMargin: '-80px 0px -70% 0px', threshold: 0 }
    );

    headings.forEach(h => observer.observe(h));

    // Show TOC after scrolling past hero
    if (tocSidebar) {
      const heroObserver = new IntersectionObserver(
        ([entry]) => {
          tocSidebar.classList.toggle('visible', !entry.isIntersecting);
        },
        { threshold: 0 }
      );

      const hero = document.querySelector('.article-hero');
      if (hero) heroObserver.observe(hero);
    }
  }

  // ── Reading Time Calculation ─────────────────────── //
  function initReadingTime() {
    const article = document.querySelector('.article-body');
    const timeEl = document.querySelector('[data-reading-time]');
    if (!article || !timeEl) return;

    const text = article.textContent || '';
    // Average reading speed: 200 words/min for Russian text
    const words = text.trim().split(/\s+/).length;
    const minutes = Math.max(1, Math.ceil(words / 200));

    // Russian plural form for "минут/минуты/минута"
    let label;
    const lastTwo = minutes % 100;
    const lastOne = minutes % 10;
    if (lastTwo >= 11 && lastTwo <= 19) {
      label = 'минут';
    } else if (lastOne === 1) {
      label = 'минута';
    } else if (lastOne >= 2 && lastOne <= 4) {
      label = 'минуты';
    } else {
      label = 'минут';
    }

    timeEl.textContent = `${minutes} ${label} чтения`;
  }

  // ── Back to Top Button ───────────────────────────── //
  function initBackToTop() {
    const btn = document.querySelector('.back-to-top');
    if (!btn) return;

    let ticking = false;
    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          btn.classList.toggle('visible', window.scrollY > 600);
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });

    btn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ── Footnote Tooltips ────────────────────────────── //
  function initFootnotes() {
    document.querySelectorAll('.footnote-ref').forEach(ref => {
      ref.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = ref.getAttribute('href').slice(1);
        const target = document.getElementById(targetId);
        if (target) {
          target.scrollIntoView({ behavior: 'smooth', block: 'center' });
          target.style.background = 'var(--color-accent-dim)';
          setTimeout(() => {
            target.style.background = '';
          }, 2000);
        }
      });
    });
  }

  // ── Image Lightbox (simple) ──────────────────────── //
  function initLightbox() {
    const images = document.querySelectorAll('.article-body figure img');
    images.forEach(img => {
      img.style.cursor = 'zoom-in';
      img.addEventListener('click', () => {
        const overlay = document.createElement('div');
        overlay.style.cssText = `
          position: fixed; inset: 0; z-index: 100000;
          background: rgba(0,0,0,0.92); display: flex;
          align-items: center; justify-content: center;
          cursor: zoom-out; animation: fadeIn 0.3s ease;
          backdrop-filter: blur(20px);
        `;

        const clone = img.cloneNode();
        clone.style.cssText = `
          max-width: 90vw; max-height: 90vh;
          object-fit: contain; border-radius: 2px;
          box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        `;

        overlay.appendChild(clone);
        document.body.appendChild(overlay);

        const close = () => {
          overlay.style.opacity = '0';
          overlay.style.transition = 'opacity 0.2s ease';
          setTimeout(() => overlay.remove(), 200);
        };

        overlay.addEventListener('click', close);
        document.addEventListener('keydown', function handler(e) {
          if (e.key === 'Escape') {
            close();
            document.removeEventListener('keydown', handler);
          }
        });
      });
    });
  }

  // ── Initialize ───────────────────────────────────── //
  document.addEventListener('DOMContentLoaded', () => {
    initReadingProgress();
    initTOC();
    initReadingTime();
    initBackToTop();
    initFootnotes();
    initLightbox();
  });
})();
