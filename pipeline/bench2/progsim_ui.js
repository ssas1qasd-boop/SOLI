// ---------- PSIM: simulator for programs that compute with fixed numbers (or the mouse). The inputs are read from the real source
// lines; changing one = editing that line and running again. Shows: the edited lines, the terminal output, the lines that ran with values, a picture.
const PSIM = (() => {
  const C = PSIMCORE, D = PSIMDEFS, F = C.F;
  const esc = s => String(s).replace(/[&<>"]/g, ch => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[ch]));
  const cache = new WeakMap();
  function parse(P){
    if (!P || !P.files) return null;
    for (const f of P.files){ const d = D[f.name], text = (f.lines || []).join('\n'); if (!d || !d.test.test(text)) continue;
      const L = {}; for (const [k, re] of Object.entries(d.lines)){ const i = f.lines.findIndex(l => re.test(l)); if (i >= 0) L[k] = {ln: i + 1, code: f.lines[i]}; }
      const src = {all: text, lines: f.lines};
      return {d, file: f.name, L, S: d.setup ? d.setup(src) : null, src}; }
    return null;
  }
  const detect = P => { if (!P) return null; if (!cache.has(P)){ let x = null; try { x = parse(P); } catch (e) {} cache.set(P, x); } return cache.get(P); };
  // ---- read a param's starting value from its source line
  const nums = s => (String(s).match(/-?\d+(?:\.\d+)?/g) || []).map(Number);
  function start(cfg, p, V){
    if (p.view) return p.def;
    const key = (p.lines || [p.line])[0], l = cfg.L[key]; if (!l) return p.def;
    const m = new RegExp(p.rx.source).exec(l.code); if (!m) return p.def;
    let x = p.type ? nums(m[1]) : parseFloat(m[1]); if (p.from) x = p.from(x, V); return x;
  }
  // ---- write a number the way the source writes it (keeps the f suffix and the decimal point)
  const lit = (x, like) => { let s = String(+(+x).toFixed(4)); if (/\./.test(like || '') && !/\./.test(s)) s += '.0'; if (/f\b/.test(like || '')) s += 'f'; return s; };
  function edit(cfg, p, V, text){
    if (p.rep) return p.rep(text, V[p.k], V);
    const re = new RegExp(p.rx.source, 'd'), m = re.exec(text); if (!m || !m.indices) return text;
    const [a, b] = m.indices[1], old = m[1];
    let nw; if (p.type){ const parts = old.split(','); nw = V[p.k].map((x, i) => lit(x, (parts[i] || parts[0]).trim())).join(', '); } else nw = lit(V[p.k], old);
    return text.slice(0, a) + nw + text.slice(b);
  }
  const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);

  function css(){ if (document.getElementById('psimcss')) return; const s = document.createElement('style'); s.id = 'psimcss';
    s.textContent = `.ps{direction:rtl;font-size:13px;line-height:1.5;margin:6px 0;border:1px solid rgba(127,127,127,.35);border-radius:10px;padding:8px;background:rgba(127,127,127,.06)}
.ps.psfull{position:fixed;inset:0;z-index:100000;overflow:auto;margin:0;border-radius:0;background:var(--bg,#101418);color:var(--fg,#e6e6e6)}
.ps .psh{display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin-bottom:6px}.ps .psh b{flex:1;min-width:120px}
.ps canvas{direction:ltr;display:block;width:100%;border-radius:8px;touch-action:none;background:#0b0f14;margin-top:4px}
.ps .pscap{font-size:11.5px;opacity:.8;margin:4px 2px 8px}
.ps button{font:inherit;padding:6px 8px;border-radius:8px;border:1px solid rgba(127,127,127,.45);background:rgba(127,127,127,.12);color:inherit}
.ps .psin{display:grid;gap:6px;margin:8px 0}.ps .psp{border:1px solid rgba(127,127,127,.25);border-radius:8px;padding:5px 7px}
.ps .psp.ch{border-color:#ff9d6e}.ps label code,.ps .pscap code{direction:ltr;unicode-bidi:isolate}.ps .psp label{display:block;font-size:12px;margin-bottom:2px}
.ps .psr{display:flex;gap:6px;align-items:center;direction:ltr}.ps .psr input[type=range]{flex:1;min-width:0}
.ps .psr input[type=number]{width:72px;font:12px ui-monospace,Menlo,Consolas,monospace;padding:3px;border-radius:6px;border:1px solid rgba(127,127,127,.45);background:rgba(0,0,0,.2);color:inherit}
.ps .psv input[type=number]{width:62px}
.ps h5{margin:10px 2px 3px;font-size:12.5px}
.ps pre{min-height:0;height:auto;direction:ltr;text-align:left;font:11.5px/1.5 ui-monospace,Menlo,Consolas,monospace;white-space:pre-wrap;word-break:break-word;margin:0;background:rgba(0,0,0,.28);border-radius:8px;padding:8px;max-height:330px;overflow:auto}
.ps.psfull pre{max-height:none}.ps .psterm{background:#05080b;color:#d7f7d0;min-height:0;height:auto}.ps .psterm .ch{color:#ff9d6e}
.ps .ln{color:#7fb6ff}.ps .cd{opacity:.6}.ps .ok{color:#7ddc8a}.ps .no{opacity:.55}.ps .hd{color:#ffcc66;font-weight:bold}.ps .chg{color:#ff9d6e}
.ps .ed del{color:#ff8080;text-decoration:none;opacity:.7}.ps .ed ins{color:#7ddc8a;text-decoration:none}`;
    document.head.appendChild(s); }

  // ================= pictures
  const COL = {bg: '#0b0f14', grid: 'rgba(255,255,255,.07)', axis: 'rgba(255,255,255,.3)', txt: 'rgba(255,255,255,.75)'};
  function ctx(cv){ const r = devicePixelRatio || 1, w = cv.clientWidth, h = cv.clientHeight; cv.width = w * r; cv.height = h * r; const g = cv.getContext('2d'); g.setTransform(r, 0, 0, r, 0, 0); g.direction = 'ltr'; g.fillStyle = COL.bg; g.fillRect(0, 0, w, h); return [g, w, h]; }
  function dot(g, x, y, col, label, rr = 4){ g.fillStyle = col; g.beginPath(); g.arc(x, y, rr, 0, 7); g.fill(); if (label){ g.font = '11px sans-serif'; const tw = g.measureText(label).width, W = g.canvas.clientWidth || 300; let tx = x + 6; if (tx + tw > W - 4) tx = Math.max(4, x - 6 - tw); g.fillText(label, tx, y < 16 ? y + 16 : y - 6); } }
  function arrow(g, x0, y0, x1, y1, col, w = 2){ g.strokeStyle = col; g.fillStyle = col; g.lineWidth = w; g.beginPath(); g.moveTo(x0, y0); g.lineTo(x1, y1); g.stroke();
    const a = Math.atan2(y1 - y0, x1 - x0), L = 8; if (Math.hypot(x1 - x0, y1 - y0) < 3) return; g.beginPath(); g.moveTo(x1, y1); g.lineTo(x1 - L * Math.cos(a - .4), y1 - L * Math.sin(a - .4)); g.lineTo(x1 - L * Math.cos(a + .4), y1 - L * Math.sin(a + .4)); g.fill(); }
  // 2D plane (x right, y up) that fits the given points
  function plane(cv, pts, pad = 1){
    const [g, w, h] = ctx(cv); let x0 = -1, x1 = 1, y0 = -1, y1 = 1; pts.forEach(p => { x0 = Math.min(x0, p[0]); x1 = Math.max(x1, p[0]); y0 = Math.min(y0, p[1]); y1 = Math.max(y1, p[1]); });
    x0 -= pad; x1 += pad; y0 -= pad; y1 += pad; const s = Math.min(w / (x1 - x0), h / (y1 - y0)), cx = w / 2 - s * (x0 + x1) / 2, cy = h / 2 + s * (y0 + y1) / 2;
    const X = x => cx + s * x, Y = y => cy - s * y, step = Math.pow(10, Math.floor(Math.log10((x1 - x0) / 4))) * ((x1 - x0) / Math.pow(10, Math.floor(Math.log10((x1 - x0) / 4))) > 20 ? 5 : 1);
    g.strokeStyle = COL.grid; g.lineWidth = 1; for (let x = Math.ceil(x0 / step) * step; x <= x1; x += step){ g.beginPath(); g.moveTo(X(x), 0); g.lineTo(X(x), h); g.stroke(); }
    for (let y = Math.ceil(y0 / step) * step; y <= y1; y += step){ g.beginPath(); g.moveTo(0, Y(y)); g.lineTo(w, Y(y)); g.stroke(); }
    g.strokeStyle = COL.axis; g.beginPath(); g.moveTo(X(x0), Y(0)); g.lineTo(X(x1), Y(0)); g.moveTo(X(0), Y(y0)); g.lineTo(X(0), Y(y1)); g.stroke();
    g.fillStyle = COL.txt; g.font = '10px sans-serif'; g.fillText('+x', w - 18, Y(0) - 4); g.fillText('+y', X(0) + 4, 12); g.fillText(`grid = ${step}`, 6, h - 6);
    return {g, X, Y, s, w, h};
  }
  const poly = (k, ps, stroke, fill) => { const g = k.g; g.beginPath(); ps.forEach((p, i) => i ? g.lineTo(k.X(p[0]), k.Y(p[1])) : g.moveTo(k.X(p[0]), k.Y(p[1]))); g.closePath(); if (fill){ g.fillStyle = fill; g.fill(); } g.strokeStyle = stroke; g.lineWidth = 2; g.stroke(); };
  // simple 3D view: yaw/pitch, drag to turn
  function view3(cv, cam, draw){ const [g, w, h] = ctx(cv), s = Math.min(w, h) * .3, cy = Math.cos(cam.yaw), sy = Math.sin(cam.yaw), cp = Math.cos(cam.pitch), sp = Math.sin(cam.pitch);
    const P = p => { const x = cy * p[0] - sy * p[2], z = sy * p[0] + cy * p[2], y = cp * p[1] - sp * z; return [w / 2 + s * x, h / 2 - s * y]; };
    [['x', [1.3, 0, 0], '#ff6b6b'], ['y', [0, 1.3, 0], '#7ddc8a'], ['z', [0, 0, 1.3], '#6ea8ff']].forEach(([n, e, col]) => { const a = P([0, 0, 0]), b = P(e), c2 = P(e.map(v => -v));
      g.strokeStyle = 'rgba(255,255,255,.18)'; g.lineWidth = 1; g.beginPath(); g.moveTo(...c2); g.lineTo(...a); g.stroke(); arrow(g, ...a, ...b, col, 1.5); g.fillStyle = col; g.font = '11px sans-serif'; g.fillText(n, b[0] + 4, b[1] - 4); });
    draw(g, P, w, h); g.fillStyle = COL.txt; g.font = '10px sans-serif'; g.fillText('drag to turn', 6, h - 6); }

  const group = pts => { const out = []; pts.forEach(p => { const q = out.find(o => o.p.slice(0, 3).every((x, i) => Math.abs(x - p.p[i]) < 1e-3)); if (q) q.l += ' = ' + p.l; else out.push({...p}); }); return out; };
  const PIC = {
    'drag.cpp'(cv, r){ const [g, w, h] = ctx(cv), S = r.scene.S, cc = S.clear.map(x => Math.round(x * 255)); g.fillStyle = `rgb(${cc})`; g.fillRect(0, 0, w, h);
      const tris = []; r.scene.M.forEach((M, ci) => { for (let k = 0; k + 2 < S.tri.length; k += 3){ const vs = [0, 1, 2].map(j => { const c4 = C.mv4(M, [...S.tri[k + j].p, 1]); return [c4[0] / c4[3], c4[1] / c4[3], c4[2] / c4[3]]; });
        const a = vs[0], b = vs[1], c3 = vs[2]; if ((b[0] - a[0]) * (c3[1] - a[1]) - (b[1] - a[1]) * (c3[0] - a[0]) <= 0) continue; tris.push({vs, z: (a[2] + b[2] + c3[2]) / 3, col: S.tri[k].c, pk: ci === r.scene.pk}); } });
      tris.sort((a, b) => b.z - a.z).forEach(t => { g.beginPath(); t.vs.forEach((v, i) => { const x = (v[0] + 1) / 2 * w, y = (1 - v[1]) / 2 * h; i ? g.lineTo(x, y) : g.moveTo(x, y); }); g.closePath();
        g.fillStyle = `rgb(${t.col.map(x => Math.round(x * 255))})`; g.fill(); g.strokeStyle = t.pk ? 'rgba(255,255,255,.5)' : 'rgba(0,0,0,.25)'; g.lineWidth = 1; g.stroke(); });
      const mx = r.scene.mx / 800 * w, my = r.scene.my / 600 * h; g.fillStyle = '#fff'; g.fillRect(mx - 16, my - 1.5, 32, 3); g.fillRect(mx - 1.2, my - 21, 2.4, 42);
      g.fillStyle = 'rgba(255,255,255,.7)'; g.font = '11px ui-monospace,monospace'; g.fillText(`mouse (${Math.round(r.scene.mx)}, ${Math.round(r.scene.my)})  picked = ${r.scene.pk}`, 8, 16); },
    'ray_math.cpp'(cv, r, cv2){ const [g, w, h] = ctx(cv), sc = r.scene; g.strokeStyle = COL.grid; for (let k = 1; k < 8; k++){ g.beginPath(); g.moveTo(k * w / 8, 0); g.lineTo(k * w / 8, h); g.stroke(); } for (let k = 1; k < 6; k++){ g.beginPath(); g.moveTo(0, k * h / 6); g.lineTo(w, k * h / 6); g.stroke(); }
      g.strokeStyle = COL.axis; g.beginPath(); g.moveTo(w / 2, 0); g.lineTo(w / 2, h); g.moveTo(0, h / 2); g.lineTo(w, h / 2); g.stroke();
      g.fillStyle = COL.txt; g.font = '10px ui-monospace,monospace'; g.fillText('GLFW (0,0)', 4, 12); g.fillText('NDC (0,0)', w / 2 + 4, h / 2 - 4); g.fillText('(800,600)', w - 58, h - 5);
      const x = sc.mx / 800 * w, y = sc.my / 600 * h; dot(g, x, y, '#ffcc66', `mouse (${C.cout(sc.mx)}, ${C.cout(sc.my)})  NDC (${C.cout(sc.nx)}, ${C.cout(sc.ny)})`, 5);
      // side view: z right, y up; camera at ez looking to -z
      const [k, W2, H2] = ctx(cv2), zmin = Math.min(sc.oz, 0) - 2, zmax = sc.ez + 1, s = W2 / (zmax - zmin), Z = z => (z - zmin) * s, Yy = yy => H2 / 2 - yy * s;
      const half = Math.tan(sc.fov * Math.PI / 360), far = sc.ez - zmin; k.strokeStyle = 'rgba(255,204,102,.25)'; k.beginPath(); k.moveTo(Z(sc.ez), Yy(0)); k.lineTo(Z(zmin), Yy(half * far)); k.moveTo(Z(sc.ez), Yy(0)); k.lineTo(Z(zmin), Yy(-half * far)); k.stroke();
      k.strokeStyle = 'rgba(110,168,255,.6)'; k.setLineDash([5, 4]); k.beginPath(); k.moveTo(Z(sc.oz), 0); k.lineTo(Z(sc.oz), H2); k.stroke(); k.setLineDash([]);
      k.strokeStyle = COL.axis; k.beginPath(); k.moveTo(0, Yy(0)); k.lineTo(W2, Yy(0)); k.stroke();
      const hit = [sc.nw[1], sc.nw[2]]; arrow(k, Z(sc.ez), Yy(0), Z(hit[1]), Yy(hit[0]), '#ffcc66', 2);
      arrow(k, Z(sc.ez), Yy(0), Z(sc.ez - 1), Yy(sc.vs[1]), '#ff9d6e', 3);
      dot(k, Z(sc.ez), Yy(0), '#fff', ''); dot(k, Z(hit[1]), Yy(hit[0]), '#7ddc8a', '', 5); dot(k, Z(0), Yy(0), '#888', '');
      k.font = '11px sans-serif'; k.textAlign = 'right'; k.fillStyle = '#fff'; k.fillText(`camera z = ${sc.ez}`, Z(sc.ez) - 6, Yy(0) + (sc.vs[1] > 0 ? 16 : -8));
      k.fillStyle = '#ff9d6e'; k.fillText('ViewSpaceVector (z = -1)', W2 - 6, H2 - 8); k.textAlign = 'left';
      k.fillStyle = '#7ddc8a'; k.fillText(`hit y = ${C.cout(sc.nw[1])}`, Z(hit[1]) + 8, Yy(hit[0]) + (hit[0] > 0 ? -8 : 16));
      k.fillStyle = 'rgba(110,168,255,.9)'; k.fillText(`object z = ${sc.oz}`, Z(sc.oz) + 4, 26);
      k.fillStyle = COL.txt; k.font = '10px sans-serif'; k.fillText('side view: z →  y ↑', 6, 12); },
    'glm_math.cpp'(cv, r){ const sc = r.scene, k = plane(cv, sc.pts.map(p => p.p));
      sc.arrows.forEach(([a, b, col, arc]) => { if (!arc) return arrow(k.g, k.X(a[0]), k.Y(a[1]), k.X(b[0]), k.Y(b[1]), col, 1.5);
        const r0 = Math.hypot(a[0], a[1]), t0 = Math.atan2(a[1], a[0]), t1 = Math.atan2(b[1], b[0]); let d = t1 - t0; while (d > Math.PI) d -= 2 * Math.PI; while (d < -Math.PI) d += 2 * Math.PI;
        k.g.strokeStyle = col; k.g.lineWidth = 1.5; k.g.setLineDash([5, 4]); k.g.beginPath(); for (let i = 0; i <= 40; i++){ const t = t0 + d * i / 40; i ? k.g.lineTo(k.X(r0 * Math.cos(t)), k.Y(r0 * Math.sin(t))) : k.g.moveTo(k.X(r0 * Math.cos(t)), k.Y(r0 * Math.sin(t))); } k.g.stroke(); k.g.setLineDash([]);
        const te = t1 - Math.sign(d) * .08; arrow(k.g, k.X(r0 * Math.cos(te)), k.Y(r0 * Math.sin(te)), k.X(b[0]), k.Y(b[1]), col, 1.5); }); group(sc.pts).forEach(p => dot(k.g, k.X(p.p[0]), k.Y(p.p[1]), p.col, p.l)); },
    'two_containers.cpp'(cv, r){ const it = r.scene.it; if (!it){ ctx(cv); return; } const sq = [[-.5, -.5], [.5, -.5], [.5, .5], [-.5, .5]].map(p => [...p, 0, 1]);
      const shapes = it.M.map(M => sq.map(p => C.mv4(M, p))), k = plane(cv, shapes.flat().concat([[1.2, 1.2], [-1.2, -1.2]]), .3), cols = ['#7ddc8a', '#ff9d6e', '#c792ea'];
      poly(k, sq, 'rgba(255,255,255,.25)'); shapes.forEach((s, i) => poly(k, s, cols[i], cols[i] + '33')); it.P.forEach((p, i) => dot(k.g, k.X(p[0]), k.Y(p[1]), cols[i], ['1', 'swapped', '2'][i]));
      k.g.fillStyle = COL.txt; k.g.font = '11px sans-serif'; k.g.fillText(`time = ${C.cout(it.time)}`, 6, 14); },
    'parent_child.cpp'(cv, r){ const sc = r.scene, sq = (M, s) => [[-s, -s], [s, -s], [s, s], [-s, s]].map(p => C.mv4(M, [...p, 0, 1]));
      const all = [...sc.a1, sc.tb, [0, 0], ...sc.a0], k = plane(cv, all, 1.2);
      poly(k, sq(C.I4(), .6), 'rgba(255,255,255,.3)', 'rgba(255,255,255,.06)'); sc.a0.forEach(p => dot(k.g, k.X(p[0]), k.Y(p[1]), 'rgba(255,255,255,.35)', ''));
      poly(k, sq(sc.T, .6), '#ffcc66', '#ffcc6633'); sc.ch.forEach((m, i) => { const M = C.mmul(sc.T, m); poly(k, sq(M, .3), '#7fb6ff', '#7fb6ff33'); const p = sc.a1[i]; dot(k.g, k.X(p[0]), k.Y(p[1]), '#7fb6ff', `${i}`, 3); });
      dot(k.g, k.X(sc.tb[0]), k.Y(sc.tb[1]), '#ffcc66', 'table'); },
    'chain_pivot.cpp'(cv, r){ const sc = r.scene, k = plane(cv, [...sc.box, ...sc.orbit, ...sc.self], .8);
      poly(k, sc.box, 'rgba(255,255,255,.35)'); poly(k, sc.orbit, '#ff9d6e', '#ff9d6e33'); poly(k, sc.self, '#7ddc8a', '#7ddc8a33');
      dot(k.g, k.X(sc.p), k.Y(0), '#fff', 'pivot'); dot(k.g, k.X(sc.corner), k.Y(0), '#fff', 'corner', 3); dot(k.g, k.X(sc.z[0]), k.Y(sc.z[1]), '#ff9d6e', 'Rz × centre'); dot(k.g, k.X(sc.c1[0]), k.Y(sc.c1[1]), '#7ddc8a', 'corner after T·R·T'); },
    'axes.cpp'(cv, r, cv2, cam){ const sc = r.scene; view3(cv, cam, (g, P) => { const a = sc.axis, o = P([0, 0, 0]), e = P(a.map(x => x * 1.4));
      g.strokeStyle = 'rgba(199,146,234,.6)'; g.setLineDash([4, 4]); g.beginPath(); g.moveTo(...P(a.map(x => -x * 1.4))); g.lineTo(...e); g.stroke(); g.setLineDash([]); g.fillStyle = '#c792ea'; g.fillText('axis', e[0] + 4, e[1]);
      group(sc.pts).forEach(p => { const q = P(p.p); arrow(g, ...o, ...q, p.col, 1.5); dot(g, ...q, p.col, p.l, 3.5); }); }); },
    'columns.cpp'(cv, r, cv2, cam){ const sc = r.scene, sz = Math.max(1, ...sc.cols.flat().map(Math.abs), ...sc.Mv.map(Math.abs)) / 1.2; view3(cv, cam, (g, P) => { const o = P([0, 0, 0]), S = p => P(p.map(x => x / sz));
      ['#ff6b6b', '#7ddc8a', '#6ea8ff'].forEach((col, i) => { const q = S(sc.cols[i]); arrow(g, ...o, ...q, col, 3); g.fillStyle = col; g.font = '11px sans-serif'; g.fillText(`M[${i}]`, q[0] + 5, q[1] + 12); });
      let at = [0, 0, 0]; sc.cols.forEach((cl, i) => { const nx = at.map((x, j) => x + sc.v[i] * cl[j]); g.setLineDash([3, 3]); arrow(g, ...S(at), ...S(nx), 'rgba(255,255,255,.45)', 1); g.setLineDash([]); at = nx; });
      const q = S(sc.Mv); arrow(g, ...o, ...q, '#ffcc66', 2.5); dot(g, ...q, '#ffcc66', `M×v ${C.cout(sc.Mv[0])}, ${C.cout(sc.Mv[1])}, ${C.cout(sc.Mv[2])}`, 3);
      g.fillStyle = COL.txt; g.font = '10px sans-serif'; g.fillText(`scale ÷ ${C.cout(+sz.toFixed(2))}`, 6, 14); }); },
    'trig.cpp'(cv, r){ const sc = r.scene, k = plane(cv, [[1.2, 1.2], [-1.2, -1.2]], 0), g = k.g; g.strokeStyle = 'rgba(255,255,255,.35)'; g.lineWidth = 1.5; g.beginPath(); g.arc(k.X(0), k.Y(0), k.s, 0, 7); g.stroke();
      g.strokeStyle = '#ffcc66'; g.lineWidth = 3; g.beginPath(); g.arc(k.X(0), k.Y(0), k.s * .35, -sc.al, -(sc.al + sc.be), sc.be > 0); g.stroke();
      arrow(g, k.X(0), k.Y(0), k.X(sc.x1), k.Y(sc.y1), '#7fb6ff'); arrow(g, k.X(0), k.Y(0), k.X(sc.x2), k.Y(sc.y2), '#7ddc8a');
      dot(g, k.X(sc.x1), k.Y(sc.y1), '#7fb6ff', `(x1, y1) = (${C.cout(C.R1000(sc.x1))}, ${C.cout(C.R1000(sc.y1))})`); dot(g, k.X(sc.x2), k.Y(sc.y2), '#7ddc8a', `(x2, y2) = (${C.cout(C.R1000(sc.x2))}, ${C.cout(C.R1000(sc.y2))})`);
      g.fillStyle = '#ffcc66'; g.font = '11px sans-serif'; g.fillText('beta', k.X(Math.cos(sc.al + sc.be / 2) * .45), k.Y(Math.sin(sc.al + sc.be / 2) * .45)); }
  };

  // ================= one simulator
  function mount(slot, P){
    const cfg = detect(P); if (!cfg){ slot.innerHTML = '<small>البرنامج المفتوح ماعندوش محاكي.</small>'; return; }
    css(); slot.innerHTML = ''; const d = cfg.d, V = {}, V0 = {}; d.params.forEach(p => { V[p.k] = start(cfg, p, V); V0[p.k] = Array.isArray(V[p.k]) ? V[p.k].slice() : V[p.k]; });
    const base = d.run(V0, cfg.S, null).out, cam = {yaw: -.6, pitch: .35}, st = {down: false, mx: null, my: null};
    const root = document.createElement('div'); root.className = 'ps';
    const two = d.mode === 'ray', isDrag = d.mode === 'drag';
    root.innerHTML = `<div class="psh"><b>${d.title} · ${esc(P.title || '')}</b><button type="button" data-a="full">⛶ كبّر</button><button type="button" data-a="reset">↺ من الأول</button></div>
<div class="pscap">${d.intro}</div><canvas class="pc1" style="height:${isDrag || two ? 'auto' : '260px'}"></canvas>${two ? '<canvas class="pc2" style="height:200px"></canvas>' : ''}${d.legend ? `<div class="pscap">${d.legend}</div>` : ''}
<div class="psin"></div><h5>✏️ السطور اللي اتغيرت في <code>${esc(cfg.file)}</code></h5><pre class="ed"></pre>
<h5>🖥️ الترمينال (اللي البرنامج بيطبعه)</h5><pre class="psterm"></pre><h5>🔎 السطور اللي اتنفذت بأرقامها</h5><pre class="log"></pre>`;
    slot.appendChild(root);
    const cv = root.querySelector('.pc1'), cv2 = root.querySelector('.pc2'), inn = root.querySelector('.psin');
    const aspect = () => { if (isDrag || two){ const w = cv.clientWidth || 300; cv.style.height = Math.round(w * (cfg.S ? cfg.S.H / cfg.S.W : .75)) + 'px'; } };
    // inputs
    d.params.forEach(p => { const box = document.createElement('div'); box.className = 'psp'; box.dataset.k = p.k;
      const lns = (p.lines || [p.line]).map(k => cfg.L[k]).filter(Boolean).map(l => l.ln);
      box.innerHTML = `<label>${p.label}${lns.length ? ` <span class="ln" style="color:#7fb6ff">(سطر ${lns.join('، ')})</span>` : ''}</label>`;
      const row = document.createElement('div'); row.className = 'psr' + (p.type ? ' psv' : '');
      if (p.type){ const n = p.type === 'vec2' ? 2 : 3; for (let i = 0; i < n; i++){ const t = document.createElement('input'); t.type = 'number'; t.step = p.step || 1; t.value = V[p.k][i]; t.oninput = () => { const x = parseFloat(t.value); if (!isNaN(x)){ V[p.k][i] = x; changed(); } }; row.appendChild(t); } }
      else { const r = document.createElement('input'); r.type = 'range'; r.min = p.min; r.max = p.max; r.step = p.step; r.value = V[p.k]; const t = document.createElement('input'); t.type = 'number'; t.step = p.step; t.value = V[p.k];
        r.oninput = () => { V[p.k] = +r.value; t.value = r.value; changed(); }; t.oninput = () => { let x = parseFloat(t.value); if (!isNaN(x)){ x = Math.max(+p.min, Math.min(+p.max, x)); V[p.k] = x; r.value = x; changed(); } }; t.onchange = () => { t.value = V[p.k]; }; row.append(r, t); }
      box.appendChild(row); inn.appendChild(box); });
    const syncInputs = () => inn.querySelectorAll('.psp').forEach(b => { const p = d.params.find(q => q.k === b.dataset.k), ins = b.querySelectorAll('input');
      if (p.type) ins.forEach((t, i) => t.value = V[p.k][i]); else ins.forEach(t => t.value = V[p.k]); });
    let last = null;
    // editing a source line = running the program again from the start, so a drag done before is gone (like the real program)
    function changed(){ if (isDrag) Object.assign(st, {down: false, mx: null, my: null}); upd(); }
    function upd(){
      const r = d.run(V, cfg.S, isDrag ? st : null); last = r;
      // edited lines
      const touched = new Map(); d.params.forEach(p => { if (p.view || same(V[p.k], V0[p.k])) return; (p.lines || [p.line]).forEach(k => { const l = cfg.L[k]; if (!l) return; const cur = touched.get(k) || {l, text: l.code}; cur.text = edit(cfg, p, V, cur.text); touched.set(k, cur); }); });
      const ed = [...touched.values()].sort((a, b) => a.l.ln - b.l.ln).filter(t => t.text !== t.l.code);
      root.querySelector('.ed').innerHTML = ed.length ? ed.map(t => `<span class="ln">${esc(cfg.file)}:${t.l.ln}</span>\n<del>- ${esc(t.l.code.trim())}</del>\n<ins>+ ${esc(t.text.trim())}</ins>`).join('\n') : '<span class="no">لسه زي الكود الأصلي. حرّك أي رقم فوق.</span>';
      inn.querySelectorAll('.psp').forEach(b => { const p = d.params.find(q => q.k === b.dataset.k); b.classList.toggle('ch', !p.view && !same(V[p.k], V0[p.k])); });
      root.querySelector('.psterm').innerHTML = r.out.map((l, i) => l === base[i] ? esc(l) : `<span class="ch">${esc(l)}</span>`).join('\n') + (r.out.length !== base.length ? `\n<span class="no">(عدد السطور ${r.out.length} بدل ${base.length})</span>` : '');
      root.querySelector('.log').innerHTML = r.log.map(([k, t, cl]) => { const l = cfg.L[k]; return (l ? `<span class="ln">${esc(cfg.file)}:${l.ln}</span> <span class="cd">${esc(l.code.trim())}</span>\n` : '') + `<span class="${cl || ''}">  ${esc(t).replace(/\n/g, '\n  ')}</span>`; }).join('\n');
      draw(); }
    function draw(){ if (!last || !root.isConnected) return; aspect(); const f = PIC[cfg.file]; if (f) f(cv, last, cv2, cam); }
    // mouse on the picture
    let lx = 0, ly = 0, turning = false;
    const toWin = e => { const b = cv.getBoundingClientRect(), W = cfg.S ? cfg.S.W : 800, H = cfg.S ? cfg.S.H : 600; return [Math.max(0, Math.min(W, (e.clientX - b.left) / b.width * W)), Math.max(0, Math.min(H, (e.clientY - b.top) / b.height * H))]; };
    cv.addEventListener('pointerdown', e => { e.preventDefault(); cv.setPointerCapture(e.pointerId); lx = e.clientX; ly = e.clientY; turning = true;
      if (isDrag){ [st.mx, st.my] = toWin(e); st.down = true; upd(); } else if (two){ [V.mx, V.my] = toWin(e).map(Math.round); syncInputs(); upd(); } });
    cv.addEventListener('pointermove', e => { if (!turning) return;
      if (isDrag){ [st.mx, st.my] = toWin(e); upd(); } else if (two){ [V.mx, V.my] = toWin(e).map(Math.round); syncInputs(); upd(); }
      else if (d.mode === '3d'){ cam.yaw += (e.clientX - lx) * .01; cam.pitch = Math.max(-1.5, Math.min(1.5, cam.pitch + (e.clientY - ly) * .01)); draw(); }
      lx = e.clientX; ly = e.clientY; });
    const up = () => { if (!turning) return; turning = false; if (isDrag){ st.down = false; upd(); } };
    cv.addEventListener('pointerup', up); cv.addEventListener('pointercancel', up);
    root.querySelector('[data-a=full]').onclick = e => { root.classList.toggle('psfull'); e.target.textContent = root.classList.contains('psfull') ? '✕ صغّر' : '⛶ كبّر'; draw(); };
    root.querySelector('[data-a=reset]').onclick = () => { d.params.forEach(p => V[p.k] = Array.isArray(V0[p.k]) ? V0[p.k].slice() : V0[p.k]); Object.assign(st, {down: false, mx: null, my: null}); cam.yaw = -.6; cam.pitch = .35; syncInputs(); upd(); };
    upd(); new ResizeObserver(() => draw()).observe(root);
  }
  const label = P => { const c = detect(P); return c ? c.d.title.replace(/^(\S+)\s+محاكي:?\s*/, '$1 افتح محاكي: ') : ''; };
  const RULE = ' البنش جواه محاكي للبرنامج ده: بيقرا الأرقام من سطور الكود نفسها، وتقدر تغيّرها وتشوف الترمينال والسطور اللي اتنفذت بالأرقام الجديدة. لو السؤال "لو غيرت الرقم ده يحصل إيه" أو عن الماوس أو عايز يجرب، جاوب في جملتين واكتب في الآخر بلوك فاضي ```camsim``` (سطرين: ```camsim ثم ```) والبنش هيفتح المحاكي.';
  return {detect, mount, label, rule: P => detect(P) ? RULE : ''};
})();
window.PSIM = PSIM;
