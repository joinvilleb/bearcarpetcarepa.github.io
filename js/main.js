/*! Bear Carpet Care — site behaviour.
 *
 * No framework. Everything here is progressive: with JavaScript off the
 * navigation still renders (CSS :hover opens the desktop submenu), links
 * work, and no content is hidden.
 */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return [].slice.call((c || document).querySelectorAll(s)); };

  /* --- Navigation ---------------------------------------------- */
  var toggle = $(".nav-toggle");
  var nav = $("#nav");

  function setNav(open) {
    if (!nav) return;
    nav.toggleAttribute("data-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  }

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      setNav(!nav.hasAttribute("data-open"));
    });
  }

  // Submenu. On desktop CSS handles hover; this covers touch and keyboard.
  $$(".subnav-toggle").forEach(function (btn) {
    var parent = btn.closest(".has-sub");
    btn.addEventListener("click", function () {
      var open = !parent.hasAttribute("data-open");
      $$(".has-sub").forEach(function (p) { p.removeAttribute("data-open"); });
      parent.toggleAttribute("data-open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });

  document.addEventListener("click", function (e) {
    if (!e.target.closest(".has-sub")) {
      $$(".has-sub").forEach(function (p) {
        p.removeAttribute("data-open");
        var t = $(".subnav-toggle", p);
        if (t) t.setAttribute("aria-expanded", "false");
      });
    }
    if (nav && nav.hasAttribute("data-open") && !e.target.closest(".site-header")) setNav(false);
  });

  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    setNav(false);
    $$(".has-sub").forEach(function (p) { p.removeAttribute("data-open"); });
  });

  /* --- Back to top --------------------------------------------- */
  var top = $(".to-top");
  if (top) {
    var ticking = false;
    var onScroll = function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        top.toggleAttribute("data-visible", window.pageYOffset > 300);
        ticking = false;
      });
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
    top.addEventListener("click", function (e) {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: reduced ? "auto" : "smooth" });
    });
  }

  /* --- Count up ------------------------------------------------- */
  var counters = $$("[data-count]");
  function run(el) {
    var target = parseInt(el.getAttribute("data-count"), 10);
    if (!target || reduced) { el.textContent = String(target || el.textContent); return; }
    var start = null, duration = 1500;
    el.textContent = "0";
    (function step(now) {
      if (start === null) start = now;
      var p = Math.min((now - start) / duration, 1);
      el.textContent = String(Math.round(target * (1 - (1 - p) * (1 - p))));
      if (p < 1) requestAnimationFrame(step);
    })(performance.now());
  }
  if (counters.length && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        run(en.target);
        io.unobserve(en.target);
      });
    }, { threshold: 0.4 });
    counters.forEach(function (c) { io.observe(c); });
  } else {
    counters.forEach(run);
  }

  /* --- Hide the call bar once the footer is reached -------------
   * By then the number is on screen anyway, and the bar would only be
   * covering content. */
  var bar = $(".callbar");
  var footer = $(".site-footer");
  if (bar && footer && "IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { bar.toggleAttribute("data-hidden", en.isIntersecting); });
    }, { rootMargin: "0px 0px -40px 0px" }).observe(footer);
  }

  /* --- Map loads on request ------------------------------------
   * The embed pulls roughly 900KB of third-party JavaScript, so it stays
   * off the critical path until someone actually wants the map. */
  var mapBtn = $("[data-map]");
  if (mapBtn) {
    mapBtn.addEventListener("click", function () {
      var f = document.createElement("iframe");
      f.src = mapBtn.getAttribute("data-map");
      f.title = "Map of the Bear Carpet Care service area around Harrisburg, Pennsylvania";
      f.loading = "lazy";
      f.referrerPolicy = "no-referrer-when-downgrade";
      f.allowFullscreen = true;
      mapBtn.parentNode.appendChild(f);
      mapBtn.remove();
    });
  }

  /* --- Year ------------------------------------------------------ */
  var year = $("#year");
  if (year) year.textContent = new Date().getFullYear();
})();
