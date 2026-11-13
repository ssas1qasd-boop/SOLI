// ------------------------------------------------------------------ bench simulator: runs the open program's own camera code in the browser
// It reads the program's real source (Camera.h / Camera.cpp / main.cpp in P.files): the start position, speed, sensitivity, FOV, near/far,
// window size, vertices and indices. Each frame does exactly what the while loop does: camera.Inputs() then camera.Matrix(), and lists
// the lines that ran with their real numbers. Only programs that contain this code get the simulator (CAMSIM.detect).
const CAMSIM = (() => {
  // ---------- math, written to match glm
  const V = (x, y, z) => [x, y, z];
  const add = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]], mul = (a, s) => [a[0] * s, a[1] * s, a[2] * s], neg = a => [-a[0], -a[1], -a[2]];
  const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2], len = a => Math.sqrt(dot(a, a));
  const norm = a => { const l = len(a); return l ? mul(a, 1 / l) : [0, 0, 0]; };
  const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  const rad = d => d * Math.PI / 180, deg = r => r * 180 / Math.PI;
  const rotate = (v, ang, axis) => { const k = norm(axis), c = Math.cos(ang), s = Math.sin(ang); // glm::rotate(vec3, angle, normal)
    return add(add(mul(v, c), mul(cross(k, v), s)), mul(k, dot(k, v) * (1 - c))); };
  const angle = (a, b) => Math.acos(Math.max(-1, Math.min(1, dot(a, b)))); // glm::angle: no normalize
  const lookAt = (e, c, up) => { const f = norm(add(c, neg(e))), s = norm(cross(f, up)), u = cross(s, f); // rows (math order)
    return [[s[0], s[1], s[2], -dot(s, e)], [u[0], u[1], u[2], -dot(u, e)], [-f[0], -f[1], -f[2], dot(f, e)], [0, 0, 0, 1]]; };
  const perspective = (fovy, asp, n, f) => { const t = 1 / Math.tan(fovy / 2);
    return [[t / asp, 0, 0, 0], [0, t, 0, 0], [0, 0, -(f + n) / (f - n), -2 * f * n / (f - n)], [0, 0, -1, 0]]; };
  const mm = (A, B) => A.map(r => [0, 1, 2, 3].map(c => r[0] * B[0][c] + r[1] * B[1][c] + r[2] * B[2][c] + r[3] * B[3][c]));
  const mv = (M, v) => M.map(r => r[0] * v[0] + r[1] * v[1] + r[2] * v[2] + r[3] * v[3]);
  const f2 = x => { const r = Math.abs(x) < 5e-5 ? 0 : x; return r.toFixed(2); }, f3 = x => (Math.abs(x) < 5e-6 ? 0 : x).toFixed(3);
  const v3 = a => `(${f2(a[0])}, ${f2(a[1])}, ${f2(a[2])})`;
  const esc = s => String(s).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));

  // ---------- read the program
  const nums = s => (String(s).match(/-?\d+(?:\.\d+)?(?:e-?\d+)?/gi) || []).map(Number);
  function parse(P){
    if (!P || !P.files) return null;
    const F = {}; P.files.forEach((f, k) => { F[f.name] = {k, text: f.lines.join('\n'), lines: f.lines}; });
    const all = Object.values(F).map(f => f.text).join('\n');
    if (!/Camera::Inputs/.test(all) || !/glm::lookAt/.test(all) || !/glm::perspective/.test(all)) return null;
    const find = (re, pref) => { const order = Object.keys(F).sort((a, b) => (b === pref) - (a === pref));
      for (const n of order){ const k = F[n].lines.findIndex(l => re.test(l)); if (k >= 0) return {file: n, f: F[n].k, ln: k + 1, code: F[n].lines[k].trim()}; } return null; };
    const val = (re, d) => { const m = re.exec(all); return m ? m[1] : d; };
    const vec = (re, d) => { const m = re.exec(all); if (!m) return d; const n = nums(m[1]); return n.length >= 3 ? n.slice(0, 3) : d; };
    const W = +val(/(?:unsigned\s+)?int\s+width\s*=\s*(\d+)/, P.W || 800), H = +val(/(?:unsigned\s+)?int\s+height\s*=\s*(\d+)/, P.H || 800);
    const camCall = /Camera\s+\w+\s*\(\s*\w+\s*,\s*\w+\s*,\s*glm::vec3\(([^)]*)\)/.exec(all);
    const mat = /\.Matrix\(\s*([-\d.]+)f?\s*,\s*([-\d.]+)f?\s*,\s*([-\d.]+)f?/.exec(all);
    const cfg = {W, H,
      pos: camCall ? nums(camCall[1]).slice(0, 3) : [0, 0, 2],
      ori: vec(/Orientation\s*=\s*glm::vec3\(([^)]*)\)/, [0, 0, -1]), up: vec(/\bUp\s*=\s*glm::vec3\(([^)]*)\)/, [0, 1, 0]),
      speed: +val(/float\s+speed\s*=\s*([-\d.]+)/, .1), sens: +val(/float\s+sensitivity\s*=\s*([-\d.]+)/, 100),
      fast: +val(/speed\s*=\s*([-\d.]+)f?\s*;\s*\n\s*else/, .4),
      fov: mat ? +mat[1] : 45, near: mat ? +mat[2] : .1, far: mat ? +mat[3] : 100,
      clear: vec(/glClearColor\(([^)]*)\)/, [.07, .13, .17]), lock: +val(/glm::radians\(([\d.]+)f?\)\s*\|\|/, 5)};
    // the slow speed is the value set when Shift is released
    cfg.slow = +val(/GLFW_RELEASE\)\s*\n\s*speed\s*=\s*([-\d.]+)/, cfg.speed);
    // vertices: stride and offsets from glVertexAttribPointer
    const vm = /(?:GLfloat|float)\s+vertices\s*\[\s*\]\s*=\s*\{([\s\S]*?)\};/.exec(all), im = /(?:GLuint|unsigned\s+int|int)\s+indices\s*\[\s*\]\s*=\s*\{([\s\S]*?)\};/.exec(all);
    if (!vm) return null;
    const vv = nums(vm[1]); const ap = [...all.matchAll(/glVertexAttribPointer\(\s*(\d+)\s*,\s*(\d+)[^;]*?(\d+)\s*\*\s*sizeof\([^)]*\)\s*,\s*\(void\*\)\s*\(?\s*(\d+)?/g)];
    const stride = ap.length ? +ap[0][3] : 6, cOff = (ap.find(a => a[1] === '1') || [])[4], hasC = cOff != null;
    const verts = []; for (let k = 0; k + 2 < vv.length; k += stride) verts.push({p: vv.slice(k, k + 3), c: hasC ? vv.slice(k + +cOff, k + +cOff + 3) : [.8, .8, .8]});
    const idx = im ? nums(im[1]) : verts.map((_, k) => k);
    const tris = []; for (let k = 0; k + 2 < idx.length; k += 3) tris.push([idx[k], idx[k + 1], idx[k + 2]]);
    const uniq = []; verts.forEach(v => { if (!uniq.some(u => u[0] === v.p[0] && u[1] === v.p[1] && u[2] === v.p[2])) uniq.push(v.p); });
    cfg.verts = verts; cfg.tris = tris; cfg.uniq = uniq;
    // the real lines, so every value can point at where it came from
    const C = 'Camera.cpp';
    cfg.L = {W: find(/GLFW_KEY_W\b/, C), A: find(/GLFW_KEY_A\b/, C), S: find(/GLFW_KEY_S\b/, C), D: find(/GLFW_KEY_D\b/, C),
      SPACE: find(/GLFW_KEY_SPACE\b/, C), CTRL: find(/GLFW_KEY_LEFT_CONTROL\b/, C), SHIFT: find(/GLFW_KEY_LEFT_SHIFT\)\s*==\s*GLFW_PRESS/, C),
      mouse: find(/glfwGetMouseButton[^;]*GLFW_PRESS/, C), first: find(/if\s*\(\s*firstClick/, C), rotX: find(/float\s+rotX/, C), rotY: find(/float\s+rotY/, C),
      newO: find(/newOrientation\s*=/, C), lockL: find(/glm::angle\(newOrientation/, C), yaw: find(/Orientation\s*=\s*glm::rotate\(Orientation,\s*glm::radians\(-rotY/, C),
      release: find(/GLFW_MOUSE_BUTTON_LEFT\)\s*==\s*GLFW_RELEASE/, C), view: find(/view\s*=\s*glm::lookAt/, C), proj: find(/projection\s*=\s*glm::perspective/, C),
      upl: find(/glUniformMatrix4fv/, C), inputs: find(/\.Inputs\(/, 'main.cpp'), matrix: find(/\.Matrix\(/, 'main.cpp'),
      shader: find(/gl_Position\s*=/, 'main.cpp'), draw: find(/glDrawElements|glDrawArrays/, 'main.cpp')};
    return cfg;
  }
  const cache = new WeakMap();
  const detect = P => { if (!P) return null; if (!cache.has(P)) { let c = null; try { c = parse(P); } catch (e) {} cache.set(P, c); } return cache.get(P); };
  const wants = q => /محاكي|محاكى|simulat|camsim|جرّ?ب\s*(ال)?كاميرا|حرّ?ك\s*(ال)?كاميرا|\bwasd\b|w\s*a\s*s\s*d/i.test(String(q || '')) || /(دوس|داس|دوست|اضغط|ضغط|ضغطت)\S*\s+(على\s+)?(W|A|S|D|Space|Shift|Ctrl)\b.*(كاميرا|بيحصل|يحصل|إيه|ايه)/i.test(String(q || ''));

  // ---------- styles (once)
  function css(){ if (document.getElementById('camsimcss')) return; const s = document.createElement('style'); s.id = 'camsimcss';
    s.textContent = `.cs{direction:rtl;font-size:13px;line-height:1.5;margin:6px 0;border:1px solid rgba(127,127,127,.35);border-radius:10px;padding:8px;background:rgba(127,127,127,.06)}
.cs.csfull{position:fixed;inset:0;z-index:100000;overflow:auto;margin:0;border-radius:0;background:var(--bg,#101418);color:var(--fg,#e6e6e6)}
.cs .csh{display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin-bottom:6px}.cs .csh b{flex:1;min-width:120px}
.cs canvas{direction:ltr;display:block;width:100%;border-radius:8px;touch-action:none;background:#0b0f14}
.cs .cscap{font-size:11.5px;opacity:.8;margin:4px 2px 8px}
.cs .cskeys{display:grid;grid-template-columns:repeat(4,1fr);gap:5px;margin:6px 0;direction:ltr}
.cs button{font:inherit;padding:7px 4px;border-radius:8px;border:1px solid rgba(127,127,127,.45);background:rgba(127,127,127,.12);color:inherit;user-select:none;-webkit-user-select:none;touch-action:none}
.cs button.on{background:#2f7de1;color:#fff;border-color:#2f7de1}
.cs .csread{direction:ltr;text-align:left;font:12px/1.45 ui-monospace,Menlo,Consolas,monospace;display:grid;grid-template-columns:auto 1fr;gap:1px 10px;margin:6px 0}
.cs .csread span:nth-child(odd){opacity:.7}
.cs .cslog{direction:ltr;text-align:left;font:11.5px/1.5 ui-monospace,Menlo,Consolas,monospace;white-space:pre-wrap;word-break:break-word;max-height:360px;overflow:auto;background:rgba(0,0,0,.25);border-radius:8px;padding:8px}
.cs.csfull .cslog{max-height:none}
.cs .cslog .ln{color:#7fb6ff}.cs .cslog .ok{color:#7ddc8a}.cs .cslog .no{opacity:.55}.cs .cslog .hd{color:#ffcc66;font-weight:bold}.cs .cslog .ch{color:#ff9d6e}
.cs .csmat{display:inline-grid;grid-template-columns:repeat(4,auto);gap:0 10px;border-left:2px solid #888;border-right:2px solid #888;padding:0 6px;margin:2px 0 2px 14px}
.cs .csmat i{font-style:normal;text-align:right}
.cs table{border-collapse:collapse;font-size:11px;margin:2px 0 4px}.cs td,.cs th{padding:1px 6px;border-bottom:1px solid rgba(127,127,127,.25);text-align:right}
.cs .csrow{display:flex;gap:6px;flex-wrap:wrap;align-items:center;margin:4px 0}`;
    document.head.appendChild(s); }

  // ---------- one simulator
  function mount(slot, P){
    const cfg = detect(P); if (!cfg){ slot.innerHTML = '<small>البرنامج المفتوح مافيهوش كاميرا (Camera::Inputs و lookAt)، فالمحاكي مش هيشتغل هنا.</small>'; return; }
    css(); slot.innerHTML = '';
    const st = {pos: cfg.pos.slice(), ori: norm(cfg.ori), up: cfg.up.slice(), speed: cfg.speed, first: true, frame: 0, keys: new Set(), down: false, dx: 0, dy: 0, slow: true, last: 0, run: false, log: ''};
    const fileOf = l => l ? `<span class="ln">${esc(l.file)}:${l.ln}</span>` : '';
    const root = document.createElement('div'); root.className = 'cs';
    root.innerHTML = `<div class="csh"><b>🎥 محاكي الكاميرا · ${esc(P.title || '')}</b><button type="button" data-a="full">⛶ كبّر</button><button type="button" data-a="reset">↺ من الأول</button></div>
<canvas class="cstop" height="230"></canvas><div class="cscap">🗺️ من فوق (x يمين، z لتحت). النقطة = <code>Position</code>، السهم = <code>Orientation</code>، والخطين = حدود اللي الكاميرا شايفاه (FOV ${cfg.fov}°).</div>
<canvas class="cscam"></canvas><div class="cscap">🎥 اللي الكاميرا شايفاه (شباك ${cfg.W}×${cfg.H}). اسحب بصباعك عليه = الماوس الشمال متداس.</div>
<div class="cskeys"><button type="button" data-k="SPACE">↑ Space</button><button type="button" data-k="W">W</button><button type="button" data-k="CTRL">↓ Ctrl</button><button type="button" data-k="SHIFT">Shift</button><button type="button" data-k="A">A</button><button type="button" data-k="S">S</button><button type="button" data-k="D">D</button><button type="button" data-a="step">⏭ فريم</button></div>
<div class="csrow"><label><input type="checkbox" class="csslow" checked> بطيء (6 فريم/ثانية) علشان تلحق تقرا</label></div>
<div class="csread"></div><div class="cslog"></div>`;
    slot.appendChild(root);
    const top = root.querySelector('.cstop'), cam = root.querySelector('.cscam'), read = root.querySelector('.csread'), logEl = root.querySelector('.cslog');
    const size = () => { const w = Math.max(200, root.clientWidth - 18), r = devicePixelRatio || 1;
      top.width = w * r; top.height = 230 * r; top.style.height = '230px';
      const ch = Math.round(w * cfg.H / cfg.W); cam.width = w * r; cam.height = ch * r; cam.style.height = ch + 'px'; };

    // ---------- one turn of the while loop
    function frame(){
      st.frame++; const L = cfg.L, out = []; const k = n => st.keys.has(n);
      out.push(`<span class="hd">فريم ${st.frame}</span> ${fileOf(L.inputs)} camera.Inputs(window);`);
      const move = (n, dir, name) => { const p0 = st.pos; if (k(n)){ st.pos = add(st.pos, mul(dir, st.speed));
          out.push(`${fileOf(L[n])} <span class="ok">${name} متداس ✔</span>\n   Position += ${f2(st.speed)} × ${v3(dir)}\n   <span class="ch">${v3(p0)} → ${v3(st.pos)}</span>`); return 1; } return 0; };
      const right = norm(cross(st.ori, st.up)); let moved = 0;
      moved += move('W', st.ori, 'W'); moved += move('A', neg(right), 'A'); moved += move('S', neg(st.ori), 'S'); moved += move('D', right, 'D');
      moved += move('SPACE', st.up, 'Space'); moved += move('CTRL', neg(st.up), 'Ctrl');
      const off = ['W', 'A', 'S', 'D', 'SPACE', 'CTRL'].filter(n => !k(n)); if (off.length) out.push(`<span class="no">${off.map(n => n === 'SPACE' ? 'Space' : n === 'CTRL' ? 'Ctrl' : n).join(' ، ')}: مش متداسين ← الـ if مش بيتنفذ</span>`);
      if (k('W') || k('A') || k('S') || k('D')) out.push(`<span class="no">   (يمين الكاميرا = normalize(cross(Orientation, Up)) = ${v3(right)})</span>`);
      const sp0 = st.speed; st.speed = k('SHIFT') ? cfg.fast : cfg.slow;
      out.push(`${fileOf(L.SHIFT)} Shift ${k('SHIFT') ? '<span class="ok">متداس ✔</span>' : 'مش متداس'} → speed = ${f2(st.speed)}${sp0 !== st.speed ? ` <span class="ch">(كانت ${f2(sp0)}، والحركة اللي فوق في نفس الفريم مشيت بالقديمة)</span>` : ''}`);
      if (st.down){
        if (st.first){ st.first = false; st.dx = 0; st.dy = 0; out.push(`${fileOf(L.mouse)} <span class="ok">الماوس متداس ✔</span>\n${fileOf(L.first)} firstClick = true → glfwSetCursorPos(${cfg.W / 2}, ${cfg.H / 2}) و firstClick = false`); }
        const mx = cfg.W / 2 + st.dx, my = cfg.H / 2 + st.dy; st.dx = 0; st.dy = 0;
        const rotX = cfg.sens * (my - cfg.H / 2) / cfg.H, rotY = cfg.sens * (mx - cfg.W / 2) / cfg.W;
        out.push(`${fileOf(L.rotX)} mouse = (${f2(mx)}, ${f2(my)})\n   rotX = ${cfg.sens} × (${f2(my)} − ${cfg.H / 2}) / ${cfg.H} = ${f3(rotX)}°\n${fileOf(L.rotY)} rotY = ${cfg.sens} × (${f2(mx)} − ${cfg.W / 2}) / ${cfg.W} = ${f3(rotY)}°`);
        if (rotX || rotY){
          const o0 = st.ori, nO = rotate(st.ori, rad(-rotX), norm(cross(st.ori, st.up)));
          const aU = deg(angle(nO, st.up)), aD = deg(angle(nO, neg(st.up))), blocked = aU <= cfg.lock || aD <= cfg.lock;
          out.push(`${fileOf(L.newO)} newOrientation = rotate(Orientation, ${f3(-rotX)}°, يمين) = ${v3(nO)}\n${fileOf(L.lockL)} الزاوية مع Up = ${f2(aU)}° ومع −Up = ${f2(aD)}° ` + (blocked ? `<span class="ch">← أقل من ${cfg.lock}°: مش هيتقبل (علشان الكاميرا ماتتقلبش)</span>` : '<span class="ok">← تمام، Orientation = newOrientation</span>'));
          if (!blocked) st.ori = nO;
          const o1 = st.ori; st.ori = rotate(st.ori, rad(-rotY), st.up);
          out.push(`${fileOf(L.yaw)} Orientation = rotate(Orientation, ${f3(-rotY)}°, Up)\n   <span class="ch">${v3(o0)} → ${v3(st.ori)}</span>`);
          void o1;
        } else out.push('<span class="no">   الصباع ماتحركش من آخر فريم ← rotX = rotY = 0، الاتجاه زي ما هو</span>');
        out.push(`<span class="no">   glfwSetCursorPos(${cfg.W / 2}, ${cfg.H / 2}): المؤشر يرجع للنص علشان الفريم الجاي يقيس من الأول</span>`);
      } else { if (!st.first) out.push(`${fileOf(L.release)} الماوس اتساب ← firstClick = true`); st.first = true;
        out.push(`<span class="no">${L.mouse ? esc(L.mouse.file) + ':' + L.mouse.ln : ''} الماوس مش متداس ← مفيش لف</span>`); }
      // camera.Matrix
      const center = add(st.pos, st.ori), view = lookAt(st.pos, center, st.up), proj = perspective(rad(cfg.fov), cfg.W / cfg.H, cfg.near, cfg.far), M = mm(proj, view);
      st.M = M;
      const matHtml = m => `<span class="csmat">${m.map(r => r.map(x => `<i>${f3(x)}</i>`).join('')).join('')}</span>`;
      out.push(`${fileOf(L.matrix)} camera.Matrix(${cfg.fov}, ${cfg.near}, ${cfg.far}, …)\n${fileOf(L.view)} view = lookAt(eye ${v3(st.pos)}, center ${v3(center)}, up ${v3(st.up)})\n${fileOf(L.proj)} projection = perspective(${cfg.fov}°, ${cfg.W}/${cfg.H} = ${f2(cfg.W / cfg.H)}, ${cfg.near}, ${cfg.far})\n${fileOf(L.upl)} camMatrix = projection × view =\n${matHtml(M)}`);
      // the vertex shader for every corner
      const rows = cfg.uniq.map(p => { const c = mv(M, [p[0], p[1], p[2], 1]), w = c[3];
        if (w <= 1e-6) return `<tr><td>${v3(p)}</td><td>w = ${f2(w)}</td><td colspan="2">ورا الكاميرا: مش هيظهر</td></tr>`;
        const n = [c[0] / w, c[1] / w, c[2] / w], px = (n[0] + 1) / 2 * cfg.W, py = (1 - (n[1] + 1) / 2) * cfg.H, inside = Math.abs(n[0]) <= 1 && Math.abs(n[1]) <= 1 && Math.abs(n[2]) <= 1;
        return `<tr><td>${v3(p)}</td><td>(${f2(c[0])}, ${f2(c[1])}, ${f2(c[2])}, ${f2(w)})</td><td>${v3(n)}</td><td>${inside ? `(${Math.round(px)}, ${Math.round(py)})` : 'برا الشاشة'}</td></tr>`; }).join('');
      out.push(`${fileOf(L.shader)} gl_Position = camMatrix × vec4(aPos, 1.0) لكل ركن:\n<table><tr><th>aPos</th><th>gl_Position</th><th>÷ w = NDC</th><th>بكسل (من فوق)</th></tr>${rows}</table>${fileOf(L.draw)} glDrawElements(… ${cfg.tris.length * 3} index …) ← ${cfg.tris.length} مثلث اترسموا`);
      st.log = out.join('\n'); }

    // ---------- drawing
    function drawTop(){ const g = top.getContext('2d'), r = devicePixelRatio || 1, w = top.width / r, h = top.height / r; g.setTransform(r, 0, 0, r, 0, 0); g.direction = 'ltr';
      g.fillStyle = '#0b0f14'; g.fillRect(0, 0, w, h);
      const ext = Math.max(2.2, Math.abs(st.pos[0]) + .8, Math.abs(st.pos[2]) + .8), s = Math.min(w, h) / 2 / ext, cx = w / 2, cy = h / 2;
      const X = x => cx + x * s, Z = z => cy + z * s;
      g.strokeStyle = 'rgba(255,255,255,.07)'; g.lineWidth = 1; for (let a = -Math.ceil(ext * 2); a <= Math.ceil(ext * 2); a++){ const t = a / 2; g.beginPath(); g.moveTo(X(t), 0); g.lineTo(X(t), h); g.moveTo(0, Z(t)); g.lineTo(w, Z(t)); g.stroke(); }
      g.strokeStyle = 'rgba(255,255,255,.25)'; g.beginPath(); g.moveTo(X(0), 0); g.lineTo(X(0), h); g.moveTo(0, Z(0)); g.lineTo(w, Z(0)); g.stroke();
      g.fillStyle = 'rgba(255,255,255,.5)'; g.font = '10px sans-serif'; g.fillText('+x', w - 18, Z(0) - 4); g.fillText('+z', X(0) + 4, h - 4); g.fillText('-z', X(0) + 4, 11);
      cfg.tris.forEach(t => { const c = cfg.verts[t[0]].c; g.fillStyle = `rgba(${c.map(v => Math.round(v * 255)).join(',')},.35)`; g.strokeStyle = `rgb(${c.map(v => Math.round(v * 255)).join(',')})`;
        g.beginPath(); t.forEach((i, n) => { const p = cfg.verts[i].p; n ? g.lineTo(X(p[0]), Z(p[2])) : g.moveTo(X(p[0]), Z(p[2])); }); g.closePath(); g.fill(); g.stroke(); });
      const yaw = Math.atan2(st.ori[2], st.ori[0]), half = Math.atan(Math.tan(rad(cfg.fov) / 2) * cfg.W / cfg.H), L = ext * 3;
      g.fillStyle = 'rgba(255,214,102,.10)'; g.beginPath(); g.moveTo(X(st.pos[0]), Z(st.pos[2]));
      g.lineTo(X(st.pos[0] + Math.cos(yaw - half) * L), Z(st.pos[2] + Math.sin(yaw - half) * L)); g.lineTo(X(st.pos[0] + Math.cos(yaw + half) * L), Z(st.pos[2] + Math.sin(yaw + half) * L)); g.closePath(); g.fill();
      g.strokeStyle = 'rgba(255,214,102,.7)'; g.beginPath(); [yaw - half, yaw + half].forEach(a => { g.moveTo(X(st.pos[0]), Z(st.pos[2])); g.lineTo(X(st.pos[0] + Math.cos(a) * L), Z(st.pos[2] + Math.sin(a) * L)); }); g.stroke();
      const flat = Math.hypot(st.ori[0], st.ori[2]); g.strokeStyle = '#ffd666'; g.lineWidth = 2.5; g.beginPath(); g.moveTo(X(st.pos[0]), Z(st.pos[2]));
      g.lineTo(X(st.pos[0] + st.ori[0] / (flat || 1) * .6), Z(st.pos[2] + st.ori[2] / (flat || 1) * .6)); g.stroke();
      g.fillStyle = '#ffd666'; g.beginPath(); g.arc(X(st.pos[0]), Z(st.pos[2]), 5, 0, 7); g.fill();
      g.fillStyle = '#fff'; g.font = '11px ui-monospace,monospace'; g.fillText(`y = ${f2(st.pos[1])}`, 6, 14); }
    function drawCam(){ const g = cam.getContext('2d'), r = devicePixelRatio || 1, w = cam.width / r, h = cam.height / r; g.setTransform(r, 0, 0, r, 0, 0); g.direction = 'ltr';
      g.fillStyle = `rgb(${cfg.clear.map(v => Math.round(v * 255)).join(',')})`; g.fillRect(0, 0, w, h);
      const M = st.M, polys = [];
      cfg.tris.forEach(t => { let poly = t.map(i => mv(M, [...cfg.verts[i].p, 1]));
        // clip against the near plane (z >= -w), like the GPU does
        const out = []; for (let n = 0; n < poly.length; n++){ const a = poly[n], b = poly[(n + 1) % poly.length], da = a[2] + a[3], db = b[2] + b[3];
          if (da >= 0) out.push(a); if ((da >= 0) !== (db >= 0)){ const u = da / (da - db); out.push(a.map((v, j) => v + (b[j] - v) * u)); } }
        if (out.length < 3) return; const c = [0, 1, 2].map(j => t.reduce((s, i) => s + cfg.verts[i].c[j], 0) / 3);
        polys.push({pts: out.map(p => [(p[0] / p[3] + 1) / 2 * w, (1 - (p[1] / p[3] + 1) / 2) * h]), d: out.reduce((s, p) => s + p[3], 0) / out.length, c}); });
      polys.sort((a, b) => b.d - a.d).forEach(p => { g.fillStyle = `rgb(${p.c.map(v => Math.round(v * 255)).join(',')})`; g.beginPath(); p.pts.forEach((q, n) => n ? g.lineTo(q[0], q[1]) : g.moveTo(q[0], q[1])); g.closePath(); g.fill(); });
      g.strokeStyle = 'rgba(255,255,255,.25)'; g.beginPath(); g.moveTo(w / 2 - 6, h / 2); g.lineTo(w / 2 + 6, h / 2); g.moveTo(w / 2, h / 2 - 6); g.lineTo(w / 2, h / 2 + 6); g.stroke();
      if (st.down){ g.fillStyle = 'rgba(47,125,225,.85)'; g.font = '11px sans-serif'; g.fillText('🖱️ الماوس متداس', 8, 16); } }
    function show(){ drawTop(); drawCam();
      const yaw = deg(Math.atan2(st.ori[0], -st.ori[2])), pitch = deg(Math.asin(Math.max(-1, Math.min(1, st.ori[1]))));
      read.innerHTML = [['frame', st.frame], ['Position', v3(st.pos)], ['Orientation', v3(st.ori)], ['speed', f2(st.speed)], ['yaw / pitch', `${f2(yaw)}° / ${f2(pitch)}°`], ['firstClick', st.first]].map(([a, b]) => `<span>${a}</span><span>${b}</span>`).join('');
      logEl.innerHTML = st.log; root.querySelectorAll('[data-k]').forEach(b => b.classList.toggle('on', st.keys.has(b.dataset.k))); }

    // ---------- loop: runs only while something is held
    const busy = () => st.keys.size > 0 && [...st.keys].some(x => x !== 'SHIFT') || st.down;
    function tick(t){ if (!root.isConnected){ st.run = false; return; }
      if (!busy()){ st.run = false; return; }
      const gap = root.querySelector('.csslow').checked ? 1000 / 6 : 1000 / 60; if (t - st.last >= gap){ st.last = t; frame(); show(); }
      requestAnimationFrame(tick); }
    const kick = () => { if (!st.run && busy()){ st.run = true; st.last = 0; requestAnimationFrame(tick); } };
    // on-screen keys: hold to keep pressing; Shift toggles (it is held together with another key)
    root.querySelectorAll('[data-k]').forEach(b => { const n = b.dataset.k;
      if (n === 'SHIFT'){ b.onclick = () => { st.keys.has(n) ? st.keys.delete(n) : st.keys.add(n); show(); }; return; }
      const on = e => { e.preventDefault(); st.keys.add(n); b.setPointerCapture && e.pointerId != null && b.setPointerCapture(e.pointerId); kick(); show(); };
      const off = () => { st.keys.delete(n); show(); };
      b.addEventListener('pointerdown', on); b.addEventListener('pointerup', off); b.addEventListener('pointercancel', off); b.addEventListener('lostpointercapture', off); });
    root.querySelector('[data-a=step]').onclick = () => { frame(); show(); };
    root.querySelector('[data-a=reset]').onclick = () => { Object.assign(st, {pos: cfg.pos.slice(), ori: norm(cfg.ori), speed: cfg.speed, first: true, frame: 0, keys: new Set(), down: false, dx: 0, dy: 0}); frame(); st.frame = 0; show(); };
    root.querySelector('[data-a=full]').onclick = e => { root.classList.toggle('csfull'); e.target.textContent = root.classList.contains('csfull') ? '✕ صغّر' : '⛶ كبّر'; size(); show(); };
    // drag on the camera view = left mouse button held; movement is in the program's window pixels
    let lx = 0, ly = 0;
    cam.addEventListener('pointerdown', e => { e.preventDefault(); cam.setPointerCapture(e.pointerId); st.down = true; lx = e.clientX; ly = e.clientY; kick(); });
    cam.addEventListener('pointermove', e => { if (!st.down) return; const k = cfg.W / cam.clientWidth; st.dx += (e.clientX - lx) * k; st.dy += (e.clientY - ly) * k; lx = e.clientX; ly = e.clientY; });
    const up = () => { if (!st.down) return; st.down = false; frame(); show(); };
    cam.addEventListener('pointerup', up); cam.addEventListener('pointercancel', up);
    // a real keyboard works too, while the simulator is on screen
    const map = {KeyW: 'W', KeyA: 'A', KeyS: 'S', KeyD: 'D', Space: 'SPACE', ControlLeft: 'CTRL', ShiftLeft: 'SHIFT'};
    const kd = e => { if (!root.isConnected){ removeEventListener('keydown', kd); removeEventListener('keyup', ku); return; } const n = map[e.code]; if (!n || /input|textarea/i.test((e.target || {}).tagName || '')) return; e.preventDefault(); st.keys.add(n); kick(); show(); };
    const ku = e => { const n = map[e.code]; if (n){ st.keys.delete(n); show(); } };
    addEventListener('keydown', kd); addEventListener('keyup', ku);
    size(); frame(); st.frame = 0; st.log = st.log.replace(/فريم 1/, 'قبل ما تدوس حاجة (الفريم بيتكرر كده كل لفة)'); show();
    new ResizeObserver(() => { size(); show(); }).observe(root);
  }
  // slots in the chat: <div class="agcsslot"></div>; rebuilt after the chat is restored from storage
  function mountAll(r){ (r || document).querySelectorAll('.agcsslot').forEach(s => { if (s._m) return; s._m = 1; try { mountAny(s, typeof P !== 'undefined' ? P : null); } catch (e) { s.innerHTML = '<small>المحاكي وقع: ' + esc(e.message) + '</small>'; } }); }
  new MutationObserver(ms => { for (const m of ms) for (const n of m.addedNodes) if (n.nodeType === 1 && (n.classList.contains('agcsslot') || n.querySelector('.agcsslot'))){ mountAll(); return; } })
    .observe(document.documentElement, {childList: true, subtree: true});
  const RULE = ' البرنامج ده فيه كاميرا والبنش جواه محاكي حقيقي ليها: لو السؤال عن تحريك الكاميرا أو W/A/S/D أو الماوس أو إزاي المصفوفة بتتغير، جاوب في جملتين واكتب في الآخر بلوك فاضي ```camsim``` (سطرين: ```camsim ثم ```) والبنش هيفتح المحاكي بالأرقام الحقيقية.';
  // other programs (fixed numbers / mouse): PSIM. CAMSIM is the single door the chat uses for both.
  const ps = P => (typeof PSIM !== 'undefined' && PSIM.detect(P)) || null;
  const any = P => detect(P) || ps(P);
  const mountAny = (slot, P) => (!detect(P) && ps(P)) ? PSIM.mount(slot, P) : mount(slot, P);
  const label = P => detect(P) ? '🎥 افتح محاكي الكاميرا' : ps(P) ? PSIM.label(P) : '';
  const intro = P => detect(P) ? 'ده محاكي بيشغّل كود الكاميرا بتاع البرنامج ده نفسه: نفس الأرقام اللي في <code>Camera.h</code> و <code>main.cpp</code>. دوس على الزراير أو اسحب على الصورة، وتحت هتلاقي السطور اللي اتنفذت في كل فريم بأرقامها.'
    : 'ده محاكي بيشغّل البرنامج ده نفسه: الأرقام اللي فوق متقرية من سطور الكود. غيّر أي رقم كأنك عدّلت السطر وشغلت تاني، وهتشوف السطر بعد التعديل، والترمينال، والسطور اللي اتنفذت بأرقامها.';
  const wantsAny = (q, P) => wants(q) || (!detect(P) && ps(P) && /محاكي|محاكى|simulat/i.test(String(q || '')));
  return {detect: any, wants: wantsAny, mount: mountAny, mountAll, label, intro, rule: p => detect(p) ? RULE : ps(p) ? PSIM.rule(p) : ''};
})();
window.CAMSIM = CAMSIM;

// ---------- PSIM core: runs the program's own math in float32 (like the real C++), so the printed numbers match the terminal
const PSIMCORE = (() => {
  const F = Math.fround;
  // ---- cout / printf formatting
  const rhaz = x => x < 0 ? -Math.round(-x) : Math.round(x);            // std::round: half away from zero
  function cout(x){                                                      // std::cout << float  (%g, precision 6)
    x = +x; if (Number.isNaN(x)) return 'nan'; if (!isFinite(x)) return x < 0 ? '-inf' : 'inf';
    if (x === 0) return Object.is(x, -0) ? '-0' : '0';
    const e = Math.floor(Math.log10(Math.abs(x)));
    let s = x.toPrecision(6), m = /e([+-]\d+)/.exec(s);
    const ex = m ? +m[1] : e;
    if (ex < -4 || ex >= 6){ s = x.toExponential(5); let [a, b] = s.split('e'); if (a.includes('.')) a = a.replace(/0+$/, '').replace(/\.$/, ''); const n = +b; return a + 'e' + (n < 0 ? '-' : '+') + String(Math.abs(n)).padStart(2, '0'); }
    s = x.toFixed(Math.max(0, 5 - ex)); if (s.includes('.')) s = s.replace(/0+$/, '').replace(/\.$/, ''); return s;
  }
  const pf = x => (Object.is(x, -0) ? '-' : '') + (+x).toFixed(6);          // %f (glm::to_string)
  const R1000 = x => F(F(rhaz(F(x * 1000))) / 1000) + 0;                    // std::round(x * 1000) / 1000 + 0.0f
  const R100 = x => F(F(rhaz(F(x * 100))) / 100) + 0;
  // ---- float32 scalar math
  const add = (a, b) => F(a + b), sub = (a, b) => F(a - b), mul = (a, b) => F(a * b), div = (a, b) => F(a / b);
  const cos = a => F(Math.cos(F(a))), sin = a => F(Math.sin(F(a))), tan = a => F(Math.tan(F(a)));
  const radians = d => F(F(d) * F(0.01745329251994329576923690768489));
  // ---- vec (arrays of float32)
  const v = (...a) => a.map(F);
  const vadd = (a, b) => a.map((x, i) => add(x, b[i])), vsub = (a, b) => a.map((x, i) => sub(x, b[i]));
  const vmul = (a, s) => a.map(x => mul(x, s)), vneg = a => a.map(x => F(-x));
  const dot = (a, b) => a.reduce((s, x, i) => i ? add(s, mul(x, b[i])) : mul(x, b[i]), 0);
  const cross = (a, b) => [sub(mul(a[1], b[2]), mul(b[1], a[2])), sub(mul(a[2], b[0]), mul(b[2], a[0])), sub(mul(a[0], b[1]), mul(b[0], a[1]))];
  const length = a => F(Math.sqrt(dot(a, a)));
  const normalize = a => vmul(a, F(1 / F(Math.sqrt(dot(a, a)))));
  // ---- glm::mat4 = 4 columns (column-major, exactly like glm)
  const I4 = () => [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]];
  const mmul = (A, B) => B.map(c => vadd(vadd(vadd(vmul(A[0], c[0]), vmul(A[1], c[1])), vmul(A[2], c[2])), vmul(A[3], c[3])));
  const mv4 = (M, x) => vadd(vadd(vmul(M[0], x[0]), vmul(M[1], x[1])), vadd(vmul(M[2], x[2]), vmul(M[3], x[3])));
  const translate = (m, t) => [m[0], m[1], m[2], vadd(vadd(vadd(vmul(m[0], t[0]), vmul(m[1], t[1])), vmul(m[2], t[2])), m[3])];
  const scale = (m, s) => [vmul(m[0], s[0]), vmul(m[1], s[1]), vmul(m[2], s[2]), m[3]];
  function rotate(m, a, ax){
    const c = cos(a), s = sin(a), k = normalize(ax), t = vmul(k, sub(1, c));
    const R = [[add(c, mul(t[0], k[0])), add(mul(t[0], k[1]), mul(s, k[2])), sub(mul(t[0], k[2]), mul(s, k[1]))],
      [sub(mul(t[1], k[0]), mul(s, k[2])), add(c, mul(t[1], k[1])), add(mul(t[1], k[2]), mul(s, k[0]))],
      [add(mul(t[2], k[0]), mul(s, k[1])), sub(mul(t[2], k[1]), mul(s, k[0])), add(c, mul(t[2], k[2]))]];
    const col = i => vadd(vadd(vmul(m[0], R[i][0]), vmul(m[1], R[i][1])), vmul(m[2], R[i][2]));
    return [col(0), col(1), col(2), m[3]];
  }
  function perspective(fovy, asp, n, f){ const th = tan(div(fovy, 2)), M = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]];
    M[0][0] = div(1, mul(asp, th)); M[1][1] = div(1, th); M[2][2] = F(-div(add(f, n), sub(f, n))); M[2][3] = -1; M[3][2] = F(-div(mul(mul(2, f), n), sub(f, n))); return M; }
  function lookAt(e, c, up){ const f = normalize(vsub(c, e)), s = normalize(cross(f, up)), u = cross(s, f);
    return [[s[0], u[0], F(-f[0]), 0], [s[1], u[1], F(-f[1]), 0], [s[2], u[2], F(-f[2]), 0], [F(-dot(s, e)), F(-dot(u, e)), dot(f, e), 1]]; }
  function inverse(M){ // general 4x4 inverse (computed in double, stored as float)
    const a = M.flat(), o = new Array(16); // a[c*4+r]
    const g = (c, r) => a[c * 4 + r];
    const m = [[g(0,0),g(1,0),g(2,0),g(3,0)],[g(0,1),g(1,1),g(2,1),g(3,1)],[g(0,2),g(1,2),g(2,2),g(3,2)],[g(0,3),g(1,3),g(2,3),g(3,3)]];
    const n = 4, A = m.map((r, i) => r.concat([0, 0, 0, 0].map((_, j) => +(i === j))));
    for (let c = 0; c < n; c++){ let p = c; for (let r = c + 1; r < n; r++) if (Math.abs(A[r][c]) > Math.abs(A[p][c])) p = r;
      [A[c], A[p]] = [A[p], A[c]]; const d = A[c][c]; if (!d) return I4(); for (let j = 0; j < 2 * n; j++) A[c][j] /= d;
      for (let r = 0; r < n; r++) if (r !== c){ const k = A[r][c]; for (let j = 0; j < 2 * n; j++) A[r][j] -= k * A[c][j]; } }
    return [0, 1, 2, 3].map(c => [0, 1, 2, 3].map(r => F(A[r][4 + c])));
  }
  // glm::mat3 (3 columns)
  const m3 = M4 => [M4[0].slice(0, 3), M4[1].slice(0, 3), M4[2].slice(0, 3)];
  const m3v = (M, x) => vadd(vadd(vmul(M[0], x[0]), vmul(M[1], x[1])), vmul(M[2], x[2]));
  const m3m = (A, B) => B.map(c => m3v(A, c));
  const m3T = M => [0, 1, 2].map(r => [M[0][r], M[1][r], M[2][r]]);
  const m3det = m => sub(add(mul(m[0][0], sub(mul(m[1][1], m[2][2]), mul(m[2][1], m[1][2]))), mul(m[2][0], sub(mul(m[0][1], m[1][2]), mul(m[1][1], m[0][2])))), mul(m[1][0], sub(mul(m[0][1], m[2][2]), mul(m[2][1], m[0][2]))));
  // hand-written row-major 4x4 (chain_pivot.cpp's Matrix4f): m[row][col]
  const RM = {
    I: () => I4(),
    X: a => { const r = I4(); r[1][1] = cos(a); r[1][2] = F(-sin(a)); r[2][1] = sin(a); r[2][2] = cos(a); return r; },
    Y: a => { const r = I4(); r[0][0] = cos(a); r[0][2] = sin(a); r[2][0] = F(-sin(a)); r[2][2] = cos(a); return r; },
    Z: a => { const r = I4(); r[0][0] = cos(a); r[0][1] = F(-sin(a)); r[1][0] = sin(a); r[1][1] = cos(a); return r; },
    T: (x, y, z) => { const r = I4(); r[0][3] = F(x); r[1][3] = F(y); r[2][3] = F(z); return r; },
    mul: (a, b) => [0, 1, 2, 3].map(row => [0, 1, 2, 3].map(col => { let s = 0; for (let k = 0; k < 4; k++) s = add(s, mul(a[row][k], b[k][col])); return s; })),
    apply: (M, x) => { const i = [F(x[0]), F(x[1]), F(x[2]), 1]; return [0, 1, 2, 3].map(row => { let s = 0; for (let k = 0; k < 4; k++) s = add(s, mul(M[row][k], i[k])); return s; }); }
  };
  const ts3 = a => `vec3(${a.map(pf).join(', ')})`, ts4 = a => `vec4(${a.map(pf).join(', ')})`;
  return {F, cout, pf, rhaz, R1000, R100, add, sub, mul, div, cos, sin, tan, radians, v, vadd, vsub, vmul, vneg, dot, cross, length, normalize,
    I4, mmul, mv4, translate, scale, rotate, perspective, lookAt, inverse, m3, m3v, m3m, m3T, m3det, RM, ts3, ts4};
})();

