/* Header behaviour: mobile menu + EN/ES toggle. i18n.js listens for the
   `altus-lang` event and swaps the page text. */
(function () {
  var toggle = document.querySelector('.menu-toggle');
  var mobile = document.getElementById('mobile-nav');
  if (toggle && mobile) {
    toggle.addEventListener('click', function () {
      var open = mobile.hasAttribute('hidden');
      if (open) mobile.removeAttribute('hidden'); else mobile.setAttribute('hidden', '');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  function paint(lang) {
    document.documentElement.lang = lang;
    var btns = document.querySelectorAll('.lang-toggle button');
    for (var i = 0; i < btns.length; i++) {
      var on = btns[i].getAttribute('data-lang') === lang;
      btns[i].classList.toggle('is-active', on);
      btns[i].setAttribute('aria-pressed', on ? 'true' : 'false');
    }
  }

  var lang = 'en';
  try { var saved = localStorage.getItem('altus-lang'); if (saved === 'es' || saved === 'en') lang = saved; } catch (e) {}
  paint(lang);

  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('.lang-toggle button');
    if (!b) return;
    var next = b.getAttribute('data-lang');
    try { localStorage.setItem('altus-lang', next); } catch (err) {}
    paint(next);
    try { window.dispatchEvent(new CustomEvent('altus-lang', { detail: next })); } catch (err) {}
  });
})();

/* Homepage areas accordion: one item open at a time. */
(function () {
  var accs = document.querySelectorAll('[data-accordion]');
  for (var a = 0; a < accs.length; a++) {
    (function (acc) {
      var btns = acc.querySelectorAll('.acc__btn');
      function set(btn, open) {
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
        var panel = document.getElementById(btn.getAttribute('aria-controls'));
        if (panel) { if (open) panel.removeAttribute('hidden'); else panel.setAttribute('hidden', ''); }
      }
      for (var i = 0; i < btns.length; i++) {
        btns[i].addEventListener('click', function () {
          var wasOpen = this.getAttribute('aria-expanded') === 'true';
          for (var j = 0; j < btns.length; j++) set(btns[j], false);
          if (!wasOpen) set(this, true);
        });
      }
    })(accs[a]);
  }
})();
