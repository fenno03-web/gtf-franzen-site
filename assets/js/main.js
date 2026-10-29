const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// Mobiel menu
const btn = document.querySelector('.menu-btn');
const nav = document.querySelector('.nav');
if (btn && nav) {
  const setMenu = open => {
    nav.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', open);
    document.body.classList.toggle('menu-open', open);
    document.body.style.overflow = open ? 'hidden' : '';
  };
  btn.addEventListener('click', () => setMenu(!nav.classList.contains('open')));
  nav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setMenu(false)));
  addEventListener('keydown', e => { if (e.key === 'Escape') setMenu(false); });
}

// Jaartal in de footer
document.querySelectorAll('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });

// Header krijgt een achtergrond na het scrollen
const header = document.querySelector('.site-header');
const onScroll = () => header && header.classList.toggle('solid', scrollY > 40);
addEventListener('scroll', onScroll, { passive: true });
onScroll();

// Elementen laten verschijnen tijdens het scrollen
const reveals = document.querySelectorAll('.reveal');
if ('IntersectionObserver' in window && !reduce) {
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px' });
  reveals.forEach(el => io.observe(el));
} else {
  reveals.forEach(el => el.classList.add('in'));
}

// Tellers in de feitenstrook
if (!reduce && 'IntersectionObserver' in window) {
  const co = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      co.unobserve(e.target);
      const end = +e.target.dataset.count;
      const t0 = performance.now();
      const tick = t => {
        const p = Math.min(1, (t - t0) / 1400);
        e.target.textContent = Math.round(end * (1 - Math.pow(1 - p, 3)));
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    });
  });
  document.querySelectorAll('[data-count]').forEach(el => co.observe(el));
}

// Event-kiezer (tabs)
const tablist = document.querySelector('[role="tablist"]');
if (tablist) {
  const tabs = [...tablist.querySelectorAll('[role="tab"]')];
  const select = tab => {
    tabs.forEach(t => {
      const on = t === tab;
      t.setAttribute('aria-selected', on);
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
    });
  };
  tabs.forEach((t, i) => {
    t.addEventListener('click', () => select(t));
    t.addEventListener('keydown', e => {
      const d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (!d) return;
      const next = tabs[(i + d + tabs.length) % tabs.length];
      select(next); next.focus();
    });
  });
}

// Fotogalerij met lightbox
document.querySelectorAll('[data-gallery]').forEach(g => {
  const fotos = JSON.parse(g.dataset.gallery);
  let i = 0, box, img, count, last;
  const show = n => {
    i = (n + fotos.length) % fotos.length;
    img.src = fotos[i];
    img.alt = `${g.dataset.title}, foto ${i + 1}`;
    count.textContent = `${i + 1} / ${fotos.length}`;
  };
  const close = () => { box.remove(); box = null; document.body.style.overflow = ''; if (last) last.focus(); };
  const key = e => {
    if (!box) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowRight') show(i + 1);
    if (e.key === 'ArrowLeft') show(i - 1);
  };
  addEventListener('keydown', key);
  g.addEventListener('click', e => {
    const b = e.target.closest('.ph');
    if (!b) return;
    last = b;
    box = document.createElement('div');
    box.className = 'lightbox';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.setAttribute('aria-label', g.dataset.title);
    box.innerHTML = '<img alt=""><button class="lb-close" aria-label="Sluiten">×</button><button class="lb-prev" aria-label="Vorige foto">‹</button><button class="lb-next" aria-label="Volgende foto">›</button><p class="lb-count"></p>';
    img = box.querySelector('img');
    count = box.querySelector('.lb-count');
    box.querySelector('.lb-close').onclick = close;
    box.querySelector('.lb-prev').onclick = () => show(i - 1);
    box.querySelector('.lb-next').onclick = () => show(i + 1);
    box.addEventListener('click', ev => { if (ev.target === box) close(); });
    document.body.appendChild(box);
    document.body.style.overflow = 'hidden';
    show(+b.dataset.i);
    box.querySelector('.lb-close').focus();
  });
});