// ---------- PSIM programs: one entry per source file. Each reads its inputs from the real source line,
// re-runs the same statements in float32 and returns: out (terminal lines), log ([line key, text]), scene (for the picture)
const PSIMDEFS = (() => {
  const C = PSIMCORE, F = C.F, c = C.cout, rad = C.radians;
  const v3 = a => `(${a.slice(0, 3).map(c).join(', ')})`;
  const r3 = a => `(${a.slice(0, 3).map(C.R1000).map(c).join(', ')})`;
  const mat = (M, n = 4) => '\n' + [...Array(n).keys()].map(r => '      | ' + [...Array(n).keys()].map(k => c(M[k][r]).padStart(9)).join(' ') + ' |').join('\n');  // column-major -> rows
  const rmat = (M, n = 4) => '\n' + M.slice(0, n).map(r => '      | ' + r.slice(0, n).map(x => c(x).padStart(9)).join(' ') + ' |').join('\n');
  const D = {};

  // ===================== d19_c2: drag.cpp — drag a cube with the mouse
  D['drag.cpp'] = {
    test: /DragTheObject/, title: '🖱️ محاكي سحب المكعب', mode: 'drag',
    intro: 'اسحب بصباعك على الشباك = الماوس الشمال متداس. البرنامج بيحرك المكعب اللي رقمه <code>picked</code> لحد ما يبقى تحت الماوس. المؤشرات تحت = تعديل السطور 159 و 161 وتشغيل البرنامج من الأول، فالمكعب يرجع للمكان اللي الأرقام دي بتقول عليه.',
    lines: {fn: /glm::vec3 DragTheObject/, ndcx: /float ndcX\s*=/, ndcy: /float ndcY\s*=/, focal: /float focalLength\s*=/, ray: /glm::vec3 ray\(/, hit: /glm::vec3 hit\s*=/, back: /return glm::vec3\(glm::inverse\(view\)/,
      proj: /glm::mat4 projection\s*=/, view: /glm::mat4 view\s*=/, pos: /glm::vec3 positions\[3\]/, picked: /int picked\s*=/, vz: /float objectViewZ\s*=/, m0: /double mouseX\s*=/, first: /^\s{0,6}positions\[picked\]\s*=\s*DragTheObject/, loopw: /while \(!glfwWindowShouldClose/, print: /std::cout << "cube "/,
      press: /glfwGetMouseButton\(window, GLFW_MOUSE_BUTTON_LEFT\)/, cur: /glfwGetCursorPos\(window/, call: /^\s{7,}positions\[picked\]\s*=\s*DragTheObject/, loop: /for \(int i = 0; i < 3; i\+\+\)/, model: /glm::mat4 model = glm::translate/, rot: /model = glm::rotate\(model, glm::radians\(30/, scl: /model = glm::scale/, mvp: /glm::mat4 mvp = projection \* view \* model/, draw: /glDrawArrays\(GL_TRIANGLES, 0, 36\)/, cross: /glm::mat4 atMouse/},
    params: [
      {k: 'picked', label: 'رقم المكعب اللي هيتسحب <code>picked</code>', line: 'picked', rx: /int picked = (\d+)/, def: 1, min: 0, max: 2, step: 1},
      {k: 'mx0', label: 'مكان الماوس في الأول <code>mouseX</code>', line: 'm0', rx: /mouseX = ([-\d.]+)/, def: 600, min: 0, max: 800, step: 1},
      {k: 'my0', label: 'مكان الماوس في الأول <code>mouseY</code>', line: 'm0', rx: /mouseY = ([-\d.]+)/, def: 150, min: 0, max: 600, step: 1}],
    setup(src){ // things read once from the source: window, camera, cubes, colors
      const all = src.all, n = s => (String(s).match(/-?\d+(?:\.\d+)?/g) || []).map(Number);
      const pm = /glm::perspective\(glm::radians\(([\d.]+)f?\),\s*([\d.]+)f?\s*\/\s*([\d.]+)f?,\s*([\d.]+)f?,\s*([\d.]+)f?\)/.exec(all) || [0, 45, 800, 600, .1, 100];
      const la = /glm::lookAt\(glm::vec3\(([^)]*)\),\s*glm::vec3\(([^)]*)\),\s*glm::vec3\(([^)]*)\)\)/.exec(all);
      const pos = /positions\[3\]\s*=\s*\{([^;]*)\};/.exec(all), vm = /GLfloat vertices\[\]\s*=\s*\{([\s\S]*?)\};/.exec(all);
      const vv = vm ? n(vm[1].replace(/\/\/[^\n]*/g, '')) : [];
      const tri = []; for (let k = 0; k + 5 < vv.length; k += 6) tri.push({p: vv.slice(k, k + 3), c: vv.slice(k + 3, k + 6)});
      const cc = /glClearColor\(([^)]*)\)/.exec(all);
      return {fov: +pm[1], W: +pm[2], H: +pm[3], near: +pm[4], far: +pm[5], eye: la ? n(la[1]) : [0, 0, 5], ctr: la ? n(la[2]) : [0, 0, 0], up: la ? n(la[3]) : [0, 1, 0],
        pos: pos ? [...pos[1].matchAll(/glm::vec3\(([^)]*)\)/g)].map(m => n(m[1])) : [[-2, 0, 0], [0, 0, 0], [2, 0, 0]], tri, clear: cc ? n(cc[1]) : [.07, .13, .17]};
    },
    run(V, S, st){ // st = {mx, my, down} the live mouse; null = only the part before the loop
      const P = C.perspective(rad(S.fov), C.div(S.W, S.H), S.near, S.far), View = C.lookAt(C.v(...S.eye), C.v(...S.ctr), C.v(...S.up));
      const pk = Math.max(0, Math.min(2, V.picked | 0)), pos = S.pos.map(p => C.v(...p)), log = [], out = [];
      const vz = C.mv4(View, [...pos[pk], 1])[2];
      const drag = (mx, my, tell) => { const nx = C.div(C.sub(F(mx), 400), 400), ny = C.div(C.sub(C.sub(600, F(my)), 300), 300);
        const fl = C.div(1, C.tan(C.div(rad(45), 2))), ray = [C.div(C.mul(nx, C.div(800, 600)), fl), C.div(ny, fl), -1], hit = C.vmul(ray, F(-vz));
        const w = C.mv4(C.inverse(View), [...hit, 1]).slice(0, 3);
        if (tell){ log.push(['fn', `DragTheObject(mouseX = ${c(mx)}, mouseY = ${c(my)}, view, objectViewZ = ${c(vz)})`]);
          log.push(['ndcx', `ndcX = (${c(mx)} - 400) / 400 = ${c(nx)}`]); log.push(['ndcy', `ndcY = ((600 - ${c(my)}) - 300) / 300 = ${c(ny)}`]);
          log.push(['focal', `focalLength = 1 / tan(45° / 2) = ${c(fl)}`]); log.push(['ray', `ray = (${c(nx)} × 1.33333 / ${c(fl)}, ${c(ny)} / ${c(fl)}, -1) = ${v3(ray)}`]);
          log.push(['hit', `hit = ray × ${c(-vz)} = ${v3(hit)}`]); log.push(['back', `inverse(view) × (hit, 1) = ${v3(w)}  ← مكان المكعب الجديد في العالم`]); }
        return w; };
      log.push(['proj', `projection = perspective(${S.fov}°, ${S.W}/${S.H}, ${S.near}, ${S.far})`]); log.push(['view', `view = lookAt(eye ${v3(S.eye)}, center ${v3(S.ctr)}, up ${v3(S.up)})`]);
      log.push(['picked', `picked = ${pk}  → المكعب اللي في ${v3(pos[pk])}`]); log.push(['vz', `objectViewZ = (view × (${pos[pk].map(c).join(', ')}, 1)).z = ${c(vz)}  ← بعده عن الكاميرا، ثابت طول البرنامج`]);
      log.push(['m0', `mouseX = ${c(V.mx0)}, mouseY = ${c(V.my0)}`]);
      log.push(['first', `positions[${pk}] = DragTheObject(${c(V.mx0)}, ${c(V.my0)}, ...)  ← مرة واحدة قبل اللفة`]); pos[pk] = drag(V.mx0, V.my0, !st); out.push(`cube ${pk} dragged to (${pos[pk].map(c).join(', ')})`);
      log.push(['print', `يطبع: ${out[0]}`]);
      let mx = V.mx0, my = V.my0;
      if (st){ log.push(['loopw', '— جوه اللفة: ده بيتكرر كل فريم —', 'hd']);
        if (st.down){ mx = st.mx; my = st.my; log.push(['press', 'الماوس الشمال متداس ✔', 'ok']); log.push(['cur', `glfwGetCursorPos → mouseX = ${c(mx)}, mouseY = ${c(my)}`]); log.push(['call', `positions[${pk}] = DragTheObject(...)`]); pos[pk] = drag(mx, my, true); }
        else { if (st.mx != null){ mx = st.mx; my = st.my; } log.push(['press', 'الماوس مش متداس ← الـ if مش بيتنفذ: مفيش glfwGetCursorPos، فـ mouseX و mouseY والمكعب فاضلين زي ما هما', 'no']); if (st.mx != null) pos[pk] = drag(mx, my, false); } }
      const M = pos.map((p, i) => { let m = C.translate(C.I4(), p); m = C.rotate(m, rad(30), [1, 1, 0]); m = C.scale(m, [.4, .4, .4]); return C.mmul(C.mmul(P, View), m); });
      if (st){ log.push(['loop', 'i من 0 لـ 2: المكعبات التلاتة']); pos.forEach((p, i) => { log.push(['model', `i = ${i}: model = translate${v3(p)}`]); });
        log.push(['rot', 'model = rotate(model, 30°, (1, 1, 0)) ، model = scale(model, 0.4)']);
        log.push(['mvp', `mvp للمكعب ${pk} = projection × view × model =${mat(M[pk])}`]);
        log.push(['draw', 'glDrawArrays 36 رأس × 3 مكعبات']);
        log.push(['cross', `atMouse = translate(((${c(mx)} - 400) / 400, (300 - ${c(my)}) / 300, -0.99)) = (${c(C.div(C.sub(F(mx), 400), 400))}, ${c(C.div(C.sub(300, F(my)), 300))})  ← العلامة البيضا`]); }
      return {out, log, scene: {M, pos, pk, mx, my, S}};
    }
  };

  // ===================== d19_c1: ray_math.cpp — from the mouse to a ray, on paper
  D['ray_math.cpp'] = {
    legend: 'فوق: شباك 800×600 زي GLFW (الصفر فوق الشمال). تحت: من الجنب، الكاميرا يمين وبتبص ناحية −z، 🟧 الشعاع على بعد 1، 🟨 لحد ما يخبط في مستوى الجسم 🟩.',
    test: /ViewSpaceVector/, title: '🎯 محاكي: من الماوس لـ Ray', mode: 'ray',
    intro: 'اسحب على الشباك فوق = تغيّر <code>MouseX</code> و <code>MouseY</code> (سطر 14). تحت هتشوف الشعاع من الجنب، وهو بيخبط في المستوى اللي فيه الجسم.',
    lines: {wh: /const float WindowWidth\s*=/, asp: /const float AspectRatio/, fov: /const float FieldOfView/, proj: /glm::mat4 Projection\s*=/, view: /glm::mat4 View\s*=/, mouse: /float MouseX\s*=/, wx: /float WindowX\s*=/, wy: /float WindowY\s*=/, p1: /"1\. GLFW mouse/,
      cen: /float CenterX\s*=/, nx: /float NdcX\s*=/, ny: /float NdcY\s*=/, p2: /"2\. NDC/, fl: /float FocalLength\s*=/, vsv: /glm::vec3 ViewSpaceVector\(/, p3: /"3\. focal length/,
      an1: /glm::vec4 Anton = glm::inverse/, an2: /Anton = glm::vec4\(Anton\.x/, p3b: /Anton \(inverse projection\)/, obj: /glm::vec3 ObjectWorld\(/, ovz: /float ObjectViewZ\s*=/, ip: /glm::vec3 IntersectionPoint\s*=/, p4: /"4\. object view z/,
      nw: /glm::vec4 NewWorldPosition\s*=/, p5: /"5\. new world position/, clip: /glm::vec4 clip\s*=/, ndc: /glm::vec3 ndc\s*=/, bx: /float backX\s*=/, by: /float backY\s*=/, chk: /"check: the object projects/},
    params: [
      {k: 'mx', label: '<code>MouseX</code>', line: 'mouse', rx: /MouseX = ([-\d.]+)/, def: 600, min: 0, max: 800, step: 1},
      {k: 'my', label: '<code>MouseY</code> (GLFW بيعده من فوق)', line: 'mouse', rx: /MouseY = ([-\d.]+)/, def: 150, min: 0, max: 600, step: 1},
      {k: 'fov', label: 'زاوية الرؤية <code>FieldOfView</code> بالدرجات', line: 'fov', rx: /radians\(([\d.]+)f?\)/, def: 45, min: 10, max: 120, step: 1},
      {k: 'ez', label: 'الكاميرا واقفة على z =', line: 'view', rx: /lookAt\(glm::vec3\(0, 0, ([-\d.]+)\)/, def: 5, min: 1, max: 15, step: .5},
      {k: 'oz', label: 'الجسم واقف على z = (<code>ObjectWorld</code>)', line: 'obj', rx: /ObjectWorld\([-\d.]+f?, [-\d.]+f?, ([-\d.]+)f?\)/, def: 0, min: -10, max: 4, step: .5}],
    run(V){
      const W = 800, H = 600, AR = C.div(W, H), FOV = rad(V.fov), Pr = C.perspective(FOV, AR, .1, 100), Vw = C.lookAt([0, 0, F(V.ez)], [0, 0, 0], [0, 1, 0]);
      const out = [], log = [], L = (k, t, cl) => log.push([k, t, cl]);
      L('wh', `WindowWidth = 800, WindowHeight = 600`); L('asp', `AspectRatio = 800 / 600 = ${c(AR)}`); L('fov', `FieldOfView = radians(${c(V.fov)}) = ${c(FOV)}`);
      L('view', `View = lookAt((0, 0, ${c(V.ez)}), (0, 0, 0), (0, 1, 0)) =${mat(Vw)}`);
      const mx = F(V.mx), my = F(V.my), wx = mx, wy = C.sub(H, my);
      L('mouse', `MouseX = ${c(mx)}, MouseY = ${c(my)}`); L('wy', `WindowY = 600 - ${c(my)} = ${c(wy)}  ← GLFW بيعد من فوق، OpenGL من تحت`);
      out.push(`1. GLFW mouse (${c(mx)}, ${c(my)}) -> window from the bottom (${c(wx)}, ${c(wy)})`); L('p1', out[0], 'ok');
      const cx = C.div(W, 2), cy = C.div(H, 2), nx = C.div(C.sub(wx, cx), C.div(W, 2)), ny = C.div(C.sub(wy, cy), C.div(H, 2));
      L('nx', `NdcX = (${c(wx)} - 400) / 400 = ${c(nx)}`); L('ny', `NdcY = (${c(wy)} - 300) / 300 = ${c(ny)}`);
      out.push(`2. NDC (${c(nx)}, ${c(ny)})`); L('p2', out[1], 'ok');
      const fl = C.div(1, C.tan(C.div(FOV, 2))), vs = [C.div(C.mul(nx, AR), fl), C.div(ny, fl), -1];
      L('fl', `FocalLength = 1 / tan(${c(FOV)} / 2) = ${c(fl)}`); L('vsv', `ViewSpaceVector = (${c(nx)} × ${c(AR)} / ${c(fl)}, ${c(ny)} / ${c(fl)}, -1) = ${v3(vs)}`);
      out.push(`3. focal length ${c(fl)}, view space ray (${vs.map(c).join(', ')})`); L('p3', out[2], 'ok');
      let an = C.mv4(C.inverse(Pr), [nx, ny, -1, 1]); L('an1', `inverse(Projection) × (${c(nx)}, ${c(ny)}, -1, 1) = (${an.map(c).join(', ')})`);
      an = [C.div(an[0], F(-an[2])), C.div(an[1], F(-an[2])), -1, 0]; L('an2', `÷ -z  → (${an.slice(0, 3).map(c).join(', ')})  ← نفس الشعاع بطريقة تانية`);
      out.push(`   Anton (inverse projection): (${an.slice(0, 3).map(c).join(', ')})`); L('p3b', out[3], 'ok');
      const ow = [0, 0, F(V.oz)], ovz = C.mv4(Vw, [...ow, 1])[2], ip = C.vmul(vs, F(-ovz));
      L('obj', `ObjectWorld = ${v3(ow)}`); L('ovz', `ObjectViewZ = (View × (${ow.map(c).join(', ')}, 1)).z = ${c(ovz)}`); L('ip', `IntersectionPoint = ray × ${c(-ovz)} = ${v3(ip)}`);
      out.push(`4. object view z ${c(ovz)}, intersection in view space (${ip.map(c).join(', ')})`); L('p4', out[4], 'ok');
      const nw = C.mv4(C.inverse(Vw), [...ip, 1]); L('nw', `NewWorldPosition = inverse(View) × (${ip.map(c).join(', ')}, 1) = ${v3(nw)}`);
      out.push(`5. new world position (${nw.slice(0, 3).map(c).join(', ')})`); L('p5', out[5], 'ok');
      const clip = C.mv4(C.mmul(Pr, Vw), nw), nd = [C.div(clip[0], clip[3]), C.div(clip[1], clip[3]), C.div(clip[2], clip[3])];
      const bx = C.add(cx, C.mul(C.div(W, 2), nd[0])), by = C.sub(H, C.add(cy, C.mul(C.div(H, 2), nd[1])));
      L('clip', `clip = Projection × View × world = (${clip.map(c).join(', ')})`); L('ndc', `ndc = clip / w = ${v3(nd)}`); L('bx', `backX = 400 + 400 × ${c(nd[0])} = ${c(bx)}`); L('by', `backY = 600 - (300 + 300 × ${c(nd[1])}) = ${c(by)}`);
      out.push(`check: the object projects back to mouse (${c(F(F(C.rhaz(F(bx * 100))) / 100))}, ${c(F(F(C.rhaz(F(by * 100))) / 100))})`); L('chk', out[6], 'ok');
      return {out, log, scene: {mx, my, nx, ny, vs, ip, nw, fov: V.fov, ez: +V.ez, oz: +V.oz, AR}};
    }
  };

  // ===================== d16_t2: glm_math.cpp — GLM basics
  D['glm_math.cpp'] = {
    legend: '🟩 <code>T × R</code>: يلف <code>nose</code> مكانها وبعدين ينقلها ، 🟧 <code>R × T</code>: ينقلها وبعدين يلفها حوالين (0,0) (القوس).',
    test: /value_ptr\(T\)/, title: '🧮 محاكي حسابات GLM', mode: 'plane',
    intro: 'غيّر الأرقام: كأنك عدّلت السطر في الكود وشغلت البرنامج تاني. الصورة: النقطة <code>nose</code> بعد <code>T×R</code> (لف وبعدين انقل) و <code>R×T</code> (انقل وبعدين لف).',
    lines: {a: /glm::vec3 a\(/, b: /glm::vec3 b\(/, p1: /"a \+ b = "/, p2: /"dot\(a, b\) = "/, p3: /"length\(a\) = "/, T: /glm::mat4 T = glm::translate/, p4: /"translate\(/, vp: /const float\* p = glm::value_ptr/, p5: /"value_ptr: /, p6: /"T\[3\]/,
      R: /glm::mat4 R = glm::rotate/, nose: /glm::vec4 nose\(/, spin: /glm::vec4 spin = T \* R \* nose/, orbit: /glm::vec4 orbit = R \* T \* nose/, p7: /"T \* R \* \(1, 0, 0, 1\)/, p8: /"R \* T \* \(1, 0, 0, 1\)/, ch: /glm::mat4 chained = glm::rotate\(T/, p9: /"glm::rotate\(T, \.\.\.\) == T \* R/, p10: /sizeof\(glm::vec3\)/},
    params: [
      {k: 'a', type: 'vec', label: '<code>a</code>', line: 'a', rx: /vec3 a\(([^)]*)\)/, def: [1, 2, 3], step: 1},
      {k: 'b', type: 'vec', label: '<code>b</code>', line: 'b', rx: /vec3 b\(([^)]*)\)/, def: [4, 5, 6], step: 1},
      {k: 't', type: 'vec', label: 'النقل <code>translate</code>', line: 'T', rx: /glm::vec3\(([^)]*)\)/, def: [7, 3, 5], step: 1},
      {k: 'ang', label: 'زاوية <code>R</code> حوالين z', line: 'R', rx: /radians\(([\d.-]+)f?\)/, def: 90, min: -180, max: 180, step: 5}],
    run(V){
      const out = [], log = [], L = (k, t, cl) => log.push([k, t, cl]), a = C.v(...V.a), b = C.v(...V.b), t = C.v(...V.t);
      L('a', `a = ${v3(a)}`); L('b', `b = ${v3(b)}`);
      out.push(`a + b = ${C.ts3(C.vadd(a, b))}`); L('p1', out[0], 'ok');
      out.push(`dot(a, b) = ${c(C.dot(a, b))}, cross(a, b) = ${C.ts3(C.cross(a, b))}`); L('p2', `dot = ${a.map((x, i) => `${c(x)}×${c(b[i])}`).join(' + ')} = ${c(C.dot(a, b))}\n${out[1]}`, 'ok');
      out.push(`length(a) = ${c(C.length(a))}`); L('p3', `length = √(${a.map(x => c(x) + '²').join(' + ')}) = ${c(C.length(a))}`, 'ok');
      const T = C.translate(C.I4(), t), pt = C.v(1, -1, 2, 1);
      L('T', `T = translate(${t.map(c).join(', ')}) =${mat(T)}`);
      out.push(`translate(7, 3, 5) * (1, -1, 2, 1) = ${C.ts4(C.mv4(T, pt))}`); L('p4', out[3] + (t.join() !== '7,3,5' ? '\n  (النص "translate(7, 3, 5)" مكتوب ثابت في الكود، فمش بيتغير لما تغيّر الأرقام)' : ''), 'ok');
      const fl = [0, 1, 2, 3].flatMap(k => T[k]); L('vp', `p = value_ptr(T) → ${fl.map(c).join(', ')}  ← العواميد ورا بعض`);
      out.push(`value_ptr: p[12], p[13], p[14] = ${c(fl[12])}, ${c(fl[13])}, ${c(fl[14])}  (column-major: the 4th column is stored last)`); L('p5', out[4], 'ok');
      out.push(`T[3] (the 4th column) = ${C.ts4(T[3])}`); L('p6', out[5], 'ok');
      const R = C.rotate(C.I4(), rad(V.ang), [0, 0, 1]), nose = [1, 0, 0, 1], TR = C.mmul(T, R), RT = C.mmul(R, T), spin = C.mv4(TR, nose), orbit = C.mv4(RT, nose);
      L('R', `R = rotate(${c(V.ang)}°, z) =${mat(R)}`); L('nose', 'nose = (1, 0, 0, 1)');
      L('spin', `T × R × nose: R يلف nose الأول → ${v3(C.mv4(R, nose))}، وبعدين T ينقلها → ${v3(spin)}`); L('orbit', `R × T × nose: T ينقل nose الأول → ${v3(C.mv4(T, nose))}، وبعدين R يلفها حوالين الأصل → ${v3(orbit)}`);
      out.push(`T * R * (1, 0, 0, 1) = (${spin.slice(0, 3).map(c).join(', ')})`); L('p7', out[6], 'ok');
      out.push(`R * T * (1, 0, 0, 1) = (${orbit.slice(0, 3).map(c).join(', ')})`); L('p8', out[7], 'ok');
      const ch = C.rotate(T, rad(90), [0, 0, 1]), same = ch.every((col, k) => col.every((x, r) => x === TR[k][r]));
      L('ch', `chained = rotate(T, 90°, z)  ← glm::rotate بيضرب T × R من اليمين` + (V.ang != 90 ? '\n  (السطر ده مكتوب فيه 90 ثابتة، و R بقت ' + c(V.ang) + '°)' : ''));
      out.push(`glm::rotate(T, ...) == T * R ? ${same ? 'yes' : 'no'}`); L('p9', out[8], same ? 'ok' : 'ch');
      out.push('sizeof(glm::vec3) = 12, sizeof(glm::mat4) = 64'); L('p10', out[9] + '  (3 × 4 بايت ، 16 × 4 بايت)', 'ok');
      return {out, log, scene: {pts: [{p: nose, l: 'nose', col: '#bbb'}, {p: C.mv4(R, nose), l: 'R×nose', col: '#888'}, {p: spin, l: 'T×R×nose', col: '#7ddc8a'}, {p: C.mv4(T, nose), l: 'T×nose', col: '#888'}, {p: orbit, l: 'R×T×nose', col: '#ff9d6e'}],
        arrows: [[nose, C.mv4(R, nose), '#888'], [C.mv4(R, nose), spin, '#7ddc8a'], [nose, C.mv4(T, nose), '#888'], [C.mv4(T, nose), orbit, '#ff9d6e', 'arc']]}};
    }
  };

  // ===================== d17_t2: axes.cpp — rotation axes and order
  D['axes.cpp'] = {
    legend: '🟩 <code>Rx × Ry × p</code> ، 🟧 <code>Ry × Rx × p</code> ، 🟪 <code>R × p</code> و <code>R × q</code> حوالين المحور المتقطع.',
    test: /R \* R\^T diagonal/, title: '🧭 محاكي محاور الدوران', mode: '3d',
    intro: 'غيّر الزاوية وشوف النقط بتروح فين. الصورة 3D: اسحب عليها عشان تلفها.',
    lines: {I: /glm::mat4 I\(1\.0f\)/, p: /glm::vec4 p\(/, q: /glm::vec4 q\(/, z: /Show\("Rz\(90\)/, x: /Show\("Rx\(90\)/, y: /Show\("Ry\(90\)/, Rx: /glm::mat4 Rx = /, Ry: /glm::mat4 Ry = /, xy: /Show\("Rx \* Ry/, yx: /Show\("Ry \* Rx/,
      ax: /glm::vec3 axis = glm::normalize/, R: /glm::mat4 R = glm::rotate\(I, glm::radians\(/, Rp: /Show\("R\(120, \(1,1,1\)\) \* \(1, 0, 0\)/, Rq: /Show\("R\(120, \(1,1,1\)\) \* \(0, 1, 0\)/, R3: /glm::mat3 R3\(R\)/, chk: /glm::mat3 check = /, pd: /"R \* R\^T diagonal/, len: /"length before = "/},
    params: [
      {k: 'a', label: 'زاوية <code>Rx</code> و <code>Ry</code> و <code>Rz</code> (سطور 16 لـ 21)', lines: ['z', 'x', 'y', 'Rx', 'Ry'], rx: /radians\(([\d.-]+)f?\)/, def: 90, min: -180, max: 180, step: 5},
      {k: 'b', label: 'زاوية <code>R</code> حوالين المحور', line: 'R', rx: /radians\(([\d.-]+)f?\)/, def: 120, min: -180, max: 180, step: 5},
      {k: 'axis', type: 'vec', label: 'المحور <code>axis</code> (قبل normalize)', line: 'ax', rx: /glm::vec3\(([^)]*)\)/, def: [1, 1, 1], step: .5}],
    run(V){
      const out = [], log = [], L = (k, t, cl) => log.push([k, t, cl]), I = C.I4(), p = [1, 0, 0, 1], q = [0, 1, 0, 1], a = rad(V.a), A = c(V.a);
      const Rz = C.rotate(I, a, [0, 0, 1]), Rx = C.rotate(I, a, [1, 0, 0]), Ry = C.rotate(I, a, [0, 1, 0]);
      const show = (k, name, x) => { const s = `${name} ${r3(x)}`; out.push(s); L(k, s, 'ok'); };
      L('p', 'p = (1, 0, 0) ، q = (0, 1, 0)');
      show('z', `Rz(90) * (1, 0, 0) =`, C.mv4(Rz, p)); show('x', `Rx(90) * (0, 1, 0) =`, C.mv4(Rx, q)); show('y', `Ry(90) * (1, 0, 0) =`, C.mv4(Ry, p));
      if (V.a != 90) L('z', `(النص "90" اللي بيتطبع مكتوب ثابت؛ الزاوية الحقيقية ${A}°)`, 'no');
      L('Rx', `Rx = rotate(${A}°, x) =${mat(Rx, 3)}`); L('Ry', `Ry = rotate(${A}°, y) =${mat(Ry, 3)}`);
      const xy = C.mv4(C.mmul(Rx, Ry), p), yx = C.mv4(C.mmul(Ry, Rx), p);
      L('xy', `Rx × Ry × p: Ry الأول → ${r3(C.mv4(Ry, p))} ثم Rx → ${r3(xy)}`); show('xy', `Rx * Ry * (1, 0, 0) =`, xy);
      L('yx', `Ry × Rx × p: Rx الأول → ${r3(C.mv4(Rx, p))} ثم Ry → ${r3(yx)}`); show('yx', `Ry * Rx * (1, 0, 0) =`, yx);
      const ax = C.normalize(C.v(...V.axis)), R = C.rotate(I, rad(V.b), ax);
      L('ax', `axis = normalize(${V.axis.map(c).join(', ')}) = ${v3(ax)}`); L('R', `R = rotate(${c(V.b)}°, axis) =${mat(R, 3)}`);
      const Rp = C.mv4(R, p), Rq = C.mv4(R, q); show('Rp', `R(120, (1,1,1)) * (1, 0, 0) =`, Rp); show('Rq', `R(120, (1,1,1)) * (0, 1, 0) =`, Rq);
      const R3 = C.m3(R), ck = C.m3m(R3, C.m3T(R3)), det = C.m3det(R3);
      L('chk', `R3 × transpose(R3) =${mat(ck, 3)}  ← لازم تطلع I لو R دوران سليم`);
      out.push(`R * R^T diagonal = ${c(ck[0][0])}, ${c(ck[1][1])}, ${c(ck[2][2])},  det(R) = ${c(det)}`); L('pd', out[out.length - 1], 'ok');
      out.push(`length before = ${c(C.length([1, 0, 0]))}, after = ${c(C.length(Rp.slice(0, 3)))}`); L('len', out[out.length - 1] + '  ← الدوران مش بيغيّر الطول', 'ok');
      return {out, log, scene: {axis: ax, pts: [{p, l: 'p', col: '#bbb'}, {p: q, l: 'q', col: '#bbb'}, {p: xy, l: 'Rx·Ry·p', col: '#7ddc8a'}, {p: yx, l: 'Ry·Rx·p', col: '#ff9d6e'}, {p: Rp, l: 'R·p', col: '#c792ea'}, {p: Rq, l: 'R·q', col: '#c792ea'}]}};
    }
  };

  // ===================== d17_c1: two_containers.cpp — transform order
  D['two_containers.cpp'] = {
    legend: '🟩 translate ثم rotate (container 1) ، 🟧 rotate ثم translate (swapped) ، 🟪 scale بـ sin (container 2) ، الإطار الرمادي = الصندوق قبل أي تحويل.',
    test: /container 1 \(translate, rotate\)/, title: '📦 محاكي: ترتيب التحويلات', mode: 'plane',
    intro: 'الصورة بترسم الصناديق في اللفة اللي تختارها. الأخضر = translate ثم rotate، البرتقاني = rotate ثم translate، البنفسجي = scale بـ sin. النقطة = الركن (0.5, 0.5).',
    lines: {loop: /for \(int second = 0; second <= /, time: /float time = second \*/, pt: /"time = "/, f1: /first = glm::translate\(first/, f2: /first = glm::rotate\(first/, c1: /Corner\("  container 1/, s1: /swapped = glm::rotate\(swapped/, s2: /swapped = glm::translate\(swapped/, c2: /Corner\("  swapped/,
      sn: /float s = std::sin\(time\)/, t2: /second2 = glm::translate\(second2/, sc: /second2 = glm::scale\(second2/, c3: /Corner\("  container 2/, cor: /glm::vec4 c = M \* glm::vec4\(0\.5f, 0\.5f/},
    params: [
      {k: 'n', label: 'عدد اللفات: <code>second &lt;= ?</code>', line: 'loop', rx: /second <= (\d+)/, def: 2, min: 0, max: 8, step: 1},
      {k: 'dt', label: 'الوقت بيزيد كل لفة <code>time = second × ?</code>', line: 'time', rx: /second \* ([\d.]+)f?/, def: .7854, min: 0, max: 3.1416, step: .0001},
      {k: 'tr', type: 'vec2', label: 'نقل الصندوق الأول <code>translate</code> (سطر 20 و 26)', lines: ['f1', 's2'], rx: /glm::vec3\(([-\d.]+f?, [-\d.]+f?)/, def: [.5, -.5], step: .1},
      {k: 'see', view: 1, label: '👁️ الصورة ترسم اللفة رقم', def: 1, min: 0, max: 8, step: 1}],
    run(V){
      const out = [], log = [], L = (k, t, cl) => log.push([k, t, cl]), corner = [.5, .5, 0, 1], sc = [];
      const tr = [F(V.tr[0]), F(V.tr[1]), 0], tl = `(${tr.slice(0, 2).map(c).join(', ')})`;
      for (let s = 0; s <= V.n; s++){
        const time = C.mul(s, F(V.dt)); out.push(`time = ${c(time)} s`); L('time', `— second = ${s}: time = ${s} × ${c(F(V.dt))} = ${c(time)}`, 'hd'); L('pt', out[out.length - 1], 'ok');
        const cor = (k, name, M, how) => { const p = C.mv4(M, corner); const s2 = `${name} corner (0.5, 0.5) -> (${c(C.R100(p[0]))}, ${c(C.R100(p[1]))})`; out.push(s2); L(k, how + '\n' + s2, 'ok'); return p; };
        let f = C.translate(C.I4(), tr); f = C.rotate(f, time, [0, 0, 1]);
        L('f2', `first = translate${tl} × rotate(${c(time)})`); const a = cor('c1', '  container 1 (translate, rotate)', f, `الركن بيتلف ${c(time)} راديان حوالين (0,0) بتاعه، وبعدين يتنقل ${tl}`);
        let w = C.rotate(C.I4(), time, [0, 0, 1]); w = C.translate(w, tr);
        L('s2', `swapped = rotate(${c(time)}) × translate${tl}`); const b = cor('c2', '  swapped (rotate, translate) ', w, `الركن بيتنقل ${tl} الأول، وبعدين يتلف حوالين أصل الشاشة`);
        const sn = C.sin(time); L('sn', `s = sin(${c(time)}) = ${c(sn)}`);
        let t = C.translate(C.I4(), [-.5, .5, 0]); t = C.scale(t, [sn, sn, sn]);
        const d = cor('c3', '  container 2 (scale by sin)   ', t, `الركن بيتكبّر × ${c(sn)}، وبعدين يتنقل (-0.5, 0.5)`);
        sc.push({time, M: [f, w, t], P: [a, b, d]});
      }
      return {out, log, scene: {it: sc[Math.min(sc.length - 1, Math.max(0, V.see | 0))], n: sc.length}};
    }
  };

  // ===================== d17_c2: parent_child.cpp — table and chairs
  D['parent_child.cpp'] = {
    legend: 'الرمادي الباهت = الطرابيزة وكراسيها وهي في الأصل ، 🟨 الطرابيزة بعد النقل واللف ، 🟦 الكراسي (الرقم = i).',
    test: /table moved to/, title: '🪑 محاكي: Parent و Child', mode: 'plane',
    intro: 'الكراسي متعرفة بالنسبة للطرابيزة (chairs[i])، فلما تحرك أو تلف الطرابيزة كلهم بيمشوا معاها: <code>table × chairs[i]</code>.',
    lines: {loop1: /chairs\[i\] = glm::rotate\(glm::mat4\(1\.0f\), glm::radians\(/, tr: /chairs\[i\] = glm::translate\(chairs\[i\]/, t0: /glm::mat4 table = glm::mat4\(1\.0f\)/, p0: /"table at the origin:"/, w0: /Where\("  chair", table \* chairs\[i\]\);/,
      tt: /table = glm::translate\(glm::mat4\(1\.0f\)/, tro: /table = glm::rotate\(table/, p1: /"table moved to/, wt: /Where\("  table", table\)/, fn: /glm::vec4 p = M \* glm::vec4\(0\.0f/},
    params: [
      {k: 'step', label: 'الكراسي بتتلف كل واحد <code>90 × i</code>', line: 'loop1', rx: /radians\(([\d.]+)f? \* i\)/, def: 90, min: 0, max: 180, step: 5},
      {k: 'd', label: 'بعد الكرسي عن الطرابيزة', line: 'tr', rx: /glm::vec3\(([\d.]+)f?/, def: 1.5, min: 0, max: 5, step: .1},
      {k: 'tp', type: 'vec2', label: 'مكان الطرابيزة', line: 'tt', rx: /glm::vec3\(([-\d.]+f?, [-\d.]+f?)/, def: [10, 5], step: 1},
      {k: 'ta', label: 'لفة الطرابيزة', line: 'tro', rx: /radians\(([-\d.]+)f?\)/, def: 45, min: -180, max: 180, step: 5}],
    run(V){
      const out = [], log = [], L = (k, t, cl) => log.push([k, t, cl]), o = [0, 0, 0, 1], ch = [];
      for (let i = 0; i < 4; i++){ let m = C.rotate(C.I4(), rad(C.mul(F(V.step), i)), [0, 0, 1]); m = C.translate(m, [F(V.d), 0, 0]); ch.push(m);
        L('tr', `i = ${i}: chairs[${i}] = rotate(${c(C.mul(F(V.step), i))}°) × translate(${c(F(V.d))}, 0) → الكرسي في ${r3(C.mv4(m, o)).replace(/, [^,]*\)$/, ')')} بالنسبة للطرابيزة`); }
      const where = (k, name, M) => { const p = C.mv4(M, o), s = `${name} at (${c(C.R100(p[0]))}, ${c(C.R100(p[1]))})`; out.push(s); L(k, s, 'ok'); return p; };
      let T = C.I4(); out.push('table at the origin:'); L('p0', out[0], 'ok'); const a0 = ch.map(m => where('w0', '  chair', C.mmul(T, m)));
      T = C.translate(C.I4(), [F(V.tp[0]), F(V.tp[1]), 0]); T = C.rotate(T, rad(V.ta), [0, 0, 1]);
      L('tro', `table = translate(${V.tp.map(c).join(', ')}) × rotate(${c(V.ta)}°) =${mat(T, 3)}`);
      out.push(`table moved to (10, 5) and turned 45:`); L('p1', out[out.length - 1] + ((V.tp[0] != 10 || V.tp[1] != 5 || V.ta != 45) ? '\n  (النص ده مكتوب ثابت في الكود)' : ''), 'ok');
      const tb = where('wt', '  table', T); const a1 = ch.map((m, i) => { L('w0', `table × chairs[${i}]`); return where('w0', '  chair', C.mmul(T, m)); });
      return {out, log, scene: {T, ch, a0, a1, tb}};
    }
  };

  // ===================== d18_t2: columns.cpp — a column = where an axis goes
  D['columns.cpp'] = {
    legend: '🟥🟩🟦 العواميد <code>M[0]</code> و <code>M[1]</code> و <code>M[2]</code> ، 🟨 <code>M × v</code> ، والمتقطع = v.x خطوة على العمود الأول + v.y على التاني + v.z على التالت.',
    test: /1\*M\[0\] \+ 2\*M\[1\]/, title: '🧱 محاكي: العمود = مكان المحور', mode: '3d',
    intro: 'كل عمود في <code>M</code> هو المكان اللي المحور بيروحله. <code>M × v</code> = x × العمود الأول + y × التاني + z × التالت. اسحب على الصورة عشان تلفها.',
    lines: {M: /glm::mat3 M\(/, v: /glm::vec3 v\(/, mv: /Print\("M \* \(1, 2, 3\)/, sum: /Print\("1\*M\[0\]/, g: /glm::mat3 fromGlm/, g0: /column 0 =", fromGlm\[0\]/, g2: /column 2 =", fromGlm\[2\]/, sh: /glm::mat3 shear\(/, a: /Print\("shear \* \(M \* v\)/, b: /Print\("\(shear \* M\) \* v/, c: /Print\("\(M \* shear\) \* v/, d: /Print\("column 0 of shear \* M/, e: /Print\("shear \* \(where i goes/},
    params: [
      {k: 'm0', type: 'vec', label: 'العمود الأول <code>M[0]</code> = فين x بيروح', line: 'M', rx: /M\(glm::vec3\(([^)]*)\)/, def: [0, 0, -1], step: 1},
      {k: 'm1', type: 'vec', label: 'العمود التاني <code>M[1]</code> = فين y بيروح', line: 'M', rx: /\), glm::vec3\(([^)]*)\), glm::vec3/, def: [0, 1, 0], step: 1},
      {k: 'm2', type: 'vec', label: 'العمود التالت <code>M[2]</code> = فين z بيروح', line: 'M', rx: /glm::vec3\(([^)]*)\)\);\s*$/, def: [1, 0, 0], step: 1},
      {k: 'v', type: 'vec', label: '<code>v</code>', line: 'v', rx: /vec3 v\(([^)]*)\)/, def: [1, 2, 3], step: 1},
      {k: 'k', label: 'ميل الـ shear (أول رقم في عموده التاني)', line: 'sh', rx: /\), glm::vec3\(([-\d.]+)/, def: 1, min: -3, max: 3, step: .5}],
    run(V){
      const out = [], log = [], L = (k, t, cl) => log.push([k, t, cl]), M = [C.v(...V.m0), C.v(...V.m1), C.v(...V.m2)], v = C.v(...V.v);
      const P = (k, name, x, how) => { const s = `${name} ${r3(x)}`; out.push(s); L(k, (how ? how + '\n' : '') + s, 'ok'); return x; };
      L('M', `M =${mat(M, 3)}  (العواميد: ${M.map(v3).join(' ، ')})`); L('v', `v = ${v3(v)}`);
      const Mv = P('mv', 'M * (1, 2, 3)               =', C.m3v(M, v));
      P('sum', '1*M[0] + 2*M[1] + 3*M[2]    =', C.vadd(C.vadd(C.vmul(M[0], v[0]), C.vmul(M[1], v[1])), C.vmul(M[2], v[2])), `${c(v[0])}×${v3(M[0])} + ${c(v[1])}×${v3(M[1])} + ${c(v[2])}×${v3(M[2])}`);
      const G = C.m3(C.rotate(C.I4(), rad(90), [0, 1, 0])); L('g', `fromGlm = rotate(90°, y) =${mat(G, 3)}`);
      P('g0', 'glm::rotate(90, y) column 0 =', G[0], 'x بيروح على -z'); P('g2', 'glm::rotate(90, y) column 2 =', G[2], 'z بيروح على x');
      const S = [[1, 0, 0], C.v(V.k, 1, 0), [0, 0, 1]]; L('sh', `shear =${mat(S, 3)}  ← y بيميل ${c(F(V.k))} ناحية x`);
      P('a', 'shear * (M * v)             =', C.m3v(S, Mv)); P('b', '(shear * M) * v             =', C.m3v(C.m3m(S, M), v), 'نفس اللي فوق: الضرب بيتجمّع');
      P('c', '(M * shear) * v             =', C.m3v(C.m3m(M, S), v), 'الترتيب اتعكس ← نتيجة تانية');
      P('d', 'column 0 of shear * M       =', C.m3m(S, M)[0]); P('e', 'shear * (where i goes, M[0])=', C.m3v(S, M[0]), 'العمود الأول للحاصل = shear مطبق على العمود الأول');
      return {out, log, scene: {cols: M, Mv, v}};
    }
  };

  // ===================== d18_c2: trig.cpp — the rotation formula
  D['trig.cpp'] = {
    legend: '🟦 <code>(x1, y1)</code> عند alpha ، 🟩 <code>(x2, y2)</code> بعد ما لفينا beta (القوس الأصفر).',
    test: /cos\/sin\(75\)/, title: '📐 محاكي: صيغة الدوران', mode: 'circle',
    intro: 'النقطة على الدايرة عند <code>alpha</code>، ونلفها <code>beta</code> بالصيغة: x2 = x1·cos − y1·sin ، y2 = x1·sin + y1·cos. لازم تطلع نفس cos/sin(alpha + beta).',
    lines: {ab: /float alpha = glm::radians/, x1: /float x1 = std::cos/, x2: /float x2 = x1/, y2: /float y2 = x1/, p1: /"start \("/, p2: /"formula:/, p3: /"cos\/sin\(75\)/, ang: /float angle = 0\.0f/, loop: /for \(int frame = 0; frame < /, inc: /angle \+= /, p4: /"60 frames x 6 degrees/,
      b: /float b = glm::radians/, rx: /float rx\[3\]\[3\]/, ry: /float ry\[3\]\[3\]/, gx: /glm::mat4 gx = /, gy: /glm::mat4 gy = /, w: /worst = std::fmax\(worst, std::fabs\(rx/, p5: /"hand Rx, Ry/, p6: /"Rx row 1 = \("/},
    params: [
      {k: 'al', label: '<code>alpha</code> (البداية)', line: 'ab', rx: /alpha = glm::radians\(([\d.-]+)f?\)/, def: 30, min: -180, max: 180, step: 1},
      {k: 'be', label: '<code>beta</code> (اللفة)', line: 'ab', rx: /beta = glm::radians\(([\d.-]+)f?\)/, def: 45, min: -180, max: 180, step: 1},
      {k: 'fr', label: 'عدد الفريمات', line: 'loop', rx: /frame < (\d+)/, def: 60, min: 0, max: 240, step: 1},
      {k: 'st', label: 'درجات كل فريم', line: 'inc', rx: /angle \+= ([\d.]+)f?/, def: 6, min: 0, max: 30, step: .5},
      {k: 'b', label: 'زاوية Rx و Ry في الآخر', line: 'b', rx: /radians\(([\d.-]+)f?\)/, def: 90, min: -180, max: 180, step: 5}],
    run(V){
      const out = [], log = [], L = (k, t, cl) => log.push([k, t, cl]), R = C.R1000, al = rad(V.al), be = rad(V.be);
      const x1 = C.cos(al), y1 = C.sin(al), x2 = C.sub(C.mul(x1, C.cos(be)), C.mul(y1, C.sin(be))), y2 = C.add(C.mul(x1, C.sin(be)), C.mul(y1, C.cos(be)));
      L('ab', `alpha = ${c(al)} راديان ، beta = ${c(be)} راديان`); L('x1', `x1 = cos(alpha) = ${c(x1)} ، y1 = sin(alpha) = ${c(y1)}`);
      L('x2', `x2 = ${c(x1)}×${c(C.cos(be))} − ${c(y1)}×${c(C.sin(be))} = ${c(x2)}`); L('y2', `y2 = ${c(x1)}×${c(C.sin(be))} + ${c(y1)}×${c(C.cos(be))} = ${c(y2)}`);
      out.push(`start (${c(R(x1))}, ${c(R(y1))}) at 30 degrees, turn 45`); L('p1', out[0] + ((V.al != 30 || V.be != 45) ? '\n  ("30" و "45" مكتوبين ثابت في النص)' : ''), 'ok');
      out.push(`formula:      (${c(R(x2))}, ${c(R(y2))})`); L('p2', out[1], 'ok');
      const ab = C.add(al, be); out.push(`cos/sin(75):  (${c(R(C.cos(ab)))}, ${c(R(C.sin(ab)))})`); L('p3', out[2], 'ok');
      let ang = 0; for (let f = 0; f < V.fr; f++) ang = C.add(ang, F(V.st)); L('inc', `angle += ${c(F(V.st))}  × ${V.fr | 0} مرة = ${c(ang)}`);
      out.push(`60 frames x 6 degrees = ${c(ang)} degrees (one full turn per second at 60 fps)`); L('p4', out[3], 'ok');
      const b = rad(V.b), cb = C.cos(b), sb = C.sin(b);
      const rx = [[1, 0, 0], [0, cb, F(-sb)], [0, sb, cb]], ry = [[cb, 0, sb], [0, 1, 0], [F(-sb), 0, cb]];
      const gx = C.rotate(C.I4(), b, [1, 0, 0]), gy = C.rotate(C.I4(), b, [0, 1, 0]); let worst = 0;
      for (let r = 0; r < 3; r++) for (let k = 0; k < 3; k++){ worst = F(Math.max(worst, F(Math.abs(C.sub(rx[r][k], gx[k][r]))))); worst = F(Math.max(worst, F(Math.abs(C.sub(ry[r][k], gy[k][r]))))); }
      L('rx', `rx (بإيدنا، صف صف) =${rmat(rx, 3)}`); L('gx', `gx = glm::rotate(${c(V.b)}°, x) (glm بيخزن عواميد، فبنقارن rx[row][col] مع gx[col][row]) =${mat(gx, 3)}`);
      out.push(`hand Rx, Ry (row by row) vs glm::rotate: biggest difference ${c(worst)}`); L('p5', out[4] + '  ← فرق تقريب float بس', 'ok');
      out.push(`Rx row 1 = (${rx[1].map(R).map(c).join(', ')}), Ry row 2 = (${ry[2].map(R).map(c).join(', ')})`); L('p6', out[5], 'ok');
      return {out, log, scene: {al, be, x1, y1, x2, y2}};
    }
  };

  // ===================== d20_t2: chain_pivot.cpp — chained rotations and a pivot
  D['chain_pivot.cpp'] = {
    legend: '⬜ الصندوق في الأول ، 🟧 <code>RotationZ</code> لوحده (بيلف حوالين (0,0)) ، 🟩 <code>T(p) × R × T(−p)</code> (بيلف حوالين نفسه). تابع النقطة <code>corner</code>.',
    test: /aroundSelf/, title: '🔁 محاكي: سلسلة Rotations و Pivot', mode: 'plane',
    intro: 'الصندوق اللي مركزه عند <code>pivot</code>: لو لفيته بـ <code>RotationZ</code> لوحده بيلف حوالين (0,0). عشان يلف حوالين نفسه: انقله للأصل، لفه، رجّعه: <code>T(p) × R × T(−p)</code>.',
    lines: {a: /float a = glm::radians/, ch: /Matrix4f chain = RotationZ/, g: /glm::mat4 g = glm::rotate/, w: /worst = std::fmax\(worst, std::fabs\(chain/, p1: /"chain Rz \* Ry \* Rx vs glm/, p2: /Apply\("chain \* \(0, 1, 0\)/, p3: /Apply\("RotationZ\(90\) \* \(3, 0, 0\)/, as: /Matrix4f aroundSelf = /, p4: /Apply\("T\(3\) R T\(-3\) \* centre/, p5: /Apply\("T\(3\) R T\(-3\) \* corner/},
    params: [
      {k: 'a', label: 'الزاوية <code>a</code>', line: 'a', rx: /radians\(([\d.-]+)f?\)/, def: 90, min: -180, max: 180, step: 5},
      {k: 'p', label: 'مركز الصندوق (الـ pivot) على x', lines: ['p3', 'as', 'p4', 'p5'], rx: /, ([-\d.]+), 0, 0\);/, def: 3, min: -5, max: 5, step: .5,
        rep: (s, x, V) => /corner/.test(s) ? s.replace(/aroundSelf, [-\d.]+, 0, 0\)/, `aroundSelf, ${+V.p + +V.r}, 0, 0)`) : s.replace(/(RotationZ\(a\)|aroundSelf), [-\d.]+, 0, 0\);/, `$1, ${x}, 0, 0);`).replace(/Translation\([\d.]+, 0, 0\) \*/, `Translation(${x}, 0, 0) *`).replace(/Translation\(-[\d.]+, 0, 0\);/, `Translation(${-x}, 0, 0);`)},
      {k: 'r', label: 'نص عرض الصندوق (الركن = pivot + ?)', line: 'p5', rx: /aroundSelf, ([\d.]+), 0, 0\)/, def: 1, min: .5, max: 3, step: .5, from: (x, V) => x - V.p, rep: (s, x, V) => s.replace(/aroundSelf, [\d.]+, 0, 0\)/, `aroundSelf, ${+V.p + +x}, 0, 0)`)}],
    run(V){
      const out = [], log = [], L = (k, t, cl) => log.push([k, t, cl]), M = C.RM, a = rad(V.a), A = c(V.a), p = F(V.p), corner = C.add(p, F(V.r));
      const r3n = o => `(${o.slice(0, 3).map(C.R1000).map(c).join(', ')})`;
      L('a', `a = radians(${A}) = ${c(a)}`);
      const chain = M.mul(M.mul(M.Z(a), M.Y(a)), M.X(a)); L('ch', `chain = RotationZ × RotationY × RotationX (صف صف) =${rmat(chain)}`);
      const g = C.mmul(C.mmul(C.rotate(C.I4(), a, [0, 0, 1]), C.rotate(C.I4(), a, [0, 1, 0])), C.rotate(C.I4(), a, [1, 0, 0]));
      let worst = 0; for (let r = 0; r < 4; r++) for (let k = 0; k < 4; k++) worst = F(Math.max(worst, F(Math.abs(C.sub(chain[r][k], g[k][r])))));
      L('g', 'g = نفس السلسلة بـ glm (بيخزن عواميد، فبنقارن chain.m[row][col] مع g[col][row])');
      out.push(`chain Rz * Ry * Rx vs glm: biggest difference ${c(worst)}`); L('p1', out[0] + '  ← فرق تقريب float بس', 'ok');
      const ap = (k, name, Mx, x, how) => { const o = M.apply(Mx, x), s = `${name} ${r3n(o)}`; out.push(s); L(k, (how ? how + '\n' : '') + s, 'ok'); return o; };
      ap('p2', 'chain * (0, 1, 0) =', chain, [0, 1, 0], `Rx الأول ← ${r3n(M.apply(M.X(a), [0, 1, 0]))} ثم Ry ← ${r3n(M.apply(M.mul(M.Y(a), M.X(a)), [0, 1, 0]))} ثم Rz`);
      const z = ap('p3', `RotationZ(90) * (3, 0, 0)          =`, M.Z(a), [p, 0, 0], `المركز (${c(p)}, 0) بيلف حوالين (0,0) ← بيبعد عن مكانه`);
      const as = M.mul(M.mul(M.T(p, 0, 0), M.Z(a)), M.T(F(-p), 0, 0)); L('as', `aroundSelf = T(${c(p)}) × RotationZ(${A}°) × T(${c(-p)}) =${rmat(as)}`);
      const c0 = ap('p4', `T(3) R T(-3) * centre (3, 0, 0)    =`, as, [p, 0, 0], 'T(−p) ← المركز يروح (0,0) ، R ← يفضل (0,0) ، T(p) ← يرجع مكانه');
      const c1 = ap('p5', `T(3) R T(-3) * corner (4, 0, 0)    =`, as, [corner, 0, 0], `الركن (${c(corner)}, 0) بيلف حوالين المركز`);
      if (V.a != 90 || V.p != 3 || V.r != 1) L('p5', '(الأرقام اللي جوه النصوص "(3, 0, 0)" و "90" مكتوبة ثابت؛ الحساب نفسه بقى بالأرقام الجديدة)', 'no');
      const box = [[-1, -1], [1, -1], [1, 1], [-1, 1]].map(([x, y]) => [C.add(p, C.mul(x, F(V.r))), C.mul(y, F(V.r)), 0]);
      return {out, log, scene: {box, orbit: box.map(q => M.apply(M.Z(a), q)), self: box.map(q => M.apply(as, q)), p, z, c0, c1, corner}};
    }
  };
  return D;
})();

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
.ps pre{direction:ltr;text-align:left;font:11.5px/1.5 ui-monospace,Menlo,Consolas,monospace;white-space:pre-wrap;word-break:break-word;margin:0;background:rgba(0,0,0,.28);border-radius:8px;padding:8px;max-height:330px;overflow:auto}
.ps.psfull pre{max-height:none}.ps .term{background:#05080b;color:#d7f7d0}.ps .term .ch{color:#ff9d6e}
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
<h5>🖥️ الترمينال (اللي البرنامج بيطبعه)</h5><pre class="term"></pre><h5>🔎 السطور اللي اتنفذت بأرقامها</h5><pre class="log"></pre>`;
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
      root.querySelector('.term').innerHTML = r.out.map((l, i) => l === base[i] ? esc(l) : `<span class="ch">${esc(l)}</span>`).join('\n') + (r.out.length !== base.length ? `\n<span class="no">(عدد السطور ${r.out.length} بدل ${base.length})</span>` : '');
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

// ------------------------------------------------------------------ bench helper: a small offline agent (no AI model) + a 3D robot
// It reads only what is already in the page: the real trace (steps, RAM, GPU state), line explanations, the story, the glossary.
const AG = (() => {
  // ---------- text normalisation (Arabic + code)
  const AR_DIG = '٠١٢٣٤٥٦٧٨٩';
  const strip = h => String(h || '').replace(/<[^>]+>/g, ' ').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"');
  function norm(s){
    return strip(s).replace(/[ً-ْـ‎‏‪-‮]/g, '').replace(/[أإآٱ]/g, 'ا').replace(/ة/g, 'ه').replace(/ى/g, 'ي').replace(/ؤ/g, 'و').replace(/ئ/g, 'ي')
      .replace(/[٠-٩]/g, d => AR_DIG.indexOf(d)).replace(/([a-z])([A-Z])/g, '$1 $2').toLowerCase(); }
  const STOP = new Set(('ليه ليش لماذا لم انت انتا انتي عملت عمل عملنا بيعمل بتعمل هو هي هم ده دي دا دول ايه اي ما في فى من علي على عن الي الى اللي ان انه انها و او ' +
    'كل ال الـ انهي نهي سطر خطوه هدف الهدف اهداف وظيفه وظيفته دوره دورها شغلته لزمته لازمته فايده فايدته بيفيد بتفيد استخدام بنستخدم محتاجين فيه فيها فيهم بيه بنعمل بيعمل بتعمل نعمل يعمل تعمل عملت عملنا بنكتب كتبنا بيكتب البرنامج برنامج الكود كود علاقه علاقة يعني كام كم عدد فين امتي ازاي ازay ليه طب طيب بس كده كدا مع لو هل يا ياريت ممكن عاوز عايز اعرف قولي قلي وضحلي اشرحلي اشرح فهمني مش مفيش لسه برضه برده كمان جوه بره هنا هناك ' +
    'the a an of to is in on and or for it this that what why how many').split(/\s+/));
  function stem(w){
    if (/^[a-z0-9_]+$/.test(w)) return w;
    for (const p of ['وبال', 'وال', 'بال', 'كال', 'فال', 'لل', 'ال']) if (w.startsWith(p) && w.length - p.length >= 2){ w = w.slice(p.length); break; }
    if (w.length > 3 && w[0] === 'و') w = w.slice(1);
    if (w.length >= 5 && w[0] === 'ل') w = w.slice(1);
    if (w.length >= 5 && /^(بي|بت|بن)/.test(w)) w = w.slice(2); else if (w.length >= 4 && /^[يتنا]/.test(w)) w = w.slice(1);
    if (w.length >= 4 && w[0] === 'ت') w = w.slice(1);
    for (const s of ['ات', 'ين', 'ون', 'ها', 'هم', 'ه']) if (w.endsWith(s) && w.length - s.length >= 3){ w = w.slice(0, -s.length); break; }
    return w; }
  // concepts: every word on the left means the same thing as the key
  const SYN = {
    buffer: 'buffer buffers بافر بفر بوفر صندوق صناديق صندوقين vbo ibo ebo glgenbuffers glbufferdata glbindbuffer array_buffer',
    ebo: 'ebo ibo indices index اندكس انديكس ترتيب element element_array_buffer gldrawelements',
    vao: 'vao vaos ورقه اوراق ورقة vertex array glgenvertexarrays glbindvertexarray layout',
    attrib: 'attrib attribute خانه خانات glvertexattribpointer glenablevertexattribarray stride offset شكل وصف layout',
    gpu: 'gpu جي كارت الكارت كرت جرافيك vram',
    ram: 'ram رام الرام ذاكره stack ستاك متغير متغيرات',
    cpu: 'cpu بروسيسور معالج',
    window: 'window شباك نافذه glfwcreatewindow glfw',
    shader: 'shader شيدر شادر vertex fragment glsl glcreateshader glcompileshader',
    program: 'program glcreateprogram gllinkprogram gluseprogram createshader',
    uniform: 'uniform يونيفورم gluniform4f gluniform2f gluniform1i gluniform1f u_color u_offset location',
    color: 'لون الوان color u_color برتقاني ازرق احمر اخضر',
    draw: 'draw رسم ارسم رسمه رسمات بيرسم gldrawarrays gldrawelements',
    bind: 'bind ربط اربط يربط بيربط glbindbuffer glbindvertexarray glbindtexture',
    loop: 'loop لوب لفه لفات تكرار while frame فريم فريمات',
    square: 'square مربع مستطيل rect rectangle',
    triangle: 'triangle مثلث مثلثات',
    texture: 'texture تكستشر تكسشر glgentextures glteximage2d stbi_load',
    clear: 'clear امسح مسح شاشه الشاشه glclear gl_color_buffer_bit',
    swap: 'swap glfwswapbuffers تبديل',
    terminal: 'terminal تيرمنال طباعه اطبع cout print',
    method: 'method طريقه طريقة',
    upload: 'upload بعت ابعت نبعت بنبعت ارفع نقل انقل نسخ انسخ glbufferdata gl_static_draw gl_dynamic_draw glteximage2d',
    delete: 'delete امسح مسح gldeletebuffers gldeleteprogram gldeletevertexarrays'
  };
  const CMAP = new Map();
  for (const [k, ws] of Object.entries(SYN)) for (const w of ws.split(/\s+/)){ const st = stem(norm(w)); CMAP.set(st, (CMAP.get(st) || []).concat(k)); }
  function toks(s){
    const out = [];
    const raw = strip(s); // keep code identifiers whole too
    (raw.match(/[A-Za-z_][A-Za-z0-9_]{2,}/g) || []).forEach(id => { const l = id.toLowerCase(); out.push(l); const c = CMAP.get(l); if (c) c.forEach(x => out.push('§' + x)); });
    for (let w of norm(s).split(/[^a-z0-9_\u0621-\u064A]+/)){ if (!w || STOP.has(w)) continue; w = stem(w); if (!w || STOP.has(w)) continue; out.push(w); const c = CMAP.get(w); if (c) c.forEach(x => out.push('§' + x)); }
    return out; }

  // ---------- index (all programs on the page)
  let DOCS = [], DF = new Map(), AVG = 1, FACTS = {};
  const SEM0 = (typeof AG_SEM !== 'undefined' && AG_SEM) || {assoc: {}, vocab: []}; const SEM = {assoc: new Map(Object.entries(SEM0.assoc)), vocab: SEM0.vocab};
  const tri = w => { const s = ' ' + w + ' ', o = new Set(); for (let k = 0; k < s.length - 2; k++) o.add(s.slice(k, k + 3)); return o; };
  function addDoc(d){ const tf = new Map(); let len = 0;
    for (const [txt, w] of d.fields){ for (const t of toks(txt)){ tf.set(t, (tf.get(t) || 0) + w); len += w;
      const A_ = SEM.assoc.get(t); if (A_) for (const [c, aw] of A_) tf.set(c, (tf.get(c) || 0) + w * aw * .35); } }
    d.tf = tf; d.len = len || 1; delete d.fields; DOCS.push(d); }
  const lineOfStep = (p, s) => (p.files[s.f].lines[s.ln - 1] || '').trim();
  function build(){
    DOCS = [];
    for (const p of PROGS){
      const seen = new Set();
      p.steps.forEach((s, k) => { const code = lineOfStep(p, s); const key = s.f + ':' + s.ln;
        const first = !seen.has(key); seen.add(key);
        addDoc({pid: p.id, k, kind: 'step', first, title: s.ti, code, ex: s.ex,
          fields: [[s.ti, 2], [code, 3], [s.ex, 2], [(s.dy || []).join(' '), first ? .5 : .2], [(s.lv || []).map(l => l.join(' ')).join(' '), .6]]}); });
      p.files.forEach((f, fi) => f.lines.forEach((l, n) => { const t = l.trim(); if (!t || /^[{}];?$/.test(t) || seen.has(fi + ':' + (n + 1))) return;
        addDoc({pid: p.id, k: null, f: fi, ln: n + 1, kind: 'line', first: true, title: 'سطر ' + (n + 1), code: t, ex: (f.lx || [])[n] || '', fields: [[t, 3], [(f.lx || [])[n] || '', 2]]}); }));
      const S = PSTORY[p.id];
      if (S && S.goal) addDoc({pid: p.id, k: null, kind: 'goal', title: p.title, text: S.goal, fields: [[S.goal, 1.2], [p.title + ' ' + p.desc, 2]]});
      if (S && S.loop) addDoc({pid: p.id, k: null, kind: 'loop', title: 'ليه بنعمل لوب؟', text: S.loop, fields: [[S.loop, 1], ['loop لوب لفه while', 1]]});
    }
    const KB = (typeof AG_KB !== 'undefined' && AG_KB) || [];
    KB.forEach((e, n) => addDoc({pid: e.pid, k: null, kind: 'kb', n, title: e.q[0], text: e.a, qset: new Set(toks(e.q.join(' \n ')).flatMap(t => [t, ...((SEM.assoc.get(t) || []).map(x => x[0]))])), fields: [[e.q.join(' \n '), 3], [e.a, .4]]}));
    for (const [t, v] of Object.entries(G)) addDoc({pid: null, k: null, kind: 'gloss', title: t, text: v[0] + ' <span class="eg">مثال: ' + v[1] + '</span>', fields: [[t, 4], [v[0], 1]]});
    DF = new Map(); VOC = null; let L = 0; for (const d of DOCS){ L += d.len; for (const t of d.tf.keys()) DF.set(t, (DF.get(t) || 0) + 1); } AVG = L / DOCS.length; pretrain(); }
  let VOC = null;
  function fixWord(t){ if (DF.has(t) || t.length < 3 || /^\d+$/.test(t) || t[0] === '§') return null;
    if (!VOC){ VOC = [...new Set([...DF.keys()].filter(x => x[0] !== '§' && x.length >= 3).concat(SEM.vocab))].map(x => [x, tri(x)]); }
    const a = tri(t); let best = null, bs = 0;
    for (const [x, b] of VOC){ if (Math.abs(x.length - t.length) > 2) continue; let n = 0; for (const g of a) if (b.has(g)) n++; const j = n / (a.size + b.size - n); if (j > bs){ bs = j; best = x; } }
    return bs >= .42 ? best : null; }
  const LA_KEY = 'benchHelperAssoc', CL_KEY = 'benchHelperFromClaude';
  const lsGet = (k, d) => { try { return JSON.parse(localStorage.getItem(k) || '') || d; } catch (e){ return d; } };
  const lsSet = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e){} };
  let LEARN = lsGet(LA_KEY, {});
  function qweights(q, noLearn){ const W_ = new Map(), add = (t, w) => W_.set(t, Math.max(W_.get(t) || 0, w)); const fixed = [];
    if (!noLearn) for (const t of toks(q)){ const la = LEARN[t]; if (la) for (const [c, w] of Object.entries(la)) add(c, Math.min(.8, w)); }
    for (const t of toks(q)){ add(t, 1); let base = t; if (!DF.has(t)){ const f = fixWord(t); if (f){ add(f, .85); base = f; fixed.push([t, f]); const c = CMAP.get(f); if (c) c.forEach(x => add('§' + x, .7)); } }
      const A_ = SEM.assoc.get(base); if (A_) for (const [c, aw] of A_) add(c, .55 * aw); }
    W_.fixed = fixed; return W_; }
  function bm25(qw, d){ let sc = 0; const N = DOCS.length;
    for (const [t, qv] of qw){ const f = d.tf.get(t); if (!f) continue; const n = DF.get(t) || 1; const idf = Math.log(1 + (N - n + .5) / (n + .5));
      sc += qv * idf * f * 2.2 / (f + 1.2 * (.25 + .75 * d.len / AVG)) * (t[0] === '§' ? .8 : 1); }
    return sc; }
  // ---------- a small linear model that trains while you use the helper (online softmax regression over the bench's lines)
  // features = the question's words + concepts + learned meanings; classes = steps / lines / prepared answers of this program
  const MKEY = 'benchHelperModel';
  let USER = lsGet0(MKEY, {v: 1, n: 0, ev: 0, W: {}}); const BASE = {W: {}};
  function lsGet0(k, d){ try { return JSON.parse(localStorage.getItem(k) || '') || d; } catch (e){ return d; } }
  const did = d => d.kind === 'step' ? 's:' + d.k : d.kind === 'line' ? 'l:' + d.f + ':' + d.ln : d.kind === 'kb' ? 'kb:' + d.n : null;
  const byId = (pid, id) => { const [a, b, c] = id.split(':'); return DOCS.find(d => d.pid === pid && (a === 's' ? d.kind === 'step' && d.k === +b : a === 'l' ? d.kind === 'line' && d.f === +b && d.ln === +c : d.kind === 'kb' && d.n === +b)); };
  const feats = q => { const m = qweights(q, true); const out = new Map(); for (const [t, w] of m) if (w >= .2) out.set(t, w); return out; };
  function lscore(pid, fx, id){ let s = 0; for (const M of [BASE, USER]){ const W = M.W[pid]; if (!W) continue; for (const [f, x] of fx){ const r = W[f]; if (r && r[id]) s += x * r[id]; } } return s; }
  function sgd(M, pid, fx, targets, cands, lr){ // targets: {id: weight>0}; cands: ids to normalise over
    const ids = [...new Set([...Object.keys(targets), ...cands])]; if (!ids.length) return;
    const sc = ids.map(id => lscore(pid, fx, id)); const mx = Math.max(...sc); const ex = sc.map(v => Math.exp(v - mx)); const Z = ex.reduce((a, b) => a + b, 0);
    const tsum = Object.values(targets).reduce((a, b) => a + b, 0) || 1;
    const W = M.W[pid] || (M.W[pid] = {});
    ids.forEach((id, n) => { const g = (targets[id] || 0) / tsum - ex[n] / Z; if (Math.abs(g) < 1e-3) return;
      for (const [f, x] of fx){ const r = W[f] || (W[f] = {}); r[id] = Math.max(-4, Math.min(4, (r[id] || 0) + lr * x * g)); if (Math.abs(r[id]) < .005) delete r[id]; } }); }
  function saveUser(){ // keep it small: drop tiny weights, cap the number of features
    for (const pid in USER.W){ const W = USER.W[pid]; for (const f in W){ for (const id in W[f]) if (Math.abs(W[f][id]) < .02) delete W[f][id]; if (!Object.keys(W[f]).length) delete W[f]; }
      const fs = Object.keys(W); if (fs.length > 4000) fs.sort((a, b) => Object.values(W[a]).reduce((s, v) => s + Math.abs(v), 0) - Object.values(W[b]).reduce((s, v) => s + Math.abs(v), 0)).slice(0, fs.length - 4000).forEach(f => delete W[f]); }
    try { localStorage.setItem(MKEY, JSON.stringify(USER)); } catch (e){} }
  function train(q, pos, neg = [], lr = .6, kind = 'fb'){ const fx = feats(q); if (!fx.size) return 0;
    const cands = search(q, {pid: P.id, kinds: ['step', 'line', 'kb'], n: 12}).map(x => did(x.d)).filter(Boolean).concat(neg);
    const T = {}; pos.forEach(([id, w]) => { T[id] = (T[id] || 0) + w; }); if (!Object.keys(T).length) return 0;
    for (let e = 0; e < 3; e++) sgd(USER, P.id, fx, T, cands, lr);
    USER.n++; USER.ev = (USER.ev || 0) + 1; (USER.log = USER.log || []).push({t: Date.now(), k: kind, q: q.slice(0, 80), pid: P.id}); USER.log = USER.log.slice(-60); saveUser(); return 1; }
  function pretrain(){ BASE.W = {}; const KB = (typeof AG_KB !== 'undefined' && AG_KB) || [];
    const SHIP = (typeof AG_MODEL !== 'undefined' && AG_MODEL) || {}; for (const pid in SHIP){ BASE.W[pid] = JSON.parse(JSON.stringify(SHIP[pid])); } // lessons you sent back, built into the page for every device
    for (let e = 0; e < 4; e++) KB.forEach((x, n) => x.q.forEach(v => { const fx = feats(v); const pid = x.pid; const cands = KB.map((y, m) => y.pid === pid ? 'kb:' + m : null).filter(Boolean);
      const W0 = BASE.W; sgd(BASE, pid, fx, {['kb:' + n]: 1}, cands, .5); })); }
  function predict(q, pid){ const fx = feats(q); const W = [BASE.W[pid], USER.W[pid]]; const ids = new Set();
    for (const M of W){ if (!M) continue; for (const f of fx.keys()) if (M[f]) Object.keys(M[f]).forEach(id => ids.add(id)); }
    return [...ids].map(id => [id, lscore(pid, fx, id)]).sort((a, b) => b[1] - a[1]); }
  function modelStats(){ const W = USER.W[P.id] || {}; const pairs = [];
    for (const f in W) for (const id in W[f]) if (W[f][id] > .3) pairs.push([f, id, W[f][id]]);
    pairs.sort((a, b) => b[2] - a[2]); return {n: USER.n || 0, feats: Object.keys(W).length, top: pairs.slice(0, 10).map(([f, id, w]) => { const d = byId(P.id, id); return {f, id, w, code: d ? (d.code || d.title) : id, d}; }), log: (USER.log || []).filter(x => x.pid === P.id).slice(-8)}; }
  function exportModel(){ return JSON.stringify({model: USER, assoc: LEARN, claude: lsGet(CL_KEY, []), free: lsGet('benchHelperFreeLessons', []), picks: lsGet0('benchHelperLearn', [])}); }
  function importModel(txt){ const o = JSON.parse(txt); if (!o || !o.model || !o.model.W) throw new Error('bad');
    for (const pid in o.model.W){ const W = USER.W[pid] || (USER.W[pid] = {}); for (const f in o.model.W[pid]){ const r = W[f] || (W[f] = {}); for (const id in o.model.W[pid][f]) r[id] = Math.max(-4, Math.min(4, (r[id] || 0) + o.model.W[pid][f][id])); } }
    USER.n = (USER.n || 0) + (o.model.n || 0); saveUser();
    if (o.assoc){ for (const w in o.assoc){ LEARN[w] = LEARN[w] || {}; for (const c in o.assoc[w]) LEARN[w][c] = Math.min(.8, Math.max(LEARN[w][c] || 0, o.assoc[w][c])); } lsSet(LA_KEY, LEARN); }
    if (o.claude) lsSet(CL_KEY, lsGet(CL_KEY, []).concat(o.claude).slice(-200));
    if (o.free) lsSet('benchHelperFreeLessons', lsGet('benchHelperFreeLessons', []).concat(o.free).slice(-150));
    if (o.picks) try { localStorage.setItem('benchHelperLearn', JSON.stringify(lsGet0('benchHelperLearn', []).concat(o.picks).slice(-300))); } catch (e){}
    return true; }
  function resetModel(){ USER = {v: 1, n: 0, ev: 0, W: {}}; LEARN = {}; try { ['benchHelperModel', 'benchHelperAssoc', 'benchHelperFromClaude', 'benchHelperLearn', 'benchHelperFreeLessons'].forEach(k => localStorage.removeItem(k)); } catch (e){} }
  function search(q, {pid, kinds, n = 8} = {}){
    const qt = qweights(q); if (!qt.size) return []; let FX = null;
    const qc = [...qt.keys()].filter(t => t[0] === '§' && qt.get(t) >= .7);
    return DOCS.filter(d => (!kinds || kinds.includes(d.kind)) && (!pid || d.pid === pid || d.pid === null))
      .map(d => ({d, s: bm25(qt, d) * (d.code && qc.length ? 1 + .3 * qc.filter(c => (d.cset || (d.cset = new Set(toks(d.code)))).has(c)).length : 1) * (d.pid === P.id ? 1.6 : d.pid === null ? 1 : .7) * (d.kind === 'step' && !d.first ? .75 : 1)}))
      .filter(x => x.s > 0).map(x => { if (x.d.pid && (x.d.kind === 'step' || x.d.kind === 'line' || x.d.kind === 'kb')){ const id = did(x.d); const ls = lscore(x.d.pid, FX || (FX = feats(q)), id); x.ls = ls; x.s = x.s * Math.exp(Math.max(-1.5, Math.min(2.5, ls * .8))); } return x; })
      .sort((a, b) => b.s - a.s).slice(0, n); }

  // ---------- facts about the current program, taken from the trace
  function facts(){
    if (FACTS[P.id]) return FACTS[P.id];
    const F = {bufs: {}, vaos: {}, draws: [], vars: new Map(), laps: P.laps || 0, uni: {}};
    const last = ST[ST.length - 1].gp || {};
    ST.forEach((s, k) => { const code = stepText(s);
      (s.lv || []).forEach(([kind, lab]) => {
        const mb = /Buffer (\d+)/.exec(lab || ''), mv = /VAO (\d+)/.exec(lab || '');
        if (s.an === 'new' && kind === 'buf' && mb && !F.bufs[mb[1]]) F.bufs[mb[1]] = {id: mb[1], v: (/&(\w+)/.exec(code) || [])[1], gen: k, up: null, src: null, binds: []};
        if (s.an === 'new' && kind === 'vao' && mv && !F.vaos[mv[1]]) F.vaos[mv[1]] = {id: mv[1], v: (/&(\w+)/.exec(code) || [])[1], gen: k, draws: 0, set: []};
        if (s.an === 'upload' && mb && F.bufs[mb[1]] && F.bufs[mb[1]].up === null){ F.bufs[mb[1]].up = k; const a = code.split(','); F.bufs[mb[1]].src = (a[2] || '').trim().replace(/^&/, ''); }
      });
      if (/glBindBuffer\(/.test(code)){ const v = (/,\s*(\w+)\s*\)/.exec(code) || [])[1]; Object.values(F.bufs).forEach(b => { if (b.v === v) b.binds.push(k); }); }
      if (/glVertexAttribPointer|glEnableVertexAttribArray|glBindBuffer\(GL_ELEMENT/.test(code) && s.gp && s.gp.bvao && F.vaos[s.gp.bvao]) F.vaos[s.gp.bvao].set.push(k);
      if (s.an === 'draw'){ F.draws.push({k, code, vao: s.gp && s.gp.bvao, lap: s.lap}); if (s.gp && F.vaos[s.gp.bvao]) F.vaos[s.gp.bvao].draws++; }
      const fr = s.st && s.st[s.st.length - 1];
      if (fr) for (const [n, v, u] of fr.v){ if (u) continue; const h = F.vars.get(n) || []; if (!h.length || h[h.length - 1].v !== v) h.push({k, v, fn: fr.fn}); F.vars.set(n, h); }
    });
    Object.values(F.bufs).forEach(b => { const g = (last.bufs || {})[b.id] || {}; b.t = g.t; b.bytes = g.bytes; b.vals = g.vals || []; });
    Object.values(F.vaos).forEach(v => { const g = (last.vaos || {})[v.id] || {}; v.at = g.at || {}; v.ebo = g.ebo; });
    F.uni = last.uni || {}; F.lapsSeen = new Set(F.draws.map(d => d.lap)).size || 1;
    return (FACTS[P.id] = F); }

  // ---------- answer helpers
  const C = t => `<code>${esc(String(t))}</code>`;
  const N = n => `عدد ${n}`;
  const chip = (k, pid) => { const s = (PROGS.find(p => p.id === (pid || P.id)) || P).steps[k]; return `<button type="button" class="agchip" data-k="${k}"${pid && pid !== P.id ? ` data-pid="${pid}"` : ''}>خطوة ${k + 1} · سطر ${s.ln}</button>`; };
  const lchip = d => `<button type="button" class="agchip" data-f="${d.f}" data-ln="${d.ln}"${d.pid !== P.id ? ` data-pid="${d.pid}"` : ''}>سطر ${d.ln} (مش بيتنفذ لوحده)</button>`;
  const anyChip = d => d.kind === 'line' ? lchip(d) : chip(d.k, d.pid);
  const names = {buf: id => { const b = facts().bufs[id]; return `<bdi dir="ltr">Buffer ${id}${b && b.v ? ` (${esc(b.v)})` : ''}</bdi>`; }, vao: id => { const v = facts().vaos[id]; return `<bdi dir="ltr">VAO ${id}${v && v.v ? ` (${esc(v.v)})` : ''}</bdi>`; }};
  function bufPurpose(b){
    if (b.t === 'EBO') return `ترتيب الأركان (EBO): ${N(b.vals.length)} أرقام ${b.vals.length % 3 ? '' : `= ${N(b.vals.length / 3)} مثلث`}، ${b.bytes} بايت`;
    const who = b.src ? `فيه أرقام ${C(b.src)}` : 'فيه أركان';
    return `${who}: ${N(b.vals.length)} أرقام، ${b.bytes || 0} بايت`; }
  function whoUses(id){ return Object.values(facts().vaos).filter(v => Object.values(v.at || {}).some(a => +a.buf === +id) || +v.ebo === +id).map(v => names.vao(v.id)); }
  function whyText(k){ try { return strip(whyHtml(k)).replace(/\s+/g, ' ').trim().slice(0, 420); } catch (e){ return ''; } }

  // ---------- intents
  function intent(q){
    const n = norm(q);
    const num = (n.match(/\d+/g) || []).map(Number);
    return {
      nav: /(روح|وديني|خدني|ودّيني|افتح).*(خطوه|سطر)/.test(n) && num.length,
      here: /(الخطوه دي|السطر ده|ده بيعمل|دي بتعمل|هنا بيحصل|اللي بيحصل دلوقتي|الخطوه الحاليه|انا فين)/.test(n),
      count: /(كام|عدد|كم |how many)/.test(n),
      why: /(ليه|ليش|لماذا|سبب|why|هدف|الهدف|اهداف|وظيف|دوره|دورها|شغلت|لزمت|لازمت|فايد|بيفيد|بتفيد|استخدام|بنستخدم|بيستخدم في|بتستخدم في|محتاجين|عشان ايه|علشان ايه)/.test(n),
      purpose: /(هدف|الهدف|اهداف|وظيف|دوره|دورها|شغلت|لزمت|لازمت|فايد|بيفيد|بتفيد|استخدام|بنستخدم|بيستخدم في|بتستخدم في|محتاجين|عشان ايه|علشان ايه)/.test(n),
      where: /(فين|امتي|انهي سطر|انهي خطوه|اي سطر|سطر كام|خطوه كام|اتعمل|بيتعمل|اتنده|where|when)/.test(n),
      value: /(قيمه|قيمته|قيمتها|بيساوي|يساوي|بكام|value|=)/.test(n),
      diff: /(الفرق|فرق|مقارنه|قارن|بالمقارنه| vs )/.test(n),
      what: /(يعني ايه|يعني اي|ايه هو|ايه هي|ما هو|ما هي|معني|تعريف|what is)/.test(n) || (/^\s*(ايه|اي|وايه)\s/.test(n) && n.trim().split(/\s+/).length <= 4),
      result: /(النتيجه|طلع ايه|بيطلع ايه|ظهر ايه|بيظهر ايه|شكل الشاشه|الصوره النهاييه|اتطبع|بيطبع ايه|الخرج|output)/.test(n) || (/(هيظهر|بيظهر|يظهر|ظاهر|هيطلع|بيطلع|هنشوف|بنشوف|هشوف|يتعرض|هيترسم|اترسم ايه)/.test(n) && /(شاشه|شباك|صوره|اخر|الاخر|نهايه|ايه)/.test(n)) || /(اخر البرنامج|في الاخر|نهايه البرنامج).*(ايه|شكل)|(ايه|شكل).*(اخر البرنامج|نهايه البرنامج)/.test(n),
      whose: /(بتاع مين|لمين|مين بتاع|يخص|تبع مين)/.test(n),
      num, n }; }
  function entities(q){
    const t = toks(q), E = {concepts: new Set(t.filter(x => x[0] === '§').map(x => x.slice(1))), vars: [], bufIds: [], vaoIds: []};
    const F = facts(); const n = norm(q);
    for (const name of F.vars.keys()) if (new RegExp('\\b' + name.toLowerCase() + '\\b').test(strip(q).toLowerCase())) E.vars.push(name);
    if (!E.vars.length) for (const id of strip(q).match(/[A-Za-z_][A-Za-z0-9_]{3,}/g) || []){ const a = tri(id.toLowerCase()); let best = null, bs = 0;
      for (const name of F.vars.keys()){ const b = tri(name.toLowerCase()); let k = 0; for (const g of a) if (b.has(g)) k++; const j = k / (a.size + b.size - k); if (j > bs){ bs = j; best = name; } }
      if (bs >= .5 && best.toLowerCase() !== id.toLowerCase()){ E.vars.push(best); E.fixedVar = [id, best]; } }
    (n.match(/(buffer|بافر|بفر|بوفر|صندوق)\s*(رقم\s*)?(\d+)/g) || []).forEach(m => E.bufIds.push(+m.match(/\d+/)[0]));
    (n.match(/vao\s*(رقم\s*)?(\d+)/g) || []).forEach(m => E.vaoIds.push(+m.match(/\d+/)[0]));
    E.method = (n.match(/(طريقه|method)\s*(رقم\s*)?(\d|الاولي|الاول|التانيه|التاني|الثانيه)/) || [])[3];
    return E; }

  // ---------- answer builders (each returns {html, target, conf} or null)
  const A = {};
  A.nav = (I) => { const n = I.num[0]; if (/سطر/.test(I.n)){ const k = ST.findIndex(s => s.ln === n); if (k < 0) return null; return {html: `السطر ${n}: ${C(stepText(ST[k]))}<br>أول مرة اتنفذ في الخطوة ${k + 1}.`, go: k, conf: 1}; }
    if (n < 1 || n > ST.length) return {html: `البرنامج ده فيه ${N(ST.length)} خطوة بس.`, conf: 1}; return {html: `رحت للخطوة ${n}: ${C(stepText(ST[n - 1]))}`, go: n - 1, conf: 1}; };
  A.here = () => { const s = ST[i]; const w = whyText(i);
    return {html: `<b>الخطوة ${i + 1} · سطر ${s.ln}:</b> ${C(stepText(s))}<br>${s.ex || ''}${(s.dy || []).length ? '<br>' + s.dy.slice(0, 2).join('<br>') : ''}${w ? `<br><b>ليه السطر ده موجود؟</b> ${esc(w)}` : ''}`, conf: 1, k: i}; };
  A.countBuf = (I) => { const F = facts(), B = Object.values(F.bufs); if (!B.length) return {html: 'البرنامج ده ماعملش ولا Buffer (مفيش <code>glGenBuffers</code>).', conf: .9};
    return {html: `فيه <b>${N(B.length)} Buffer</b> على الكارت:<ul>${B.map(b => `<li><b>${names.buf(b.id)}</b>: ${bufPurpose(b)}.${whoUses(b.id).length ? ` بيستخدمه ${whoUses(b.id).join(' و ')}.` : ''} ${chip(b.gen)}${b.up !== null ? chip(b.up) : ''}</li>`).join('')}</ul>` +
      (I.why ? `<b>ليه العدد ده؟</b> كل حاجة الكارت محتاج يقراها لازم تبقى في صندوق عنده. ${B.filter(b => b.t !== 'EBO').length > 1 ? 'كل شكل ليه أركانه في صندوق لوحده' : 'الأركان في صندوق'}${B.some(b => b.t === 'EBO') ? '، وترتيب الأركان (EBO) في صندوق تاني عشان مانكررش الأركان' : ''}.` : ''), target: ['buf', B[0].id], conf: 1}; };
  A.countVao = (I) => { const F = facts(), V = Object.values(F.vaos); if (!V.length) return {html: 'البرنامج ده مافيهوش VAO.', conf: .9};
    return {html: `فيه <b>${N(V.length)} VAO</b>:<ul>${V.map(v => `<li><b>${names.vao(v.id)}</b>: ${Object.entries(v.at).map(([l, a]) => `الخانة ${l} من Buffer ${a.buf}، ${a.size} رقم لكل ركن، stride ${a.stride}`).join('؛ ') || 'لسه مفيش خانات'}${v.ebo ? `، والـ EBO = Buffer ${v.ebo}` : ''}. اترسم بيه ${N(v.draws)} مرة.${(() => { const L = v.set.filter(k => ST[k].lap != null); return L.length ? ` <i>الوصف ده بيتكتب من جديد جوه اللوب (${N(L.length)} أمر في التشغيل)، واللي مكتوب هنا آخر وصف اتكتب فيه.</i>` : ''; })()} ${chip(v.gen)}</li>`).join('')}</ul>` +
      (I.why ? '<b>ليه؟</b> الـ VAO بيحفظ «شكل الركن» وأنهي صندوق، فبدل ما نوصف كل حاجة قبل كل رسمة، نربط VAO واحد بسطر واحد.' : ''), target: ['vao', V[0].id], conf: 1}; };
  A.countDraw = () => { const F = facts(); const per = F.draws.filter(d => d.lap === F.draws[0]?.lap);
    if (!F.draws.length) return {html: 'مفيش أوامر رسم في البرنامج ده.', conf: .9};
    return {html: `فيه <b>${N(per.length)} أمر رسم في كل لفة</b> (${N(F.draws.length)} في التشغيل كله):<ul>${per.map(d => `<li>${C(d.code)}${d.vao ? ` بـ VAO ${d.vao}` : ''} ${chip(d.k)}</li>`).join('')}</ul>`, conf: 1}; };
  A.countLaps = () => ({html: `اللوب اتلفّت ${N(facts().lapsSeen)} لفة في التشغيل اللي اتسجل، والبرنامج كله ${N(ST.length)} خطوة.`, conf: 1});
  A.countSteps = () => ({html: `البرنامج ده ${N(ST.length)} خطوة، و ${P.files.map(f => `${C(f.name)} ${N(f.lines.length)} سطر`).join(' و ')}.`, conf: 1});
  A.countUni = () => { const u = Object.entries(facts().uni); return u.length ? {html: `فيه ${N(u.length)} uniform: ${u.map(([n, v]) => `${C(n)} = ${esc(v)}`).join(' و ')} (آخر قيمة اتبعتت).`, conf: 1} : null; };
  A.value = (I, E) => { const F = facts(); const name = E.vars[0]; if (!name) return null; const h = F.vars.get(name) || [];
    let at = i; const ms = /خطوه\s*(\d+)/.exec(I.n); if (ms) at = Math.min(ST.length - 1, +ms[1] - 1);
    const cur = [...h].reverse().find(x => x.k <= at);
    return {html: `${C(name)} ${cur ? `في الخطوة ${at + 1} = <b dir="ltr">${esc(cur.v)}</b>` : `لسه ما اتحطلوش قيمة في الخطوة ${at + 1}`}.` +
      (h.length ? `<br>اتغيّر ${N(h.length)} مرة: ${h.slice(0, 6).map(x => `<span dir="ltr">${esc(String(x.v).slice(0, 40))}</span> ${chip(x.k)}`).join(' ← ')}${h.length > 6 ? ' …' : ''}` : ''), conf: 1, go: cur ? null : null}; };
  A.where = (I, E, q) => { let key = E.vars[0];
    const hits = [];
    if (key){ ST.forEach((s, k) => { if (new RegExp('\\b' + key + '\\b').test(stepText(s))) hits.push(k); }); }
    else { const r = search(q, {pid: P.id, kinds: ['step'], n: 12}); r.forEach(x => hits.push(x.d.k)); }
    if (!hits.length) return null; const byLine = new Map(); hits.forEach(k => { const L = ST[k].f + ':' + ST[k].ln; if (!byLine.has(L)) byLine.set(L, k); });
    if (!key){ const list = [...byLine.values()].slice(0, 4); return {html: `أقرب السطور لسؤالك:<ul>${list.map(k => `<li>${C(stepText(ST[k]))} ${chip(k)}<br><small>${ST[k].ex || ''}</small></li>`).join('')}</ul>`, conf: .7, go: list[0]}; }
    const list = [...byLine.values()].sort((a, b) => a - b).slice(0, 8);
    return {html: `${E.fixedVar ? `(قصدك ${C(E.fixedVar[1])}؟) ` : ''}${C(key)} بيظهر في ${N(byLine.size)} سطر (أول مرة في الخطوة ${hits[0] + 1}):<ul>${list.map(k => `<li>${C(stepText(ST[k]))} ${chip(k)}</li>`).join('')}</ul>`, conf: 1, go: list[0]}; };
  A.what = (I, E, q) => { const qt = new Set(toks(q).filter(t => t[0] !== '§')); const ids = (strip(q).match(/gl[A-Za-z0-9_]{3,}/g) || []).map(x => x.toLowerCase()); const r = search(q, {kinds: ['gloss'], n: 5}).find(x => ids.length ? ids.some(id => toks(x.d.title).includes(id)) : toks(x.d.title).some(t => qt.has(t))); const s = search(q, {pid: P.id, kinds: ['step', 'line'], n: 6}).find(x => [...qt].some(t => x.d.tf.has(t)));
    if (!r && !s) return null; return {html: (r ? `<b>${esc(r.d.title)}:</b> ${r.d.text}` : '') + (s ? `<br>في البرنامج ده: ${C(s.d.code)} ${anyChip(s.d)}<br>${s.d.ex || ''}` : ''), conf: r ? Math.min(1, r.s / 4) : .5}; };
  A.result = () => { const S = PSTORY[P.id] || {}; const res = (/النتيجة الحقيقية:<\/b>([^<]*)/.exec(S.goal || '') || [])[1]; const fr = P.frames.length - 1;
    return {html: `${res ? `<b>النتيجة الحقيقية:</b> ${res}<br>` : ''}${P.term && P.term.length ? `<b>اللي اتطبع:</b><pre class="agterm">${esc(P.term.join('\n'))}</pre>` : ''}${fr >= 0 ? `<img class="agimg" src="${P.frames[fr]}" alt="آخر صورة حقيقية من الكارت">` : ''}`, conf: 1}; };
  A.loop = () => { const S = PSTORY[P.id] || {}; const k = ST.findIndex(s => /^\s*(while|for)\b/.test(stepText(s))); if (k < 0 && !S.loop) return null; const F = facts();
    return {html: `${S.loop || (P.frames.length ? STATIC_LOOP : 'اللوب بتكرر نفس السطور لحد ما الشرط يبقى false.')}${k >= 0 ? `<br>اللوب في ${C(stepText(ST[k]))} ${chip(k)}` : ''}${F.draws.length ? `<br>في التشغيل اللي اتسجل اتلفّت ${N(F.lapsSeen)} لفة، وفي كل لفة ${N(F.draws.filter(d => d.lap === F.draws[0].lap).length)} أمر رسم.` : ''}`, conf: 1}; };
  const GKEY = {vao: 'VAO', buffer: 'Buffer', ebo: 'EBO (Index Buffer)', shader: 'Shader', program: 'Program', uniform: 'Uniform', attrib: 'Attribute', window: 'Context', loop: 'Render loop', draw: 'Draw call', bind: 'Bind', gpu: 'GPU', cpu: 'CPU', ram: 'Stack', swap: 'Double buffering', clear: 'glClearColor'};
  A.concept = (E, I, q) => { const order = ['vao', 'ebo', 'buffer', 'attrib', 'uniform', 'shader', 'program', 'draw', 'bind', 'loop', 'swap', 'clear', 'window', 'gpu', 'cpu', 'ram'];
    const c = order.find(x => E.concepts.has(x)); if (!c || !G[GKEY[c]]) return null; const g = G[GKEY[c]];
    const ids = (strip(q || '').match(/gl[A-Za-z0-9_]{3,}/g) || []).map(x => x.toLowerCase()); if (ids.length && !ids.includes(GKEY[c].toLowerCase())) return null;
    let here = '';
    if (c === 'vao' && Object.keys(facts().vaos).length){ const r = A.countVao({why: false}); here = r.html; }
    else if ((c === 'buffer' || c === 'ebo') && Object.keys(facts().bufs).length){ const r = A.countBuf({why: false}); here = r.html; }
    else if (c === 'loop'){ const r = A.loop(); here = r ? r.html : ''; }
    else { const s0 = DOCS.find(d => d.pid === P.id && d.kind === 'step' && d.first && toks(d.code).includes('§' + c)) || DOCS.find(d => d.pid === P.id && d.kind === 'step' && d.first && d.tf.has('§' + c)); if (s0) here = `أول مرة في البرنامج ده: ${C(s0.code)} ${chip(s0.k)}<br>${s0.ex || ''}`; }
    return {html: `<b>${esc(GKEY[c])}${I.purpose ? ': هدفه إيه؟' : ''}</b><br>${g[0]}<br><span class="eg">مثال من الحياة: ${g[1]}</span>${here ? `<div class="agpart"><b>في البرنامج ده:</b> ${here}</div>` : ''}`, target: c === 'vao' && Object.keys(facts().vaos)[0] ? ['vao', Object.keys(facts().vaos)[0]] : (c === 'buffer' && Object.keys(facts().bufs)[0] ? ['buf', Object.keys(facts().bufs)[0]] : null), conf: 1}; };
  const noteAbove = k => { const s0 = ST[k], L = P.files[s0.f].lines; for (let n = s0.ln - 2; n >= Math.max(0, s0.ln - 5); n--){ const m = /\/\/\s*-*\s*(.+)/.exec(L[n] || ''); if (m) return m[1]; } return ''; };
  A.oneVao = (id, I) => { const v = facts().vaos[id]; if (!v) return {html: `مفيش VAO رقم ${id} في البرنامج ده (فيه ${N(Object.keys(facts().vaos).length)} بس).`, conf: 1};
    const nt = noteAbove(v.gen), inLoop = v.set.filter(k => ST[k].lap != null);
    const users = facts().draws.filter(d => +d.vao === +id);
    return {html: `<b>${names.vao(id)}</b> اتعمل في ${chip(v.gen)}${nt ? `، والتعليق اللي فوقه في الكود: ${C(nt)}` : ''}.<br>${ST[v.gen].ex || ''}<br>الخانات: ${Object.entries(v.at).map(([l, a]) => `الخانة ${l} من Buffer ${a.buf}، ${a.size} رقم لكل ركن، stride ${a.stride}`).join('؛ ') || 'مفيش'}${v.ebo ? `، والـ EBO = Buffer ${v.ebo}` : ''}.` +
      `<br>اترسم بيه ${N(users.length)} مرة: ${users.slice(0, 4).map(d => `${C(d.code)} ${chip(d.k)}`).join(' ')}` + (inLoop.length ? `<br><b>مختلف عن الباقيين:</b> الوصف بتاعه بيتكتب من جديد جوه اللوب قبل كل رسمة (${N(inLoop.length)} أمر في التشغيل)، فنفس الـ VAO بيتكتب فيه المربع وبعدين المثلث.` : `<br>الوصف بتاعه اتكتب مرة واحدة قبل اللوب، وجوه اللوب بيتربط بس.`), target: ['vao', id], conf: 1}; };
  A.oneBuf = (id) => { const b = facts().bufs[id]; if (!b) return {html: `مفيش Buffer رقم ${id} في البرنامج ده.`, conf: 1}; const nt = noteAbove(b.gen);
    return {html: `<b>${names.buf(id)}</b>: ${bufPurpose(b)}. اتعمل في ${chip(b.gen)}${b.up !== null ? ` واتملا في ${chip(b.up)}` : ''}${nt ? ` (التعليق: ${C(nt)})` : ''}.${whoUses(id).length ? `<br>بيستخدمه ${whoUses(id).join(' و ')}.` : ''}${b.binds.length ? `<br>اتربط ${N(b.binds.length)} مرة: ${b.binds.slice(0, 5).map(k => chip(k)).join(' ')}` : ''}`, target: ['buf', id], conf: 1}; };
  A.whose = () => { if (typeof linkMap !== 'function') return null; let h = ''; try { h = linkMap(); } catch (e){ return null; } return h ? {html: h.replace('<details class="brk">', '<details class="brk" open>'), conf: 1} : null; };
  A.diff = (I, E, q) => { // two halves of the code split by comments, or two entities
    const L = P.files[0].lines; const cm = []; L.forEach((l, k) => { const m = /\/\/\s*-*\s*(.*method\s*\d.*|.*half.*)/i.exec(l); if (m) cm.push(k); });
    if (/(طريق|method)/.test(I.n) && cm.length >= 2){
      const sec = cm.map((c, j) => { const end = cm.slice(j + 1).find(x => x > c) || L.length; const body = L.slice(c + 1, end).map(x => x.trim()).filter(x => /^gl\w+\(/.test(x));
        const calls = body.filter(x => /glBind|glVertexAttribPointer|glEnableVertexAttribArray/.test(x)).length;
        return `<li><b>${esc(L[c].replace(/^\s*\/\/\s*-*\s*/, ''))}</b> (سطر ${c + 1}): ${N(body.length)} أمر gl، منهم ${N(calls)} ربط أو وصف للخانات.</li>`; });
      return {html: `الكود فيه ${N(cm.length)} أجزاء متعلّم عليها بتعليقات:<ul>${sec.join('')}</ul>الطريقة اللي فيها VAO لكل شكل بتسجّل الوصف مرة واحدة قبل اللوب، فجوه اللوب ربط واحد قبل كل رسمة. والطريقة اللي فيها VAO واحد لازم توصف الشكل من جديد قبل كل رسمة.${A.whose() ? '<br>وتفاصيل مين بتاع مين:' + A.whose().html : ''}`, conf: 1}; }
    const parts = strip(q).split(/\s+(?:و|ولا|vs|مقابل|او|أو)\s+|،|,/).map(x => x.trim()).filter(Boolean);
    const terms = parts.map(x => toks(x).filter(t => t[0] !== '§' && !/^(فرق|الفرق|بين|ايه|اي)$/.test(t)).pop()).filter(Boolean).slice(-2);
    if (terms.length < 2) return null;
    const pick = t => { const st = DOCS.filter(d => d.pid === P.id && (d.kind === 'step' || d.kind === 'line') && d.first && d.tf.has(t)).sort((a, b) => (b.code.toLowerCase().includes(t) ? 1 : 0) - (a.code.toLowerCase().includes(t) ? 1 : 0) || (a.kind === 'line' ? -1 : 1) - (b.kind === 'line' ? -1 : 1))[0];
      const gl = DOCS.find(d => d.kind === 'gloss' && toks(d.title).includes(t)); return {t, st, gl}; };
    const L2 = terms.map(pick); if (!L2.some(x => x.st || x.gl)) return null;
    return {html: `<b>المقارنة:</b><ul>${L2.map(x => `<li><b>${esc(x.t)}</b>: ${x.st ? `${C(x.st.code)} ${anyChip(x.st)}<br>${x.st.ex || ''}` : ''}${x.gl ? `${x.st ? '<br>' : ''}${x.gl.text}` : ''}${!x.st && !x.gl ? 'مش موجود في البرنامج ده.' : ''}</li>`).join('')}</ul>`, conf: .8}; };

  // ---------- the router
  let lastQ = null;
  function md(t){ return esc(t).replace(/`([^`]+)`/g, '<code dir="ltr">$1</code>').replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>')
      .replace(/^\s*[-•*]\s+(.*)$/gm, '<li>$1</li>').replace(/(<li>.*<\/li>\n?)+/g, m => '<ul>' + m.replace(/\n/g, '') + '</ul>')
      .replace(/خطوة\s+(\d+)((?:\s*(?:و|،|,)\s*\d+)*)/g, (m, n, more) => { const ns = [n, ...(more.match(/\d+/g) || [])].map(Number); return ns.every(x => x >= 1 && x <= ST.length) ? ns.map(x => chip(x - 1)).join(' ') : m; }).replace(/\n/g, '<br>'); }
  function learnFromClaude(q, text){ const k = [...new Set(toks(q).filter(t => t[0] !== '§'))]; if (!k.length) return 0;
    const L = lsGet(CL_KEY, []).filter(x => !(x.pid === P.id && x.q.join(' ') === k.join(' '))); L.push({pid: P.id, q: k, w: Object.fromEntries([...qweights(q, true)].filter(([t, v]) => v >= .3)), raw: q, text, t: Date.now()}); lsSet(CL_KEY, L.slice(-200));
    const steps = [...new Set([...text.matchAll(/خطوة\s+(\d+)((?:\s*(?:و|،|,)\s*\d+)*)/g)].flatMap(m => [m[1], ...(m[2].match(/\d+/g) || [])]).map(x => +x - 1).filter(n => n >= 0 && n < ST.length))]; let n = 0;
    for (const w of k.filter(t => /[\u0621-\u064A]/.test(t) && !DF.has(t) || /[\u0621-\u064A]/.test(t))) for (const sk of steps.slice(0, 3)) for (const c of toks(stepText(ST[sk])).filter(c => c[0] !== '§' && c.length > 3)){
      LEARN[w] = LEARN[w] || {}; LEARN[w][c] = Math.min(.8, (LEARN[w][c] || 0) + .25); n++; }
    lsSet(LA_KEY, LEARN); if (steps.length) train(q, steps.slice(0, 4).map((k2, j) => ['s:' + k2, j ? .5 : 1]), [], .5, 'claude'); return steps.length; }
  // lessons the local brain reads before answering: Claude's answers/corrections that match the question
  const FL_KEY = 'benchHelperFreeLessons';
  function saveFreeLesson(q, text){ const k = [...new Set(toks(q).filter(t => t[0] !== '§'))]; if (!k.length) return; const L = lsGet(FL_KEY, []).filter(x => x.raw !== q); L.push({q: k, raw: q, text, t: Date.now()}); lsSet(FL_KEY, L.slice(-150)); }
  function lessons(q, free, n = 2){ const k = [...new Set(toks(q).filter(t => t[0] !== '§'))]; if (!k.length) return [];
    const qw = qweights(q, true); const sc = [];
    for (const x of free ? lsGet(FL_KEY, []) : lsGet(CL_KEY, []).filter(x => x.pid === P.id)){ let j;
      if (x.w){ let mn = 0, mx = 0; const keys = new Set([...Object.keys(x.w), ...qw.keys()]); for (const t of keys){ const a = x.w[t] || 0, b = qw.get(t) || 0; mn += Math.min(a, b); mx += Math.max(a, b); } j = mx ? mn / mx : 0; }
      else { const inter = x.q.filter(t => k.includes(t)).length; j = inter / new Set([...x.q, ...k]).size; }
      if (j >= .2) sc.push([j, x]); }
    return sc.sort((a, b) => b[0] - a[0]).slice(0, n).map(([j, x]) => ({q: x.raw || x.q.join(' '), a: x.text, j})); }
  const lessonCount = () => ({bench: lsGet(CL_KEY, []).length, free: lsGet(FL_KEY, []).length});
  function recallClaude(q){ const k = [...new Set(toks(q).filter(t => t[0] !== '§'))]; if (!k.length) return null; let best = null, bs = 0;
    const qw = qweights(q, true);
    for (const x of lsGet(CL_KEY, [])){ if (x.pid !== P.id) continue; let j;
      if (x.w){ let mn = 0, mx = 0; const keys = new Set([...Object.keys(x.w), ...qw.keys()]); for (const t of keys){ const a = x.w[t] || 0, b = qw.get(t) || 0; mn += Math.min(a, b); mx += Math.max(a, b); } j = mx ? mn / mx : 0; }
      else { const inter = x.q.filter(t => k.includes(t)).length; j = inter / new Set([...x.q, ...k]).size; }
      if (j > bs){ bs = j; best = x; } }
    return bs >= .45 ? best : null; }
  // ---------- what the helper learned from you (thumbs up / picking the right answer), kept in this browser
  const MEM_KEY = 'benchHelperLearn';
  const memLoad = () => { try { return JSON.parse(localStorage.getItem(MEM_KEY) || '[]'); } catch (e){ return []; } };
  const memSave = m => { try { localStorage.setItem(MEM_KEY, JSON.stringify(m.slice(-300))); } catch (e){} };
  const qkey = q => [...new Set(toks(q).filter(t => t[0] !== '§'))];
  function remember(q, pid, ref, good){ const m = memLoad().filter(x => !(x.pid === pid && x.q.join(' ') === qkey(q).join(' ') && x.ref === ref)); m.push({q: qkey(q), pid, ref, good: !!good, t: Date.now()}); memSave(m); }
  function recall(q){ const k = qkey(q); if (!k.length) return null; let best = null, bs = 0;
    for (const x of memLoad()){ if (x.pid !== P.id || !x.good) continue; const inter = x.q.filter(t => k.includes(t)).length; const j = inter / (new Set([...x.q, ...k]).size); if (j > bs){ bs = j; best = x; } }
    return bs >= .6 ? best : null; }
  function refDoc(ref){ const [kind, a, b] = ref.split(':'); return kind === 's' ? DOCS.find(d => d.pid === P.id && d.kind === 'step' && d.k === +a) : DOCS.find(d => d.pid === P.id && d.kind === 'line' && d.f === +a && d.ln === +b); }
  function docForLine(ln){ return DOCS.find(d => d.pid === P.id && d.kind === 'step' && d.first && ST[d.k].ln === ln && ST[d.k].f === 0) || DOCS.find(d => d.pid === P.id && d.kind === 'line' && d.ln === ln); }
  function alternatives(q, shown){ return search(q, {pid: P.id, kinds: ['step', 'line'], n: 18}).filter(x => !/^\/\//.test(x.d.code)).filter(x => x.d.pid === P.id).map(x => x.d)
      .filter((d, n, a) => a.findIndex(e => e.code === d.code) === n).filter(d => !shown.includes(d.kind === 'step' ? 's:' + d.k : 'l:' + d.f + ':' + d.ln)).slice(0, 6); }
  function answer(q){
    q = q.trim(); if (!q) return null;
    const TR = []; const qw = qweights(q);
    const ar = {count: 'عدد', why: 'سبب', purpose: 'هدف', where: 'مكان', value: 'قيمة', diff: 'مقارنة', what: 'تعريف', result: 'النتيجة', whose: 'مين بتاع مين', nav: 'روح لـ', here: 'الخطوة الحالية'};
    const think = (src) => { const I0 = intent(q); const kinds = Object.keys(ar).filter(x => I0[x]).map(x => ar[x]);
      const conc = [...qw.keys()].filter(t => t[0] === '§').map(t => t.slice(1)); const lr = toks(q).filter(t => LEARN[t]);
      return `<details class="agthink"><summary>🧠 فكّرت إزاي؟</summary><ul><li>نوع السؤال: ${kinds.length ? kinds.join(' + ') : 'مش واضح، فدوّرت بالمعنى'}</li>${conc.length ? `<li>فهمت إنه عن: ${conc.map(c => C(c)).join(' ')}</li>` : ''}${qw.fixed && qw.fixed.length ? `<li>صحّحت: ${qw.fixed.map(([a, b]) => `«${esc(a)}» ← «${esc(b)}»`).join('، ')}</li>` : ''}${lr.length ? `<li>كلمات اتعلّمتها من Claude: ${lr.map(esc).join('، ')}</li>` : ''}<li>الإجابة جت من: ${src}</li>${TR.map(x => `<li>${x}</li>`).join('')}</ul></details>`; };
    const mem = recall(q);
    if (mem){ const d = refDoc(mem.ref); if (d){ lastQ = q; return {html: `<div class="agpart"><span class="aglearn">اتعلّمتها منك قبل كده</span><br>${C(d.code)} ${anyChip(d)}<br>${d.ex || ''}</div>` + think('اختيارك قبل كده (👎 ثم اخترت)'), go: d.kind === 'step' ? d.k : null, conf: 1, low: false, learned: true}; } }
    { const pr = predict(q, P.id); if (pr.length && pr[0][1] >= 2.2 && (pr.length < 2 || pr[0][1] - pr[1][1] >= .8) && /^(s|l):/.test(pr[0][0])){ const d = byId(P.id, pr[0][0]);
        if (d){ TR.push(`النموذج الخطي واثق: ${pr[0][1].toFixed(2)} (التاني ${pr[1] ? pr[1][1].toFixed(2) : '—'})`); lastQ = q; return {html: `<div class="agpart"><span class="aglearn">🧠 اتعلّمتها من تصحيحاتك (النموذج الخطي)</span><br>${C(d.code)} ${anyChip(d)}<br>${d.ex || ''}</div>` + think('النموذج الخطي اللي بيتدرب معاك'), go: d.kind === 'step' ? d.k : null, conf: 1, low: false, learned: true}; } } }
    const cm = recallClaude(q);
    if (cm){ lastQ = q; return {html: `<div class="agpart"><span class="aglearn">🧠 اتعلّمتها من Claude قبل كده (من غير نت دلوقتي)</span><br>${md(cm.text)}</div>` + think('إجابة Claude المحفوظة لسؤال شبهه: «' + esc(cm.raw) + '»'), conf: 1, low: false, learned: true}; }
    { const kq = [...qw.keys()].filter(t => t[0] !== '§' && (t.length >= 2 || /^\d$/.test(t)) && qw.get(t) >= .85);
      const kb = search(q, {pid: P.id, kinds: ['kb'], n: 1})[0];
      if (kb && kb.d.pid === P.id){ const cov = kq.length ? kq.filter(t => kb.d.qset.has(t)).length / kq.length : 0; TR.push(`أقرب سؤال محفوظ: «${esc(kb.d.title)}» (تغطية ${Math.round(cov * 100)}%)`);
        if (kq.length >= 2 && cov >= .75 && kb.s >= 4){ lastQ = q; const e = AG_KB[kb.d.n]; return {html: `<div class="agpart"><span class="aglearn">🧠 من الشرح اللي Claude جهّزه للبرنامج ده</span><br>${md(e.a)}</div>` + think('الأسئلة المحفوظة'), conf: 1, low: false}; } } }
    if (/^(طب|طيب|و)\s*\S+(\s*\S+)?\s*[؟?]?$/.test(q.trim()) && lastQ){ const nq = norm(q);
      if (/مثلث|triangle/.test(nq)) q = lastQ.replace(/square/g, 'triangle').replace(/Square/g, 'Triangle').replace(/مربع/g, 'مثلث');
      else if (/مربع|square/.test(nq)) q = lastQ.replace(/triangle/g, 'square').replace(/Triangle/g, 'Square').replace(/مثلث/g, 'مربع');
      else q = lastQ + ' ' + q.replace(/^(طب|طيب)\s*/, '');
      if (q === lastQ) q = lastQ + ' ' + nq.replace(/^(طب|طيب)\s*و?/, ''); }
    const I = intent(q), E = entities(q), F = facts(); const out = [];
    const has = c => E.concepts.has(c);
    if (I.nav) out.push(A.nav(I));
    if (!I.nav && !I.count && E.vaoIds.length) E.vaoIds.slice(0, 2).forEach(id => out.push(A.oneVao(id, I)));
    if (!I.nav && !I.count && E.bufIds.length) E.bufIds.slice(0, 2).forEach(id => out.push(A.oneBuf(id)));
    if (I.here) out.push(A.here());
    if (I.result) out.push(A.result());
    if (I.whose) out.push(A.whose());
    if (I.diff) out.push(A.diff(I, E, q));
    if (I.why && has('loop') && E.concepts.size === 1 && !I.count) out.push(A.loop());
    if (I.count){
      if (has('vao')) out.push(A.countVao(I));
      else if (has('buffer') || has('ebo')) out.push(A.countBuf(I));
      else if (has('draw')) out.push(A.countDraw());
      else if (has('loop')) out.push(A.countLaps());
      else if (has('uniform')) out.push(A.countUni());
      else if (/(خطو|سطر)/.test(I.n)) out.push(A.countSteps());
    }
    if (!out.filter(Boolean).length && E.vars.length && (I.value || I.count)) out.push(A.value(I, E));
    if (!out.filter(Boolean).length && (I.purpose || I.what) && !I.count){ const cg = A.concept(E, I, q); if (cg) out.push(cg); }
    if (!out.filter(Boolean).length && I.why && (has('buffer') || has('ebo')) && Object.keys(F.bufs).length) out.push(A.countBuf(Object.assign({}, I, {why: true})));
    if (!out.filter(Boolean).length && I.why && has('vao') && Object.keys(F.vaos).length) out.push(A.countVao(Object.assign({}, I, {why: true})));
    if (!out.filter(Boolean).length && I.where) out.push(A.where(I, E, q));
    if (!out.filter(Boolean).length && I.what) out.push(A.what(I, E, q));
    if (!out.filter(Boolean).length && E.vars.length) out.push(A.value(I, E), A.where(I, E, q));
    let res = out.filter(Boolean);
    if (!res.length){ const kb = search(q, {pid: P.id, kinds: ['kb'], n: 1})[0]; const kq = [...qw.keys()].filter(t => t[0] !== '§' && qw.get(t) >= .85);
      const cov = kb && kq.length ? kq.filter(t => kb.d.qset.has(t)).length / kq.length : 0;
      if (kb && kb.d.pid === P.id && cov >= .6 && kb.s >= 3){ lastQ = q; return {html: `<div class="agpart"><span class="aglearn">🧠 من الشرح اللي Claude جهّزه للبرنامج ده</span><br>${md(AG_KB[kb.d.n].a)}</div>` + think('الأسئلة المحفوظة (أقرب سؤال: «' + esc(kb.d.title) + '»)'), conf: 1, low: false}; } }
    // retrieval: always add the best evidence; it is the answer when no rule fired
    const R = search(q, {n: 6, kinds: ['step', 'line', 'gloss', 'goal', 'loop']}); const top = R.filter(x => x.d.kind === 'step' && x.d.pid === P.id).slice(0, 3);
    if (!res.length){
      const GEN = new Set(['برنامج', 'كود', 'سطر', 'خطوه', 'علاق', 'علاقه', 'بيعمل', 'بتعمل', 'عمل', 'فايد', 'فايده', 'program']);
      const own = DOCS.filter(d => d.pid === P.id);
      const miss = [...new Set(toks(q).filter(t => t[0] !== '§' && t.length >= 3 && !/^\d+$/.test(t) && !GEN.has(t) && !own.some(d => d.tf.has(t) || (CMAP.get(t) || []).some(x => d.tf.has('§' + x)))))];
      const content = [...new Set(toks(q).filter(t => t[0] !== '§' && t.length >= 3 && !/^\d+$/.test(t) && !GEN.has(t)))];
      if (miss.length && miss.length === content.length){ const other = search(miss.join(' '), {n: 4}).filter(x => x.d.pid !== P.id);
        const og = other.find(x => x.d.kind === 'gloss'), os = other.filter(x => x.d.kind === 'step' || x.d.kind === 'line').slice(0, 2);
        const words = strip(q).split(/[^A-Za-z0-9_\u0621-\u064A]+/).filter(w => w && miss.includes(stem(norm(w).replace(/[^a-z0-9_\u0621-\u064A]/g, '')))); return {html: `البرنامج ده مافيهوش «${esc((words.length ? words : miss).join(' '))}».${og ? `<br><b>${esc(og.d.title)}:</b> ${og.d.text}` : ''}${os.length ? `<br>موجود في: ${os.map(x => { const pp = PROGS.find(y => y.id === x.d.pid); return `<b>${esc(pp.title)}</b> ${C(x.d.code)} ${anyChip(x.d)}`; }).join('<br>')}` : ''}`, conf: .8, low: !og && !os.length}; }
      if (!R.length || R[0].s < 1.2) return {html: `مش لاقي حاجة واضحة عن ده في البنش. جرّب تكتب اسم من الكود (زي ${C(Object.keys(F.bufs).length ? facts().bufs[Object.keys(F.bufs)[0]].v || 'glGenBuffers' : 'main')}) أو كلمة زي «Buffer» أو «VAO» أو «اللوب».`, conf: 0, low: true};
      const b = R[0].d;
      if (b.kind === 'line' && b.pid === P.id) res.push({html: `${C(b.code)} ${lchip(b)}<br>${b.ex || ''}`, conf: Math.min(1, R[0].s / 6)});
      else if (b.kind === 'step' && b.pid === P.id){ const w = I.why ? whyText(b.k) : ''; res.push({html: `${C(b.code)} ${chip(b.k)}<br>${b.ex || ''}${w ? `<br><b>ليه؟</b> ${esc(w)}` : ''}`, go: null, conf: Math.min(1, R[0].s / 6)}); }
      else if (b.kind === 'step' || b.kind === 'line'){ const p = PROGS.find(x => x.id === b.pid); res.push({html: `لقيته في برنامج تاني: <b>${esc(p.title)}</b> (${DAYN_[p.day] || 'اليوم ' + p.day}):<br>${C(b.code)} ${anyChip(b)}<br>${b.ex || ''}`, conf: Math.min(1, R[0].s / 6)}); }
      else res.push({html: `<b>${esc(b.title)}:</b> ${b.text}`, conf: Math.min(1, R[0].s / 6)});
    }
    const ev = (I.result || I.nav || I.here || I.whose || !R.length || R[0].s < 2) ? [] : top.filter(x => !res.some(r => (r.html || '').includes(`data-k="${x.d.k}"`))).slice(0, 2);
    if (!I.nav && !I.here) lastQ = q;
    return {html: res.map(r => `<div class="agpart">${r.html}</div>`).join('') + (ev.length ? `<div class="agsee"><span>شوف كمان:</span> ${ev.map(x => `${chip(x.d.k)} <small>${esc(x.d.title)}</small>`).join(' ')}</div>` : '') + think(out.filter(Boolean).length ? 'حساب من التشغيل الحقيقي (الصناديق والـ VAOs والمتغيرات)' : 'البحث في الخطوات والشرح بالمعنى'),
      go: (res.find(r => r.go != null) || {}).go, target: (res.find(r => r.target) || {}).target, conf: Math.max(...res.map(r => r.conf || 0)), low: false}; }
  const DAYN_ = {8: 'الأسبوع 3 · اليوم 1', 9: 'الأسبوع 3 · اليوم 2'};
  function suggestions(){ const F = facts(), S = [];
    if (Object.keys(F.bufs).length) S.push(`ليه فيه ${N(Object.keys(F.bufs).length)} Buffer؟`);
    if (Object.keys(F.vaos).length > 1) S.push('كام VAO ومين بيستخدم كل واحد؟');
    if (P.files[0].lines.some(l => /method\s*\d/i.test(l))) S.push('إيه الفرق بين الطريقتين؟');
    const v = (Object.values(F.bufs)[0] || {}).v || [...F.vars.keys()].find(n => /vao|count|speed|result|sum|total/i.test(n)) || [...F.vars.keys()].find(n => n.length > 2);
    if (v) S.push(`${v} اتغيّر فين؟`);
    if (F.draws.length) S.push('كام أمر رسم في اللفة؟');
    S.push('الخطوة دي بتعمل إيه؟', 'النتيجة طلعت إيه؟');
    return S.slice(0, 6); }
  function context(q, o){ const sh = !!(o && o.short), big = !!(o && o.big); const F = facts(); const R = search(q, {pid: P.id, kinds: ['step', 'line'], n: big ? 24 : 10}).map(x => x.d).filter((d, n, a) => a.findIndex(e => e.code === d.code) === n).slice(0, big ? 20 : sh ? 4 : 8);
    const L = [];
    L.push(`البرنامج: ${P.title} — ${P.desc}`);
    L.push(`الملفات: ${P.files.map(f => f.name + ' (' + f.lines.length + ' سطر)').join('، ')}. عدد الخطوات: ${ST.length}.${sh && !(o && o.here) ? '' : ` الخطوة اللي المستخدم واقف عليها: ${i + 1} (سطر ${ST[i].ln}: ${stepText(ST[i])}).`}`);
    if (Object.keys(F.bufs).length) L.push('الـ Buffers في التشغيل الحقيقي: ' + Object.values(F.bufs).map(b => `Buffer ${b.id} = ${b.v || '?'} (${b.t || ''}، ${b.bytes || 0} بايت${b.src ? '، فيه ' + b.src : ''}، اتعمل في خطوة ${b.gen + 1})`).join('؛ '));
    if (Object.keys(F.vaos).length) L.push('الـ VAOs: ' + Object.values(F.vaos).map(v => `VAO ${v.id} = ${v.v || '?'} (اتعمل في خطوة ${v.gen + 1}، اترسم بيه ${v.draws} مرة${v.set.some(k => ST[k].lap != null) ? '، وصفه بيتكتب من جديد جوه اللوب' : ''})`).join('؛ '));
    if (F.draws.length) L.push('أوامر الرسم: ' + F.draws.slice(0, sh ? 4 : 8).map(d => `خطوة ${d.k + 1}: ${d.code}${d.vao ? ' (VAO ' + d.vao + ')' : ''}`).join('؛ '));
    const S = PSTORY[P.id]; if (S && S.goal) L.push('الهدف والنتيجة: ' + strip(S.goal).replace(/\s+/g, ' ').slice(0, sh ? 720 : 900));
    if (!sh && P.term && P.term.length) L.push('اللي اتطبع: ' + P.term.slice(0, 8).join(' | '));
    L.push('أقرب السطور للسؤال (من البنش):');
    R.forEach(d => L.push(`- ${d.kind === 'step' ? 'خطوة ' + (d.k + 1) + '، ' : ''}سطر ${d.kind === 'step' ? ST[d.k].ln : d.ln}: ${d.code} — ${strip(d.ex || '').slice(0, sh ? 90 : 220)}${d.kind === 'step' ? '' : ' (سطر مش بيتنفذ لوحده)'}`));
    // a model that can read a lot gets the whole program, with line numbers, and what was printed
    if (big){ if (P.term && P.term.length) L.push('اللي اتطبع: ' + P.term.slice(0, 40).join(' | '));
      L.push('الكود كامل (رقم السطر: السطر):'); P.files.forEach(f => L.push('--- ' + f.name + '\n' + f.lines.map((l, k) => (k + 1) + ': ' + l).join('\n'))); }
    return L.join('\n') + (window.__agDayAll ? '\n\n' + dayBlock(q, sh && !big) : ''); }
  // «📅 اليوم كله»: a short card for every program of the open day + the closest lines from the other programs (no step numbers: those belong to the open program)
  function dayBlock(q, sh){ const ps = PROGS.filter(p => p.day === P.day);
    const L = [`وضع «اليوم كله»: البرامج اللي في نفس اليوم (عدد ${ps.length}). المستخدم ممكن يسأل عن أي واحد فيهم أو عن العلاقة بينهم:`];
    ps.forEach(p => { const tm = (p.term || []).filter(x => x && x[0] !== '\u0001').slice(0, sh ? 2 : 4).join(' / ');
      L.push(`• «${p.title}»${p.id === P.id ? ' (ده المفتوح)' : ''}: ${p.desc}${tm ? ' | اتطبع: ' + tm.slice(0, sh ? 170 : 320) : ''}`); });
    const ids = new Set(ps.map(p => p.id).filter(id => id !== P.id));
    const R = search(q, {kinds: ['step', 'line'], n: 40}).map(x => x.d).filter(d => ids.has(d.pid)).filter((d, n, a) => a.findIndex(e => e.code === d.code && e.pid === d.pid) === n).slice(0, sh ? 4 : 8);
    if (R.length){ L.push('أقرب السطور للسؤال في برامج اليوم التانية (اكتب اسم البرنامج لما تذكرها، ومن غير رقم خطوة):');
      R.forEach(d => { const p = PROGS.find(x => x.id === d.pid); const f = p.files[d.kind === 'step' ? p.steps[d.k].f : d.f]; const ln = d.kind === 'step' ? p.steps[d.k].ln : d.ln;
        L.push(`- [${p.title}] ${f ? f.name + ' ' : ''}سطر ${ln}: ${d.code} — ${strip(d.ex || '').slice(0, sh ? 90 : 200)}`); }); }
    return L.join('\n'); }
  return {lessons, saveFreeLesson, lessonCount, build, answer, suggestions, search, norm, toks, facts, qweights, context, learnFromClaude, train, predict, modelStats, exportModel, importModel, resetModel, remember, alternatives, docForLine, refDoc, forget(){ memSave([]); }, chipFor: d => anyChip(d), reset(){ lastQ = null; }};
})();

// ---------- the robot (built from simple shapes)
const robot = (() => {
  const g = new T.Group(); const W = M(0xeef1f6, {roughness:.35, metalness:.05}), Wd = M(0xc9ced8, {roughness:.4});
  const glow = new T.MeshBasicMaterial({color:0x5ee6ff}), visorM = new T.MeshStandardMaterial({color:0x0e2233, roughness:.25, metalness:.3});
  const body = new T.Mesh(new T.SphereGeometry(.62, 32, 24), W); body.scale.set(1, 1.18, .92); body.position.y = .7; g.add(body);
  const belt = new T.Mesh(new T.TorusGeometry(.6, .015, 6, 40), Wd); belt.rotation.x = Math.PI / 2; belt.position.y = .55; belt.scale.set(1, .92, 1); g.add(belt);
  const neck = new T.Mesh(new T.CylinderGeometry(.16, .2, .18, 20), Wd); neck.position.y = 1.45; g.add(neck);
  const head = new T.Group(); head.position.y = 1.95; g.add(head);
  const skull = new T.Mesh(new T.SphereGeometry(.62, 32, 24), W); skull.scale.set(1.18, .82, .9); head.add(skull);
  const visor = new T.Mesh(new T.SphereGeometry(.5, 32, 24), visorM); visor.scale.set(1.08, .68, .36); visor.position.set(0, 0, .42); head.add(visor);
  const eyes = []; for (const x of [-.22, .22]){ const e = new T.Mesh(new T.CircleGeometry(.085, 24, 0, Math.PI), glow); e.position.set(x, .05, .605); head.add(e); eyes.push(e); }
  const smile = new T.Mesh(new T.CircleGeometry(.05, 20, Math.PI, Math.PI), glow); smile.position.set(0, -.13, .6); head.add(smile);
  for (const x of [-.74, .74]){ const ear = new T.Mesh(new T.CylinderGeometry(.13, .13, .12, 20), Wd); ear.rotation.z = Math.PI / 2; ear.position.set(x, 0, 0); head.add(ear); }
  const cap = new T.Mesh(new T.SphereGeometry(.2, 20, 12), Wd); cap.scale.set(1.3, .45, 1); cap.position.y = .52; head.add(cap);
  const arms = []; for (const s of [-1, 1]){ const sh = new T.Group(); sh.position.set(s * .66, 1.08, 0); const a = new T.Mesh(new T.SphereGeometry(.17, 20, 14), W); a.scale.set(1, 2.6, 1); a.position.y = -.38; sh.add(a); sh.rotation.z = s * .18; g.add(sh); arms.push(sh); }
  g.scale.setScalar(.72); g.position.set(5.55, 0, 2.35); g.rotation.y = -.45; scene.add(g);
  const tagC = texCanvas(256, 64); { const g2 = tagC.g; g2.fillStyle = '#c0392b'; g2.fillRect(0, 0, 256, 64); g2.fillStyle = '#fff'; g2.font = '700 38px "IBM Plex Sans Arabic", "Segoe UI", Tahoma, sans-serif'; g2.textAlign = 'center'; g2.textBaseline = 'middle'; g2.direction = 'rtl'; g2.fillText('اسألني', 128, 34); tagC.t.needsUpdate = true; }
  const tag = new T.Mesh(new T.PlaneGeometry(.9, .24), new T.MeshBasicMaterial({map:tagC.t, transparent:true})); tag.position.set(0, 2.85, 0); g.add(tag);
  let mood = 'idle', t0 = 0, aim = null;
  function setMood(m, target){ mood = m; t0 = performance.now(); aim = target || null; }
  function tick(){ const t = performance.now() / 1000, el = (performance.now() - t0) / 1000;
    g.position.y = Math.sin(t * 2) * .03; tag.lookAt(cam.position);
    const blink = (t % 4) < .12; eyes.forEach(e => e.scale.y = blink ? .15 : 1);
    if (mood === 'think'){ eyes.forEach((e, k) => e.position.x = (k ? .22 : -.22) + Math.sin(el * 9) * .07); head.rotation.z = Math.sin(el * 5) * .08; arms[1].rotation.z = .18 + .9 + Math.sin(el * 6) * .2; }
    else { eyes.forEach((e, k) => e.position.x = k ? .22 : -.22); head.rotation.z *= .9; }
    if (mood === 'point' && aim){ const w = new T.Vector3(); aim.getWorldPosition(w); const lp = g.worldToLocal(w.clone()); const ang = Math.atan2(lp.x, lp.z);
      head.rotation.y += (Math.max(-1, Math.min(1, ang)) - head.rotation.y) * .1; arms[0].rotation.z += (-1.9 - arms[0].rotation.z) * .12; arms[0].rotation.y = Math.max(-1, Math.min(1, ang)); if (el > 6) setMood('idle'); }
    else if (mood !== 'think'){ head.rotation.y *= .92; arms[0].rotation.z += (-.18 - arms[0].rotation.z) * .1; arms[0].rotation.y *= .9; arms[1].rotation.z += (.18 - arms[1].rotation.z) * .1; }
    if (mood === 'happy'){ g.rotation.y = -.45 + Math.sin(el * 8) * .1; if (el > 1.2) setMood('idle'); } }
  (function loop(){ tick(); requestAnimationFrame(loop); })();
  return {g, setMood};
})();

// ---------- the chat panel (floats over the page, opens and closes like a site chat)
(() => {
  const box = $('askbot'), fab = $('agFab'); if (!box || !fab) return;
  const q = $('agQ'), log = $('agLog'), sug = $('agSug');
  let built = false;
  const ensure = () => { if (!built){ AG.build(); built = true; } };
  const small = () => matchMedia('(max-width: 960px)').matches;
  function openChat(on){ box.hidden = !on; fab.hidden = on; fab.setAttribute('aria-expanded', on); document.body.classList.toggle('agopen', on); if (on){ ensure(); if (!log.children.length) renderSug(); setTimeout(() => { try { q.focus({preventScroll: true}); } catch (e) {} }, 60); } }
  function renderSug(){ ensure(); sug.hidden = false; sug.innerHTML = ((typeof CAMSIM !== 'undefined' && CAMSIM.detect(P)) ? [CAMSIM.label(P)] : []).concat(AG.suggestions()).map(s => `<button type="button" class="agsug">${esc(s)}</button>`).join(''); sug.querySelectorAll('.agsug').forEach(b => b.onclick = () => { q.value = b.textContent; ask(); }); }
  function bubble(cls, html){ const d = document.createElement('div'); d.className = 'agmsg ' + cls; d.innerHTML = html; log.appendChild(d); log.scrollTop = log.scrollHeight; return d; }
  // ---------- attachments: images and text files the viewer adds to a question (read only by the local brain and Claude)
  let pending = []; const attList = $('agAttList'), fileIn = $('agFile');
  const TXT_RE = /\.(txt|md|cpp|cc|c|h|hpp|py|js|ts|json|glsl|vert|frag|shader|csv|log|xml|html|css)$/i;
  async function shrink(file, max, q){ const bm = await createImageBitmap(file); const k = Math.min(1, max / Math.max(bm.width, bm.height));
    const cv = document.createElement('canvas'); cv.width = Math.max(1, Math.round(bm.width * k)); cv.height = Math.max(1, Math.round(bm.height * k)); cv.getContext('2d').drawImage(bm, 0, 0, cv.width, cv.height);
    return new Promise(res => cv.toBlob(b => res(b), 'image/jpeg', q)); }
  const toDataURL = b => new Promise((res, rej) => { const r = new FileReader(); r.onload = () => res(r.result); r.onerror = rej; r.readAsDataURL(b); });
  function renderAtt(){ attList.hidden = !pending.length; attList.innerHTML = pending.map((a, n) => `<span class="agattc">${a.kind === 'img' ? `<img src="${a.thumb}" alt="">` : '📄'}<span>${esc(a.name)}</span><button type="button" data-n="${n}" aria-label="شيل">✕</button></span>`).join('');
    attList.querySelectorAll('button').forEach(b => b.onclick = () => { pending.splice(+b.dataset.n, 1); renderAtt(); }); }
  $('agAtt').onclick = () => fileIn.click();
  fileIn.onchange = async () => { for (const f of [...fileIn.files]){ try {
        if (/^image\//.test(f.type)){ const blob = await shrink(f, 1280, .85), thumb = await toDataURL(await shrink(f, 160, .7)); pending.push({kind: 'img', name: f.name || 'صورة', blob, thumb}); }
        else if (TXT_RE.test(f.name) || /^text\//.test(f.type)){ if (f.size > 400000) throw new Error('big'); pending.push({kind: 'txt', name: f.name, text: await f.text()}); }
        else bubble('bot low', `الملف <b>${esc(f.name)}</b> مش مدعوم. ينفع صور أو ملفات نصية (كود، txt، md، json، csv).`);
      } catch (e){ bubble('bot low', `مش قادر أقرا <b>${esc(f.name)}</b>${e && e.message === 'big' ? ': الملف أكبر من 400 كيلوبايت' : ''}.`); } }
    fileIn.value = ''; renderAtt(); q.focus(); };
  const attText = (att, max) => { let out = '', left = max; for (const a of att.filter(a => a.kind === 'txt')){ const c = a.text.length > left ? a.text.slice(0, left) + '\n…(الباقي اتقطع)' : a.text; left -= c.length; out += `\n\n📄 ملف مرفق «${a.name}»:\n\`\`\`\n${c}\n\`\`\``; if (left <= 0) break; } return out; };
  // ---------- training data: every answer Claude writes or corrects becomes an example the local model can be fine-tuned on
  const TR_KEY = 'benchHelperTrain';
  const trAll = () => { try { return JSON.parse(localStorage.getItem(TR_KEY) || '[]'); } catch (e){ return []; } };
  function trAdd(q, a, src, free){ if (!q || !a) return; const L = trAll().filter(x => !(x.q === q && x.free === !!free && (x.pid || '') === (free ? '' : P.id)));
    L.push({q, a: a.trim(), src, free: !!free, pid: free ? '' : P.id, title: free ? '' : P.title, t: Date.now()});
    for (let k = L.length; ; k--){ try { localStorage.setItem(TR_KEY, JSON.stringify(L.slice(-k))); break; } catch (e){ if (k < 2) break; } } }
  // 🔔 alarm when the training examples reach the goal
  const TR_GOAL = 100, TR_ALERT_KEY = 'benchHelperTrainAlerted';
  function trCheck(){ const n = trAll().length; let done = false; try { done = localStorage.getItem(TR_ALERT_KEY) === String(TR_GOAL); } catch (e) {}
    const br = $('agBrain'); if (br) br.dataset.tr = n >= TR_GOAL ? '🎓' : '';
    if (n < TR_GOAL || done) return; try { localStorage.setItem(TR_ALERT_KEY, String(TR_GOAL)); } catch (e) {}
    try { navigator.vibrate && navigator.vibrate([300, 150, 300, 150, 600]); } catch (e) {}
    try { const ac = new (window.AudioContext || window.webkitAudioContext)(); [0, .25, .5].forEach((t, i) => { const o = ac.createOscillator(), g = ac.createGain(); o.frequency.value = [660, 880, 1320][i]; g.gain.setValueAtTime(.18, ac.currentTime + t); g.gain.exponentialRampToValueAtTime(.001, ac.currentTime + t + .22); o.connect(g).connect(ac.destination); o.start(ac.currentTime + t); o.stop(ac.currentTime + t + .23); }); } catch (e) {}
    if (box.hidden) openChat(true);
    const m = bubble('bot agalarm', `🔔 <b>وصلنا عدد ${n} مثال تدريب!</b><br>ده كفاية علشان ندرّب المخ نفسه (fine-tuning). افتح 🧠 ودوس «📦 نزّل بيانات تدريب المخ»، وبعدين «🎓 درّبه على Colab»، وقول لـ Claude في الشات إنك جاهز.`);
    try { robot.setMood('happy'); } catch (e) {} log.scrollTop = m.offsetTop - 8; }
  setTimeout(trCheck, 1500);
  const _trAdd = trAdd; trAdd = function(...a){ _trAdd(...a); trCheck(); };
  function trJSONL(){ return trAll().map(x => JSON.stringify({messages: [
      {role: 'system', content: x.free ? FREE_RULES : LOCAL_RULES + (x.title ? ` البرنامج المفتوح: «${x.title}».` : '')},
      {role: 'user', content: x.q}, {role: 'assistant', content: x.a}], source: x.src})).join('\n') + '\n'; }
  // ---------- answer mode: restricted to the bench (default) or a free question about anything
  const FREE_KEY = 'benchHelperFree'; let FREE = false; try { FREE = localStorage.getItem(FREE_KEY) === '1'; } catch (e) {}
  const freeBtn = $('agFree'), qPh = q.placeholder;
  function setFree(on){ FREE = on; try { localStorage.setItem(FREE_KEY, on ? '1' : '0'); } catch (e) {}
    freeBtn.setAttribute('aria-pressed', on); freeBtn.textContent = on ? '🌍 حر' : '🔒 البنش';
    freeBtn.title = on ? 'سؤال حر: المخ وClaude بيجاوبوا من معلوماتهم عن أي حاجة. دوس ترجع للبنش' : 'مقيّد بالبنش: الإجابات من التشغيل الحقيقي بس. دوس للسؤال الحر';
    q.placeholder = on ? 'اسأل أي سؤال، حتى لو برّه المحاضرات…' : qPh; }
  freeBtn.onclick = () => { setFree(!FREE); bubble('bot', FREE ? '🌍 <b>الوضع الحر:</b> اسأل في أي حاجة. المخ المحلي أو Claude هيجاوبوا من معلوماتهم العامة، والإجابة مش متراجعة على التشغيل الحقيقي، فممكن تغلط.' : '🔒 <b>رجعنا للبنش:</b> الإجابات من التشغيل الحقيقي للبرنامج المفتوح بس.'); };
  setFree(FREE);
  const dayBtn = $('agDay'), DAY_KEY = 'benchHelperDay';
  function setDay(on){ window.__agDayAll = on; try { localStorage.setItem(DAY_KEY, on ? '1' : '0'); } catch (e) {}
    if (!dayBtn) return; dayBtn.setAttribute('aria-pressed', on); dayBtn.textContent = on ? '📅 اليوم كله' : '📄 البرنامج';
    dayBtn.title = on ? 'الحقايق من كل برامج اليوم. دوس ترجع للبرنامج المفتوح بس' : 'الحقايق من البرنامج المفتوح بس. دوس عشان تسأل عن كل برامج اليوم'; }
  if (dayBtn) dayBtn.onclick = () => { setDay(!window.__agDayAll); bubble('bot', window.__agDayAll ? '📅 <b>اليوم كله:</b> مع كل سؤال هبعت ملخص كل برامج اليوم، وأقرب السطور ليه من البرامج التانية. اسأل عن أي برنامج أو عن العلاقة بينهم. (المخ المحلي هياخد وقت أطول شوية في القراية)' : '📄 <b>البرنامج ده بس:</b> الحقايق من البرنامج المفتوح بس.'); };
  { let d0 = false; try { d0 = localStorage.getItem(DAY_KEY) === '1'; } catch (e) {} setDay(d0); }
  // ---------- the divider on top of the chat (like Android split screen): drag to resize, double-tap = full / back
  { const box = $('askbot'), grip = $('agGrip'), HK = 'benchHelperH';
    const lim = h => Math.round(Math.max(160, Math.min(window.innerHeight - 40, h)));
    const setH = (h, save) => { box.style.height = lim(h) + 'px'; if (save) try { localStorage.setItem(HK, String(lim(h))); } catch (e) {} };
    try { const h0 = +localStorage.getItem(HK); if (h0) setH(h0); } catch (e) {}
    let y0 = 0, h0 = 0, id = null, lastTap = 0, prevH = 0;
    if (grip){
      grip.addEventListener('pointerdown', e => { id = e.pointerId; y0 = e.clientY; h0 = box.getBoundingClientRect().height; grip.setPointerCapture(id); grip.classList.add('drag'); e.preventDefault(); });
      grip.addEventListener('pointermove', e => { if (e.pointerId !== id) return; setH(h0 + (y0 - e.clientY)); });
      const end = e => { if (e.pointerId !== id) return; id = null; grip.classList.remove('drag'); const h = box.getBoundingClientRect().height; setH(h, true);
        if (Math.abs(e.clientY - y0) < 6){ const t = performance.now(); if (t - lastTap < 350){ const full = window.innerHeight - 40;
            if (h < full - 4){ prevH = h; setH(full, true); } else setH(prevH || window.innerHeight * .46, true); lastTap = 0; } else lastTap = t; } };
      grip.addEventListener('pointerup', end); grip.addEventListener('pointercancel', end);
      grip.addEventListener('keydown', e => { const h = box.getBoundingClientRect().height; if (e.key === 'ArrowUp'){ setH(h + 40, true); e.preventDefault(); } if (e.key === 'ArrowDown'){ setH(h - 40, true); e.preventDefault(); } });
      window.addEventListener('resize', () => { const h = box.getBoundingClientRect().height; if (h) setH(h); }); } }
  const SCENE_RULE = ' لو السؤال عن شكل ثلاثي الأبعاد أو نقط في الفراغ (هرم، مكعب، مثلث بنقطه، كاميرا، محاور x y z، indices)، ارسمه في بلوك ```scene3d فيه JSON بس، والبنش هيحوّله لرسمة 3D تفاعلية تتلف بالإصبع. الشكل: {"title":"اسم قصير","points":[[x,y,z],...],"faces":[{"p":[رقم,رقم,رقم],"name":"وش يمين","color":"#4a9eff"}],"lines":[[رقم,رقم]],"start":0}. الأرقام في faces و lines هي ترتيب النقطة في points وبتبدأ من 0؛ و start هو رقم أول نقطة اللي يتكتب على الرسمة (مثلاً 7 لو النقط هي 7 و 8 و 9 في البرنامج). لو البرنامج فيه vertices أو indices حقيقية استخدمها هي بالظبط ماتألّفش غيرها. من 3 لـ 60 نقطة. JSON سليم من غير تعليقات. مثال هرم:\n```scene3d\n{"title":"هرم","points":[[-0.5,-0.5,0.5],[0.5,-0.5,0.5],[0.5,-0.5,-0.5],[-0.5,-0.5,-0.5],[0,0.5,0]],"faces":[{"p":[0,1,4],"name":"وش أمامي"},{"p":[1,2,4],"name":"وش يمين"},{"p":[2,3,4],"name":"وش خلفي"},{"p":[3,0,4],"name":"وش شمال"},{"p":[0,1,2,3],"name":"القاعدة"}]}\n```\nولو السؤال عن الكاميرا (cameraPos أو cameraFront أو lookAt أو view matrix أو yaw و pitch أو WASD أو FOV)، زوّد في نفس الـ JSON "camera":{"pos":[0,0,2],"yaw":-90,"pitch":0,"fov":45} (أو "front":[0,0,-1] بدل yaw و pitch) بقيم البرنامج الحقيقية لو موجودة، والبنش هيعمل لوحتين: الكاميرا من فوق كمثلث برتقالي والمنطقة اللي شايفاها، وشباك باللي الكاميرا شايفاه بيتلف بالسحب ومعاه أزرار W A S D وقراية Position و Front. مثال كاميرا بتبص على هرم:\n```scene3d\n{"title":"الكاميرا والهرم","points":[[-0.5,-0.5,0.5],[0.5,-0.5,0.5],[0.5,-0.5,-0.5],[-0.5,-0.5,-0.5],[0,0.5,0]],"faces":[{"p":[0,1,4],"color":"#f2a03d"},{"p":[1,2,4],"color":"#4a9eff"},{"p":[2,3,4],"color":"#6cc56c"},{"p":[3,0,4],"color":"#e8678f"},{"p":[0,1,2,3],"name":"القاعدة","color":"#8d7660"}],"camera":{"pos":[0,0,2],"yaw":-90,"pitch":0,"fov":45}}\n```\nولو المستخدم طلب بنفسه رسمة 3D أو شكل مجسّم أو قال «ارسم/وريني»، ارسمه حتى لو السؤال مش عن الكود ومش موجود في البرنامج: ساعتها خد الشكل من معلوماتك العامة وقول في سطر إنه شكل توضيحي مش من التشغيل الحقيقي. ماتكتبش HTML ولا JavaScript للرسم، وماتقولش إنك مش بتعرف ترسم 3D.';
  // the user can ask for a drawing in plain words: add an explicit order to the prompt so even the small local model draws it
  const want3d = q => { q = String(q || '');
    if (/(3\s*d|٣\s*d|ثلاث[يى]\s*الأبعاد|ثلاث[يى]\s*الابعاد|ثلاث[يى]|مجس[ّ]?م|هرم|مكعب|متوازي|منشور|كور[ةه]|(?:^|\s)(?:ال)?كر[ةه](?:\s|$)|اسطوان|أسطوان|مخروط|في\s*الفراغ|محاور\s*x|scene3d|كاميرا|كاميره|camera|lookat|wasd)/i.test(q))
      return '\n\n(المستخدم طالب رسمة 3D صراحة: لازم يكون في ردك بلوك ```scene3d واحد على الأقل بالشكل اللي فوق. لو الشكل مش في البرنامج ارسمه من معلوماتك العامة وقول إنه توضيحي.)';
    if (/(ارسم|إرسم|ارسمل|ارسمه|ارسمها|رسم[ةه]|ورين[يى]\s*(شكل|رسم)|وضح\s*بالرسم|بالرسم|\bdraw\b|\bdiagram\b|visuali[sz]e)/i.test(q))
      return '\n\n(المستخدم طالب رسمة صراحة: لازم يكون في ردك رسمة. لو الفكرة فيها شكل أو نقط في الفراغ استخدم ```scene3d، ولو خطوات أو حاجة رايحة لحاجة استخدم ```diagram.)';
    return ''; };
  const DIAG_RULE = ' لو السؤال محتاج شرح ورسمة هتوضح الفكرة (خطوات، أو حاجة رايحة لحاجة، أو أجزاء متوصلة)، ارسمها في بلوك ```diagram وكل سطر فيه «اسم -> اسم : كلمتين»، والأسماء قصيرة (من 1 لـ 3 كلمات، ومن غير أقواس ولا أرقام طويلة)، وكلام السهم بعد «:» كلمة أو اتنين بس (مش جملة)، ومن 2 لـ 8 أسطر. ماتطلّعش أكتر من 3 أسهم من نفس الاسم: لو الخطوات ورا بعض اعملها سلسلة (أ -> ب، ب -> ج) مش كلها طالعة من اسم واحد. ماتحطش إحداثيات أو أرقام نقط أو indices كأسماء في diagram: دي مكانها بلوك scene3d. ماتكتبش نفس الكلام برّه الرسمة وجواها، وماتحطش أكتر من رسمة diagram واحدة في الرد إلا لو اتطلب. مثال:\n```diagram\nnew -> malloc : تحجز\nmalloc -> Constructor : بعدها\n```\nالبنش هيحوّلها لرسمة. ماتقولش إنك مش بتعرف ترسم.' + SCENE_RULE;
  const FREE_RULES = 'انت مساعد ذكي ودود بيتكلم بالعامية المصرية. جاوب على أي سؤال من معلوماتك العامة، بوضوح وبجمل قصيرة. لو مش متأكد من معلومة قول كده بصراحة، وماتألّفش مصادر. اكتب الكود بين علامات `.' +
    ' جاوب على قد السؤال بس: السؤال البسيط (معلومة واحدة زي عاصمة أو تاريخ أو تعريف) جاوبه في سطر أو اتنين، من غير رسمة ومن غير معلومات جانبية. ماتجيبش سيرة البنش أو البرنامج أو الكود ولا ترسم عنهم إلا لو السؤال عنهم.' +
    ' لو في الرسالة «من البرنامج المفتوح»، ابدأ بأقرب حاجة في البرنامج ده للسؤال: اذكر السطر أو الخطوة (مثلاً «خطوة 12» أو «سطر 18») واستخدم أسماء المتغيرات والدوال اللي فيه، وبعدها كمّل من معلوماتك العامة. ماتكتبش كود جديد من برّه البرنامج إلا لو السؤال طالب كده صراحة.' + DIAG_RULE;
  // a free question gets the open program only when it is plausibly about code/graphics, so «what is the capital of X» stays clean
  const aboutProg = q => { q = String(q || '');
    if (/البرنامج|الكود|كود|السطر|سطر\s*\d|الخطو[ةه]|خطو[ةه]\s*\d|المتغير|الدال[ةه]|الشيدر|shader|buffer|vao|vbo|opengl|gl[A-Z]|matrix|مصفوف|كاميرا|camera|ر[أا]س|vertex|pixel|بكسل|texture|uniform|pointer|مؤشر|\.cpp|\.py|main/i.test(q)) return true;
    try { const top = (AG.search(q, {pid: P.id, kinds: ['step', 'line'], n: 1})[0] || {}).d; if (!top || !top.code) return false;
      const qt = AG.toks(q).filter(t => t[0] !== '§' && t.length > 2 && /[a-z_]/i.test(t)); const ct = new Set(AG.toks(top.code)); return qt.some(t => ct.has(t)); } catch (e) { return false; } };
  const freeCtx = q => { if (!aboutProg(q)) return ''; try { return '\n\nمن البرنامج المفتوح «' + P.title + '» (أقرب سطور وخطوات للسؤال، من التشغيل الحقيقي):\n' + AG.context(q, {short: true}); } catch (e) { return ''; } };
  function freeAsk(text, att){ const wait = bubble('bot', '<div class="aglearn">🌍 سؤال حر: الإجابة هتيجي من معلومات النموذج العامة، مش من التشغيل الحقيقي.</div><div class="agfb">' +
      (LOCAL.ok ? '<button type="button" class="aglocal">🧠 اسأل المخ المحلي</button>' : '') + (SAMPLE ? '<button type="button" class="agmore">✨ اسأل Claude</button>' : '') + (!SAMPLE && !ONCLAUDE ? '<button type="button" class="agext">✨ اسأل Claude</button>' : '') + '</div>');
    wait.dataset.free = '1'; wait._att = att; wait._free = true;
    const lb = wait.querySelector('.aglocal'), mb = wait.querySelector('.agmore'), xb = wait.querySelector('.agext');
    if (lb) lb.onclick = () => askLocal(text, wait, lb); if (mb) mb.onclick = () => explain(text, wait, mb); if (xb) xb.onclick = () => askClaudeOutside(text, wait, xb);
    if (!lb && !mb && !xb) wait.insertAdjacentHTML('beforeend', '<small>مفيش مخ محلي شغال ولا Claude هنا. شغّل llama-server في Termux.</small>');
    robot.setMood('think'); if (lb) askLocal(text, wait, lb); else if (mb) explain(text, wait, mb); }
  function ask(){ let text = q.value.trim(); if (!text && !pending.length) return; ensure(); robot.setMood('think'); sug.hidden = true; q.value = '';
    const att = pending; pending = []; renderAtt(); if (!text) text = att.some(a => a.kind === 'img') ? 'اشرحلي الصورة دي' : 'اشرحلي الملف ده';
    bubble('me', esc(text) + (FREE ? '<span class="agfreetag">🌍 حر</span>' : '') + (att.length ? `<div class="agattm">${att.map(a => a.kind === 'img' ? `<img src="${a.thumb}" alt="${esc(a.name)}">` : `<span>📄 ${esc(a.name)}</span>`).join('')}</div>` : ''));
    if (!att.length && typeof CAMSIM !== 'undefined' && CAMSIM.detect(P) && CAMSIM.wants(text, P)){ const b = bubble('bot', '<div class="aglearn">🎥 ' + CAMSIM.intro(P) + '</div><div class="agcsslot"></div>'); robot.setMood('happy'); return; }
    if (FREE){ freeAsk(text, att); return; }
    const wait = bubble('bot wait', 'بدوّر في البنش…'); wait._att = att;
    setTimeout(() => { let r; try { r = AG.answer(text); } catch (e){ r = {html: 'حصل خطأ وأنا بدوّر. جرّب تكتب السؤال بشكل تاني.', low: true}; }
      if (wait._att && wait._att.length) r.html = '<div class="aglearn">📎 البحث المحلي مابيقراش المرفقات. دوس «🧠 اسأل المخ المحلي» أو «✨ Claude» تحت علشان يقروها.</div>' + r.html;
      wait.className = 'agmsg bot' + (r.low ? ' low' : ''); wait.innerHTML = r.html + `<div class="agfb"><button type="button" class="agup" title="الإجابة مفيدة">👍</button><button type="button" class="agdown" title="مش دي">👎 مش دي</button>${SAMPLE ? '<button type="button" class="agmore">✨ اشرحلي أكتر (Claude)</button>' : ''}${LOCAL.ok ? '<button type="button" class="aglocal">🧠 اسأل المخ المحلي</button>' : ''}${!SAMPLE && !ONCLAUDE ? '<button type="button" class="agext">✨ اسأل Claude</button>' : ''}</div>`; fixBidi(wait);
      const more = wait.querySelector('.agmore'); if (more) more.onclick = () => explain(text, wait, more);
      const lb = wait.querySelector('.aglocal'); if (lb) lb.onclick = () => askLocal(text, wait, lb);
      const xb = wait.querySelector('.agext'); if (xb) xb.onclick = () => askClaudeOutside(text, wait, xb);
      const shown = [...wait.querySelectorAll('.agchip')].map(b => b.dataset.ln ? `l:${b.dataset.f}:${b.dataset.ln}` : `s:${b.dataset.k}`);
      wait.querySelector('.agup').onclick = e => { if (shown[0]){ AG.remember(text, P.id, shown[0], true); AG.train(text, [[shown[0], 1]], [], .6, 'up'); } e.target.parentElement.innerHTML = '<span class="aglearn">تمام، هفتكرها 👍</span>'; robot.setMood('happy'); };
      wait.querySelector('.agdown').onclick = e => { const alt = AG.alternatives(text, shown); const fb = e.target.parentElement;
        fb.innerHTML = `<div class="agalt"><b>${alt.length ? 'أنهي واحدة فيهم كنت عايزها؟' : 'مش لاقي بدايل قريبة.'}</b>${alt.map((d, n) => `<button type="button" class="agpick" data-n="${n}"><code dir="ltr">${esc(d.code.slice(0, 60))}</code><small>${esc((d.ex || '').slice(0, 70))}</small></button>`).join('')}<form class="agline"><input type="number" inputmode="numeric" min="1" placeholder="أو اكتب رقم السطر الصح في الكود"><button type="submit">علّمه</button></form><button type="button" class="agnone">ولا واحدة</button></div>`;
        const teach = (d, label) => { const ref = d.kind === 'step' ? 's:' + d.k : 'l:' + d.f + ':' + d.ln;
          AG.remember(text, P.id, ref, true); if (shown[0]) AG.remember(text, P.id, shown[0], false); AG.train(text, [[ref, 1]], shown, .9, 'pick');
          fb.innerHTML = `<span class="aglearn">اتعلّمت ✔ المرة الجاية هجاوبك بده:</span><br><code dir="ltr">${esc(d.code)}</code> ${AG.chipFor(d)}<br>${d.ex || ''}`; fixBidi(fb); wire(fb, text); robot.setMood('happy'); };
        fb.querySelector('.agline').onsubmit = ev => { ev.preventDefault(); const ln = +ev.target.querySelector('input').value; const d = AG.docForLine(ln);
          if (d) teach(d); else ev.target.querySelector('input').value = '', ev.target.querySelector('input').placeholder = 'السطر ده مش موجود، جرّب رقم تاني'; };
        fb.querySelectorAll('.agpick').forEach(b => b.onclick = () => teach(alt[+b.dataset.n]));
        const nb = fb.querySelector('.agnone'); if (nb) nb.onclick = () => { fb.innerHTML = '<span class="aglearn">تمام. السؤال ده هيوصلني في التحديث الجاي لو بعته لـ Claude في الشات.</span>'; }; };
      wire(wait, text);
      log.scrollTop = wait.offsetTop - 8;
      if (r.go != null){ play(false); go(r.go); }
      const tg = r.target ? anchor(r.target[0], (r.target[0] === 'buf' ? 'Buffer ' : 'VAO ') + r.target[1]) : null;
      robot.setMood(r.low ? 'idle' : tg ? 'point' : 'happy', tg);
      if (SAMPLE && autoClaude() && (r.low || (r.conf || 0) < .5) && !r.learned){ const mb = wait.querySelector('.agmore'); if (mb) explain(text, wait, mb); } }, 300); }
  function wire(root, qtext){ root.querySelectorAll('.agchip').forEach(b => b.onclick = () => { if (qtext && !b.dataset.pid){ try { AG.train(qtext, [[b.dataset.ln ? `l:${b.dataset.f}:${b.dataset.ln}` : `s:${b.dataset.k}`, 1]], [], .2, 'click'); } catch (e) {} } if (b.dataset.pid && b.dataset.pid !== P.id) loadProgram(b.dataset.pid, false, true); play(false);
        if (small()) openChat(false);
        if (b.dataset.ln){ showLine(+b.dataset.f, +b.dataset.ln); $('codeFig').scrollIntoView({behavior: reduce ? 'auto' : 'smooth', block: 'center'}); return; }
        go(+b.dataset.k); stage.scrollIntoView({behavior: reduce ? 'auto' : 'smooth', block: 'center'}); }); }
  // ---------- optional: Claude writes a fuller explanation from the facts the helper found (published page + internet only)
  let SAMPLE = null;
  try { if (window.claude && window.claude.use) window.claude.use('sample').then(f => { SAMPLE = f || null; }).catch(() => {}); } catch (e) {}
  // outside claude.ai: a tiny bridge on the phone (claude_bridge.py in Termux) runs Claude Code and answers here, inside the bench
  const BRIDGE = 'http://127.0.0.1:8081'; let VIA_BRIDGE = false;
  function bridgeSample(prompt, o = {}){ const ctl = new AbortController(); if (o.signal) o.signal.addEventListener('abort', () => ctl.abort());
    if (o.images && o.images.length) prompt += '\n\n(ملحوظة: الصور مابتعدّيش من الجسر، فجاوب من الكلام بس، وقول للمستخدم يوصف الصورة لو مهمة.)';
    return fetch(BRIDGE + '/ask', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({prompt}), signal: ctl.signal})
      .then(async r => { const j = await r.json().catch(() => ({})); if (!r.ok) throw Object.assign(new Error(j.error || ('HTTP ' + r.status)), {code: 'bridge'}); const text = j.text || ''; if (o.onText) o.onText({text, delta: text}); return {text, truncated: false}; })
      .catch(e => { if (e.name === 'AbortError') throw Object.assign(new Error('cancelled'), {code: 'cancelled'}); throw e; }); }
  async function probeBridge(){ if (SAMPLE && !VIA_BRIDGE) return true; try { const ctl = new AbortController(); const t = setTimeout(() => ctl.abort(), 2000);
      const r = await fetch(BRIDGE + '/ping', {signal: ctl.signal}); clearTimeout(t); const j = await r.json(); if (j.ok){ SAMPLE = bridgeSample; VIA_BRIDGE = true; return true; } } catch (e) {}
    if (VIA_BRIDGE){ SAMPLE = null; VIA_BRIDGE = false; } return false; }
  if (!/claude\.ai|claudeusercontent/.test(location.hostname)) probeBridge();
  const RULES = 'انت مساعد شرح جوه «بنش» تعليمي بيعرض برنامج C++/OpenGL أو Python اتشغّل فعلاً خطوة بخطوة. اكتب بالعامية المصرية لطالب مبتدئ، بجمل قصيرة. ' +
    'اعتمد بس على «حقايق البنش» اللي تحت (دي من التشغيل الحقيقي)؛ ماتألّفش أرقام ولا قيم ولا أسطر مش موجودة. لو المعلومة مش موجودة في الحقايق، قول كده بصراحة. ' +
    'لما تذكر خطوة اكتبها بالشكل «خطوة 12» عشان تتحول لزرار. قبل أي رقم معناه عدد اكتب كلمة «عدد» (مثلاً: عدد 3 Buffers)، واستخدم «رقم» للأرقام اللي هي أسماء (VAO رقم 3). ' +
    'خلّي الرد من 4 لـ 10 سطور، ومن غير عناوين كبيرة. الكود اكتبه بين علامتي `.' + DIAG_RULE;
  function diagramSvg(src){ const E = [], N = []; const id = x => { x = x.trim().slice(0, 40); if (!x) return -1; let k = N.indexOf(x); if (k < 0){ N.push(x); k = N.length - 1; } return k; };
    for (const raw of String(src).split('\n')){ const L = raw.replace(/^[-*•\s]+/, ''); const m = /^(.+?)\s*(?:->|→|=>)\s*(.+?)(?:\s*[:：]\s*(.*))?$/.exec(L);
      if (m){ const a = id(m[1]), b = id(m[2]); if (a >= 0 && b >= 0) E.push([a, b, (m[3] || '').trim().slice(0, 30)]); } else if (L.trim()) id(L); }
    if (!N.length || N.length > 16) return '';
    // text width without a canvas: Arabic letters are narrower than bold Latin
    const tw = (s, fs) => [...s].reduce((w, ch) => w + (/[\u0600-\u06ff]/.test(ch) ? .52 : /[A-Z0-9MW]/.test(ch) ? .68 : .56), 0) * fs;
    const lvl = N.map(() => 0); for (let it = 0; it < N.length; it++) for (const [a, b] of E) if (a !== b && lvl[b] < lvl[a] + 1 && lvl[a] + 1 < N.length) lvl[b] = lvl[a] + 1;
    const byLvl = []; N.forEach((n, k) => { (byLvl[lvl[k]] = byLvl[lvl[k]] || []).push(k); });
    // at most 3 boxes side by side: a wider level is split into more rows, so names never squeeze into each other
    // a level with more than 4 names is split into sub-rows that sit close together (one group), the lower one shifted into the gaps
    const rows = []; byLvl.filter(Boolean).forEach(r => { const per = r.length > 4 ? Math.ceil(r.length / Math.ceil(r.length / 4)) : 4;
      for (let i = 0; i < r.length; i += per) rows.push({ks: r.slice(i, i + per), sub: i > 0, last: i + per >= r.length, per}); });
    const W = 340, GX = 12, hasLab = E.some(e => e[2]), GY = hasLab ? 70 : 46, pos = []; let y = 10;
    // each name: shrink the font, then use two lines, then cut with …
    const fit = (s, w) => { for (const fs of [12, 11, 10]) if (tw(s, fs) <= w - 10) return {fs, lines: [s]};
      const words = s.split(/\s+/); if (words.length > 1){ for (const fs of [11, 10]){ let best = null;
          for (let i = 1; i < words.length; i++){ const l1 = words.slice(0, i).join(' '), l2 = words.slice(i).join(' '); const m = Math.max(tw(l1, fs), tw(l2, fs)); if (!best || m < best.m) best = {m, lines: [l1, l2]}; }
          if (best.m <= w - 10) return {fs, lines: best.lines}; } }
      let c = s; while (c.length > 2 && tw(c + '…', 10) > w - 10) c = c.slice(0, -1); return {fs: 10, lines: [c + '…']}; };
    rows.forEach(R => { const r = R.ks, cols = Math.max(r.length, R.sub ? R.per : 1), bw = Math.min(160, (W - GX * (cols + 1)) / cols), F = r.map(k => fit(N[k], bw)), bh = F.some(f => f.lines.length > 1) ? 40 : 30;
      let x0 = (W - (r.length * bw + (r.length - 1) * GX)) / 2; if (R.sub && r.length < R.per) x0 = Math.min(x0, (W - (R.per * bw + (R.per - 1) * GX)) / 2 + (bw + GX) / 2);
      r.forEach((k, j) => { pos[k] = {x: x0 + j * (bw + GX), y, w: bw, h: bh, f: F[j]}; }); y += bh + (R.last ? GY : 12); });
    let H = y - GY + 10; const t = s0 => esc(s0);
    let lines = '', labs = ''; const taken = []; N.forEach((n, k) => taken.push({x: pos[k].x - 2, y: pos[k].y - 2, w: pos[k].w + 4, h: pos[k].h + 4}));
    const hit = r => taken.some(o => r.x < o.x + o.w && o.x < r.x + r.w && r.y < o.y + o.h && o.y < r.y + r.h), notes = [];
    for (const [a, b, lab] of E){ const A = pos[a], B = pos[b]; const x1 = A.x + A.w / 2, y1 = A.y + A.h, x2 = B.x + B.w / 2, y2 = B.y, up = y2 <= y1;
      const d = up ? `M${A.x + A.w} ${A.y + A.h / 2} C ${Math.min(W - 4, A.x + A.w + 50)} ${A.y - 24}, ${Math.min(W - 4, B.x + B.w + 50)} ${B.y + B.h + 24}, ${B.x + B.w} ${B.y + B.h / 2}` : `M${x1} ${y1} L${x2} ${y2}`;
      lines += `<path d="${d}" fill="none" stroke="currentColor" stroke-width="1.6" marker-end="url(#agar)" opacity=".7"/>`;
      if (!lab) continue;
      // the edge's words sit on a small dark tag along the arrow; try a few spots, and if every spot overlaps something, put a number on the arrow and the words under the drawing
      const fs = 10.5, lw = tw(lab, fs) + 10, lh = 16; let spot = null;
      const cand = up ? [[Math.min(W - lw / 2 - 2, Math.max(A.x + A.w, B.x + B.w) + 8), (A.y + B.y + B.h) / 2]] : [.5, .35, .65, .22, .78].map(f => [x1 + (x2 - x1) * f, y1 + (y2 - y1) * f]);
      for (const [cx, cy] of cand){ const r = {x: Math.max(2, Math.min(W - lw - 2, cx - lw / 2)), y: cy - lh / 2, w: lw, h: lh}; if (!hit(r)){ spot = r; break; } }
      if (spot){ taken.push(spot); labs += `<rect x="${spot.x}" y="${spot.y}" width="${spot.w}" height="${lh}" rx="5" fill="rgba(15,17,23,.88)" stroke="rgba(245,158,11,.5)"/><text x="${spot.x + spot.w / 2}" y="${spot.y + lh / 2 + 3.6}" font-size="${fs}" fill="#f59e0b" text-anchor="middle">${t(lab)}</text>`; }
      else { notes.push(lab); const n = notes.length, [cx, cy] = up ? cand[0] : [x1 + (x2 - x1) * .5, y1 + (y2 - y1) * .5];
        labs += `<circle cx="${cx}" cy="${cy}" r="8" fill="rgba(15,17,23,.92)" stroke="#f59e0b"/><text x="${cx}" y="${cy + 3.5}" font-size="10" font-weight="700" fill="#f59e0b" text-anchor="middle">${n}</text>`; } }
    let boxes = ''; N.forEach((n, k) => { const p = pos[k], f = p.f, n2 = f.lines.length;
      boxes += `<rect x="${p.x}" y="${p.y}" width="${p.w}" height="${p.h}" rx="7" fill="rgba(23,37,64,.95)" stroke="#60a5fa"/>`;
      f.lines.forEach((ln, i) => { boxes += `<text x="${p.x + p.w / 2}" y="${p.y + p.h / 2 + (i - (n2 - 1) / 2) * (f.fs + 2) + f.fs * .36}" font-size="${f.fs}" font-weight="700" text-anchor="middle" fill="currentColor">${t(ln)}</text>`; }); });
    const svg = `<svg viewBox="0 0 ${W} ${H}" width="100%" style="max-width:460px;display:block;margin:6px auto;color:inherit" direction="ltr"><defs><marker id="agar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>${lines}${boxes}${labs}</svg>`;
    const leg = notes.length ? '<div dir="rtl" style="font-size:.8rem;margin:2px 8px 6px;color:#f59e0b;text-align:right">' + notes.map((s, i) => `<div>${i + 1}. ${t(s)}</div>`).join('') + '</div>' : '';
    return `<div class="agdiag">${svg}${leg}</div>`; }
  // ---------- ```scene3d: an interactive 3D shape inside a chat answer (the model only DESCRIBES it as JSON; the bench draws it, nothing it writes is run)
  const S3_COLORS = ['#4a9eff', '#e8678f', '#6cc56c', '#f2a03d', '#a98bd8', '#3fc1c9', '#d9b44a', '#8d7660'];
  function s3parse(src){
    let o; const s = String(src).trim().replace(/^[^{]*/, '').replace(/[^}]*$/, '');
    try { o = JSON.parse(s); } catch (e){ try { o = JSON.parse(s.replace(/,\s*([\]}])/g, '$1').replace(/'/g, '"')); } catch (e2){ return null; } }
    if (!o || !Array.isArray(o.points) || !o.points.length) return null;
    const num = v => (typeof v === 'number' && isFinite(v)) ? v : (isFinite(parseFloat(v)) ? parseFloat(v) : 0);
    const P = o.points.slice(0, 120).map(p => Array.isArray(p) ? [num(p[0]), num(p[1]), num(p[2])] : (p && typeof p === 'object' ? [num(p.x), num(p.y), num(p.z)] : null));
    if (P.some(p => !p)) return null;
    const ok = i => Number.isInteger(i) && i >= 0 && i < P.length;
    const F = (Array.isArray(o.faces) ? o.faces : []).slice(0, 80).map((f, k) => { const idx = Array.isArray(f) ? f : (f && (f.p || f.idx || f.points)); if (!Array.isArray(idx) || idx.length < 3 || !idx.every(ok)) return null;
      return {p: idx, color: (f && typeof f.color === 'string' && /^#[0-9a-f]{3,8}$|^[a-z]{3,20}$/i.test(f.color)) ? f.color : S3_COLORS[k % S3_COLORS.length], name: (f && f.name ? String(f.name) : '').slice(0, 30)}; }).filter(Boolean);
    const Ln = (Array.isArray(o.lines) ? o.lines : []).slice(0, 120).filter(l => Array.isArray(l) && l.length >= 2 && ok(l[0]) && ok(l[1]));
    const names = Array.isArray(o.labels) ? o.labels.map(x => String(x).slice(0, 12)) : null;
    const base = Number.isInteger(o.start) ? o.start : 0;   // first point number (e.g. 7 when the shape uses indices 7, 8, 9)
    let cam = null; const c0 = o.camera;
    if (c0 && typeof c0 === 'object' && !Array.isArray(c0)){ const pos = Array.isArray(c0.pos || c0.position) ? (c0.pos || c0.position).slice(0, 3).map(num) : [0, 0, 3];
      const fr = Array.isArray(c0.front) ? c0.front.map(num) : null;   // a front vector works too, it becomes yaw / pitch
      const yaw = fr ? Math.atan2(fr[2], fr[0]) * 180 / Math.PI : (c0.yaw != null ? num(c0.yaw) : -90), pitch = fr ? Math.asin(Math.max(-1, Math.min(1, fr[1] / (Math.hypot(...fr) || 1)))) * 180 / Math.PI : num(c0.pitch);
      cam = {pos: pos.length === 3 ? pos : [0, 0, 3], yaw, pitch: Math.max(-89, Math.min(89, pitch)), fov: Math.max(20, Math.min(120, c0.fov != null ? num(c0.fov) : 45))}; }
    else if (Array.isArray(c0) && c0.length >= 3) cam = {pos: c0.slice(0, 3).map(num), yaw: -90, pitch: 0, fov: 45};
    return {title: String(o.title || '').slice(0, 60), P, F, L: Ln, names, base, showLabels: o.labels !== false, axes: o.axes !== false, cam};
  }
  function s3css(){ if (document.getElementById('ag3dcss')) return; const st = document.createElement('style'); st.id = 'ag3dcss';
    st.textContent = '.ag3d{margin:8px 0;border:1px solid var(--rule,#444);border-radius:10px;padding:6px;background:var(--paper,transparent)}' +
      '.ag3d canvas{display:block;width:100%;touch-action:none;border-radius:8px;cursor:grab}.ag3d .ag3t{font-weight:700;font-size:.85rem;margin:2px 4px 4px}' +
      '.ag3d .ag3b{display:flex;flex-wrap:wrap;gap:5px;margin-top:6px}.ag3d .ag3b button{font:inherit;font-size:.78rem;padding:4px 9px;border-radius:8px;border:1px solid var(--rule,#555);background:transparent;color:inherit;cursor:pointer}' +
      '.ag3d .ag3b button.on{border-color:#f59e0b;color:#f59e0b}.ag3d .ag3b i{display:inline-block;width:.8em;height:.8em;border-radius:3px;margin-inline-end:5px;vertical-align:-1px}' +
      '.ag3d .ag3i{font-size:.78rem;margin-top:6px;direction:ltr;text-align:left;font-family:monospace;white-space:pre-wrap;opacity:.9}.ag3d .ag3h{font-size:.72rem;opacity:.6;margin:4px 4px 0}' +
      '.ag3wait{font-size:.8rem;opacity:.7;margin:6px 0}'; document.head.appendChild(st); }
  function s3build(S){ s3css();
    const box = document.createElement('div'); box.className = 'ag3d'; box.dir = 'rtl';
    box.innerHTML = (S.title ? `<div class="ag3t">${esc(S.title)}</div>` : '') + '<canvas></canvas><div class="ag3h">اسحب بإصبعك عشان تلفه، وإصبعين عشان تقرّب.</div><div class="ag3b"></div><div class="ag3i" dir="ltr" hidden></div>';
    const cv = box.querySelector('canvas'), bar = box.querySelector('.ag3b'), info = box.querySelector('.ag3i'), g = cv.getContext('2d');
    // fit the shape: centre of its box at 0, biggest side = 2
    const mn = [0, 1, 2].map(a => Math.min(...S.P.map(p => p[a]))), mx = [0, 1, 2].map(a => Math.max(...S.P.map(p => p[a])));
    const c = mn.map((v, a) => (v + mx[a]) / 2), sz = Math.max(1e-6, ...mx.map((v, a) => v - mn[a])) / 2;
    const V = S.P.map(p => p.map((v, a) => (v - c[a]) / sz)); const RM = Math.max(.2, ...V.map(p => Math.hypot(...p)));   // fits at any angle
    const V0 = {yaw: -.6, pitch: .45, zoom: 1}; let st = {...V0}, auto = false, sel = -1, raf = 0;
    const lab = i => S.names && S.names[i] != null ? S.names[i] : String(S.base + i);
    const fmt = p => '(' + p.map(v => (+v.toFixed(3)).toString()).join(', ') + ')';
    function draw(){ const dpr = window.devicePixelRatio || 1, W = cv.clientWidth || 300, H = Math.round(Math.min(320, W * .8));
      if (cv.width !== Math.round(W * dpr) || cv.height !== Math.round(H * dpr)){ cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr); cv.style.height = H + 'px'; }
      g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, W, H);
      const fg = getComputedStyle(box).color || '#ddd', cy = Math.cos(st.yaw), sy = Math.sin(st.yaw), cp = Math.cos(st.pitch), sp = Math.sin(st.pitch), R = Math.min(W, H) * .4 * st.zoom / RM;
      const pr = p => { const x1 = p[0] * cy + p[2] * sy, z1 = -p[0] * sy + p[2] * cy, y2 = p[1] * cp - z1 * sp, z2 = p[1] * sp + z1 * cp, k = 4 / (4 - z2);
        return {x: W / 2 + x1 * R * k, y: H / 2 - y2 * R * k, z: z2}; };
      if (S.axes){ const o = pr([-c[0] / sz, -c[1] / sz, -c[2] / sz]); [['x', '#e5534b', [1, 0, 0]], ['y', '#57ab5a', [0, 1, 0]], ['z', '#539bf5', [0, 0, 1]]].forEach(([n, col, d]) => {
        const e = pr(d.map((v, a) => (v * 1.3) + (-c[a] / sz))); g.strokeStyle = col; g.globalAlpha = .55; g.lineWidth = 1.2; g.setLineDash([4, 3]); g.beginPath(); g.moveTo(o.x, o.y); g.lineTo(e.x, e.y); g.stroke();
        g.setLineDash([]); g.globalAlpha = .9; g.fillStyle = col; g.font = '11px sans-serif'; g.fillText(n, e.x + 3, e.y - 3); }); g.globalAlpha = 1; }
      const Q = V.map(pr);
      const faces = S.F.map((f, k) => ({f, k, z: f.p.reduce((s, i) => s + Q[i].z, 0) / f.p.length})).sort((a, b) => a.z - b.z);
      for (const {f, k} of faces){ g.beginPath(); f.p.forEach((i, j) => j ? g.lineTo(Q[i].x, Q[i].y) : g.moveTo(Q[i].x, Q[i].y)); g.closePath();
        g.globalAlpha = sel < 0 ? .72 : (sel === k ? .92 : .14); g.fillStyle = f.color; g.fill(); g.globalAlpha = sel < 0 || sel === k ? .95 : .3; g.strokeStyle = sel === k ? '#fff' : f.color; g.lineWidth = sel === k ? 2 : 1; g.stroke(); }
      g.globalAlpha = .85; g.strokeStyle = fg; g.lineWidth = 1.5; for (const [a, b] of S.L){ g.beginPath(); g.moveTo(Q[a].x, Q[a].y); g.lineTo(Q[b].x, Q[b].y); g.stroke(); } g.globalAlpha = 1;
      const hot = sel >= 0 ? new Set(S.F[sel].p) : null;
      if (S.showLabels) Q.forEach((q, i) => { if (hot && !hot.has(i)) return; const t = lab(i); g.font = 'bold 11px sans-serif'; const w = Math.max(18, g.measureText(t).width + 10);
        g.fillStyle = 'rgba(20,20,28,.85)'; g.strokeStyle = fg; g.lineWidth = 1; g.beginPath(); g.arc(q.x, q.y, w / 2, 0, 7); g.fill(); g.stroke(); g.fillStyle = '#fff'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(t, q.x, q.y + .5); g.textAlign = 'start'; g.textBaseline = 'alphabetic'; });
      else Q.forEach(q => { g.fillStyle = fg; g.beginPath(); g.arc(q.x, q.y, 2.5, 0, 7); g.fill(); }); }
    function loop(){ raf = 0; if (!box.isConnected && !box._kept) return; if (auto){ st.yaw += .012; draw(); raf = requestAnimationFrame(loop); } }
    function setAuto(v){ auto = v; bAuto.classList.toggle('on', v); if (v && !raf) raf = requestAnimationFrame(loop); }
    function showFace(k){ sel = sel === k ? -1 : k; [...bar.querySelectorAll('.ag3f')].forEach((b, j) => b.classList.toggle('on', j === sel));
      if (sel < 0){ info.hidden = true; } else { const f = S.F[sel]; info.hidden = false; info.textContent = 'indices: ' + f.p.map(lab).join(', ') + '\n' + f.p.map(i => lab(i) + ': ' + fmt(S.P[i])).join('\n'); } draw(); }
    const mk = (html, fn, cls) => { const b = document.createElement('button'); b.type = 'button'; if (cls) b.className = cls; b.innerHTML = html; b.onclick = fn; bar.appendChild(b); return b; };
    const bAuto = mk('لف تلقائي', () => setAuto(!auto));
    mk('رجّعه زي ما كان', () => { st = {...V0}; setAuto(false); if (sel >= 0) showFace(sel); else draw(); });
    S.F.forEach((f, k) => mk(`<i style="background:${f.color}"></i>${esc(f.name || ('وش ' + (k + 1)))}`, () => showFace(k), 'ag3f'));
    // drag = rotate, two fingers / wheel = zoom
    const pts = new Map(); let last = null, pinch = 0;
    cv.addEventListener('pointerdown', e => { cv.setPointerCapture(e.pointerId); pts.set(e.pointerId, [e.clientX, e.clientY]); setAuto(false); last = [e.clientX, e.clientY];
      if (pts.size === 2){ const [a, b] = [...pts.values()]; pinch = Math.hypot(a[0] - b[0], a[1] - b[1]); } });
    cv.addEventListener('pointermove', e => { if (!pts.has(e.pointerId)) return; pts.set(e.pointerId, [e.clientX, e.clientY]);
      if (pts.size === 2){ const [a, b] = [...pts.values()], d = Math.hypot(a[0] - b[0], a[1] - b[1]); if (pinch) st.zoom = Math.max(.4, Math.min(4, st.zoom * d / pinch)); pinch = d; draw(); return; }
      st.yaw += (e.clientX - last[0]) * .01; st.pitch = Math.max(-1.5, Math.min(1.5, st.pitch + (e.clientY - last[1]) * .01)); last = [e.clientX, e.clientY]; draw(); });
    const up = e => { pts.delete(e.pointerId); if (pts.size < 2) pinch = 0; if (pts.size === 1) last = [...pts.values()][0]; };
    cv.addEventListener('pointerup', up); cv.addEventListener('pointercancel', up);
    cv.addEventListener('wheel', e => { e.preventDefault(); st.zoom = Math.max(.4, Math.min(4, st.zoom * (e.deltaY < 0 ? 1.1 : .9))); draw(); }, {passive: false});
    box._draw = draw; requestAnimationFrame(draw); return box; }
  // ---------- scene3d + "camera": two panels like an OpenGL camera lesson — 1) the scene from above with the camera and what it can see, 2) what the camera sees; drag = look around, W A S D = walk
  function s3cam(S){ s3css();
    const C = S.cam, box = document.createElement('div'); box.className = 'ag3d ag3cam'; box.dir = 'rtl';
    box.innerHTML = (S.title ? `<div class="ag3t">${esc(S.title)}</div>` : '') +
      '<div class="ag3h" style="opacity:.85;font-size:.8rem">1) الكاميرا من فوق (الشكل في النص، والكاميرا المثلث البرتقالي)</div><canvas class="ag3top"></canvas>' +
      '<div class="ag3h" style="opacity:.85;font-size:.8rem;margin-top:8px">2) الشباك: اللي الكاميرا شايفاه (اسحب عليه بإصبعك عشان تلف الكاميرا)</div><canvas class="ag3view"></canvas>' +
      '<div class="ag3b ag3wasd"></div><div class="ag3i" dir="ltr"></div><div class="ag3b ag3fb"></div>';
    const top = box.querySelector('.ag3top'), view = box.querySelector('.ag3view'), info = box.querySelector('.ag3i'), wasd = box.querySelector('.ag3wasd'), fb = box.querySelector('.ag3fb');
    const gt = top.getContext('2d'), gv = view.getContext('2d');
    const P = S.P, mn = [0, 1, 2].map(a => Math.min(...P.map(p => p[a]))), mx = [0, 1, 2].map(a => Math.max(...P.map(p => p[a])));
    const ext = Math.max(1e-6, ...mx.map((v, a) => v - mn[a])), step = ext * .08;
    const D = d => d * Math.PI / 180, R2 = v => (Math.abs(v) < .005 ? 0 : v).toFixed(2);
    const V0 = {pos: C.pos.slice(), yaw: C.yaw, pitch: C.pitch}; let cam = {pos: C.pos.slice(), yaw: C.yaw, pitch: C.pitch}, sel = -1;
    const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]], dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
    const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]], nrm = a => { const l = Math.hypot(...a) || 1; return a.map(v => v / l); };
    const basis = () => { const f = nrm([Math.cos(D(cam.yaw)) * Math.cos(D(cam.pitch)), Math.sin(D(cam.pitch)), Math.sin(D(cam.yaw)) * Math.cos(D(cam.pitch))]); const r = nrm(cross(f, [0, 1, 0])); return {f, r, u: cross(r, f)}; };
    const size = (cv, ratio) => { const dpr = window.devicePixelRatio || 1, W = cv.clientWidth || 300, H = Math.round(Math.min(300, W * ratio));
      if (cv.width !== Math.round(W * dpr) || cv.height !== Math.round(H * dpr)){ cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr); cv.style.height = H + 'px'; }
      const g = cv.getContext('2d'); g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, W, H); return [W, H]; };
    const fade = k => sel < 0 || sel === k;
    function drawTop(){ const [W, H] = size(top, .62), fg = getComputedStyle(box).color || '#ddd', {f} = basis();
      // fit the shape and the camera, x to the right and z downwards (as seen from above)
      const xs = P.map(p => p[0]).concat(cam.pos[0]), zs = P.map(p => p[2]).concat(cam.pos[2]);
      const cx = (Math.min(...xs) + Math.max(...xs)) / 2, cz = (Math.min(...zs) + Math.max(...zs)) / 2;
      const span = Math.max(ext, Math.max(...xs) - Math.min(...xs), Math.max(...zs) - Math.min(...zs)) * 1.5, s = Math.min(W, H) / span;
      const T = p => [W / 2 + (p[0] - cx) * s, H / 2 + (p[2] - cz) * s];
      gt.globalAlpha = .35; gt.strokeStyle = fg; gt.lineWidth = 1; gt.setLineDash([2, 4]); const o = T([0, 0, 0]);
      gt.beginPath(); gt.moveTo(0, o[1]); gt.lineTo(W, o[1]); gt.moveTo(o[0], 0); gt.lineTo(o[0], H); gt.stroke(); gt.setLineDash([]); gt.globalAlpha = .8; gt.fillStyle = fg; gt.font = '11px sans-serif';
      gt.fillText('x', W - 12, o[1] - 5); gt.fillText('z', o[0] + 5, H - 5); gt.globalAlpha = 1;
      // what the camera can see, as a wedge on the floor
      const half = D(C.fov) / 2 * (view.clientWidth || 300) / Math.max(1, view.clientHeight || 240), fy = Math.atan2(f[2], f[0]), L = span * .62, c0 = T(cam.pos);
      gt.beginPath(); gt.moveTo(...c0); gt.lineTo(c0[0] + Math.cos(fy - half) * L * s, c0[1] + Math.sin(fy - half) * L * s); gt.lineTo(c0[0] + Math.cos(fy + half) * L * s, c0[1] + Math.sin(fy + half) * L * s); gt.closePath();
      gt.fillStyle = 'rgba(245,158,11,.16)'; gt.fill(); gt.strokeStyle = 'rgba(245,158,11,.55)'; gt.stroke();
      S.F.map((F, k) => ({F, k, y: F.p.reduce((a, i) => a + P[i][1], 0) / F.p.length})).sort((a, b) => a.y - b.y).forEach(({F, k}) => {
        gt.beginPath(); F.p.forEach((i, j) => j ? gt.lineTo(...T(P[i])) : gt.moveTo(...T(P[i]))); gt.closePath(); gt.globalAlpha = fade(k) ? .8 : .15; gt.fillStyle = F.color; gt.fill();
        gt.globalAlpha = fade(k) ? .9 : .2; gt.strokeStyle = fg; gt.lineWidth = .8; gt.stroke(); }); gt.globalAlpha = 1;
      gt.strokeStyle = fg; gt.globalAlpha = .7; for (const [a, b] of S.L){ gt.beginPath(); gt.moveTo(...T(P[a])); gt.lineTo(...T(P[b])); gt.stroke(); } gt.globalAlpha = 1;
      // the camera: a small orange triangle and an arrow where it looks
      const ax = Math.cos(fy), az = Math.sin(fy), tip = [c0[0] + ax * 34, c0[1] + az * 34];
      gt.strokeStyle = '#f59e0b'; gt.fillStyle = '#f59e0b'; gt.lineWidth = 2; gt.beginPath(); gt.moveTo(...c0); gt.lineTo(...tip); gt.stroke();
      gt.beginPath(); gt.moveTo(...tip); gt.lineTo(tip[0] - ax * 9 - az * 5, tip[1] - az * 9 + ax * 5); gt.lineTo(tip[0] - ax * 9 + az * 5, tip[1] - az * 9 - ax * 5); gt.fill();
      gt.beginPath(); gt.moveTo(c0[0] + ax * 6, c0[1] + az * 6); gt.lineTo(c0[0] - ax * 6 - az * 6, c0[1] - az * 6 + ax * 6); gt.lineTo(c0[0] - ax * 6 + az * 6, c0[1] - az * 6 - ax * 6); gt.fill(); }
    function drawView(){ const [W, H] = size(view, .75), fg = getComputedStyle(box).color || '#ddd', {f, r, u} = basis(), fl = (H / 2) / Math.tan(D(C.fov) / 2), near = ext * .02;
      gv.strokeStyle = fg; gv.globalAlpha = .3; gv.strokeRect(.5, .5, W - 1, H - 1); gv.globalAlpha = 1;
      const toCam = p => { const d = sub(p, cam.pos); return [dot(d, r), dot(d, u), dot(d, f)]; }, scr = q => [W / 2 + q[0] / q[2] * fl, H / 2 - q[1] / q[2] * fl];
      const clip = poly => { const out = []; for (let i = 0; i < poly.length; i++){ const a = poly[i], b = poly[(i + 1) % poly.length], ia = a[2] >= near, ib = b[2] >= near;
          if (ia) out.push(a); if (ia !== ib){ const t = (near - a[2]) / (b[2] - a[2]); out.push([a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, near]); } } return out; };
      const Q = P.map(toCam);
      S.F.map((F, k) => ({F, k, z: F.p.reduce((a, i) => a + Q[i][2], 0) / F.p.length})).sort((a, b) => b.z - a.z).forEach(({F, k}) => { const poly = clip(F.p.map(i => Q[i])); if (poly.length < 3) return;
        gv.beginPath(); poly.forEach((q, j) => j ? gv.lineTo(...scr(q)) : gv.moveTo(...scr(q))); gv.closePath(); gv.globalAlpha = fade(k) ? .88 : .15; gv.fillStyle = F.color; gv.fill();
        gv.globalAlpha = fade(k) ? .6 : .15; gv.strokeStyle = '#fff'; gv.lineWidth = .8; gv.stroke(); }); gv.globalAlpha = 1;
      gv.strokeStyle = fg; gv.lineWidth = 1.4; for (const [a, b] of S.L){ const seg = clip([Q[a], Q[b]]); if (seg.length >= 2){ gv.beginPath(); gv.moveTo(...scr(seg[0])); gv.lineTo(...scr(seg[1])); gv.stroke(); } }
      if (S.showLabels) Q.forEach((q, i) => { if (q[2] < near || (sel >= 0 && !S.F[sel].p.includes(i))) return; const [x, y] = scr(q); if (x < -20 || y < -20 || x > W + 20 || y > H + 20) return;
        const t = S.names && S.names[i] != null ? S.names[i] : String(S.base + i); gv.font = 'bold 10px sans-serif'; const w = Math.max(16, gv.measureText(t).width + 8);
        gv.fillStyle = 'rgba(20,20,28,.8)'; gv.beginPath(); gv.arc(x, y, w / 2, 0, 7); gv.fill(); gv.fillStyle = '#fff'; gv.textAlign = 'center'; gv.textBaseline = 'middle'; gv.fillText(t, x, y + .5); gv.textAlign = 'start'; gv.textBaseline = 'alphabetic'; });
      gv.fillStyle = fg; gv.globalAlpha = .5; gv.fillRect(W / 2 - 5, H / 2 - .5, 10, 1); gv.fillRect(W / 2 - .5, H / 2 - 5, 1, 10); gv.globalAlpha = 1;
      const v3 = v => '<bdi dir="ltr">(' + v.map(R2).join(', ') + ')</bdi>'; info.style.whiteSpace = 'normal';
      info.innerHTML = '<div dir="rtl" style="text-align:right">مكانها (Position): ' + v3(cam.pos) + '</div><div dir="rtl" style="text-align:right">بتبص ناحية (Front): ' + v3(f) + '</div><div dir="rtl" style="text-align:right">yaw <bdi dir="ltr">' + cam.yaw.toFixed(0) + '°</bdi> · pitch <bdi dir="ltr">' + cam.pitch.toFixed(0) + '°</bdi></div>'; }
    const draw = () => { drawTop(); drawView(); };
    const move = k => { const {f, r} = basis(); const d = {w: f, s: f.map(v => -v), a: r.map(v => -v), d: r}[k]; cam.pos = cam.pos.map((v, i) => v + d[i] * step); draw(); };
    [['w', 'W · قدام'], ['s', 'S · ورا'], ['a', 'A · شمال'], ['d', 'D · يمين']].forEach(([k, t]) => { const b = document.createElement('button'); b.type = 'button'; b.textContent = t; b.style.flex = '1';
      let rep = 0; const stop = () => { clearInterval(rep); rep = 0; };
      b.addEventListener('pointerdown', e => { e.preventDefault(); move(k); stop(); rep = setInterval(() => move(k), 90); }); ['pointerup', 'pointerleave', 'pointercancel'].forEach(ev => b.addEventListener(ev, stop)); wasd.appendChild(b); });
    const mk = (html, fn, cls) => { const b = document.createElement('button'); b.type = 'button'; if (cls) b.className = cls; b.innerHTML = html; b.onclick = fn; fb.appendChild(b); return b; };
    mk('رجّع الكاميرا', () => { cam = {pos: V0.pos.slice(), yaw: V0.yaw, pitch: V0.pitch}; draw(); });
    S.F.forEach((F, k) => mk(`<i style="background:${F.color}"></i>${esc(F.name || ('وش ' + (k + 1)))}`, () => { sel = sel === k ? -1 : k; [...fb.querySelectorAll('.ag3f')].forEach((b, j) => b.classList.toggle('on', j === sel)); draw(); }, 'ag3f'));
    let last = null; view.tabIndex = 0;
    view.addEventListener('pointerdown', e => { view.setPointerCapture(e.pointerId); last = [e.clientX, e.clientY]; });
    view.addEventListener('pointermove', e => { if (!last) return; cam.yaw += (e.clientX - last[0]) * .35; cam.pitch = Math.max(-89, Math.min(89, cam.pitch - (e.clientY - last[1]) * .35)); last = [e.clientX, e.clientY]; draw(); });
    ['pointerup', 'pointercancel'].forEach(ev => view.addEventListener(ev, () => { last = null; }));
    view.addEventListener('keydown', e => { const k = e.key.toLowerCase(); if ('wasd'.includes(k) && k.length === 1){ move(k); e.preventDefault(); } });
    view.style.cursor = 'grab'; box._draw = draw; requestAnimationFrame(draw); return box; }
  // the answer is redrawn many times while it streams in: keep one built scene per source and move it back in, so it keeps its rotation
  const S3_CACHE = new Map();
  function s3mount(root){ (root || document).querySelectorAll('.ag3slot').forEach(slot => { const key = slot.dataset.s || ''; let box = S3_CACHE.get(key);
      if (!box){ const S = s3parse(decodeURIComponent(key)); if (!S){ slot.outerHTML = '<div class="ag3wait">⚠️ الشكل اللي المساعد وصفه مش مفهوم، فماقدرتش أرسمه.</div>'; return; } box = S.cam ? s3cam(S) : s3build(S); S3_CACHE.set(key, box); if (S3_CACHE.size > 40) S3_CACHE.delete(S3_CACHE.keys().next().value); }
      slot.replaceWith(box); if (box._draw) requestAnimationFrame(box._draw); }); }
  new MutationObserver(ms => { for (const m of ms) for (const n of m.addedNodes) if (n.nodeType === 1 && (n.classList.contains('ag3slot') || n.querySelector('.ag3slot'))){ s3mount(); return; } })
    .observe(document.documentElement, {childList: true, subtree: true});
  window.addEventListener('resize', () => S3_CACHE.forEach(b => { if (b.isConnected && b._draw) b._draw(); }));
  function mdToHtml(t){ const pre = []; t = String(t).replace(/```([\w+-]*)\n?([\s\S]*?)(```|$)/g, (m, lang, c) => { pre.push({lang: (lang || '').toLowerCase(), c: c.replace(/\n+$/, ''), done: m.endsWith('```') && m.length > 6}); return '\u0000' + (pre.length - 1) + '\u0000'; });
    return mdInline(t).replace(/\u0000(\d+)\u0000(<br>)?/g, (m, n) => { const p = pre[+n]; if (p.lang === 'camsim') return '<div class="agcsslot"></div>'; if (p.lang === 'scene3d') return p.done ? `<div class="ag3slot" data-s="${encodeURIComponent(p.c)}"></div>` : '<div class="ag3wait">🧊 بيرسم شكل 3D…</div>'; if (p.lang === 'diagram'){ const svg = p.done ? diagramSvg(p.c) : ''; return svg || `<pre class="agpre" dir="ltr"><code>${esc(p.c)}</code></pre>`; } return `<pre class="agpre" dir="ltr"><code>${esc(p.c)}</code></pre>`; }); }
  function mdInline(t){ return esc(t).replace(/`([^`]+)`/g, '<code dir="ltr">$1</code>').replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>')
      .replace(/^\s*[-•*]\s+(.*)$/gm, '<li>$1</li>').replace(/(<li>.*<\/li>\n?)+/g, m => '<ul>' + m.replace(/\n/g, '') + '</ul>')
      .replace(/خطوة\s+(\d+)((?:\s*(?:و|،|,)\s*\d+)*)/g, (m, n, more) => { const ns = [n, ...(more.match(/\d+/g) || [])].map(Number); return ns.every(x => x >= 1 && x <= ST.length) ? ns.map(x => `<button type="button" class="agchip" data-k="${x - 1}">خطوة ${x} · سطر ${ST[x - 1].ln}</button>`).join(' ') : m; }).replace(/\n/g, '<br>'); }
  function explain(question, after, btn){ if (!SAMPLE) return; btn.disabled = true;
    const ctl = new AbortController();
    const b = document.createElement('div'); b.className = 'agmsg bot claude'; if (after._free || after.dataset.free) b.dataset.free = '1'; b.innerHTML = '<span class="agtag">✨ Claude' + (VIA_BRIDGE ? ' · 🌉 جوه البنش' : '') + (b.dataset.free ? ' · 🌍 حر' : '') + '</span><div class="agct">بيفكّر… (أول مرة هيطلب منك إذن)</div><button type="button" class="agstop">⏹ وقّف</button>';
    after.after(b); log.scrollTop = b.offsetTop - 8; const ct = b.querySelector('.agct'), stop = b.querySelector('.agstop'); stop.onclick = () => ctl.abort();
    const tmp = document.createElement('div'); tmp.innerHTML = after.innerHTML.replace(/<div class="agfb">[\s\S]*$/, ''); const helper = (tmp.textContent || '').replace(/\s+/g, ' ').slice(0, 1500);
    const att = after._att || [], imgs = att.filter(a => a.kind === 'img').map(a => a.blob);
    const free = !!(after._free || after.dataset.free);
    const prompt = free ? FREE_RULES + `\n\n(للمعلومية: المستخدم بيذاكر جرافيكس وOpenGL.)` + freeCtx(question) + attText(att, 60000) + (imgs.length ? `\n\nالمستخدم رفع عدد ${imgs.length} صورة (مرفقة).` : '') + '\n\nالسؤال: ' + question + want3d(question) : RULES + (typeof CAMSIM !== 'undefined' ? CAMSIM.rule(P) : '') + '\n\nحقايق البنش:\n' + AG.context(question) + '\n\nإجابة المساعد المحلي (ممكن تكون ناقصة أو غلط):\n' + helper + attText(att, 60000) + (imgs.length ? `\n\nالمستخدم رفع عدد ${imgs.length} صورة مع السؤال (مرفقة). اقراها واربطها بالبنش لو ليها علاقة.` : '') + '\n\nسؤال المستخدم: ' + question + want3d(question);
    SAMPLE(prompt, {signal: ctl.signal, ...(imgs.length ? {images: imgs} : {}), onText: ({text}) => { ct.innerHTML = mdToHtml(text); }})
      .then(({text, truncated}) => { if (!truncated) trAdd(question, text, 'claude', !!b.dataset.free); ct.innerHTML = mdToHtml(text) + (truncated ? '<br><small>(الرد اتقطع، اسأل عن جزء أصغر)</small>' : ''); if (!truncated && b.dataset.free){ AG.saveFreeLesson(question, text); ct.insertAdjacentHTML('beforeend', '<div class="aglearn">📚 المخ المحلي هيقرا الإجابة دي لو سألته سؤال شبهه.</div>'); }
        if (!truncated && !b.dataset.free){ const n = AG.learnFromClaude(question, text); ct.insertAdjacentHTML('beforeend', `<div class="aglearn">🧠 المساعد حفظ الشرح ده${n ? ` واتعلّم يربط كلمات سؤالك بـ عدد ${n} خطوة` : ''}: لو سألت سؤال شبهه هيجاوبك بيه من غير نت.</div>`); } fixBidi(ct); wire(ct, question); })
      .catch(e => { const code = e && e.code; if (e && e.text) ct.innerHTML = mdToHtml(e.text);
        const msg = e && e.code === 'bridge' ? 'جسر Claude رد بخطأ: ' + esc(e.message || '') : {images_unavailable: 'Claude مش قادر يشوف صور في الصفحة دي.', image_rejected: 'Claude رفض الصورة (نوعها أو حجمها مش مناسب).', cancelled: 'وقّفته.', not_granted: 'الإذن اترفض، فزرار Claude هيختفي في الفتحة دي.', sampling_disabled: 'Claude مش متاح للحساب ده.', rate_limited: 'أسئلة كتير ورا بعض، استنى شوية وجرّب تاني.', session_expired: 'محتاج تسجّل دخول تاني.', refused: 'Claude ماجاوبش على السؤال ده. جرّب صياغة تانية.'}[code] || (VIA_BRIDGE ? 'مش قادر أوصل لجسر Claude. اتأكد إن claude_bridge.py شغال في Termux.' : 'حصلت مشكلة في الاتصال. جرّب تاني بعد شوية.');
        if (!e || !e.text) ct.innerHTML = ''; ct.insertAdjacentHTML('beforeend', `<br><small>${msg}</small>`);
        if (['not_granted', 'sampling_disabled', 'not_declared', 'capability_disabled', 'capability_removed'].includes(code)){ SAMPLE = null; log.querySelectorAll('.agmore').forEach(x => x.remove()); } })
      .finally(() => { stop.remove(); btn.disabled = false; }); }
  // ---------- optional: a local model on this device (llama-server in Termux on the phone, or Ollama-style server on a PC)
  // Only works where the page may reach 127.0.0.1 (the GitHub copy of the bench); inside claude.ai the CSP blocks it, so the button stays hidden.
  const LOCAL_KEY = 'benchHelperLocalBrain';
  const LOCAL = (() => { let c = {}; try { c = JSON.parse(localStorage.getItem(LOCAL_KEY) || '{}'); } catch (e) {} return {url: c.url || 'http://127.0.0.1:8080', think: !!c.think, ok: false, model: '', ctx: 0}; })();
  const saveLocal = () => { try { localStorage.setItem(LOCAL_KEY, JSON.stringify({url: LOCAL.url, think: LOCAL.think})); } catch (e) {} };
  const LOCAL_MAX = 7000; // longest answer the local model may write (thinking included)
  async function probeLocal(){ try { const ctl = new AbortController(); const t = setTimeout(() => ctl.abort(), 2500);
      const r = await fetch(LOCAL.url.replace(/\/$/, '') + '/v1/models', {signal: ctl.signal}); clearTimeout(t);
      if (!r.ok) throw 0; const j = await r.json(); LOCAL.model = String(((j.data || [])[0] || {}).id || 'local').split('/').pop().replace(/\.gguf$/i, ''); LOCAL.ok = true;
      // how much the server can read at once (llama-server -c): the bench sends more of the program when it is big
      try { const pr = await fetch(LOCAL.url.replace(/\/$/, '') + '/props'); const pj = pr.ok ? await pr.json() : {}; LOCAL.ctx = +((pj.default_generation_settings || {}).n_ctx || pj.n_ctx || 0) || 0; } catch (e){ LOCAL.ctx = 0; } }
    catch (e){ LOCAL.ok = false; } return LOCAL.ok; }
  // tokens left for the question after the rules and the longest answer; ~2 characters per token for Egyptian Arabic mixed with code
  const ctxRoom = () => LOCAL.ctx ? Math.max(0, LOCAL.ctx - LOCAL_MAX - 2000) : 0;
  const BIG = () => ctxRoom() >= 16000;
  if (!/claude\.ai|claudeusercontent/.test(location.hostname)) probeLocal();
  // the rule wording is chosen so a small model does not get stuck on it (no «ماتألّفش أرقام»)
  const LOCAL_RULES = 'انت مساعد شرح جوه «بنش» تعليمي بيعرض برنامج C++/OpenGL أو Python اتشغّل فعلاً خطوة بخطوة. ' +
    'جاوب على طول بالعامية المصرية لطالب مبتدئ، في 3 لـ 6 جمل قصيرة، من غير مقدمات. ' +
    'اعتمد على «حقايق البنش» اللي في الرسالة، وخد الأرقام منها هي. لو المعلومة مش فيها قول «مش موجود في البنش». ' +
    'لما تذكر خطوة اكتب «خطوة N»، وخد رقمها من الحقايق بس، ولو مش متأكد ماتكتبش رقم. اكتب الكود بين علامتي `.' +
    ' جاوب السؤال نفسه على طول: ماتعلّقش على «إجابة البحث المحلي» (دي ملاحظات ليك بس)، وماتتكلمش عن الخطوة اللي المستخدم واقف عليها إلا لو السؤال عنها.' + DIAG_RULE;
  const METHOD_RULE = ' لو الحقايق فيها «الطريقة 1» و«الطريقة 2»، اكتب كل طريقة برقمها زي ما هو مكتوب في الحقايق بالظبط (مثلاً: الطريقة 2 = VAO لكل شكل، الطريقة 1 = VAO واحد مشترك)، وماتقولش «الأولى» و«التانية» حسب ترتيب كلامك.';
  const localRules = t => LOCAL_RULES + (/الطريقة [12]/.test(t) ? METHOD_RULE : '') + (typeof CAMSIM !== 'undefined' ? CAMSIM.rule(P) : '');
  // 👍 / 👎 under a local-brain answer; rebuilt after the chat is restored from storage (the question and answer live on the bubble)
  // ---------- Claude grades a local-brain answer (in-page on claude.ai; elsewhere opens a Claude chat with the same prompt)
  const JUDGE_RULES = 'انت مصحّح بيراجع إجابة نموذج ذكاء صناعي صغير شغال على موبايل طالب. اكتب بالعامية المصرية وباختصار، بالشكل ده بالظبط:\n' +
    'التقييم: X من 10\n✅ الصح: (نقط قصيرة)\n❌ الغلط أو الناقص: (نقط قصيرة، ولو مفيش اكتب «مفيش»)\n📝 الإجابة المظبوطة: (من 3 لـ 5 جمل)\n' +
    'خليك دقيق وعادل: ماتنقصش درجات على الأسلوب لو المعنى صح. قبل أي رقم معناه عدد اكتب «عدد».';
  function judgePrompt(b){ const free = !!b.dataset.free;
    return JUDGE_RULES + (free ? '\n\n(سؤال عام، مش لازم يكون عن البنش. احكم من معلوماتك.)' : '\n\nحقايق البنش (من التشغيل الحقيقي، احكم بيها):\n' + AG.context(b.dataset.q)) +
      '\n\nسؤال الطالب: ' + b.dataset.q + '\n\nإجابة النموذج المحلي:\n' + b.dataset.a; }
  function judgeBtn(b){ if (!b.dataset.a) return; b.querySelectorAll('.agjrow').forEach(x => x.remove());
    const row = document.createElement('div'); row.className = 'agfb agjrow';
    row.innerHTML = '<button type="button" class="agjudge">⚖️ خلي Claude يقيّم الإجابة دي</button>'; b.appendChild(row);
    row.querySelector('button').onclick = e => judge(b, e.target); }
  function showJudge(b, text){ const j = document.createElement('div'); j.className = 'agmsg bot claude agjudged';
    j.innerHTML = '<span class="agtag">⚖️ تقييم <bdi>Claude</bdi></span><div class="agct"></div>'; const ct = j.querySelector('.agct'); ct.innerHTML = mdToHtml(text);
    let at = b; while (at.nextElementSibling && at.nextElementSibling.classList.contains('agjudged')) at = at.nextElementSibling; at.after(j);
    const m = /(\d+(?:\.\d+)?)\s*من\s*10/.exec(text); if (m){ j.querySelector('.agtag').innerHTML = `⚖️ تقييم <bdi>Claude</bdi>: ${m[1]} من 10`; if (!/⚖️ \d/.test(b.querySelector('.agtag').textContent)) b.querySelector('.agtag').insertAdjacentText('beforeend', ` · ⚖️ ${m[1]}/10`); }
    fixBidi(ct); wire(ct, b.dataset.q); log.scrollTop = j.offsetTop - 8; }
  function judge(b, btn){ const prompt = judgePrompt(b);
    if (!SAMPLE){ // no Claude inside this page (GitHub copy): open a Claude chat with the request, then paste Claude's reply back here
      let ok = false; (navigator.clipboard ? navigator.clipboard.writeText(prompt).then(() => { ok = true; }).catch(() => {}) : Promise.resolve()).finally(() => {
        const href = 'https://claude.ai/new?q=' + encodeURIComponent(prompt);
        const n = document.createElement('div'); n.className = 'agfb agjpaste';
        n.innerHTML = `<div class="aglearn">1️⃣ ${ok ? 'نسخت طلب التقييم، و' : ''}فتحتلك Claude. لو الخانة هناك فاضية، الصق وابعت. <a href="${href}" target="_blank" rel="noopener">افتح Claude تاني ↗</a></div>` +
          '<div class="aglearn">2️⃣ لما Claude يرد، انسخ رده وارجع هنا والصقه:</div><textarea rows="3" placeholder="الصق رد Claude هنا"></textarea><button type="button" class="agjudge">⚖️ حط رد Claude في الشات</button>';
        btn.parentElement.replaceWith(n);
        n.querySelector('button').onclick = () => { const t = n.querySelector('textarea').value.trim(); if (!t){ n.querySelector('textarea').focus(); return; } n.remove(); showJudge(b, t); };
        try { window.open(href, '_blank', 'noopener'); } catch (x) {} }); return; }
    btn.disabled = true; const ctl = new AbortController();
    const j = document.createElement('div'); j.className = 'agmsg bot claude agjudged'; j.innerHTML = '<span class="agtag">⚖️ Claude بيقيّم المخ المحلي</span><div class="agct">بيراجع…</div><button type="button" class="agstop">⏹ وقّف</button>';
    b.after(j); log.scrollTop = j.offsetTop - 8; const ct = j.querySelector('.agct'), stop = j.querySelector('.agstop'); stop.onclick = () => ctl.abort();
    SAMPLE(prompt, {signal: ctl.signal, onText: ({text}) => { ct.innerHTML = mdToHtml(text); }})
      .then(({text}) => { ct.innerHTML = mdToHtml(text); fixBidi(ct); wire(ct, b.dataset.q);
        const m = /التقييم:\s*(\d+(?:\.\d+)?)\s*من\s*10/.exec(text); if (m){ const sc = +m[1]; j.querySelector('.agtag').innerHTML = `⚖️ تقييم <bdi>Claude</bdi>: ${sc} من 10`; b.querySelector('.agtag').insertAdjacentText('beforeend', ` · ⚖️ ${sc}/10`); }
        let fix = (/📝[^:：\n]*[:：]?\s*([\s\S]+)$/.exec(text) || [])[1]; if (fix) fix = fix.replace(/^[*_\s]+/, '').trim();
        if (fix) trAdd(b.dataset.q, fix.trim(), 'judge', !!b.dataset.free);
        if (fix && b.dataset.free){ AG.saveFreeLesson(b.dataset.q, fix.trim()); j.insertAdjacentHTML('beforeend', '<div class="aglearn">📚 المخ المحلي هيقرا التصحيح ده المرة الجاية لما تسأل سؤال شبهه.</div>'); }
        if (fix && !b.dataset.free){ const k0 = AG.learnFromClaude(b.dataset.q, fix.trim()); j.insertAdjacentHTML('beforeend', `<div class="aglearn">📚 المخ المحلي هيقرا التصحيح ده المرة الجاية${k0 ? `، والمساعد ربطه بـ عدد ${k0} خطوة` : ''}.</div>`); }
        if (false){ const sv = document.createElement('button'); sv.type = 'button'; sv.textContent = '🧠 احفظ الإجابة المظبوطة في تعلّم المساعد';
          sv.onclick = () => { const k = AG.learnFromClaude(b.dataset.q, fix.trim()); sv.replaceWith(Object.assign(document.createElement('span'), {className: 'aglearn', textContent: `🧠 اتحفظت${k ? ` واتربطت بـ عدد ${k} خطوة` : ''}`})); };
          const r = document.createElement('div'); r.className = 'agfb'; r.appendChild(sv); j.appendChild(r); } })
      .catch(e => { ct.innerHTML = '<small>' + ({cancelled: 'وقّفته.', not_granted: 'الإذن اترفض.', rate_limited: 'أسئلة كتير ورا بعض، استنى شوية.'}[e && e.code] || (e && e.code === 'bridge' ? 'جسر Claude رد بخطأ: ' + esc(e.message || '') : 'حصلت مشكلة في الاتصال بـ Claude.')) + '</small>'; })
      .finally(() => { stop.remove(); btn.disabled = false; }); }
  function localFeedback(b){ if (b.dataset.done || !b.dataset.a) return; b.querySelectorAll('.aglfb').forEach(x => x.remove());
    const fb = document.createElement('div'); fb.className = 'agfb aglfb';
    fb.innerHTML = '<button type="button" class="agup" title="الإجابة صح">👍 صح، احفظها</button><button type="button" class="agdown" title="فيها غلط">👎 فيها غلط</button>';
    const done = (v, txt) => { b.dataset.done = v; fb.remove(); b.appendChild(Object.assign(document.createElement('div'), {className: 'aglearn', textContent: txt})); };
    fb.querySelector('.agup').onclick = () => { trAdd(b.dataset.q, b.dataset.a, 'local-👍', !!b.dataset.free); if (b.dataset.free){ done('1', '👍 تمام. (الإجابات الحرة مابتتحفظش في تعلّم البنش، علشان مش من التشغيل الحقيقي.)'); return; } const k = AG.learnFromClaude(b.dataset.q, b.dataset.a); done('1', `🧠 اتحفظت${k ? ` واتربطت بـ عدد ${k} خطوة` : ''}: لو سألت سؤال شبهه هجاوبك بيها على طول.`); robot.setMood('happy'); };
    fb.querySelector('.agdown').onclick = () => done('0', 'تمام، مش هحفظها. جرّب تسأل بصياغة تانية، أو اسأل Claude.');
    b.appendChild(fb); }
  async function askLocal(question, after, btn){ btn.disabled = true;
    const ctl = new AbortController(); let cid = null, think = '', ans = '';
    const b = document.createElement('div'); b.className = 'agmsg bot localb';
    b.innerHTML = `<span class="agtag">🧠 المخ المحلي · ${esc(LOCAL.model)}</span><details class="agthink"${LOCAL.think ? ' open' : ''} hidden><summary>بيفكّر…</summary><div class="agthinkt"></div></details><div class="agct">${LOCAL.think ? 'بيقرا الحقايق وبيفكّر…' : 'بيقرا الحقايق…'}</div><div class="agfb"><button type="button" class="agenough" hidden>✋ كفاية تفكير، جاوب</button><button type="button" class="agstop">⏹ وقّف</button></div>`;
    b.dataset.q = question; after.after(b); log.scrollTop = b.offsetTop - 8;
    const ct = b.querySelector('.agct'), th = b.querySelector('.agthink'), tht = b.querySelector('.agthinkt'), stop = b.querySelector('.agstop'), enough = b.querySelector('.agenough');
    stop.onclick = () => ctl.abort();
    enough.onclick = async () => { enough.disabled = true; enough.textContent = 'بقوله يجاوب…';
      try { const r = await fetch(LOCAL.url.replace(/\/$/, '') + '/v1/chat/completions/control', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({id: cid, action: 'reasoning_end'})}); const j = await r.json().catch(() => ({}));
        if (!r.ok || j.success === false) throw 0; enough.remove(); }
      catch (e){ enough.textContent = 'النسخة دي مش بتدعمه، دوس ⏹ وجرّب «جاوب على طول»'; } };
    const tmp = document.createElement('div'); tmp.innerHTML = after.innerHTML.replace(/<div class="agfb">[\s\S]*$/, ''); tmp.querySelectorAll('details, .agthink, .agtag, .agstat, .aglearn').forEach(x => x.remove()); const helper = (tmp.textContent || '').replace(/\s+/g, ' ').slice(0, 300);
    const big = BIG(), room = ctxRoom(); const user = 'حقايق البنش:\n' + AG.context(question, {short: !big, big, here: /هنا|ده\s|دي\s|الخطو[ةه] (دي|ده)|السطر (ده|دا)|دلوقتي|واقف/.test(question)}) + '\n\nإجابة البحث المحلي (ممكن تكون ناقصة):\n' + helper + '\n\nالسؤال: ' + question + want3d(question);
    const att = after._att || [], imgAtt = att.filter(a => a.kind === 'img');
    const userText = user + attText(att, big ? Math.max(2500, room * 2 - user.length) : 2500) + (imgAtt.length ? `\n\n(المستخدم رفع عدد ${imgAtt.length} صورة مع السؤال، وهي مرفقة.)` : '');
    let content = userText;
    if (imgAtt.length){ content = [{type: 'text', text: userText}]; for (const a of imgAtt) content.push({type: 'image_url', image_url: {url: await toDataURL(a.blob)}}); }
    if (window.__agDayAll && !(after._free || after.dataset.free)) b.querySelector('.agtag').insertAdjacentText('beforeend', ' · 📅 اليوم كله');
    const free = !!(after._free || after.dataset.free); if (free){ b.dataset.free = '1'; b.querySelector('.agtag').insertAdjacentText('beforeend', ' · 🌍 حر');
      const ft = freeCtx(question) + '\n\nالسؤال: ' + question + want3d(question) + attText(att, big ? Math.max(2500, room * 2) : 2500) + (imgAtt.length ? `\n\n(المستخدم رفع عدد ${imgAtt.length} صورة، وهي مرفقة.)` : '');
      if (Array.isArray(content)) content[0].text = ft; else content = ft; }
    const les = AG.lessons(question, free);
    if (les.length){ const lt = '\n\n📚 دروس اتعلّمتها قبل كده من Claude في أسئلة شبه دي (الإجابات دي مظبوطة، استخدمها لو مناسبة للسؤال):\n' + les.map(l => 'س: ' + l.q + '\nج: ' + l.a.slice(0, big ? 4000 : 700)).join('\n\n');
      if (Array.isArray(content)) content[0].text = lt + '\n\n' + content[0].text; else content = lt + '\n\n' + content;
      b.querySelector('.agtag').insertAdjacentText('beforeend', ` · 📚 عدد ${les.length} درس من Claude`); }
    const body = {messages: [{role: 'system', content: free ? FREE_RULES : localRules(Array.isArray(content) ? content.map(c => c.text || '').join(' ') : content)}, {role: 'user', content}], stream: true, temperature: .5, max_tokens: LOCAL.ctx ? Math.max(512, Math.min(LOCAL_MAX, LOCAL.ctx - Math.ceil(JSON.stringify(content).length / 2) - 1500)) : LOCAL_MAX,
      reasoning_format: 'deepseek', reasoning_control: true, chat_template_kwargs: {enable_thinking: LOCAL.think}};
    if (!LOCAL.think) body.reasoning_effort = 'none';
    const t0 = performance.now(); let n = 0, first = 0, fin = '';
    const paint = () => { if (think){ th.hidden = false; tht.textContent = think; th.querySelector('summary').textContent = ans ? `🧠 فكّر إزاي (عدد ${think.split(/\s+/).length} كلمة)` : 'بيفكّر…'; enough.hidden = !!ans || !cid; }
      if (ans) ct.innerHTML = mdToHtml(ans.trim()); };
    fetch(LOCAL.url.replace(/\/$/, '') + '/v1/chat/completions', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body), signal: ctl.signal})
      .then(async r => { if (!r.ok){ const t = await r.text().catch(() => ''); if (imgAtt.length && /image|mmproj|multimodal|vision/i.test(t)) throw new Error('VISION'); throw new Error('HTTP ' + r.status + (t ? ': ' + t.slice(0, 160) : '')); } const rd = r.body.getReader(), dec = new TextDecoder(); let buf = '';
        for (;;){ const {value, done} = await rd.read(); if (done) break; buf += dec.decode(value, {stream: true});
          let i; while ((i = buf.indexOf('\n')) >= 0){ const line = buf.slice(0, i).trim(); buf = buf.slice(i + 1);
            if (!line.startsWith('data:')) continue; const data = line.slice(5).trim(); if (data === '[DONE]') continue;
            let j; try { j = JSON.parse(data); } catch (e){ continue; } if (j.id && !cid) cid = j.id;
            const d = (j.choices && j.choices[0] && j.choices[0].delta) || {};
            if (j.choices && j.choices[0] && j.choices[0].finish_reason) fin = j.choices[0].finish_reason;
            if (d.reasoning_content){ think += d.reasoning_content; n++; }
            if (d.content){ ans += d.content; n++; if (!first) first = performance.now(); }
            paint(); } }
        // a server without reasoning parsing returns <think> inside the text
        const m = /<think>([\s\S]*?)(<\/think>|$)/.exec(ans); if (m){ think += m[1]; ans = ans.replace(/<think>[\s\S]*?(<\/think>|$)/, ''); paint(); }
        if (!ans.trim()) ct.innerHTML = '<small>خلص من غير ما يكتب إجابة. جرّب «جاوب على طول» من 🧠.</small>';
        const sec = (performance.now() - t0) / 1000;
        ct.insertAdjacentHTML('beforeend', `<div class="agstat">عدد ${n} توكن في ${sec.toFixed(1)} ثانية${first ? ` · أول كلمة بعد ${((first - t0) / 1000).toFixed(1)} ثانية` : ''}</div>`);
        if (fin === 'length') ct.insertAdjacentHTML('beforeend', `<div class="agstat">✂️ الرد وصل لأقصى طول (عدد ${LOCAL_MAX} توكن). اسأل عن جزء أصغر، أو قول له «كمّل».</div>`);
        if (ans.trim()){ b.dataset.q = question; b.dataset.a = ans.trim(); localFeedback(b); judgeBtn(b); }
        fixBidi(ct); wire(ct, question); })
      .catch(e => { if (e && e.name === 'AbortError'){ ct.insertAdjacentHTML('beforeend', '<br><small>وقّفته.</small>'); return; }
        if (ans.trim()){ ct.insertAdjacentHTML('beforeend', '<br><small>✂️ الاتصال اتقطع قبل ما الإجابة تخلص.</small>'); return; }
        if (e && e.message === 'VISION'){ ct.innerHTML = '<small>المخ المحلي شغال من غير «عيون». علشان يقرا الصور، شغّل llama-server ومعاه ملف الرؤية <code dir="ltr">--mmproj</code> (الأوامر عند Claude في الشات).</small>'; return; }
        ct.innerHTML = `<small>مش قادر أوصل للمخ المحلي على <code dir="ltr">${esc(LOCAL.url)}</code>. اتأكد إن llama-server شغال في Termux. (${esc(String(e && e.message || e))})</small>`; LOCAL.ok = false; })
      .finally(() => { stop.remove(); enough.remove(); btn.disabled = false; }); }
  // ---------- outside claude.ai (GitHub copy): Claude can't be called from the page, so open a new Claude chat with the question + bench facts
  const ONCLAUDE = /claude\.ai|claudeusercontent/.test(location.hostname);
  async function askClaudeOutside(question, after, btn){
    // the bridge (Claude Code on the phone) may have started after this button was drawn: if it answers, Claude replies right here in the chat
    btn.disabled = true; const viaBridge = await probeBridge(); btn.disabled = false; if (viaBridge && SAMPLE){ const nb = btn; return explain(question, after, nb); }
    const tmp = document.createElement('div'); tmp.innerHTML = after.innerHTML.replace(/<div class="agfb">[\s\S]*$/, ''); const helper = (tmp.textContent || '').replace(/\s+/g, ' ').slice(0, 800);
    const att = after._att || [], nImg = att.filter(a => a.kind === 'img').length;
    const prompt = (after._free || after.dataset.free) ? FREE_RULES + freeCtx(question) + attText(att, 6000) + '\n\nالسؤال: ' + question + want3d(question) : RULES + (typeof CAMSIM !== 'undefined' ? CAMSIM.rule(P) : '') + '\n\nحقايق البنش:\n' + AG.context(question) + '\n\nإجابة المساعد المحلي (ممكن تكون ناقصة أو غلط):\n' + helper + attText(att, 6000) + (nImg ? `\n\n(هرفع عدد ${nImg} صورة مع الرسالة دي.)` : '') + '\n\nسؤال المستخدم: ' + question + want3d(question);
    let copied = false; try { await navigator.clipboard.writeText(prompt); copied = true; } catch (e) {}
    const a = document.createElement('a'); a.href = 'https://claude.ai/new?q=' + encodeURIComponent(prompt); a.target = '_blank'; a.rel = 'noopener'; a.textContent = 'افتح Claude ↗';
    const n = document.createElement('div'); n.className = 'aglearn'; n.append(copied ? '✔ نسخت السؤال ومعاه حقايق البنش. ' : '', a, copied ? ' ولو لقيت الخانة فاضية، الصق.' : '', nImg ? ' 📎 الصور مابتتنقلش لوحدها: ارفعها بنفسك في شات Claude.' : '');
    btn.replaceWith(n); try { window.open(a.href, '_blank', 'noopener'); } catch (e) {} }
  const AUTO_KEY = 'benchHelperAutoClaude';
  const autoClaude = () => { try { return localStorage.getItem(AUTO_KEY) === '1'; } catch (e){ return false; } };
  function brain(){ ensure(); const st = AG.modelStats(); const kinds = {up: '👍', pick: '👎 واخترت', click: 'دوست خطوة', claude: 'من Claude', fb: 'تصحيح'};
    const b = bubble('bot brain', `<b>🧠 اللي اتعلّمته في البرنامج ده</b><ul><li>عدد ${st.n} درس اتعلّمته (من كل البرامج).</li><li>📚 دروس Claude اللي المخ المحلي بيقراها: عدد ${AG.lessonCount().bench} عن البنش، وعدد ${AG.lessonCount().free} أسئلة حرة.</li><li>عدد ${st.feats} كلمة ليها أوزان في البرنامج ده.</li></ul>` +
      (st.top.length ? `<b>أقوى الروابط اللي اتعلّمتها:</b><ul>${st.top.map(x => `<li>«${esc(x.f.replace(/^§/, ''))}» ← <code dir="ltr">${esc(String(x.code).slice(0, 50))}</code> (${x.w.toFixed(2)})</li>`).join('')}</ul>` : '<p>لسه ماتعلّمتش حاجة في البرنامج ده. دوس 👍 أو 👎 تحت الإجابات، أو اسأل Claude.</p>') +
      (st.log.length ? `<b>آخر الدروس:</b><ul>${st.log.map(x => `<li>${kinds[x.k] || x.k}: «${esc(x.q)}»</li>`).join('')}</ul>` : '') +
      `<label class="agauto"><input type="checkbox" id="agAuto"${autoClaude() ? ' checked' : ''}> لما أكون مش متأكد، اسأل Claude لوحدك واتعلّم من إجابته${SAMPLE ? '' : ' (مش متاح هنا: محتاج الصفحة المنشورة ونت)'}</label>` +
      `<div class="aglocalset"><b>🌉 جسر Claude</b> <span class="agbst">${VIA_BRIDGE ? '✅ متوصّل: Claude بيرد جوه البنش' : (SAMPLE ? '✅ Claude جوه الصفحة' : '⚪ مش متوصّل: شغّل claude_bridge.py في Termux')}</span> <button type="button" class="agbchk">اختبر</button></div>` +
      `<div class="aglocalset"><b>🧠 المخ المحلي</b> <span class="aglst">${LOCAL.ok ? '✅ متوصّل: ' + esc(LOCAL.model) + (LOCAL.ctx ? ` · السياق عدد ${LOCAL.ctx} توكن${BIG() ? ' (بيقرا البرنامج كله)' : ''}` : '') : '⚪ مش متوصّل'}</span><div class="agrow"><input class="agurl" dir="ltr" value="${esc(LOCAL.url)}"><button type="button" class="agchk">اختبر</button></div><label class="agauto"><input type="radio" name="agmode" value="0"${LOCAL.think ? '' : ' checked'}> ⚡ جاوب على طول (أسرع)</label><label class="agauto"><input type="radio" name="agmode" value="1"${LOCAL.think ? ' checked' : ''}> 🧠 فكّر شوية قبل ما تجاوب (أبطأ)</label></div>` +
      `<div class="agfb"><button type="button" class="agexp">📋 انسخ اللي اتعلّمته</button><button type="button" class="agimp">📥 ضيف تعلّم من جهاز تاني</button><button type="button" class="agrst">🗑️ امسح التعلّم</button></div>` +
      `<div class="agfb"><button type="button" class="agtrexp">📦 نزّل بيانات تدريب المخ (عدد ${trAll().length} من ${TR_GOAL} مثال)</button><a class="agtrhow" href="https://colab.research.google.com/github/ssas1qasd-boop/SOLI/blob/main/train/finetune_mokh.ipynb" target="_blank" rel="noopener">🎓 درّبه على Colab ↗</a></div>` +
      `<div class="agfb"><button type="button" class="agchexp">💬 انسخ كل المحادثات (عدد ${Object.keys(chatAll()).length} برنامج)</button><button type="button" class="agchimp">📥 رجّع محادثات</button></div><div class="agchbox" hidden><textarea rows="3" placeholder="الصق هنا المحادثات اللي نسختها"></textarea><button type="button" class="agchgo">رجّعها</button></div><div class="agimpbox" hidden><textarea rows="3" placeholder="الصق هنا اللي نسخته من جهاز تاني"></textarea><button type="button" class="agimpgo">ضيف</button></div>`);
    b.querySelector('.agbchk').onclick = async e => { e.target.textContent = '…'; const ok = await probeBridge(); e.target.textContent = 'اختبر'; b.querySelector('.agbst').textContent = ok ? (VIA_BRIDGE ? '✅ متوصّل: Claude بيرد جوه البنش' : '✅ Claude جوه الصفحة') : '❌ مش لاقيه. شغّل python ~/claude_bridge.py في Termux'; };
    b.querySelectorAll('input[name=agmode]').forEach(r => r.onchange = () => { LOCAL.think = r.value === '1' && r.checked; saveLocal(); });
    b.querySelector('.agchk').onclick = async e => { LOCAL.url = b.querySelector('.agurl').value.trim() || LOCAL.url; saveLocal(); e.target.textContent = '…';
      const ok = await probeLocal(); e.target.textContent = 'اختبر'; b.querySelector('.aglst').textContent = ok ? '✅ متوصّل: ' + LOCAL.model : '❌ مش لاقيه. شغّل llama-server في Termux';
      if (ok) log.querySelectorAll('.agmsg.bot .agfb').forEach(fb => { if (!fb.querySelector('.aglocal') && fb.querySelector('.agup, .agmore')){ /* new answers will show the button */ } }); };
    b.querySelector('#agAuto').onchange = e => { try { localStorage.setItem(AUTO_KEY, e.target.checked ? '1' : '0'); } catch (x) {} };
    b.querySelector('.agexp').onclick = async e => { const t = AG.exportModel(); try { await navigator.clipboard.writeText(t); e.target.textContent = '✔ اتنسخ'; } catch (x){ const ta = b.querySelector('textarea'); b.querySelector('.agimpbox').hidden = false; ta.value = t; ta.select(); e.target.textContent = 'انسخه من المربع'; } };
    b.querySelector('.agimp').onclick = () => { b.querySelector('.agimpbox').hidden = false; b.querySelector('textarea').value = ''; b.querySelector('textarea').focus(); };
    b.querySelector('.agimpgo').onclick = e => { try { AG.importModel(b.querySelector('textarea').value); e.target.textContent = '✔ اتضاف'; } catch (x){ e.target.textContent = 'النص ده مش تعلّم صالح'; } };
    b.querySelector('.agtrexp').onclick = async e => { const n = trAll().length; if (!n){ e.target.textContent = 'لسه مفيش أمثلة: اسأل Claude أو خليه يقيّم'; return; }
      if (ONCLAUDE){ try { await navigator.clipboard.writeText(trJSONL()); e.target.textContent = `✔ نسخت عدد ${n} مثال: الصقهم في ملف اسمه mokh_train.jsonl، أو نزّلهم من نسخة GitHub`; } catch (x){ e.target.textContent = 'النسخ اترفض هنا: نزّلهم من نسخة GitHub'; } return; }
      const blob = new Blob([trJSONL()], {type: 'application/jsonl'}); const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'mokh_train.jsonl'; document.body.appendChild(a); a.click(); a.remove();
      setTimeout(() => URL.revokeObjectURL(a.href), 4000); e.target.textContent = `✔ نزل mokh_train.jsonl (عدد ${n} مثال)`; };
    b.querySelector('.agchexp').onclick = async e => { chatSave(); const t = JSON.stringify({benchChats: 1, chats: chatAll(), archive: archAll()}); try { await navigator.clipboard.writeText(t); e.target.textContent = '✔ اتنسخت، الصقها في أي مكان تحفظ فيه'; } catch (x){ const bx = b.querySelector('.agchbox'); bx.hidden = false; const ta = bx.querySelector('textarea'); ta.value = t; ta.select(); e.target.textContent = 'انسخها من المربع'; } };
    b.querySelector('.agchimp').onclick = () => { const bx = b.querySelector('.agchbox'); bx.hidden = false; bx.querySelector('textarea').value = ''; bx.querySelector('textarea').focus(); };
    b.querySelector('.agchgo').onclick = e => { try { const j = JSON.parse(b.querySelector('.agchbox textarea').value); const inc = j && j.chats; if (!inc || typeof inc !== 'object') throw 0;
        if (Array.isArray(j.archive)){ const A = archAll(), ids = new Set(A.map(a => a.id)); j.archive.forEach(a => { if (a && a.id && typeof a.h === 'string' && !ids.has(a.id)) A.push(a); }); A.sort((x, y) => x.t - y.t); archWrite(A); }
        const all = chatAll(); let n = 0; for (const [k, v] of Object.entries(inc)){ if (!v || typeof v.h !== 'string' || !PROGS.some(p => p.id === k)) continue; if (!all[k] || (v.t || 0) > (all[k].t || 0)){ all[k] = {h: v.h, t: v.t || Date.now(), open: false}; n++; } }
        chatWrite(all); e.target.textContent = `✔ رجعت عدد ${n} محادثة`; } catch (x){ e.target.textContent = 'النص ده مش محادثات صالحة'; } };
    b.querySelector('.agrst').onclick = e => { if (e.target.dataset.sure){ AG.resetModel(); e.target.textContent = '✔ اتمسح'; } else { e.target.dataset.sure = '1'; e.target.textContent = 'متأكد؟ دوس تاني للمسح'; } };
    sug.hidden = true; }
  $('agBrain').onclick = brain;
  $('agForm').addEventListener('submit', e => { e.preventDefault(); ask(); });
  $('agNew').onclick = () => { const saved = archiveCurrent(); log.innerHTML = ''; chatSave(); AG.reset(); renderSug();
    if (saved){ const n = bubble('bot', '🕘 المحادثة اللي فاتت اتحفظت في <b>المحادثات القديمة</b>. <button type="button" class="agopenarch">افتحها</button>'); n.querySelector('button').onclick = openArchive; } q.focus(); };
  $('agHist').onclick = openArchive;
  $('agX').onclick = () => openChat(false);
  fab.onclick = () => openChat(true);
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !box.hidden) openChat(false); });
  // tapping the robot in the 3D scene opens the chat
  const ray = new T.Raycaster(); let pd = null;
  stage.addEventListener('pointerdown', e => { pd = [e.clientX, e.clientY]; });
  stage.addEventListener('pointerup', e => { if (!pd || Math.hypot(e.clientX - pd[0], e.clientY - pd[1]) > 8) return; const r = stage.getBoundingClientRect();
    ray.setFromCamera(new T.Vector2((e.clientX - r.left) / r.width * 2 - 1, -(e.clientY - r.top) / r.height * 2 + 1), cam);
    if (ray.intersectObject(robot.g, true).length){ openChat(true); robot.setMood('happy'); } });
  // ---------- 📋 copy button on every message
  function addCopy(m){ if (m.querySelector(':scope > .agcopy') || m.classList.contains('wait')) return; const c = document.createElement('button'); c.type = 'button'; c.className = 'agcopy'; c.title = 'انسخ الرسالة'; c.setAttribute('aria-label', 'انسخ الرسالة'); c.textContent = '📋';
    c.onclick = async e => { e.stopPropagation(); const t = m.cloneNode(true); t.querySelectorAll('.agcopy, .agfb, .agstop, .agenough, .agthink, details, textarea, .agstat').forEach(x => x.remove());
      t.querySelectorAll('br').forEach(x => x.replaceWith('\n')); t.querySelectorAll('.agtag, li, p, div, pre').forEach(x => x.append('\n')); t.querySelectorAll('li').forEach(x => x.prepend('• '));
      const txt = (t.textContent || '').replace(/[ \t]+\n/g, '\n').replace(/\n{3,}/g, '\n\n').trim();
      try { await navigator.clipboard.writeText(txt); c.textContent = '✔'; } catch (x){ const r = document.createRange(); r.selectNodeContents(m.querySelector('.agct') || m); const sel = getSelection(); sel.removeAllRanges(); sel.addRange(r); c.textContent = '⬚'; }
      setTimeout(() => { c.textContent = '📋'; }, 1500); };
    m.prepend(c); }
  new MutationObserver(() => log.querySelectorAll(':scope > .agmsg:not(.brain)').forEach(addCopy)).observe(log, {childList: true, subtree: true, attributes: true, attributeFilter: ['class']});
  // ---------- keep the chat when the phone drops the page from memory (Chrome reloads it when you come back)
  const CHAT_KEY = 'benchHelperChat';
  const chatAll = () => { try { return JSON.parse(localStorage.getItem(CHAT_KEY) || '{}'); } catch (e){ return {}; } };
  function chatSave(){ try { const all = chatAll(); const c = log.cloneNode(true);
      c.querySelectorAll('.agmsg.brain, .agmsg.agarch').forEach(x => x.remove()); c.querySelectorAll('.agopenarch').forEach(x => x.closest('.agmsg').remove()); c.querySelectorAll('.agfb, .agstop, .agenough, .agimpbox, .agchbox, .aglocalset, .agcopy').forEach(x => x.remove()); c.querySelectorAll('.wait').forEach(x => x.remove());
      const h = c.innerHTML.trim();
      if (h) all[P.id] = {h, t: Date.now(), open: !box.hidden}; else delete all[P.id];
      chatWrite(all); } catch (e) {} }
  // ---------- old chats: «جديد» moves the current chat here instead of deleting it
  const ARCH_KEY = 'benchHelperChatArchive';
  const archAll = () => { try { return JSON.parse(localStorage.getItem(ARCH_KEY) || '[]'); } catch (e){ return []; } };
  function archWrite(L){ for (;;){ try { localStorage.setItem(ARCH_KEY, JSON.stringify(L)); return true; } catch (e){ if (!L.length) return false; L.shift(); } } }
  function archiveCurrent(){ chatSave(); const cur = chatAll()[P.id]; if (!cur || !cur.h) return false;
    const tmp = document.createElement('div'); tmp.innerHTML = cur.h; const me = tmp.querySelector('.agmsg.me'); const first = me ? me.textContent.replace(/\s+/g, ' ').trim().slice(0, 70) : '';
    const n = tmp.querySelectorAll('.agmsg.me').length; if (!n) return false;
    const L = archAll(); L.push({id: Date.now().toString(36), pid: P.id, title: P.title, h: cur.h, t: Date.now(), first, n}); archWrite(L); return true; }
  function openArchive(){ ensure(); const L = archAll().slice().reverse(); const fmt = t => new Date(t).toLocaleString('ar-EG', {day: 'numeric', month: 'short', hour: 'numeric', minute: '2-digit'});
    const row = x => `<li class="agarch-it" data-id="${x.id}"><div><b>${esc(x.first || '(من غير سؤال)')}</b><small>${esc(x.title)} · عدد ${x.n} سؤال · ${fmt(x.t)}</small></div><span><button type="button" class="agaopen">افتح</button><button type="button" class="agadel" title="امسح">🗑</button></span></li>`;
    const here = L.filter(x => x.pid === P.id), other = L.filter(x => x.pid !== P.id);
    const b = bubble('bot brain agarch', `<b>🕘 المحادثات القديمة</b>` + (L.length ? '' : '<p>لسه مفيش. لما تدوس «جديد»، المحادثة اللي قبلها بتتحفظ هنا.</p>') +
      (here.length ? `<p class="agarch-h">في البرنامج ده (عدد ${here.length}):</p><ul class="agarch">${here.map(row).join('')}</ul>` : '') +
      (other.length ? `<details><summary>في برامج تانية (عدد ${other.length})</summary><ul class="agarch">${other.map(row).join('')}</ul></details>` : ''));
    b.querySelectorAll('.agaopen').forEach(btn => btn.onclick = () => { const id = btn.closest('li').dataset.id; const x = archAll().find(a => a.id === id); if (!x) return;
      b.remove(); archiveCurrent(); archWrite(archAll().filter(a => a.id !== id)); const all = chatAll(); all[x.pid] = {h: x.h, t: Date.now(), open: true}; chatWrite(all);
      if (x.pid !== P.id) loadProgram(x.pid, false); else { chatRestore(P.id); } openChat(true); log.scrollTop = log.scrollHeight; });
    b.querySelectorAll('.agadel').forEach(btn => btn.onclick = () => { if (!btn.dataset.sure){ btn.dataset.sure = '1'; btn.textContent = 'متأكد؟'; return; }
      const li = btn.closest('li'); archWrite(archAll().filter(a => a.id !== li.dataset.id)); li.remove(); });
    sug.hidden = true; log.scrollTop = b.offsetTop - 8; }
  // no fixed limit: keep every program's chat; only if the browser runs out of room, drop the oldest chats until it fits
  function chatWrite(all){ const ks = Object.keys(all).sort((a, b) => all[a].t - all[b].t);
    for (;;){ try { localStorage.setItem(CHAT_KEY, JSON.stringify(all)); return true; } catch (e){ const k = ks.shift(); if (!k || k === P.id) return false; delete all[k]; } } }
  function chatRestore(id){ const s = chatAll()[id]; if (!s || !s.h) return null; log.innerHTML = s.h; sug.hidden = true; wire(log); fixBidi(log); log.querySelectorAll('.localb[data-a]').forEach(b => { localFeedback(b); judgeBtn(b); });
    // an answer that was still being written when the phone dropped the page: say so and offer to ask again
    log.querySelectorAll('.localb[data-q]:not([data-a])').forEach(b => { if (b.querySelector('.agcut')) return; const n = document.createElement('div'); n.className = 'agfb agcut';
      n.innerHTML = '<span class="aglearn">✂️ الإجابة دي اتقطعت لما خرجت من الصفحة.</span> <button type="button" class="aglocal">🧠 اسأل المخ تاني</button>';
      n.querySelector('button').onclick = e => { const q = b.dataset.q; n.remove(); if (LOCAL.ok) askLocal(q, b, e.target); else { probeLocal().then(ok => ok ? askLocal(q, b, e.target) : b.insertAdjacentHTML('beforeend', '<small>المخ المحلي مش شغال. شغّل llama-server في Termux.</small>')); } };
      b.appendChild(n); });
    return s; }
  let saveT = 0; new MutationObserver(() => { clearTimeout(saveT); saveT = setTimeout(chatSave, 600); }).observe(log, {childList: true, subtree: true, characterData: true});
  document.addEventListener('visibilitychange', () => { if (document.hidden) chatSave(); });
  addEventListener('pagehide', chatSave);
  const _load = loadProgram; loadProgram = function(id, keep, fromChat){ if (!fromChat) chatSave(); const r = _load(id, keep); AG.reset(); if (!fromChat){ if (!chatRestore(P.id)){ log.innerHTML = ''; renderSug(); } } return r; };
  { const s = chatRestore(P.id); if (s){ ensure(); if (s.open) openChat(true); setTimeout(() => { log.scrollTop = log.scrollHeight; }, 50); } }
  window.__agent = {ask: t => { ensure(); return AG.answer(t); }, AG, open: openChat};
})();
