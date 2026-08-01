/*! Bear Carpet Care — contact form.
 *
 * GitHub Pages serves static files only, so the old mail/contact.php could
 * never run and every submission fell through to an error. Until a form
 * endpoint exists, a valid submission hands off to the visitor's email
 * client with everything filled in.
 *
 * TO RECEIVE SUBMISSIONS SERVER-SIDE:
 *   1. Create a free endpoint (Formspree, Web3Forms, Basin, ...).
 *   2. Paste the URL into ENDPOINT below.
 * The form then POSTs there and shows the inline success message instead.
 */
(function () {
  "use strict";

  var ENDPOINT = ""; // e.g. "https://formspree.io/f/xxxxxxxx"
  var MAILTO = "bearcarpetcarepa@gmail.com";
  var PHONE = "(717) 454-7347";

  var form = document.getElementById("quote-form");
  if (!form) return;

  var status = document.getElementById("form-status");
  var button = form.querySelector("[type=submit]");
  var fields = [].slice.call(form.querySelectorAll("[required]"));

  function validate(field) {
    var err = document.getElementById(field.id + "-err");
    var ok = field.checkValidity();
    field.setAttribute("aria-invalid", ok ? "false" : "true");
    if (err) {
      err.textContent = ok ? "" : (field.validity.valueMissing
        ? field.getAttribute("data-msg") || "This field is required"
        : "Please enter a valid " + (field.type === "email" ? "email address" : "value"));
    }
    return ok;
  }

  fields.forEach(function (field) {
    field.addEventListener("blur", function () { validate(field); });
    field.addEventListener("input", function () {
      if (field.getAttribute("aria-invalid") === "true") validate(field);
    });
  });

  function say(kind, html) {
    if (!status) return;
    status.innerHTML = '<div class="alert alert-' + kind + '" role="alert">' + html + "</div>";
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    if (!fields.map(validate).every(Boolean)) {
      var bad = form.querySelector('[aria-invalid="true"]');
      if (bad) bad.focus();
      return;
    }

    var data = {};
    ["name", "email", "phone", "message"].forEach(function (k) {
      var el = form.querySelector("#" + k);
      data[k] = el ? el.value.trim() : "";
    });

    button.disabled = true;
    var done = function (kind, html) { say(kind, html); button.disabled = false; };

    if (ENDPOINT) {
      fetch(ENDPOINT, {
        method: "POST",
        headers: { Accept: "application/json", "Content-Type": "application/json" },
        body: JSON.stringify(data)
      })
        .then(function (r) { if (!r.ok) throw new Error(r.status); })
        .then(function () {
          form.reset();
          done("ok", "<strong>Thanks, " + data.name + ".</strong> We usually reply the same business day.");
        })
        .catch(function () {
          done("bad", 'Sorry, that did not send. Please call <a href="tel:+17174547347">' + PHONE + "</a>.");
        });
      return;
    }

    var body = "Name: " + data.name + "\nEmail: " + data.email +
               "\nPhone: " + data.phone + "\n\n" + data.message;
    window.location.href = "mailto:" + MAILTO +
      "?subject=" + encodeURIComponent("Quote request from " + data.name) +
      "&body=" + encodeURIComponent(body);

    done("ok", "<strong>Opening your email app…</strong> If nothing happens, email " +
      '<a href="mailto:' + MAILTO + '">' + MAILTO + "</a> or call " +
      '<a href="tel:+17174547347">' + PHONE + "</a>.");
  });

  var first = form.querySelector("#name");
  if (first && status) first.addEventListener("focus", function () { status.innerHTML = ""; });
})();
