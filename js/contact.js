/*!
 * Bear Carpet Care — contact form.
 *
 * Replaces jqBootstrapValidation + the jQuery AJAX POST to contact.php.
 * GitHub Pages serves static files only, so contact.php never ran — every
 * submission hit the "mail server is not responding" branch. Until a form
 * endpoint is wired up, a valid submission hands off to the visitor's email
 * client with everything pre-filled.
 *
 * TO SEND SUBMISSIONS SERVER-SIDE INSTEAD:
 *   1. Create a free endpoint (Formspree, Web3Forms, Basin, ...).
 *   2. Put the URL in FORM_ENDPOINT below.
 * The form then POSTs there and shows the inline success message; no other
 * change is needed.
 */
(function () {
  "use strict";

  var FORM_ENDPOINT = ""; // e.g. "https://formspree.io/f/xxxxxxxx"
  var MAILTO = "bearcarpetcarepa@gmail.com";

  var form = document.getElementById('contactForm');
  if (!form) return;

  var status = document.getElementById('success');
  var button = document.getElementById('sendMessageButton');
  var fields = [].slice.call(form.querySelectorAll('[required]'));

  function helpBlockFor(field) {
    var group = field.closest('.control-group') || field.parentNode;
    return group.querySelector('.help-block');
  }

  function validate(field) {
    var help = helpBlockFor(field);
    var ok = field.checkValidity();
    var message = '';

    if (!ok) {
      message = field.validity.valueMissing
        ? field.getAttribute('data-validation-required-message') || 'This field is required'
        : 'Please enter a valid ' + (field.type === 'email' ? 'email address' : 'value');
    }

    field.classList.toggle('is-invalid', !ok);
    field.setAttribute('aria-invalid', ok ? 'false' : 'true');
    if (help) help.textContent = message;
    return ok;
  }

  fields.forEach(function (field) {
    // Validate on the way out, then live-correct once it has been flagged.
    field.addEventListener('blur', function () { validate(field); });
    field.addEventListener('input', function () {
      if (field.classList.contains('is-invalid')) validate(field);
    });
  });

  function announce(type, html) {
    if (!status) return;
    status.innerHTML = '<div class="alert alert-' + type + '" role="alert">' + html + '</div>';
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    var valid = fields.map(validate).every(Boolean);
    if (!valid) {
      var firstBad = form.querySelector('.is-invalid');
      if (firstBad) firstBad.focus();
      return;
    }

    var data = {
      name: form.querySelector('#name').value.trim(),
      email: form.querySelector('#email').value.trim(),
      subject: form.querySelector('#subject').value.trim(),
      message: form.querySelector('#message').value.trim()
    };

    button.disabled = true;

    var done = function (type, html) {
      announce(type, html);
      button.disabled = false;
    };

    if (FORM_ENDPOINT) {
      fetch(FORM_ENDPOINT, {
        method: 'POST',
        headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
        .then(function (res) {
          if (!res.ok) throw new Error(res.status);
          form.reset();
          done('success', '<strong>Thanks, ' + data.name + '.</strong> Your message has been sent — we usually reply the same business day.');
        })
        .catch(function () {
          done('danger', 'Sorry, we could not send that just now. Please call us at <a href="tel:7174547347">(717) 454-7347</a>.');
        });
      return;
    }

    // No endpoint configured: hand off to the visitor's email client.
    var body =
      'Name: ' + data.name + '\n' +
      'Email: ' + data.email + '\n\n' +
      data.message;

    window.location.href =
      'mailto:' + MAILTO +
      '?subject=' + encodeURIComponent(data.subject) +
      '&body=' + encodeURIComponent(body);

    done(
      'success',
      '<strong>Opening your email app…</strong> If nothing happens, email us at ' +
      '<a href="mailto:' + MAILTO + '">' + MAILTO + '</a> or call ' +
      '<a href="tel:7174547347">(717) 454-7347</a>.'
    );
  });

  var nameField = form.querySelector('#name');
  if (nameField && status) {
    nameField.addEventListener('focus', function () { status.innerHTML = ''; });
  }
})();
