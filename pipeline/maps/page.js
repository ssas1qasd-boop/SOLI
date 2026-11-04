(() => {
  const found = document.getElementById('found');
  const R = r => r.split(',').map(p => p.trim().match(/^(\d+)(?:-(\d+))?$/)).filter(Boolean).map(m => [+m[1], +(m[2] || m[1])]);
  const span = r => R(r).reduce((a, [x, y]) => a + y - x + 1, 0);
  const scrollTo = el => window.scrollTo({top: el.getBoundingClientRect().top + scrollY - 10, left: 0});
  function toast(html){ found.hidden = false; found.innerHTML = html + ' <button type="button" class="xf" aria-label="اقفل">✕</button>'; found.querySelector('.xf').onclick = () => { found.hidden = true; }; }
  // ---- zoom: buttons, pinch (2 fingers), Ctrl + wheel, double tap. 100% = the whole map fits the width
  document.querySelectorAll('.prog').forEach(sec => {
    const fr = sec.querySelector('.frame'), svg = fr && fr.querySelector('svg'), bar = sec.querySelector('.zbar');
    if (!fr || !svg || !bar) return;
    const zv = bar.querySelector('.zv'); let z = 1, fitH = 0;
    const MAX = 6;
    function setZ(nz, cx, cy){
      nz = Math.max(1, Math.min(MAX, nz)); const r = fr.getBoundingClientRect();
      if (cx == null){ cx = r.width / 2; cy = r.height / 2; }
      const fx = (fr.scrollLeft + cx) / svg.clientWidth, fy = (fr.scrollTop + cy) / svg.clientHeight;
      if (z === 1) fitH = fr.clientHeight;
      z = nz; svg.style.width = (z * 100) + '%';
      fr.style.height = z > 1 ? Math.max(fitH, Math.min(innerHeight * 0.75, fitH * 2.2)) + 'px' : '';
      fr.style.overflow = z > 1 ? 'auto' : '';
      fr.scrollLeft = fx * svg.clientWidth - cx; fr.scrollTop = fy * svg.clientHeight - cy;
      zv.textContent = Math.round(z * 100) + '%'; compact();
    }
    const bts = [...svg.querySelectorAll('.blk')].map(g => { const r = g.querySelector('.bb'), t = g.querySelector('.bt');
      return {g, t, x: +r.getAttribute('x'), y: +r.getAttribute('y'), w: +r.getAttribute('width'), h: +r.getAttribute('height'), tx: t.getAttribute('x'), ty: t.getAttribute('y')}; });
    const zts = [...svg.querySelectorAll('.zt')];
    function compact(){
      const on = z === 1 && svg.clientWidth / svg.viewBox.baseVal.width < 0.62; if (on === svg.classList.contains('compact')) return;
      svg.classList.toggle('compact', on);
      bts.forEach(b => { if (on){ const L = b.t.textContent.length, img = b.g.querySelector('image'), fs = Math.max(13, Math.min(30, (b.w - 20) / (L * 0.62), img ? 20 : b.h * 0.42));
          b.t.style.fontSize = fs + 'px'; b.t.setAttribute('x', b.x + b.w / 2); b.t.setAttribute('text-anchor', 'middle'); b.t.setAttribute('y', img ? b.y + fs + 4 : b.y + b.h / 2 + fs * 0.35); }
        else { b.t.style.fontSize = ''; b.t.setAttribute('x', b.tx); b.t.removeAttribute('text-anchor'); b.t.setAttribute('y', b.ty); } });
      zts.forEach(t => { const r = t.previousElementSibling, w = r && r.tagName === 'rect' ? +r.getAttribute('width') - 20 : 300; t.style.fontSize = on ? Math.max(12, Math.min(20, w / (t.textContent.length * 0.62))) + 'px' : ''; });
    }
    compact();
    sec.__zoom = { get: () => z, show(g){ if (z <= 1) return; const a = fr.getBoundingClientRect(), b = g.getBoundingClientRect();
      if (b.left < a.left || b.right > a.right || b.top < a.top || b.bottom > a.bottom){ fr.scrollLeft += (b.left + b.width / 2) - (a.left + a.width / 2); fr.scrollTop += (b.top + b.height / 2) - (a.top + a.height / 2); } } };
    const amb = bar.querySelector('.zamb'); if (amb) amb.addEventListener('click', () => { const on = svg.classList.toggle('ambient'); amb.setAttribute('aria-pressed', on); });
    bar.querySelectorAll('.zb:not(.zamb)').forEach(b => b.addEventListener('click', () => { const d = +b.dataset.z; setZ(d === 0 ? 1 : (d > 0 ? z * 1.5 : z / 1.5)); }));
    fr.addEventListener('wheel', e => { if (!e.ctrlKey) return; e.preventDefault(); const r = fr.getBoundingClientRect(); setZ(z * (e.deltaY < 0 ? 1.15 : 1 / 1.15), e.clientX - r.left, e.clientY - r.top); }, {passive: false});
    let pin = null;
    const dist = t => Math.hypot(t[0].clientX - t[1].clientX, t[0].clientY - t[1].clientY);
    fr.addEventListener('touchstart', e => { if (e.touches.length === 2){ const r = fr.getBoundingClientRect(); pin = {d: dist(e.touches), z, cx: (e.touches[0].clientX + e.touches[1].clientX) / 2 - r.left, cy: (e.touches[0].clientY + e.touches[1].clientY) / 2 - r.top}; } }, {passive: true});
    fr.addEventListener('touchmove', e => { if (pin && e.touches.length === 2){ e.preventDefault(); setZ(pin.z * dist(e.touches) / pin.d, pin.cx, pin.cy); } }, {passive: false});
    fr.addEventListener('touchend', e => { if (e.touches.length < 2) pin = null; });
    let lastTap = 0;
    fr.addEventListener('dblclick', e => { const r = fr.getBoundingClientRect(); setZ(z > 1 ? 1 : 2.5, e.clientX - r.left, e.clientY - r.top); });
    addEventListener('resize', () => { if (z > 1) setZ(z); });
  });
  document.querySelectorAll('.prog').forEach(sec => {
    const pd = sec.querySelector('.pd'), frame = sec.querySelector('.frame'), box = sec.querySelector('.codebox'), notes = sec.querySelector('.notes');
    const blk = id => sec.querySelector('.blk[data-id="' + id + '"]');
    const clear = () => { sec.querySelectorAll('.blk.on, .blk.hit').forEach(g => g.classList.remove('on', 'hit')); sec.querySelectorAll('.cl.hl').forEach(x => x.classList.remove('hl')); };
    function showCode(g){ clear(); g.classList.add('on'); box.open = true; const f = g.dataset.f; let first = null;
      R(g.dataset.r).forEach(([x, y]) => { for (let n = x; n <= y; n++){ const el = sec.querySelector(`.cl[data-f="${f}"][data-n="${n}"]`); if (el){ el.classList.add('hl'); first = first || el; } } });
      const d = notes.querySelector('details[data-d="' + g.dataset.id + '"]'); if (d) d.open = true;
      if (first){ const pre = first.closest('.src'); scrollTo(pre.closest('.cf')); pre.scrollTop = first.offsetTop - pre.offsetTop - 40; pre.scrollLeft = 0; } }
    sec.querySelectorAll('.blk').forEach(g => { g.addEventListener('click', () => showCode(g)); g.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' '){ e.preventDefault(); showCode(g); } }); });
    sec.querySelectorAll('.goc').forEach(b => b.addEventListener('click', () => { const g = blk(b.dataset.id); if (g) showCode(g); }));
    sec.querySelector('.back').addEventListener('click', () => scrollTo(frame));
    sec.querySelectorAll('.cl').forEach(el => el.addEventListener('click', () => {
      const f = el.dataset.f, n = +el.dataset.n; sec.querySelectorAll('.cl.pick').forEach(x => x.classList.remove('pick')); el.classList.add('pick'); clear();
      const hits = [...sec.querySelectorAll('.blk')].filter(g => g.dataset.f === f && R(g.dataset.r).some(([x, y]) => n >= x && n <= y)).sort((a, b) => span(a.dataset.r) - span(b.dataset.r));
      const st = el.querySelector('.cs').title;
      if (!hits.length){ toast('سطر ' + n + ': مش لاقي صندوق للسطر ده.'); return; }
      hits.forEach((g, i) => g.classList.add(i === 0 ? 'hit' : 'on'));
      toast('سطر ' + n + (st ? ' (' + st + ' في البنش)' : '') + ' موجود في: ' + hits.map(g => '<b><bdi dir="ltr">' + g.dataset.t.replace(/[<&]/g, c => ({'<': '&lt;', '&': '&amp;'}[c])) + '</bdi></b>').join('، و ') + ' <button type="button" class="bk">⬇ ارجع للسطر</button>');
      found.querySelector('.bk').onclick = () => { found.hidden = true; const pre = el.closest('.src'); scrollTo(pre.closest('.cf')); pre.scrollTop = el.offsetTop - pre.offsetTop - 60; };
      const fr = frame.getBoundingClientRect(), gr = hits[0].getBoundingClientRect(); frame.scrollLeft += (gr.left + gr.width / 2) - (fr.left + fr.width / 2);
      const g2 = hits[0].getBoundingClientRect(); window.scrollTo({top: g2.top + scrollY - innerHeight / 2 + g2.height / 2, left: 0}); }));
    // ---- step / line navigator: buttons + a number box, lights the box in the map
    const nav = sec.querySelector('.nav2');
    if (nav){
      const steps = nav.dataset.steps ? nav.dataset.steps.split(',').map(t => t.split(':').map(Number)) : [];
      const nl = nav.dataset.nl.split('|').map(Number);
      const msg = nav.querySelector('.nmsg'), fsel = nav.querySelector('.nf');
      const inp = k => nav.querySelector(`.ni[data-k="${k}"]`);
      const esc = t => t.replace(/[<&>]/g, c => ({'<': '&lt;', '&': '&amp;', '>': '&gt;'}[c]));
      const fileOf = () => fsel ? +fsel.value : 0;
      const covers = (f, n) => [...sec.querySelectorAll('.blk')].filter(g => +g.dataset.f === f && R(g.dataset.r).some(([x, y]) => n >= x && n <= y)).sort((a, b) => span(a.dataset.r) - span(b.dataset.r));
      const codeText = (f, n) => { const el = sec.querySelector(`.cl[data-f="${f}"][data-n="${n}"]`); if (!el) return ''; const c = el.cloneNode(true); c.querySelectorAll('.cn, .cs').forEach(x => x.remove()); return c.textContent.trim(); };
      const fname = f => { const o = fsel && fsel.options[f]; return o ? o.textContent : ''; };
      let lastAr = [], lastHit = null; const PK = nav.dataset.pk ? JSON.parse(nav.dataset.pk) : [];
      const svg = frame.querySelector('svg'), NS = 'http://www.w3.org/2000/svg';
      const motionOK = !matchMedia('(prefers-reduced-motion: reduce)').matches;
      function chip(txt, ty){ const g = document.createElementNS(NS, 'g'); g.setAttribute('class', 'pkt'); g.setAttribute('pointer-events', 'none');
        const t = document.createElementNS(NS, 'text'); t.textContent = txt; t.setAttribute('text-anchor', 'middle'); t.setAttribute('y', '4');
        const r = document.createElementNS(NS, 'rect'); g.appendChild(r); g.appendChild(t);
        let w = Math.max(30, txt.length * 7.4 + 14), top = -11;
        if (ty){ const s = document.createElementNS(NS, 'text'); s.setAttribute('class', 'pty'); s.textContent = ty; s.setAttribute('text-anchor', 'middle'); s.setAttribute('y', '-14'); g.appendChild(s); top = -24; w = Math.max(w, ty.length * 6 + 14); }
        r.setAttribute('x', -w / 2); r.setAttribute('y', top); r.setAttribute('width', w); r.setAttribute('height', 4 - top + 7); r.setAttribute('rx', 7);
        svg.appendChild(g); return g; }
      const sc = () => Math.max(1, Math.min(2.6, (svg.viewBox.baseVal.width / svg.clientWidth) * 0.5));
      const COL = {float: '#f59e0b', double: '#f59e0b', numpy: '#f59e0b', data: '#f59e0b', int: '#06b6d4', uint: '#06b6d4', bool: '#06b6d4', bytes: '#a855f7', text: '#22c55e', char: '#22c55e', string: '#22c55e', ptr: '#ec4899', fn: '#e11d48', gpu: '#0d9488', enum: '#64748b', struct: '#d946ef'};
      function spark(x, y, col){ const c = document.createElementNS(NS, 'circle'); c.setAttribute('class', 'spk'); c.setAttribute('cx', x); c.setAttribute('cy', y); c.style.stroke = col; svg.appendChild(c);
        const t0 = performance.now(); (function an(t){ const q = Math.min(1, (t - t0) / 420); c.setAttribute('r', 4 + 22 * q); c.style.opacity = 1 - q; if (q < 1) requestAnimationFrame(an); else c.remove(); })(t0); }
      // one travelling item = a glowing ball + its name (+ its real value), drawn along the wire
      function ball(it, s, small){
        const g = document.createElementNS(NS, 'g'); g.setAttribute('class', 'eball'); const col = COL[it[2]] || '#f59e0b';
        const c = document.createElementNS(NS, 'circle'); c.setAttribute('r', small ? 2.6 : 6.5); c.style.fill = col; c.style.color = col; g.appendChild(c);
        let w = small ? 6 : 14;
        if (!small){
          const t1 = document.createElementNS(NS, 'text'); t1.setAttribute('class', 'enm'); t1.textContent = it[0]; t1.style.fill = col; t1.setAttribute('dominant-baseline', 'central'); g.appendChild(t1);
          const t2 = it[1] ? document.createElementNS(NS, 'text') : null; if (t2){ t2.setAttribute('class', 'evl'); t2.textContent = (it[2] === 'fn' || it[2] === 'bytes') ? it[1] : '= ' + it[1]; t2.setAttribute('dominant-baseline', 'central'); g.appendChild(t2); }
          svg.appendChild(g); const w1 = t1.getComputedTextLength(), w2 = t2 ? t2.getComputedTextLength() + 6 : 0; w = 14 + 4 + w1 + w2 + 8;
          const x0 = -w / 2; c.setAttribute('cx', x0 + 7); t1.setAttribute('x', x0 + 18); if (t2) t2.setAttribute('x', x0 + 18 + w1 + 6);
        } else svg.appendChild(g);
        g.__w = w * s; return g; }
      function fly(k){
        if (!timer){ svg.querySelectorAll('.pkt, .eball, .spk, .cur').forEach(x => x.remove()); sec.querySelectorAll('.blk.zap').forEach(g => g.classList.remove('zap')); }
        const items = PK[k - 1]; if (!items || !items.length || !motionOK) return 0;
        const s = sc(), col = COL[items[0][2]] || '#f59e0b', speed = mult() * 130; let longest = 0;
        const paths = lastAr.filter(x => x.getTotalLength);
        if (!paths.length){ if (!lastHit) return 0; const bb = lastHit.querySelector('.bb'), cx = +bb.getAttribute('x') + +bb.getAttribute('width') / 2, y0 = +bb.getAttribute('y');
          const gs = items.slice(0, 4).map(it => ball(it, s)), t0 = performance.now(), dur = Math.max(300, 1400 / mult());
          (function an(t){ const q = Math.min(1, (t - t0) / dur);
            gs.forEach((g, i) => { const y = y0 - 10 * s - i * 18 * s - 14 * s * q; g.setAttribute('transform', `translate(${cx} ${y}) scale(${s}) translate(0 0)`); g.style.opacity = q < 0.15 ? q / 0.15 : (q > 0.8 ? (1 - q) / 0.2 : 1); });
            if (q < 1) requestAnimationFrame(an); else gs.forEach(g => g.remove()); })(t0); return dur; }
        paths.forEach(path => {
          const L = path.getTotalLength(), cur = path.cloneNode(), tube = path.cloneNode(); [cur, tube].forEach(c => { c.removeAttribute('marker-end'); c.style.stroke = col; c.style.color = col; });
          cur.setAttribute('class', 'cur'); tube.setAttribute('class', 'cur tube'); tube.style.strokeWidth = (18 * s) + 'px'; path.after(tube); tube.after(cur);
          const seq = []; items.forEach((it, i) => { seq.push(ball(it, s)); if (i < items.length - 1) for (let e = 0; e < 3; e++) seq.push(ball(it, s, true)); });
          for (let e = 0; e < 4; e++) seq.push(ball(items[items.length - 1], s, true));
          const offs = []; let acc = 0; seq.forEach(g => { offs.push(acc + g.__w / 2); acc += g.__w + 8 * s; });
          const total = L + acc, t0 = performance.now(), dur = total / speed * 1000; longest = Math.max(longest, dur);
          const tgt = sec.querySelector('.blk[data-id="' + path.dataset.b + '"]');
          (function an(t){ const head = (t - t0) / dur * total; let alive = 0;
            seq.forEach((g, i) => { const d = head - offs[i];
              if (d < 0){ g.style.opacity = 0; alive++; return; }
              if (d > L){ if (g.style.opacity !== '0'){ g.style.opacity = 0; if (!g.querySelector('circle[r="2.6"]')){ const end = path.getPointAtLength(L); spark(end.x, end.y, COL[(items[0] || [])[2]] || col); if (tgt){ tgt.classList.remove('zap'); void tgt.getBBox(); tgt.classList.add('zap'); } } } return; }
              alive++; const a = path.getPointAtLength(Math.max(0, d - 1)), b = path.getPointAtLength(Math.min(L, d + 1)), pt = path.getPointAtLength(d);
              let ang = Math.atan2(b.y - a.y, b.x - a.x) * 180 / Math.PI; if (ang > 90) ang -= 180; if (ang <= -90) ang += 180;
              g.setAttribute('transform', `translate(${pt.x} ${pt.y}) rotate(${ang}) scale(${s})`); g.style.opacity = Math.max(0, Math.min(1, d / 16, (L - d) / 16)); });
            if (alive) requestAnimationFrame(an); else { seq.forEach(g => g.remove()); setTimeout(() => { cur.remove(); tube.remove(); }, 250); } })(t0);
        });
        return longest;
      }
      function light(f, n, head){
        lastAr = []; lastHit = null;
        pd.open = true; sec.querySelectorAll('.blk.glow').forEach(g => g.classList.remove('glow')); sec.querySelectorAll('path.aglow').forEach(x => x.classList.remove('aglow'));
        const hits = covers(f, n), code = codeText(f, n);
        const line = (fsel ? '<bdi dir="ltr">' + esc(fname(f)) + '</bdi> ' : '') + 'سطر ' + n; const cb = code ? '<span class="ncode" dir="ltr">' + esc(code) + '</span>' : '';
        if (!hits.length){ msg.innerHTML = head + line + ' · مفيش صندوق في الخريطة للسطر ده (سطر فاضي أو قوس).' + cb; return false; }
        void hits[0].getBoundingClientRect(); hits[0].classList.add('glow'); if (sec.__zoom) sec.__zoom.show(hits[0]);
        const id = hits[0].dataset.id; let ar = f === 0 ? [...sec.querySelectorAll('path.adat[data-l="' + n + '"]')] : [];
        const how = ar.length ? 'سهم السطر ده' : 'البيانات اللي داخلة للصندوق';
        if (!ar.length){ ar = [...sec.querySelectorAll('path.adat[data-b="' + id + '"]')];
          const words = new Set((code.match(/[A-Za-z_]\w{2,}/g) || []));
          const SKIP = /^(GLfloat|GLuint|GLint|GLenum|unsigned|int|float|double|char|const|std|string|vector|struct|class|text|strings|Shader)$/;
          const pick = ar.filter(x => { const src = sec.querySelector('.blk[data-id="' + x.dataset.a + '"]'); return src && (src.dataset.t.match(/[A-Za-z_]\w{2,}/g) || []).some(w => !SKIP.test(w) && words.has(w)); });
          if (pick.length) ar = pick; }
        ar.forEach(x => x.classList.add('aglow')); lastAr = ar; lastHit = hits[0];
        msg.innerHTML = head + line + ' · في الصندوق: <b><bdi dir="ltr">' + esc(hits[0].dataset.t) + '</bdi></b>' + (ar.length ? ' · نوّرنا ' + (ar.length === 1 ? 'سهم' : 'عدد ' + ar.length + ' أسهم') + ' (' + how + ')' : '') + cb;
        return true;
      }
      function goLine(n, dir){
        const f = fileOf(), max = nl[f];
        if (dir){ let m = n; do { m += dir; } while (m >= 1 && m <= max && !covers(f, m).length); if (m < 1 || m > max){ msg.textContent = dir > 0 ? 'ده آخر سطر ليه صندوق.' : 'ده أول سطر ليه صندوق.'; return; } n = m; }
        if (!(n >= 1 && n <= max)){ msg.textContent = 'اكتب رقم من 1 لـ ' + max + '.'; return; }
        inp('line').value = n; inp('line').dataset.last = n; const ks = steps.map((s, i) => s[0] === f && s[1] === n ? i + 1 : 0).filter(Boolean);
        light(f, n, ks.length ? '(خطوة ' + ks.slice(0, 6).join('، ') + (ks.length > 6 ? ' و' + (ks.length - 6) + ' كمان' : '') + ') ' : '');
      }
      function goStep(k){
        if (!steps.length){ msg.textContent = 'البرنامج ده مالوش خطوات.'; return; }
        if (!(k >= 1 && k <= steps.length)){ msg.textContent = 'اكتب رقم من 1 لـ ' + steps.length + '.'; return; }
        inp('step').value = k; inp('step').dataset.last = k; const [f, n] = steps[k - 1];
        if (fsel){ fsel.value = f; inp('line').max = nl[f]; inp('line').placeholder = '1-' + nl[f]; }
        inp('line').value = n; inp('line').dataset.last = n;
        light(f, n, '<b>خطوة ' + k + '</b> = '); return fly(k);
      }
      const pl = nav.querySelector('.npl'), spr = nav.querySelector('.nsp'), spv = nav.querySelector('.nsv'); let timer = null;
      const mult = () => spr ? Math.pow(2, +spr.value) : 1, sp = { get value(){ return 800 / mult(); } };
      if (spr) spr.addEventListener('input', () => { const m = mult(); spv.textContent = (m < 1 ? m.toFixed(2).replace(/0$/, '') : (Math.round(m * 100) / 100)) + '×'; });
      function stop(){ if (timer){ clearTimeout(timer); timer = null; } if (pl){ pl.textContent = '▶ تشغيل'; pl.setAttribute('aria-pressed', 'false'); } }
      function tick(){ const v = parseInt(inp('step').value, 10), k = isNaN(v) ? 1 : v + 1;
        if (k > steps.length){ stop(); msg.innerHTML += ' <b>· خلصت الخطوات.</b>'; return; }
        const fd = goStep(k) || 0; timer = setTimeout(tick, Math.max(+sp.value, fd + 200)); }
      if (pl) pl.addEventListener('click', () => { if (timer){ stop(); return; }
        const v = parseInt(inp('step').value, 10); if (!isNaN(v) && v >= steps.length) inp('step').value = '';
        pl.textContent = '⏸ وقف'; pl.setAttribute('aria-pressed', 'true'); tick(); });
      nav.querySelectorAll('.nb:not(.npl), .ni, .nf').forEach(x => x.addEventListener('pointerdown', stop));
      nav.querySelectorAll('.nb').forEach(b => b.addEventListener('click', () => { if (b.classList.contains('npl')) return;
        const k = b.dataset.k, d = +b.dataset.d, v = parseInt(inp(k).value, 10);
        if (d === 0){ if (isNaN(v)){ msg.textContent = 'اكتب رقم الأول.'; return; } k === 'step' ? goStep(v) : goLine(v, 0); return; }
        if (k === 'step') goStep(isNaN(v) ? (d > 0 ? 1 : steps.length) : v + d);
        else goLine(isNaN(v) ? (d > 0 ? 0 : nl[fileOf()] + 1) : v, d);
      }));
      nav.querySelectorAll('.ni').forEach(i => i.addEventListener('keydown', e => { if (e.key === 'Enter'){ e.preventDefault(); const v = parseInt(i.value, 10); i.dataset.k === 'step' ? goStep(v) : goLine(v, 0); } }));
      nav.querySelectorAll('.ni').forEach(i => i.addEventListener('change', () => { const v = parseInt(i.value, 10); if (!isNaN(v) && String(v) !== i.dataset.last) (i.dataset.k === 'step' ? goStep(v) : goLine(v, 0)); }));
      if (fsel) fsel.addEventListener('change', () => { const f = fileOf(); inp('line').max = nl[f]; inp('line').placeholder = '1-' + nl[f]; inp('line').value = ''; msg.textContent = ''; });
    }
  });
  // open the program in the address (#id), and open a program when its link in the list is tapped
  const openHash = () => { const s = location.hash && document.getElementById(location.hash.slice(1)); if (s && s.classList.contains('prog')){ s.querySelector('.pd').open = true; setTimeout(() => scrollTo(s), 30); } };
  addEventListener('hashchange', openHash); openHash();
})();
