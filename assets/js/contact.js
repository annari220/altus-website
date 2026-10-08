/* Contact form: builds an email to the Altus inbox in the visitor's own mail app.
   Nothing is sent to any third party. Used until the Microsoft Form is embedded. */
(function () {
  var form = document.getElementById('inquiry');
  if (!form) return;
  var done = form.parentNode.querySelector('.inq__done');
  var err = form.querySelector('.inq__err');
  form.addEventListener('input', clear);
  form.addEventListener('change', clear);
  function clear(e) {
    var el = e.target;
    if (el.getAttribute('aria-invalid') === 'true') {
      var bad = el.type === 'checkbox' ? !el.checked : !el.value.trim();
      if (!bad) el.setAttribute('aria-invalid', 'false');
    }
    if (!form.querySelector('[aria-invalid="true"]')) err.hidden = true;
  }
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var ok = true;
    Array.prototype.forEach.call(form.querySelectorAll('[required]'), function (el) {
      var bad = el.type === 'checkbox' ? !el.checked : !el.value.trim();
      if (el.type === 'email' && el.value && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(el.value)) bad = true;
      el.setAttribute('aria-invalid', bad ? 'true' : 'false');
      if (bad) ok = false;
    });
    err.hidden = ok;
    if (!ok) { var first = form.querySelector('[aria-invalid="true"]'); if (first) first.focus(); return; }
    var f = form.elements;
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
    var href = 'mailto:' + form.getAttribute('data-to') +
      '?subject=' + encodeURIComponent('Volunteer inquiry: ' + f.area.value + ' - ' + name) +
      '&body=' + encodeURIComponent(lines.join('\n'));
    window.location.href = href;
    form.hidden = true;
    if (done) { done.hidden = false; done.setAttribute('tabindex', '-1'); done.focus(); }
  });
})();
