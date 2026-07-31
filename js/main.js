/*!
 * Bear Carpet Care — site behaviour.
 *
 * Replaces jQuery 3.4.1, Bootstrap 4 JS bundle, easing, waypoints, counterup,
 * Owl Carousel, Isotope and Lightbox (~370KB) with the handful of behaviours
 * this site actually uses. Loaded with `defer`, so the DOM is ready on execute.
 */
(function () {
  "use strict";

  var prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------------------------------------------------------
   * Navbar: mobile collapse toggle
   * ------------------------------------------------------------- */
  var toggler = document.querySelector('.navbar-toggler[data-target]');
  var collapse = toggler && document.querySelector(toggler.getAttribute('data-target'));

  function setCollapsed(open) {
    if (!collapse) return;
    collapse.classList.toggle('show', open);
    toggler.setAttribute('aria-expanded', open ? 'true' : 'false');
  }

  if (toggler && collapse) {
    toggler.setAttribute('aria-expanded', 'false');
    toggler.setAttribute('aria-controls', collapse.id);
    toggler.addEventListener('click', function (e) {
      e.preventDefault();
      setCollapsed(!collapse.classList.contains('show'));
    });
  }

  /* ---------------------------------------------------------------
   * Navbar: Services dropdown.
   * Desktop hover is handled in CSS; this covers click / keyboard,
   * which is the only way to open it on touch devices.
   * ------------------------------------------------------------- */
  var dropdowns = [].slice.call(document.querySelectorAll('.nav-item.dropdown'));

  function closeDropdowns(except) {
    dropdowns.forEach(function (d) {
      if (d === except) return;
      d.classList.remove('show');
      var m = d.querySelector('.dropdown-menu');
      var t = d.querySelector('.dropdown-toggle');
      if (m) m.classList.remove('show');
      if (t) t.setAttribute('aria-expanded', 'false');
    });
  }

  dropdowns.forEach(function (drop) {
    var toggle = drop.querySelector('.dropdown-toggle');
    var menu = drop.querySelector('.dropdown-menu');
    if (!toggle || !menu) return;

    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-haspopup', 'true');

    toggle.addEventListener('click', function (e) {
      e.preventDefault();
      var open = !menu.classList.contains('show');
      closeDropdowns(drop);
      drop.classList.toggle('show', open);
      menu.classList.toggle('show', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  document.addEventListener('click', function (e) {
    if (!e.target.closest('.nav-item.dropdown')) closeDropdowns(null);
    if (collapse && collapse.classList.contains('show') && !e.target.closest('.site-navbar')) {
      setCollapsed(false);
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    closeDropdowns(null);
    setCollapsed(false);
  });

  /* ---------------------------------------------------------------
   * Back-to-top button
   * ------------------------------------------------------------- */
  var backToTop = document.querySelector('.back-to-top');
  if (backToTop) {
    var ticking = false;
    var onScroll = function () {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(function () {
        backToTop.classList.toggle('is-visible', window.pageYOffset > 300);
        ticking = false;
      });
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    backToTop.addEventListener('click', function (e) {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: prefersReducedMotion ? 'auto' : 'smooth' });
    });
  }

  /* ---------------------------------------------------------------
   * "30 Years Experience" count-up, fired when it scrolls into view
   * ------------------------------------------------------------- */
  var counters = [].slice.call(document.querySelectorAll('[data-toggle="counter-up"]'));

  function runCounter(el) {
    var target = parseInt(el.textContent.replace(/\D/g, ''), 10);
    if (!target || prefersReducedMotion) return;
    var duration = 1600;
    var start = null;

    el.textContent = '0';
    (function step(now) {
      if (start === null) start = now;
      var progress = Math.min((now - start) / duration, 1);
      // easeOutQuad, so it settles rather than stopping dead
      el.textContent = Math.round(target * (1 - (1 - progress) * (1 - progress)));
      if (progress < 1) window.requestAnimationFrame(step);
    })(window.performance.now());
  }

  if (counters.length) {
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          runCounter(entry.target);
          io.unobserve(entry.target);
        });
      }, { threshold: 0.4 });
      counters.forEach(function (c) { io.observe(c); });
    } else {
      counters.forEach(runCounter);
    }
  }

  /* ---------------------------------------------------------------
   * Google Maps facade — the embed only loads once the user asks for
   * it, keeping ~900KB of third-party JS off the critical path.
   * ------------------------------------------------------------- */
  var mapFacade = document.querySelector('[data-map-embed]');
  if (mapFacade) {
    var loadMap = function () {
      var iframe = document.createElement('iframe');
      iframe.src = mapFacade.getAttribute('data-map-embed');
      iframe.title = 'Map of the Bear Carpet Care service area around Harrisburg, Pennsylvania';
      iframe.loading = 'lazy';
      iframe.referrerPolicy = 'no-referrer-when-downgrade';
      iframe.allowFullscreen = true;
      iframe.width = '100%';
      iframe.height = '100%';
      iframe.style.border = '0';
      iframe.style.position = 'absolute';
      iframe.style.inset = '0';
      mapFacade.innerHTML = '';
      mapFacade.appendChild(iframe);
      mapFacade.removeAttribute('data-map-embed');
    };
    mapFacade.addEventListener('click', loadMap);
    mapFacade.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); loadMap(); }
    });
  }

  /* ---------------------------------------------------------------
   * Copyright year
   * ------------------------------------------------------------- */
  var yearEl = document.getElementById('copy-year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();
})();
