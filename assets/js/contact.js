/* Contact form: posts the volunteer's details to Altus's Power Automate flow
   (data-endpoint, from FORM_FLOW_URL in tools/content.py), which emails the
   coordinators from Altus's Microsoft 365. Sent as plain form data so the browser
   needs no CORS pre-check; the flow's Response action must return
   Access-Control-Allow-Origin for the page to see that it worked. */
(function () {
  var form = document.getElementById('inquiry');
  if (!form) return;
  var done = form.parentNode.querySelector('.enroll__done');
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

  function finish() {
    form.hidden = true;
    done.hidden = false;
    done.focus();
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
    if (f.website.value) { finish(); return; }   // honeypot: only bots fill the hidden field
    var endpoint = form.getAttribute('data-endpoint');
    if (!endpoint) { errSend.hidden = false; return; }

    var data = new URLSearchParams();
    ['first', 'last', 'phone', 'email', 'area', 'message'].forEach(function (k) { data.append(k, f[k].value.trim()); });
    data.append('language', document.documentElement.lang === 'es' ? 'Spanish' : 'English');

    btn.disabled = true;
    form.setAttribute('aria-busy', 'true');
    var ctrl = window.AbortController ? new AbortController() : null;
    var timer = ctrl && setTimeout(function () { ctrl.abort(); }, 20000);
    fetch(endpoint, { method: 'POST', body: data, signal: ctrl && ctrl.signal })
      .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); finish(); })
      .catch(function () { errSend.hidden = false; })
      .then(function () {
        clearTimeout(timer);
        btn.disabled = false;
        form.removeAttribute('aria-busy');
      });
  });
})();
