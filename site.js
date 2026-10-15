// Sladent site behaviour. Every feature degrades to plain, readable content.
(() => {
  const doc = document.documentElement;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const en = doc.lang === 'en';

  // Header shadow once the page scrolls
  const hdr = document.querySelector('.hdr');
  const onScroll = () => hdr && hdr.classList.toggle('is-scrolled', scrollY > 8);
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile menu
  const burger = document.querySelector('.burger');
  if (burger) {
    const set = (open) => {
      doc.classList.toggle('menu-open', open);
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? (en ? 'Close menu' : 'Закрити меню') : (en ? 'Open menu' : 'Відкрити меню'));
    };
    burger.addEventListener('click', () => set(!doc.classList.contains('menu-open')));
    document.querySelectorAll('.mmenu a').forEach((a) => a.addEventListener('click', () => set(false)));
    addEventListener('keydown', (e) => { if (e.key === 'Escape') set(false); });
    addEventListener('resize', () => { if (innerWidth > 1100) set(false); });
  }

  // Open / closed right now, in Kyiv time. Mon–Fri 09–20, Sat 10–15.
  const HOURS = { 1: [540, 1200], 2: [540, 1200], 3: [540, 1200], 4: [540, 1200], 5: [540, 1200], 6: [600, 900] };
  const DAY_UK = ['у неділю', 'у понеділок', 'у вівторок', 'у середу', 'у четвер', 'у пʼятницю', 'у суботу'];
  const DAY_EN = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  const hhmm = (m) => `${String(Math.floor(m / 60)).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}`;
  const kyiv = () => {
    const p = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Kyiv', weekday: 'short', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' }).formatToParts(new Date());
    const g = (t) => p.find((x) => x.type === t).value;
    return { day: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(g('weekday')), min: +g('hour') * 60 + +g('minute') };
  };
  const status = () => {
    const { day, min } = kyiv();
    const t = HOURS[day];
    if (t && min >= t[0] && min < t[1]) {
      const soon = t[1] - min <= 45;
      return { day, state: soon ? 'soon' : 'open', text: en ? (soon ? `Open, closing at ${hhmm(t[1])}` : `Open now, until ${hhmm(t[1])}`) : (soon ? `Відчинено ще до ${hhmm(t[1])}` : `Відчинено зараз, до ${hhmm(t[1])}`) };
    }
    if (t && min < t[0]) return { day, state: 'closed', text: en ? `Closed, opens today at ${hhmm(t[0])}` : `Зачинено, відчиняємось сьогодні о ${hhmm(t[0])}` };
    for (let i = 1; i <= 7; i++) {
      const d = (day + i) % 7;
      if (HOURS[d]) return { day, state: 'closed', text: en ? `Closed, opens ${i === 1 ? 'tomorrow' : DAY_EN[d]} at ${hhmm(HOURS[d][0])}` : `Зачинено, відчиняємось ${i === 1 ? 'завтра' : DAY_UK[d]} о ${hhmm(HOURS[d][0])}` };
    }
    return null;
  };
  const paint = () => {
    let s; try { s = status(); } catch (e) { return; }
    if (!s) return;
    document.querySelectorAll('[data-status]').forEach((el) => { el.textContent = s.text; el.dataset.state = s.state; el.classList.add('status'); });
    document.querySelectorAll('[data-days]').forEach((el) => el.classList.toggle('is-today', el.dataset.days.split(',').map(Number).includes(s.day)));
  };
  paint();
  setInterval(paint, 60000);

  // Before / after: the range input drives the split, so keyboard and touch both work
  document.querySelectorAll('.ba').forEach((ba) => {
    const input = ba.querySelector('input');
    const set = () => ba.style.setProperty('--pos', `${input.value}%`);
    input.addEventListener('input', set);
    set();
  });

  // Review row: arrow buttons scroll one card; disabled at either end
  document.querySelectorAll('.rrow-wrap').forEach((wrap) => {
    const row = wrap.querySelector('.rrow');
    const [prev, next] = wrap.querySelectorAll('.rrow-nav button');
    if (!row || !prev || !next) return;
    const step = () => (row.querySelector('.rcard')?.getBoundingClientRect().width || 300) + 16;
    const sync = () => { const half = step() / 2; prev.disabled = row.scrollLeft < half; next.disabled = row.scrollLeft + row.clientWidth > row.scrollWidth - half; };
    prev.addEventListener('click', () => row.scrollBy({ left: -step(), behavior: reduce ? 'auto' : 'smooth' }));
    next.addEventListener('click', () => row.scrollBy({ left: step(), behavior: reduce ? 'auto' : 'smooth' }));
    row.addEventListener('scroll', sync, { passive: true });
    addEventListener('resize', sync);
    sync();
  });

  // Background loops: play only when visible, never with reduced motion
  const vids = document.querySelectorAll('video[data-loop]');
  if (!reduce && 'IntersectionObserver' in window) {
    const vio = new IntersectionObserver((es) => es.forEach((e) => { const v = e.target; if (e.isIntersecting) { v.play().catch(() => {}); } else { v.pause(); } }), { threshold: 0.2 });
    vids.forEach((v) => { v.muted = true; vio.observe(v); });
  }

})();
