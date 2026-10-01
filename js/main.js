/*! Bear Carpet Care — site behaviour.
 *
 * No framework. Everything here is progressive: with JavaScript off the
 * navigation still renders (CSS :hover opens the desktop submenu), links
 * work, and no content is hidden.
 */
(function () {
  "use strict";
  window.bccReady = true;

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return [].slice.call((c || document).querySelectorAll(s)); };

  /* --- Navigation ---------------------------------------------- */
  var toggle = $(".nav-toggle");
  var nav = $("#nav");

  function setNav(open) {
    if (!nav || !toggle) return;
    nav.toggleAttribute("data-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    // The drawer covers the page on small screens, so stop it scrolling underneath.
    document.body.toggleAttribute("data-locked", open && !desktop.matches);
  }

  var desktop = window.matchMedia("(min-width: 1100px)");
  desktop.addEventListener("change", function () { setNav(false); });

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

  /* --- Header shadow and back to top ---------------------------- */
  var top = $(".to-top");
  var siteHeader = $(".site-header");
  var ticking = false;
  var onScroll = function () {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      var y = window.pageYOffset;
      if (top) top.toggleAttribute("data-visible", y > 600);
      if (siteHeader) siteHeader.toggleAttribute("data-scrolled", y > 8);
      ticking = false;
    });
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
  if (top) {
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

  /* --- Reveal on scroll ----------------------------------------
   * Sections fade up as they arrive. The "js" class that hides them is
   * set in <head>; without IntersectionObserver everything shows at once. */
  var reveals = $$("[data-reveal]");
  if ("IntersectionObserver" in window && !reduced) {
    var rio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add("in");
        rio.unobserve(en.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { rio.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  /* --- Testimonial slider ---------------------------------------
   * The slides are a native scroll-snap row, so swiping works with no
   * script. This adds the dots and a gentle auto-advance that stops for
   * good once someone interacts. */
  var slider = $(".slider");
  var dotsBox = $(".dots");
  if (slider && dotsBox) {
    var slides = $$(".slide", slider);
    var current = 0, auto = null;
    var dots = slides.map(function (_, i) {
      var b = document.createElement("button");
      b.type = "button";
      b.setAttribute("aria-label", "Review " + (i + 1) + " of " + slides.length);
      b.addEventListener("click", function () { stop(); go(i); });
      dotsBox.appendChild(b);
      return b;
    });
    var mark = function (i) {
      current = i;
      dots.forEach(function (d, j) { d.setAttribute("aria-current", j === i ? "true" : "false"); });
    };
    var go = function (i) {
      slider.scrollTo({ left: slides[i].offsetLeft - slider.offsetLeft, behavior: reduced ? "auto" : "smooth" });
      mark(i);
    };
    var stop = function () { if (auto) { clearInterval(auto); auto = null; } };
    slider.addEventListener("scroll", function () {
      mark(Math.round(slider.scrollLeft / slider.clientWidth));
    }, { passive: true });
    ["pointerdown", "focusin", "wheel", "touchstart"].forEach(function (ev) {
      slider.addEventListener(ev, stop, { passive: true });
    });
    mark(0);
    if (!reduced) auto = setInterval(function () { go((current + 1) % slides.length); }, 7000);
  }

  /* --- Year ------------------------------------------------------ */
  var year = $("#year");
  if (year) year.textContent = new Date().getFullYear();
})();