// Offerteformulier: vooraf invullen vanuit de event-kiezer, versturen via Web3Forms of anders als e-mail
const form = document.querySelector('.quote-form');
if (form) {
  const type = new URLSearchParams(location.search).get('type');
  const radio = type && form.querySelector(`input[name="type"][value="${CSS.escape(type)}"]`);
  if (radio) radio.checked = true;
  const note = form.querySelector('.form-note');
  const submit = form.querySelector('button[type="submit"]');
  form.addEventListener('submit', async e => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    const d = new FormData(form);
    if (d.get('botcheck')) return;
    const typeLabel = form.querySelector('input[name="type"]:checked + span');
    const soort = typeLabel ? typeLabel.textContent : 'event';
    const regels = [
      `Soort event: ${soort}`,
      `Nodig: ${d.getAll('nodig').join(', ') || 'nog niet bekend'}`,
      `Datum: ${d.get('datum') || '-'}`,
      `Aantal gasten: ${d.get('gasten') || '-'}`,
      `Locatie: ${d.get('locatie') || '-'}`,
      '',
      d.get('bericht') || '',
      '',
      `${d.get('naam')}`,
      `${d.get('telefoon') || ''}`,
      `${d.get('email')}`,
    ].join('\n');
    const onderwerp = `Offerteaanvraag: ${soort}`;
    const key = form.dataset.key;
    if (!key) {
      location.href = `mailto:${form.dataset.mail}?subject=${encodeURIComponent(onderwerp)}&body=${encodeURIComponent(regels)}`;
      note.textContent = 'Je mailprogramma opent met je aanvraag. Druk daar op verzenden, dan hoor je snel van ons.';
      return;
    }
    submit.disabled = true;
    note.textContent = 'Versturen...';
    try {
      const r = await fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ access_key: key, subject: onderwerp, from_name: 'Website GTF Franzen', name: d.get('naam'), email: d.get('email'), replyto: d.get('email'), message: regels }),
      });
      const res = await r.json();
      if (!res.success) throw new Error(res.message);
      form.reset();
      note.textContent = 'Bedankt! Je aanvraag is binnen. Je hoort snel van ons.';
    } catch (err) {
      note.textContent = `Versturen lukte niet. Mail ons gerust direct op ${form.dataset.mail}.`;
    } finally {
      submit.disabled = false;
    }
  });
}

// VU-meter in de header: beweegt mee met het scrollen, en gaat vol open als de stekker erin zit
let powered = false;
const vuRows = [...document.querySelectorAll('.vu-row')].map(r => [...r.children]);
if (vuRows.length && !reduce) {
  let energy = 0, lastY = scrollY;
  const lvl = [0, 0];
  addEventListener('scroll', () => { energy = Math.min(1, energy + Math.abs(scrollY - lastY) / 400); lastY = scrollY; }, { passive: true });
  setInterval(() => {
    energy *= .9;
    const base = powered ? .62 : .18;
    vuRows.forEach((leds, ch) => {
      const target = Math.min(1, base + energy * .7 + Math.random() * (powered ? .35 : .22));
      lvl[ch] = target > lvl[ch] ? target : lvl[ch] * .82;
      const n = Math.round(lvl[ch] * leds.length);
      leds.forEach((led, i) => led.classList.toggle('on', i < n));
    });
  }, 70);
}

// Stekker in het stopcontact steken
document.querySelectorAll('.cta-band').forEach(band => {
  const plug = band.querySelector('.plug');
  const track = band.querySelector('.power-track');
  if (!plug || !track) return;
  band.classList.add('unpowered');
  const rest = () => parseFloat(getComputedStyle(plug).right) - parseFloat(getComputedStyle(track).getPropertyValue('--base'));
  const setPower = on => {
    band.classList.toggle('powered', on);
    band.classList.toggle('unpowered', !on);
    plug.classList.toggle('in', on);
    plug.setAttribute('aria-label', on ? 'Trek de stekker eruit' : 'Steek de stekker in het stopcontact');
    plug.style.removeProperty('--plug-x');
    track.style.removeProperty('--plug-x');
    powered = on || !!document.querySelector('.cta-band.powered');
    if (on && navigator.vibrate) navigator.vibrate(30);
  };
  let startX = 0, startOff = 0, moved = false;
  plug.addEventListener('pointerdown', e => {
    startX = e.clientX; startOff = band.classList.contains('powered') ? 0 : rest(); moved = false;
    plug.setPointerCapture(e.pointerId);
    plug.classList.add('dragging');
  });
  plug.addEventListener('pointermove', e => {
    if (!plug.classList.contains('dragging')) return;
    const dx = e.clientX - startX;
    if (Math.abs(dx) > 4) moved = true;
    const off = Math.max(0, Math.min(startOff + 60, startOff - dx));
    plug.style.setProperty('--plug-x', `${off}px`);
    track.style.setProperty('--plug-x', `${off}px`);
  });
  const end = () => {
    if (!plug.classList.contains('dragging')) return;
    plug.classList.remove('dragging');
    if (!moved) return;
    const off = parseFloat(plug.style.getPropertyValue('--plug-x')) || 0;
    setPower(off < 40);
  };
  plug.addEventListener('pointerup', end);
  plug.addEventListener('pointercancel', end);
  plug.addEventListener('click', () => { if (!moved) setPower(!band.classList.contains('powered')); moved = false; });
});
