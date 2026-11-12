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
