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
