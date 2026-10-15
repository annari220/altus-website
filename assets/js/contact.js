/* Contact form: posts the volunteer's details to Altus's Power Automate flow
   (data-endpoint, from FORM_FLOW_URL in tools/content.py), which emails the
   coordinators from Altus's Microsoft 365. Sent as plain form data so the browser
   needs no CORS pre-check; the flow's Response action must return
   Access-Control-Allow-Origin for the page to see that it worked.
   With no flow URL, it opens the visitor's own email app addressed to data-to. */
(function () {
  var form = document.getElementById('inquiry');
  if (!form) return;
  var errFields = form.querySelector('[data-err="fields"]');
  var errSend = form.querySelector('[data-err="send"]');
  var btn = form.querySelector('button[type="submit"]');

  function isBad(el) {
    var v = el.value.trim();
    if (!v) return true;
    if (el.type === 'email') return !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v);
    if (el.type === 'tel') return v.replace(/\D/g, '').length < 7;
    return false;
  }
  function clear(e) {
    var el = e.target;
    if (el.getAttribute('aria-invalid') === 'true' && !isBad(el)) el.setAttribute('aria-invalid', 'false');
    if (!form.querySelector('[aria-invalid="true"]')) errFields.hidden = true;
  }
  form.addEventListener('input', clear);
  form.addEventListener('change', clear);

  function finish(kind) {
    var done = form.parentNode.querySelector('[data-done="' + kind + '"]');
    form.hidden = true;
    done.hidden = false;
    done.focus();
  }

  function openMail(f) {
    var name = f.first.value.trim() + ' ' + f.last.value.trim();
    var lines = [
      'New volunteer inquiry from altusresearch.com', '',
      'Name: ' + name,
      'Phone: ' + f.phone.value.trim(),
      'Email: ' + f.email.value.trim(),
      'Area of interest: ' + f.area.value,
      'Message: ' + (f.message.value.trim() || '(none)'),
      'Language: ' + (document.documentElement.lang === 'es' ? 'Spanish' : 'English'), '',
      'The sender agreed to be contacted about studies.'
    ];
    window.location.href = 'mailto:' + form.getAttribute('data-to') +
      '?subject=' + encodeURIComponent('Volunteer inquiry: ' + f.area.value + ' - ' + name) +
      '&body=' + encodeURIComponent(lines.join('\n'));
    finish('mail');
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    errSend.hidden = true;
    var ok = true;
    Array.prototype.forEach.call(form.querySelectorAll('[required]'), function (el) {
      var bad = isBad(el);
      el.setAttribute('aria-invalid', bad ? 'true' : 'false');
      if (bad) ok = false;
    });
    errFields.hidden = ok;
    if (!ok) { form.querySelector('[aria-invalid="true"]').focus(); return; }

    var f = form.elements;
    if (f.website.value) { finish('sent'); return; }   // honeypot: only bots fill the hidden field
    var endpoint = form.getAttribute('data-endpoint');
    if (!endpoint) { openMail(f); return; }

    var data = new URLSearchParams();
    ['first', 'last', 'phone', 'email', 'area', 'message'].forEach(function (k) { data.append(k, f[k].value.trim()); });
    data.append('language', document.documentElement.lang === 'es' ? 'Spanish' : 'English');

    btn.disabled = true;
    form.setAttribute('aria-busy', 'true');
    var ctrl = window.AbortController ? new AbortController() : null;
    var timer = ctrl && setTimeout(function () { ctrl.abort(); }, 20000);
    fetch(endpoint, { method: 'POST', body: data, signal: ctrl && ctrl.signal })
      .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); finish('sent'); })
      .catch(function () { errSend.hidden = false; })
      .then(function () {
        clearTimeout(timer);
        btn.disabled = false;
        form.removeAttribute('aria-busy');
      });
  });
})();
