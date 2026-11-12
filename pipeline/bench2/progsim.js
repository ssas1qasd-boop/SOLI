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
    intro: 'اسحب بصباعك على الشباك = الماوس الشمال متداس. البرنامج بيحرك المكعب اللي رقمه <code>picked</code> لحد ما يبقى تحت الماوس.',
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
      if (p.type){ const n = p.type === 'vec2' ? 2 : 3; for (let i = 0; i < n; i++){ const t = document.createElement('input'); t.type = 'number'; t.step = p.step || 1; t.value = V[p.k][i]; t.oninput = () => { const x = parseFloat(t.value); if (!isNaN(x)){ V[p.k][i] = x; upd(); } }; row.appendChild(t); } }
      else { const r = document.createElement('input'); r.type = 'range'; r.min = p.min; r.max = p.max; r.step = p.step; r.value = V[p.k]; const t = document.createElement('input'); t.type = 'number'; t.step = p.step; t.value = V[p.k];
        r.oninput = () => { V[p.k] = +r.value; t.value = r.value; upd(); }; t.oninput = () => { let x = parseFloat(t.value); if (!isNaN(x)){ x = Math.max(+p.min, Math.min(+p.max, x)); V[p.k] = x; r.value = x; upd(); } }; t.onchange = () => { t.value = V[p.k]; }; row.append(r, t); }
      box.appendChild(row); inn.appendChild(box); });
    const syncInputs = () => inn.querySelectorAll('.psp').forEach(b => { const p = d.params.find(q => q.k === b.dataset.k), ins = b.querySelectorAll('input');
      if (p.type) ins.forEach((t, i) => t.value = V[p.k][i]); else ins.forEach(t => t.value = V[p.k]); });
    let last = null;
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
