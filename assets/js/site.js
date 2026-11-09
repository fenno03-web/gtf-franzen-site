(function () {
  var d = document, b = d.body;
  b.classList.remove('no-js');
  var rm = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // menu
  var bt = d.querySelector('.burger');
  if (bt) {
    bt.addEventListener('click', function () {
      var o = b.classList.toggle('open');
      bt.setAttribute('aria-expanded', o ? 'true' : 'false');
    });
    d.querySelectorAll('.top nav a').forEach(function (a) {
      a.addEventListener('click', function () { b.classList.remove('open'); bt.setAttribute('aria-expanded', 'false'); });
    });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape') { b.classList.remove('open'); bt.setAttribute('aria-expanded', 'false'); } });
  }

  // hero-diavoorstelling
  var sl = d.querySelectorAll('.hero .sl'), dots = d.querySelectorAll('.dots span'), i = 0;
  if (sl.length > 1 && !rm) {
    setInterval(function () {
      if (d.hidden) return;
      sl[i].classList.remove('on'); dots[i] && dots[i].classList.remove('on');
      i = (i + 1) % sl.length;
      sl[i].classList.add('on');
      if (dots[i]) { void dots[i].offsetWidth; dots[i].classList.add('on'); }
    }, 6000);
  }

  // inschuiven
  var els = d.querySelectorAll('.rv');
  if ('IntersectionObserver' in window && !rm) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    els.forEach(function (e) { io.observe(e); });
  } else els.forEach(function (e) { e.classList.add('in'); });

  // contactformulier: opent een mail aan het algemene adres
  var f = d.querySelector('form.f');
  if (f) f.addEventListener('submit', function (e) {
    if (f.getAttribute('action')) return;
    e.preventDefault();
    var g = function (n) { var x = f.elements[n]; return x ? x.value.trim() : ''; };
    var body = [g('naam'), g('organisatie'), g('datum'), g('locatie'), '', g('bericht')].filter(function (x, k) { return x || k === 4; }).join('\n');
    location.href = 'mailto:' + f.dataset.mail + '?subject=' + encodeURIComponent(f.dataset.subject + (g('naam') ? ' · ' + g('naam') : '')) + '&body=' + encodeURIComponent(body);
  });

  // verhuur: aanvraaglijst
  var bar = d.querySelector('.cbar');
  if (bar) {
    var KEY = 'gtf-lijst', lijst = [];
    try { lijst = JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) {}
    var cnt = bar.querySelector('[data-count]'), lab = cnt.nextElementSibling;
    var sync = function () {
      d.querySelectorAll('.add').forEach(function (b) { b.setAttribute('aria-pressed', lijst.indexOf(b.dataset.item) > -1 ? 'true' : 'false'); });
      cnt.textContent = lijst.length;
      lab.textContent = lijst.length === 1 ? lab.dataset.labelOne : lab.dataset.labelMore;
      bar.classList.toggle('vis', lijst.length > 0);
      try { localStorage.setItem(KEY, JSON.stringify(lijst)); } catch (e) {}
    };
    d.querySelectorAll('.add').forEach(function (b) {
      b.addEventListener('click', function () {
        var i = lijst.indexOf(b.dataset.item);
        if (i > -1) lijst.splice(i, 1); else lijst.push(b.dataset.item);
        sync();
      });
    });
    bar.querySelector('[data-send]').addEventListener('click', function () {
      var body = bar.dataset.intro + '\n\n' + lijst.map(function (x) { return '- ' + x; }).join('\n') + '\n\n';
      location.href = 'mailto:' + bar.dataset.mail + '?subject=' + encodeURIComponent(bar.dataset.subject) + '&body=' + encodeURIComponent(body);
    });
    sync();
  }

  d.querySelectorAll('[data-year]').forEach(function (e) { e.textContent = new Date().getFullYear(); });
})();
