(() => {
const $ = id => document.getElementById(id);
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const cssv = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const esc = t => String(t).replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
const nVao = n => +n === 1 ? 'ورقة تعليمات واحدة (VAO)' : +n === 2 ? 'ورقتين تعليمات (VAO)' : `${n} أوراق تعليمات (VAO)`;
const nBuf = n => +n === 1 ? 'صندوق واحد (Buffer)' : +n === 2 ? 'صندوقين (Buffers)' : `${n} صناديق (Buffers)`;
const store = { get(k){ try { return localStorage.getItem(k); } catch(e){ return null; } }, set(k, v){ try { localStorage.setItem(k, v); } catch(e){} } };
if (!window.THREE){ $('story').textContent = 'مكتبة الرسم 3D ما اتحملتش. افتح الصفحة تاني وإنت متوصل بالنت.'; return; }
const T = THREE;
const DATA = window.__BENCH_DATA || JSON.parse($('data').textContent);
const PROGS = DATA.programs;
let P = null, ST = [], i = 0, IMGS = [];

// ------------------------------------------------------------------ three.js scene (fixed parts)
const canvas = $('gl');
const renderer = new T.WebGLRenderer({canvas, antialias:true, alpha:true});
renderer.setPixelRatio(Math.min(devicePixelRatio, 2)); renderer.setScissorTest(true);
renderer.setClearColor(0x000000, 0);
const scene = new T.Scene();
scene.add(new T.HemisphereLight(0xfff6e8, 0x6b6558, 1.05));
const sun = new T.DirectionalLight(0xffffff, .9); sun.position.set(4, 9, 6); scene.add(sun);
const M = (c, o = {}) => new T.MeshStandardMaterial(Object.assign({color:c, roughness:.65, metalness:.12}, o));
const ORANGE = 0xe0561c, TEAL = 0x2c79a6, STEEL = 0x8d8a82, GOLD = 0xffd166;
const parts = {};
function part(name, group, home, ex, label, note){ group.position.copy(home); parts[name] = {g:group, home:home.clone(), ex:new T.Vector3(...ex), label, note}; scene.add(group); return group; }
function box(w,h,d,mat,x=0,y=0,z=0){ const m = new T.Mesh(new T.BoxGeometry(w,h,d), mat); m.position.set(x,y,z); return m; }
function texCanvas(w, h){ const c = document.createElement('canvas'); c.width = w; c.height = h; const t = new T.CanvasTexture(c); t.anisotropy = 4; return {c, t, g:c.getContext('2d'), key:''}; }
function drawLines(tc, lines, opts = {}){ const key = JSON.stringify([lines, opts]); if (tc.key === key) return; tc.key = key; const {c, g} = tc;
  g.fillStyle = opts.bg || '#f4efe2'; g.fillRect(0, 0, c.width, c.height); g.fillStyle = opts.fg || '#1c1b19'; g.textAlign = opts.align || 'center'; g.textBaseline = 'middle'; g.direction = 'ltr';
  const sz = opts.size || 26; const x = opts.align === 'left' ? 14 : c.width / 2;
  lines.forEach((l, k) => { g.font = (k === 0 ? '700 ' : '500 ') + sz + 'px "IBM Plex Mono", monospace'; g.fillStyle = (opts.colors && opts.colors[k]) || opts.fg || '#1c1b19'; g.fillText(l, x, c.height / 2 + (k - (lines.length - 1) / 2) * sz * 1.3); });
  if (opts.swatch){ g.fillStyle = opts.swatch; g.fillRect(c.width - 70, 12, 56, c.height - 24); g.strokeStyle = '#000'; g.strokeRect(c.width - 70, 12, 56, c.height - 24); }
  tc.t.needsUpdate = true; }
function labelPlane(lines, w, h, pw = 256, ph = 128, opts){ const tc = texCanvas(pw, ph); drawLines(tc, lines, opts); const m = new T.Mesh(new T.PlaneGeometry(w, h), new T.MeshBasicMaterial({map:tc.t, transparent:true})); m.userData.tc = tc; return m; }

// bench
const bench = new T.Group(); bench.add(box(13, .3, 6.4, M(0x5a554b, {roughness:.9}), 0, -.15, 0));
for (const [x,z] of [[-6,-2.8],[6,-2.8],[-6,2.8],[6,2.8]]) bench.add(box(.3, 2.2, .3, M(0x3a362f), x, -1.4, z));
scene.add(bench);
// CPU + stack plates
const cpuG = new T.Group(); cpuG.add(box(2.2, 1.2, 1.8, M(ORANGE, {roughness:.5})));
cpuG.add(labelPlane(['CPU', 'بينفذ C++'], 1.6, .8, 256, 128).translateZ(.91).translateY(.1));
const cpuLamp = new T.Mesh(new T.SphereGeometry(.14, 16, 16), new T.MeshStandardMaterial({color:0x442200, emissive:0x000000})); cpuLamp.position.set(.8, .75, 0); cpuG.add(cpuLamp);
part('cpu', cpuG, new T.Vector3(-4.6, .6, .6), [-1.0, 1.0, 0], 'CPU', 'بينفذ الكود سطر سطر، ومش بيرسم');
const stackG = new T.Group(); cpuG.add(stackG); stackG.position.set(0, .6, 0); const stackPlates = [];
function setStack(frames){
  while (stackPlates.length < frames.length){ const k = stackPlates.length; const g = new T.Group(); g.add(box(1.9, .28, 1.5, M(k ? 0xf0a06a : 0xe0561c, {roughness:.55}))); const lbl = labelPlane([''], 1.7, .26, 512, 80, {size:30, bg:'#fff3e8', fg:'#7a2e08'}); lbl.position.set(0, .15, 0); lbl.rotation.x = -Math.PI/2; g.add(lbl); g.userData.lbl = lbl; g.position.y = .16 + k * .32; stackG.add(g); stackPlates.push(g); }
  stackPlates.forEach((g, k) => { const f = frames[k]; g.visible = !!f; if (f) drawLines(g.userData.lbl.userData.tc, [`${f.fn}()  · ${f.v.length} vars`], {size:30, bg:'#fff3e8', fg:'#7a2e08'}); });
}
// RAM tray with the live locals of the running function
const ramG = new T.Group(); ramG.add(box(2.5, .25, 1.3, M(0x3b3833)));
const ramScreen = labelPlane([''], 2.3, 1.15, 512, 256, {bg:'#22211f', fg:'#ffd166'}); ramScreen.rotation.x = -Math.PI/2; ramScreen.position.y = .13; ramG.add(ramScreen);
part('ram', ramG, new T.Vector3(-4.6, .15, -1.75), [-1.0, .6, -.9], 'الرام', 'متغيرات الدالة الشغالة');
// GPU housing + lid
const gpuG = new T.Group();
gpuG.add(box(6.2, .12, 3.6, M(0x2f4858), 0, .06, 0));
const wallMat = M(TEAL, {roughness:.45, transparent:true, opacity:1});
[box(6.2, 1.5, .08, wallMat, 0, .81, -1.8), box(6.2, 1.5, .08, wallMat, 0, .81, 1.8), box(.08, 1.5, 3.6, wallMat, -3.1, .81, 0), box(.08, 1.5, 3.6, wallMat, 3.1, .81, 0)].forEach(w => gpuG.add(w));
const gpuLabel = labelPlane(['GPU', 'OpenGL 3.3 core'], 2.4, .9, 256, 96, {bg:'#2c79a6', fg:'#ffffff'}); gpuLabel.position.set(0, .8, 1.85); gpuG.add(gpuLabel);
part('gpu', gpuG, new T.Vector3(.2, 0, 0), [0, 0, 0], 'كارت الشاشة', 'كل دالة بتبدأ بـ gl بتروح هنا');
const lidG = new T.Group(); const lidMat = M(TEAL, {roughness:.4, transparent:true, opacity:1}); lidG.add(box(6.2, .12, 3.6, lidMat));
part('lid', lidG, new T.Vector3(.2, 1.62, 0), [0, 1.6, 0], 'غطا الكارت', 'شيله عشان تشوف جوه');
const ctxLamp = new T.Mesh(new T.SphereGeometry(.12, 12, 12), new T.MeshStandardMaterial({color:0x113333, emissive:0})); ctxLamp.position.set(-2.8, 1.45, 1.6); gpuG.add(ctxLamp);
parts.ctx = {g: ctxLamp, label:'Context', note:'الكارت شغال للشباك ده', ex:new T.Vector3(), home:new T.Vector3(), sub:true};
// buffers (crates) and VAO tags, created per program
const bufG = new T.Group(); part('buf', bufG, new T.Vector3(-2.1, .12, -1.15), [-.9, 1.1, -1.1], 'Buffers', 'البايتات على الكارت');
const vaoG = new T.Group(); part('vao', vaoG, new T.Vector3(-2.1, .12, -.2), [-.9, 1.4, .2], 'VAOs', 'ورقة التعليمات');
const crates = {}, tags = {};
const CRATE_X = [-.55, .2, .95, -.55, .2, .95];
function crate(id){ if (crates[id]) return crates[id]; const n = Object.keys(crates).length; const g = new T.Group();
  g.add(box(.68, .42, .62, M(0x8a6a3a, {roughness:.8}), 0, .21, 0)); const top = labelPlane([''], .64, .58, 256, 232, {}); top.rotation.x = -Math.PI/2; top.position.y = .43; g.add(top); g.userData.top = top;
  const lid = labelPlane([''], .66, .2, 256, 76, {}); lid.position.set(0, .22, .32); g.add(lid); g.userData.front = lid;
  g.position.set(CRATE_X[n % 6], 0, n >= 3 ? .0 : 0); if (n >= 3) g.position.y = .44; bufG.add(g); crates[id] = g; return g; }
function tag(id){ if (tags[id]) return tags[id]; const n = Object.keys(tags).length; const g = new T.Group(); const p = labelPlane([''], .78, .62, 300, 236, {}); p.position.y = .42; g.add(p); g.add(box(.05, .3, .05, M(0x3a362f), 0, .1, 0)); g.userData.p = p;
  g.position.set(CRATE_X[n % 3] - (n >= 3 ? .1 : 0), 0, n >= 3 ? .35 : 0); vaoG.add(g); tags[id] = g; return g; }
function clearDyn(){ for (const k in crates){ bufG.remove(crates[k]); delete crates[k]; } for (const k in tags){ vaoG.remove(tags[k]); delete tags[k]; } }
// vertex shader station
const vsG = new T.Group(); vsG.add(box(1.3, .5, .8, M(STEEL)));
const vsLamps = [0,1,2].map(k => { const l = new T.Mesh(new T.SphereGeometry(.13, 16, 16), new T.MeshStandardMaterial({color:0x332200, emissive:0x000000})); l.position.set(-.4 + k*.4, .4, 0); vsG.add(l); return l; });
const vsLbl = labelPlane(['Vertex', 'Shader'], 1.1, .4, 256, 96, {size:26}); vsLbl.translateZ(.41).translateY(.02); vsG.add(vsLbl);
part('vs', vsG, new T.Vector3(-.2, .37, -.95), [0, 1.4, -1.0], 'Vertex Shader', 'بيشتغل مرة لكل ركن');
// rasterizer (real coverage mask)
const rasT = texCanvas(320, 240); rasT.t.magFilter = T.NearestFilter;
const rasG = new T.Group(); rasG.add(box(1.9, .9, .15, M(0x2a2a2a)));
const rasScreen = new T.Mesh(new T.PlaneGeometry(1.7, .75), new T.MeshBasicMaterial({map:rasT.t})); rasScreen.position.z = .08; rasG.add(rasScreen);
part('ras', rasG, new T.Vector3(1.6, .6, -1.15), [.5, 1.5, -1.2], 'Rasterizer', 'جزء ثابت جوه الكارت: أنهي بكسلات جوه الشكل؟');
// fragment shader station
const fsG = new T.Group(); fsG.add(box(1.3, .5, .8, M(STEEL)));
const fsBar = new T.Mesh(new T.BoxGeometry(1, .14, .14), new T.MeshStandardMaterial({color:0x111a40, emissive:0x000000})); fsBar.position.y = .36; fsG.add(fsBar);
const fsLbl = labelPlane(['Fragment', 'Shader'], 1.1, .4, 256, 96, {size:26}); fsLbl.translateZ(.41).translateY(.02); fsG.add(fsLbl);
part('fs', fsG, new T.Vector3(1.6, .37, .45), [.7, 1.3, 1.1], 'Fragment Shader', 'بيلوّن كل بكسل جوه الشكل');
// program bar with uniforms
const progG = new T.Group(); const progBar = new T.Mesh(new T.BoxGeometry(1.5, .16, .3), new T.MeshStandardMaterial({color:0x1a2b1a, emissive:0})); progG.add(progBar);
const progLbl = labelPlane([''], 1.5, .5, 384, 128, {}); progLbl.position.set(0, .1, .3); progLbl.rotation.x = -Math.PI/2.6; progG.add(progLbl);
part('prog', progG, new T.Vector3(.35, .25, -.05), [0, 1.0, .3], 'Program', 'الـ Shaders مربوطين + الـ uniforms');
// framebuffer carousel (A / B) with the REAL frames
const fbC = {A: texCanvas(320, 240), B: texCanvas(320, 240)};
const carG = new T.Group(); carG.add(new T.Mesh(new T.CylinderGeometry(.9, .9, .12, 32), M(0x3a362f)));
const slab = id => { const g = new T.Group(); g.add(box(1.5, 1.15, .1, M(0x24262b))); const s = new T.Mesh(new T.PlaneGeometry(1.36, 1.02), new T.MeshBasicMaterial({map:fbC[id].t})); s.position.z = .06; g.add(s);
  const tg = labelPlane(['FB ' + id], .5, .22, 128, 56, {size:30, bg:'#1c1b19', fg:'#ffffff'}); tg.position.set(0, .7, .06); g.add(tg); return g; };
const slabA = slab('A'); slabA.position.set(0, .68, .55); carG.add(slabA);
const slabB = slab('B'); slabB.position.set(0, .68, -.55); slabB.rotation.y = Math.PI; carG.add(slabB);
part('car', carG, new T.Vector3(-1.1, .06, 1.0), [-1.2, 1.5, 1.6], 'Framebuffers A و B', 'اللي قدام = FRONT، اللي ورا = BACK');
// monitor
const monT = texCanvas(400, 300);
const monG = new T.Group(); monG.add(box(2.6, 2.0, .25, M(0x24262b)));
const monScreen = new T.Mesh(new T.PlaneGeometry(2.36, 1.77), new T.MeshBasicMaterial({map:monT.t})); monScreen.position.z = .14; monG.add(monScreen);
monG.add(box(.5, .9, .5, M(0x3a362f), 0, -1.4, 0));
part('mon', monG, new T.Vector3(5.2, 1.9, 0), [1.3, .9, 0], 'الشباك (الشاشة)', 'بتعرض اللوحة اللي قدام بس');
// printer (terminal)
const paperT = texCanvas(512, 640);
const prnG = new T.Group(); prnG.add(box(1.6, .5, 1.1, M(0x3a362f)));
const paperM = new T.Mesh(new T.PlaneGeometry(1.2, 1.5), new T.MeshBasicMaterial({map:paperT.t, side:T.DoubleSide})); paperM.position.set(0, 1.0, -.2); paperM.rotation.x = -.25; prnG.add(paperM);
prnG.add(labelPlane(['Terminal'], 1.1, .3, 256, 64, {size:30, bg:'#111', fg:'#9fe8b6'}).translateZ(.56).translateY(.02));
part('prn', prnG, new T.Vector3(3.3, .25, 2.5), [1.0, .8, 1.4], 'الطابعة (الـ Terminal)', 'اللي البرنامج طبعه فعلاً');
// mouse
const mouseG = new T.Group(); mouseG.add(box(1.5, .04, 1.1, M(0x1c1b19), 0, .02, 0));
const mBody = new T.Mesh(new T.SphereGeometry(.32, 24, 16), M(0xd9d4c7, {roughness:.4})); mBody.scale.set(1, .5, 1.45); mBody.position.y = .18; mouseG.add(mBody);
const mBtnL = box(.26, .06, .3, M(0xc9c3b4), -.13, .32, -.24), mBtnR = box(.26, .06, .3, M(0xc9c3b4), .13, .32, -.24); mouseG.add(mBtnL); mouseG.add(mBtnR);
const mouseLbl = labelPlane(['Mouse'], 1.2, .3, 256, 64, {size:30, bg:'#1c1b19', fg:'#fff'}); mouseLbl.rotation.x = -Math.PI/2; mouseLbl.position.set(0, .05, .4); mouseG.add(mouseLbl);
part('mouse', mouseG, new T.Vector3(-4.4, .05, 2.55), [-.8, .9, 1.2], 'الماوس', 'الضغطات بتوصل لـ GLFW');
// data pipes
const pipePts = [[-4.6,.6,-1.75],[-2.1,.9,-1.15],[-.2,.9,-.95],[1.6,.9,-1.15],[1.6,.9,.45],[-1.1,.9,1.0],[5.2,1.9,.3]].map(p => new T.Vector3(...p));
const pipes = new T.Group(); const pipeMat = new T.MeshStandardMaterial({color:ORANGE, emissive:0x301000, transparent:true, opacity:0});
for (let k = 0; k < pipePts.length - 1; k++) pipes.add(new T.Mesh(new T.TubeGeometry(new T.LineCurve3(pipePts[k], pipePts[k+1]), 2, .04, 8), pipeMat));
scene.add(pipes);
const tokens = []; const tokMat = new T.MeshStandardMaterial({color:GOLD, emissive:0x553a00});
for (let k = 0; k < 8; k++){ const m = new T.Mesh(new T.SphereGeometry(.09, 12, 12), tokMat); m.visible = false; scene.add(m); tokens.push(m); }
// camera
const cam = new T.PerspectiveCamera(32, 1, .1, 100);
const orbit = {yaw:-.5, pitch:.42, dist:17, target:new T.Vector3(-.2, .6, .2)};
const HOME = {yaw:orbit.yaw, pitch:orbit.pitch, dist:orbit.dist};
let ex = 0, cut = 0, flow = 0, mode = 'cutaway';
function placeCam(){ const d = orbit.dist * (1 + ex * .22) * Math.max(1, 1.5 / Math.max(.3, cam.aspect)); cam.position.set(orbit.target.x + d*Math.cos(orbit.pitch)*Math.sin(orbit.yaw), orbit.target.y + d*Math.sin(orbit.pitch), orbit.target.z + d*Math.cos(orbit.pitch)*Math.cos(orbit.yaw)); cam.lookAt(orbit.target); }
const stage = $('stage'); let drag = null;
stage.addEventListener('pointerdown', e => { drag = {x:e.clientX, y:e.clientY, yaw:orbit.yaw, pitch:orbit.pitch}; stage.setPointerCapture(e.pointerId); });
stage.addEventListener('pointermove', e => { if (!drag) return; orbit.yaw = drag.yaw - (e.clientX - drag.x) * .008; orbit.pitch = Math.max(.05, Math.min(1.3, drag.pitch + (e.clientY - drag.y) * .006)); });
stage.addEventListener('pointerup', () => drag = null); stage.addEventListener('pointercancel', () => drag = null);
stage.addEventListener('wheel', e => { e.preventDefault(); orbit.dist = Math.max(6, Math.min(30, orbit.dist * (1 + Math.sign(e.deltaY) * .08))); }, {passive:false});
$('reset').onclick = () => Object.assign(orbit, HOME);
const zoom = f => { orbit.dist = Math.max(6, Math.min(30, orbit.dist * f)); };
$('zin').onclick = () => zoom(.8); $('zout').onclick = () => zoom(1.25);
{ const pts = new Map(); let pinch0 = 0, dist0 = 0;
  stage.addEventListener('pointerdown', e => { pts.set(e.pointerId, [e.clientX, e.clientY]); if (pts.size === 2){ const [a, b] = [...pts.values()]; pinch0 = Math.hypot(a[0]-b[0], a[1]-b[1]); dist0 = orbit.dist; drag = null; } });
  stage.addEventListener('pointermove', e => { if (!pts.has(e.pointerId)) return; pts.set(e.pointerId, [e.clientX, e.clientY]); if (pts.size === 2){ const [a, b] = [...pts.values()]; const d = Math.hypot(a[0]-b[0], a[1]-b[1]); if (pinch0 > 0) orbit.dist = Math.max(6, Math.min(30, dist0 * pinch0 / d)); drag = null; } });
  const up = e => { pts.delete(e.pointerId); pinch0 = 0; }; stage.addEventListener('pointerup', up); stage.addEventListener('pointercancel', up); }

// ------------------------------------------------------------------ frame images (real back-buffer read-backs)
function frameImg(k){ return k === null || k === undefined ? null : IMGS[k]; }
function paintFrame(g, w, h, k, k0, p, scan){ // draw frame k (wipe over k0 by p, top to bottom)
  const im = frameImg(k), im0 = frameImg(k0);
  const blank = () => { g.fillStyle = '#2a2f3a'; g.fillRect(0, 0, w, h); g.fillStyle = '#8a96aa'; g.font = '600 ' + Math.round(h/12) + 'px "IBM Plex Sans Arabic", sans-serif'; g.textAlign = 'center'; g.direction = 'rtl'; g.fillText('فاضية / قديمة', w/2, h/2 + 6); };
  if (p === undefined || p >= 1){ if (im && im.complete) g.drawImage(im, 0, 0, w, h); else blank(); return; }
  if (im0 && im0.complete) g.drawImage(im0, 0, 0, w, h); else blank();
  if (im && im.complete){ const y = Math.max(0, Math.min(h, h * p)); if (y > 0) g.drawImage(im, 0, 0, im.width, im.height * p, 0, 0, w, y); if (scan && p < 1){ g.fillStyle = 'rgba(255,209,102,.85)'; g.fillRect(0, y - 1, w, 2); } }
}
function texFrame(tc, k, k0, p, scan){ paintFrame(tc.g, tc.c.width, tc.c.height, k, k0, p, scan); tc.t.needsUpdate = true; }
function drawRas(mk, p, mode){ const {g, t} = rasT; g.fillStyle = '#05070c'; g.fillRect(0, 0, 320, 240); if (!mk || mode === 'off'){ t.needsUpdate = true; return; }
  const cw = 320 / mk.c, rh = 240 / mk.r, rows = mode === 'done' ? mk.r : Math.floor(p * mk.r), col = mk.col ? `rgb(${mk.col.join(',')})` : '#707a90';
  for (let r = 0; r < mk.r; r++) for (let c = 0; c < mk.c; c++){ const on = mk.m[r * mk.c + c] === '1'; g.fillStyle = on && r < rows ? (mode === 'done' ? col : '#8a93a8') : '#141821'; g.fillRect(c*cw + 1, r*rh + 1, cw - 2, rh - 2); }
  if (mode === 'scan' && rows < mk.r){ g.fillStyle = 'rgba(255,209,102,.8)'; g.fillRect(0, rows * rh, 320, 2); }
  g.fillStyle = '#ffd166'; g.font = '600 15px "IBM Plex Mono"'; g.textAlign = 'left'; g.direction = 'ltr'; g.fillText(mk.px.toLocaleString('en') + ' px', 8, 18); t.needsUpdate = true; }
function drawMonitor(k, ev, p){ const {g, c} = monT; const st = ST[i];
  if (!P || !st.gp.win){ g.fillStyle = '#16181d'; g.fillRect(0, 0, c.width, c.height); g.fillStyle = '#5c6372'; g.font = '600 22px "IBM Plex Sans Arabic"'; g.textAlign = 'center'; g.direction = 'rtl'; g.fillText('مفيش شباك لسه', 200, 156); monT.t.needsUpdate = true; return; }
  paintFrame(g, c.width, c.height, k);
  if (ev && ev.btn === 'key'){ g.fillStyle = 'rgba(0,0,0,.55)'; g.fillRect(c.width / 2 - 120, c.height - 70, 240, 44); g.fillStyle = '#ffd166'; g.font = '600 20px "IBM Plex Mono"'; g.textAlign = 'center'; g.direction = 'ltr'; g.fillText('⌨ ' + ev.key + (ev.act === 'press' ? ' ↓' : ' ↑'), c.width / 2, c.height - 41); }
  else if (ev){ const x = ev.x / P.W * c.width, y = ev.y / P.H * c.height, r = 6 + 14 * (p || 0); g.strokeStyle = ev.btn === 'left' ? '#ffd166' : '#ff6b9a'; g.lineWidth = 3; g.beginPath(); g.arc(x, y, r, 0, 7); g.stroke(); g.beginPath(); g.moveTo(x - 10, y); g.lineTo(x + 10, y); g.moveTo(x, y - 10); g.lineTo(x, y + 10); g.stroke();
    g.fillStyle = '#fff'; g.font = '600 15px "IBM Plex Mono"'; g.textAlign = x > 300 ? 'right' : 'left'; g.direction = 'ltr'; g.fillText(`(${ev.x}, ${ev.y})`, x + (x > 300 ? -14 : 14), y - 12); }
  monT.t.needsUpdate = true; }
function drawPaper(lines, nNew){ const {g} = paperT; g.fillStyle = '#f6f1e4'; g.fillRect(0, 0, 512, 640); g.font = '500 20px "IBM Plex Mono", monospace'; g.textAlign = 'left'; g.direction = 'ltr';
  const last = lines.slice(-22); last.forEach((l, k) => { g.fillStyle = k >= last.length - nNew ? '#b5400f' : '#1c1b19'; g.fillText(l.slice(0, 40), 14, 36 + k * 27); });
  if (!lines.length){ g.fillStyle = '#9a938a'; g.font = '500 22px "IBM Plex Sans Arabic"'; g.direction = 'rtl'; g.textAlign = 'center'; g.fillText('لسه مفيش طباعة', 256, 60); } paperT.t.needsUpdate = true; }

// ------------------------------------------------------------------ live callouts
const ringMat = new T.MeshBasicMaterial({color:0xe0561c, transparent:true, opacity:.9, side:T.DoubleSide});
const rings = []; for (let k = 0; k < 4; k++){ const r = new T.Mesh(new T.RingGeometry(.45, .55, 40), ringMat); r.rotation.x = -Math.PI/2; r.visible = false; scene.add(r); rings.push(r); }
const liveEls = [], liveLines = []; const svgNS = 'http://www.w3.org/2000/svg';
for (let k = 0; k < 4; k++){ const d = document.createElement('div'); d.className = 'lc'; d.style.display = 'none'; $('live').appendChild(d); liveEls.push(d); let pd = null; d.addEventListener('pointerdown', e => { e.stopPropagation(); pd = [e.clientX, e.clientY, performance.now()]; }); d.addEventListener('pointerup', e => { e.stopPropagation(); if (pd && Math.hypot(e.clientX - pd[0], e.clientY - pd[1]) < 12 && performance.now() - pd[2] < 800){ pd = null; d._t = performance.now(); gotoCodeLine(); } }); d.addEventListener('click', e => { e.stopPropagation(); if (!d._t || performance.now() - d._t > 600) gotoCodeLine(); }); d.setAttribute('role', 'button'); d.title = 'دوس تروح للسطر ده في الكود';
  const p = document.createElementNS(svgNS, 'path'); p.setAttribute('fill', 'none'); p.setAttribute('stroke', '#e0561c'); p.setAttribute('stroke-width', '1.4'); $('liveSvg').appendChild(p); const c = document.createElementNS(svgNS, 'circle'); c.setAttribute('r', '3'); c.setAttribute('fill', '#e0561c'); $('liveSvg').appendChild(c); liveLines.push([p, c]); }
let LIVE = [], liveT0 = 0;
function anchor(pn, label){
  if (pn === 'buf'){ const m = /Buffer (\d+)/.exec(label); const c = m && crates[m[1]]; if (c) return c; const ks = Object.keys(crates); return ks.length ? crates[ks[ks.length-1]] : bufG; }
  if (pn === 'vao'){ const m = /VAO (\d+)/.exec(label); const c = m && tags[m[1]]; if (c) return c; const ks = Object.keys(tags); return ks.length ? tags[ks[ks.length-1]] : vaoG; }
  return parts[pn] ? parts[pn].g : null; }
const fileLine = s => (P.files.length > 1 ? P.files[s.f].name + ' : ' : '') + s.ln;
function buildLive(){
  const s = ST[i]; LIVE = (s.lv || []).map(([pn, label, what]) => ({pn, label, what, g: anchor(pn, label)})).filter(L => L.g);
  liveT0 = performance.now();
  liveEls.forEach((d, k) => { const L = LIVE[k]; if (!L){ d.style.display = 'none'; return; } d.style.display = ''; d.style.animation = 'none'; void d.offsetWidth; d.style.animation = '';
    const code = (P.files[s.f].lines[s.ln - 1] || '').trim(); d.innerHTML = `<b>${esc(L.label)}</b><span class="ln">line ${fileLine(s)}</span> <code>${esc(code)}</code><span class="tw cur" data-full="${esc(L.what)}"></span>`; fixBidi(d.querySelector('b')); });
}

// gears live in a strip outside the code box (so copying the code never picks them up); they follow the box's scroll
function layoutGut(){ const code = $('code'), inn = $('drvGutIn'); if (!code || !inn) return;
  const D = driverLines(); inn.innerHTML = D.map(d => { const row = $('L' + d.v); if (!row) return ''; return `<b style="top:${row.offsetTop + 1}px;height:${row.offsetHeight}px;line-height:${row.offsetHeight}px" data-v="${d.v}" title="سطر ${d.ln}: الدرايفر بياخد أمر هنا${d.runs.length ? ' · دوس تروح لأول مرة اتنفذ' : ' · ما اتنفذش في التشغيل ده'}">⚙</b>`; }).join('');
  inn.style.transform = `translateY(${-code.scrollTop}px)`;
  inn.querySelectorAll('b').forEach(b => b.onclick = () => { const d = D.find(x => x.v === +b.dataset.v); if (d && d.runs.length){ play(false); go(d.runs[0]); } }); }
function renderCodeLeg(){ const el = $('codeLeg'); if (!el) return; const hasSh = P.shl.vs.length || P.shl.fs.length;
  el.innerHTML = `<details open><summary>🔑 مفتاح العلامات والألوان اللي في الكود</summary><div class="kl"><span><b class="gear">⚙</b> = سطر بيبعت أمر للدرايفر (دوس عليها تروح لأول مرة اتنفذ)</span>
    <span><i class="sw" style="background:#2a3a57;border-left:3px solid #e0561c"></i> = السطر اللي بيتنفذ دلوقتي على الـ CPU</span>
    <span><i class="sw" style="background:#1f4a45;border-left:3px solid #3fd0bb"></i> = السطر ده شغّال على الكارت (GPU)</span>
    <span><span style="color:#9aa6ba;background:#1b2130;padding:0 5px;font-family:var(--mono)">abc</span> = كتابة رمادي: سطر اتنفذ قبل كده</span>
    ${hasSh ? `<span><i class="sw" style="background:rgba(63,208,187,.35)"></i> = سطر في الـ Vertex Shader (بيشتغل وقت الرسم)</span><span><i class="sw" style="background:rgba(88,174,214,.45)"></i> = سطر في الـ Fragment Shader</span>` : ''}
    <span>العلامة ⚙ برا مربع الكود، وأرقام السطور مش بتتنسخ، فلما تنسخ بيتنسخ الكود بس.</span></div></details>`; }
$('code').addEventListener('scroll', () => { $('drvGutIn').style.transform = `translateY(${-$('code').scrollTop}px)`; }, {passive: true});
if (window.ResizeObserver) new ResizeObserver(() => layoutGut()).observe($('code'));
// tap a callout on the machine → jump to that line in the code panel
function gotoCodeLine(){ const s = ST[i]; const L = $('L' + s.v); const fig = $('codeFig'); if (!L || !fig) return;
  play(false); const bx = $('code'); bx.scrollTop = Math.max(0, L.offsetTop - bx.clientHeight / 2);
  const se = document.scrollingElement || document.documentElement; const y = fig.getBoundingClientRect().top + se.scrollTop - Math.max(8, (innerHeight - fig.offsetHeight) / 2);
  try { fig.scrollIntoView({block: 'center'}); } catch (e) {} if (Math.abs(fig.getBoundingClientRect().top - Math.max(8, (innerHeight - fig.offsetHeight) / 2)) > 40){ se.scrollTop = y; window.scrollTo(0, y); }
  L.classList.remove('flash'); void L.offsetWidth; L.classList.add('flash'); }
function tickLive(){
  const r = stage.getBoundingClientRect(); const el = (performance.now() - liveT0) / 1000;
  liveEls.forEach((d, k) => { const L = LIVE[k]; const [p, c] = liveLines[k]; const ring = rings[k];
    if (!L || r.width < 10 || mode === 'exploded'){ p.setAttribute('d', ''); c.setAttribute('r', '0'); ring.visible = false; if (!L) d.style.display = 'none'; return; }
    const w = new T.Vector3(); L.g.getWorldPosition(w); const v = w.clone().project(cam); const x = r.left + (v.x + 1) / 2 * r.width, y = r.top + (1 - v.y) / 2 * r.height;
    const tw = d.querySelector('.tw'); const full = tw.dataset.full; const n = reduce ? full.length : Math.min(full.length, Math.floor(el * 28)); if (tw.textContent.length !== n) tw.textContent = full.slice(0, n); tw.classList.toggle('cur', n < full.length);
    const narrow = r.width < 640, colW = Math.min(300, narrow ? r.width - 24 : r.width * .42); d.style.maxWidth = colW + 'px';
    const prevBottom = k === 0 ? r.top + 12 : liveEls[k-1]._bottom + 8; const bw = d.offsetWidth, bh = d.offsetHeight;
    const lx = narrow ? r.left + r.width / 2 : (x < r.left + r.width / 2 ? r.right - bw / 2 - 12 : r.left + bw / 2 + 12); const ly = prevBottom + bh / 2; d._bottom = ly + bh / 2;
    d.style.left = lx + 'px'; d.style.top = ly + 'px';
    const ax = x < lx - bw / 2 ? lx - bw / 2 : x > lx + bw / 2 ? lx + bw / 2 : x; const ay = ly + bh / 2;
    p.setAttribute('d', `M${x},${y} L${ax},${ay}`); c.setAttribute('cx', x); c.setAttribute('cy', y); c.setAttribute('r', '3.5');
    ring.visible = true; ring.position.copy(w); ring.position.y = Math.max(.12, w.y - .3); const sc = 1 + .25 * Math.sin(el * 5); ring.scale.set(sc, sc, sc); ringMat.opacity = .5 + .4 * (1 + Math.sin(el * 5)) / 2; });
}

// ------------------------------------------------------------------ per-program precomputation
let SWAPS = [], LINE_UNIT = [], FIRST = [], NV = 0, EPY = [1, 2], PRE_FRONT = [];
const unitCol = u => u === 'CPU' ? cssv('--arancio') : u === 'GPU' ? '#0f766e' : cssv('--celeste-ink');
function loadProgram(id, keepStep){
  P = PROGS.find(p => p.id === id) || PROGS[0]; ST = P.steps; NV = P.NV; store.set('bench06', P.id);
  if (location.hash.slice(1) !== P.id) history.replaceState(null, '', '#' + P.id);
  IMGS = P.frames.map(u => { const im = new Image(); im.onload = () => { if (P && ST[i]) applyStep(true); }; im.src = u; return im; });
  clearDyn();
  document.querySelectorAll('#picker button').forEach(b => b.setAttribute('aria-pressed', b.dataset.id === P.id));
  document.querySelectorAll('#picker details.pk-day').forEach(dt => { if (+dt.dataset.day === P.day){ dt.open = true; const w = dt.closest('details.pk-week'); if (w) w.open = true; } });
  $('ptitle').textContent = P.title; $('pday').textContent = P.day; $('pdesc').textContent = P.desc;
  const noGL = !P.frames.length && !ST.some(s => /\bgl[A-Z]/.test(stepText(s))); document.body.classList.toggle('nogl', noGL);
  const isPy = P.files.some(f => /\.py$/.test(f.name)); $('termCap').textContent = isPy ? 'print' : 'std::cout';
  if ($('cmdSheet') && !$('cmdSheet').hidden) setTimeout(renderCmd);
  $('pdeck').textContent = noGL ? `${ST.length} خطوة · برنامج ${isPy ? 'Python' : 'C++'} في الـ Terminal (من غير شباك)` : `${ST.length} خطوة · ${P.laps} لفة while · ${P.frames.length} صورة حقيقية من الكارت`;
  $('runmid').textContent = P.files.map(f => `${f.name} · ${f.lines.length} سطر`).join('  +  ');
  $('seek').max = ST.length - 1;
  // code panel
  const vsSet = new Set(P.shl.vs), fsSet = new Set(P.shl.fs);
  const drvSet = new Set(driverLines().map(d => d.v));
  $('code').innerHTML = P.files.map(f => `<div class="fh">${esc(f.name)}</div>` + f.lines.map((l, k) => { const v = f.off + k + 1; return `<div id="L${v}"${vsSet.has(v) ? ' data-sh="vs"' : fsSet.has(v) ? ' data-sh="fs"' : ''}${drvSet.has(v) ? ' class="drv" title="هنا الدرايفر بياخد أمر"' : ''}><i>${k+1}</i>${esc(l) || ' '}</div>`; }).join('')).join('');
  requestAnimationFrame(layoutGut); renderCodeLeg(); setupLineNav(); $('lnInfo').textContent = '';
  // swaps parity, line units, first visit
  SWAPS = []; { let n = 0; for (const s of ST){ SWAPS.push(n); if (s.an === 'swap') n++; } }
  LINE_UNIT = []; const cnt = {}; ST.forEach(x => { (cnt[x.v] = cnt[x.v] || {})[x.u] = 1; });
  for (let v = 1; v <= NV; v++){ const c = cnt[v]; LINE_UNIT[v] = !c ? null : c.GPU && !c.CPU && !c['CPU→GPU'] ? 'GPU' : c['CPU→GPU'] || (c.GPU && c.CPU) ? 'CPU→GPU' : 'CPU'; }
  FIRST = []; ST.forEach((x, k) => { if (FIRST[x.v] === undefined) FIRST[x.v] = k; });
  // laps buttons
  const lb = $('laps'); lb.innerHTML = '<span style="font-size:11px;color:var(--ink-3);align-self:center">روح للـ while:</span>';
  const first = {}; ST.forEach((x, k) => { if (x.lap && !(x.lap in first)) first[x.lap] = k; });
  Object.entries(first).forEach(([l, k]) => { const b = document.createElement('button'); b.textContent = 'اللفة ' + l + (ST.some(s => s.lap == l && s.ev && s.ev.btn === 'key') ? ' ⌨' : ST.some(s => s.lap == l && s.ev) ? ' 🖱' : ''); b.onclick = () => { play(false); go(k); if ($('lapNow')) $('lapNow').open = true; }; lb.appendChild(b); });
  const ex_ = ST.findIndex(s => s.cl); if (ex_ >= 0){ const b = document.createElement('button'); b.textContent = 'الخروج'; b.onclick = () => { play(false); go(ex_); }; lb.appendChild(b); }
  LAPNOW = -1;
  if ($('lapWhyBody')){ $('lapWhyBody').innerHTML = lapWhyHtml(); $('lapWhy').hidden = !P.phases.length; fixBidi($('lapWhyBody')); $('lapWhyBody').querySelectorAll('[data-go]').forEach(b => b.onclick = () => { play(false); go(+b.dataset.go); }); }
  $('cycleCap').textContent = P.phases.length ? `render loop · ${P.phases.length} lines` : 'render loop';
  $('fineNote').textContent = document.body.classList.contains('nogl') ? `كل رقم هنا من تشغيل حقيقي لـ ${P.files.map(f => f.name).join(' + ')} ${P.files.some(f => /\.py$/.test(f.name)) ? 'سطر سطر جوه Python (sys.settrace)' : 'تحت gdb'}: السطور بالترتيب اللي اتنفذت بيه، وقيم المتغيرات في الرام، وكل اللي اتطبع في الـ Terminal${ST.some(s => (s.ex || '').length && P.term.some(l => l.charCodeAt(0) === 1)) ? '، واللي اتكتب في الكيبورد بالأصفر' : ''}. البرنامج ده مالوش شباك، فالكارت مش شغال خالص. الماكينة نفسها موديل مبطّأ عشان تتشاف.` : `كل رقم وكل صورة هنا من تشغيل حقيقي لـ ${P.files.map(f => f.name).join(' + ')} تحت gdb على OpenGL (Mesa): السطور بالترتيب اللي اتنفذت بيه، وقيم المتغيرات، وأرقام الكائنات، و${P.frames.length} صورة اتقرت من الكارت (${P.W} × ${P.H}).` + (ST.some(s => s.ev) ? (ST.some(s => s.ev && s.ev.btn === 'key') ? ' ضغطات الماوس والكيبورد اتبعتت للشباك الحقيقي وقت التشغيل.' : ' ضغطات الماوس اتبعتت للشباك الحقيقي وقت التشغيل.') : '') + ' الماكينة نفسها موديل مبطّأ عشان تتشاف.';
  PRE_FRONT = []; drawRefMaps(); refDirty = true; if (typeof fmSync === 'function') fmSync();
  i = keepStep ? Math.min(i, ST.length - 1) : 0; play(false); frozen = false; applyStep();
  if (typeof renderStory === 'function' && $('story2') && !$('story2').hidden) renderStory();
}
const lineOf = (v, short) => { for (const f of P.files) if (v > f.off && v <= f.off + f.lines.length) return (P.files.length > 1 ? f.name.replace(/\.cpp$/, '').slice(0, short ? 4 : 20) + ':' : '') + (v - f.off); return v; };

// ------------------------------------------------------------------ state → machine
let A = {t:0, dur:1};
const secPerStep = () => 1.5 + Math.pow(+$('lever').value, 1.3) * 18;
$('leverOut').textContent = secPerStep().toFixed(1) + ' s';
const unitBadge = u => `<span class="u" style="background:${u === 'CPU' ? 'var(--arancio)' : u === 'GPU' ? 'var(--teal)' : 'var(--blueline)'}">${u}</span>`;
let backId = 'A';
function shaderSt(G, ty){ const ids = Object.keys(G.sh).filter(k => G.sh[k].ty === ty); return ids.length ? G.sh[ids[ids.length - 1]] : null; }
function uniColor(G){ for (const [n, v] of Object.entries(G.uni)){ const m = /^\(([-\d.e]+), ([-\d.e]+), ([-\d.e]+)/.exec(v); if (m) return `rgb(${[m[1], m[2], m[3]].map(x => Math.round(Math.max(0, Math.min(1, +x)) * 255)).join(',')})`; } return null; }
function applyStep(soft){ setTimeout(() => { try { syncLapNow(); } catch (e) {} });
  const s = ST[i], G = s.gp, prev = i ? ST[i-1] : null;
  if (!soft) A = {t:0, dur: secPerStep()};
  $('stepOut').textContent = `${i+1} / ${ST.length}`; $('seek').value = i; if ($('goN')) { $('goN').max = ST.length; $('goN').placeholder = `1–${ST.length}`; if (document.activeElement !== $('goN')) $('goN').value = i + 1; $('goDec').disabled = i === 0; $('goInc').disabled = i === ST.length - 1; } if ($('stepsSheet') && !$('stepsSheet').hidden) renderSteps();
  const lapTag = s.lap ? `<span class="u" style="background:var(--blueline)">while · lap ${s.lap}</span>` : s.cl ? '<span class="u" style="background:var(--blueline)">exit while</span>' : '';
  const evTag = s.ev ? (s.ev.btn === 'key' ? `<span class="u ev">⌨ ${esc(s.ev.key)}</span>` : '<span class="u ev">🖱 mouse</span>') : '';
  $('story').innerHTML = `${lapTag}${evTag}${unitBadge(s.u)} <b>سطر ${esc(fileLine(s))}: ${esc(s.ti)}</b><br>${s.ex}` + (s.dy && s.dy.length ? `<span class="dy">${s.dy.join('<br>')}</span>` : ''); fixBidi($('story'));
  $('where').textContent = `${P.files[s.f].name} : ${s.ln}` + (s.fn ? ` · ${s.fn}()` : '');
  // code panel
  document.querySelectorAll('#code div.cur, #code div.vsl, #code div.fsl').forEach(e => e.classList.remove('cur', 'g', 'vsl', 'fsl'));
  const L = $('L' + s.v); if (L){ L.classList.add('cur'); if (s.u !== 'CPU') L.classList.add('g'); }
  if (s.sv && $('L' + s.sv)) $('L' + s.sv).classList.add('cur');
  if (s.an === 'draw'){ document.querySelectorAll('#code div[data-sh]').forEach(e => e.classList.add(e.dataset.sh === 'vs' ? 'vsl' : 'fsl')); }
  const seen = new Set(); for (let k = 0; k < i; k++) seen.add(ST[k].v);
  document.querySelectorAll('#code div[id^="L"]').forEach(e => e.classList.toggle('done', seen.has(+e.id.slice(1)) && +e.id.slice(1) !== s.v));
  if (L){ const bx = $('code'); bx.scrollTop = Math.max(0, L.offsetTop - bx.clientHeight / 2); }
  // CPU, stack, RAM
  setStack(s.st); cpuLamp.material.emissive.setHex(s.u !== 'GPU' ? 0xff8a3d : 0);
  const top = s.st[s.st.length - 1]; const rl = top ? [`${top.fn}()`, ...top.v.slice(0, 6).map(([n, v, u]) => `${n} = ${u ? '?' : v}`.slice(0, 30))] : ['—'];
  drawLines(ramScreen.userData.tc, rl, {bg:'#22211f', fg:'#ffd166', size:24, align:'left', colors:['#ff9b6a']});
  // window / context
  monG.visible = G.win; ctxLamp.material.emissive.setHex(G.ctx ? 0x3fd0bb : 0);
  // buffers + VAOs (drop any crate/tag that does not exist yet at this step, e.g. after stepping back)
  for (const k in crates) if (!(k in G.bufs)){ bufG.remove(crates[k]); delete crates[k]; }
  for (const k in tags) if (!(k in G.vaos)){ vaoG.remove(tags[k]); delete tags[k]; }
  for (const [id, b] of Object.entries(G.bufs)){ const c = crate(id); const hot = (s.lv || []).some(l => l[0] === 'buf' && l[1] === 'Buffer ' + id);
    drawLines(c.userData.front.userData.tc, [`Buffer ${id} ${b.t || ''}`], {size:30, bg: hot ? '#ffd166' : '#4a3620', fg: hot ? '#1c1b19' : '#ffd166'});
    const vals = b.vals || []; const rows = []; for (let r = 0; r < Math.min(5, Math.ceil(vals.length / 3)); r++) rows.push(vals.slice(r * 3, r * 3 + 3).map(x => String(+x.toFixed(2))).join('  '));
    drawLines(c.userData.top.userData.tc, [b.bytes ? `${b.bytes} B` : 'فاضي', ...rows], {size:24, bg:'#4a3620', fg:'#ffd166'}); }
  for (const [id, v] of Object.entries(G.vaos)){ const tg = tag(id); const ls = [`VAO ${id}${G.bvao == id ? ' ●' : ''}`];
    for (const [loc, a] of Object.entries(v.at)) ls.push(`loc${loc}: ${a.size || '?'}f /${a.stride || '?'}B @${a.off || 0}${a.buf ? ' b' + a.buf : ''}${a.on ? '' : ' off'}`);
    if (v.ebo) ls.push(`EBO = Buffer ${v.ebo}`);
    drawLines(tg.userData.p.userData.tc, ls.slice(0, 5), {size:21, bg: G.bvao == id ? '#fff6c9' : '#e9e2c9', fg:'#5c4400'}); }
  // shaders / program
  const vsS = shaderSt(G, 'Vertex'), fsS = shaderSt(G, 'Fragment');
  vsLamps.forEach(l => l.material.emissive.setHex(!vsS ? 0 : vsS.st === 'del' ? 0xa05a10 : vsS.st === 'ok' ? 0xffd166 : 0x554400));
  fsBar.material.emissive.setHex(!fsS ? 0 : fsS.st === 'del' ? 0xa05a10 : fsS.st === 'ok' ? 0x3355ff : 0x202a60);
  const pr = Object.entries(G.pr)[0]; progBar.material.emissive.setHex(!pr ? 0 : pr[1].use ? 0x3fd0bb : pr[1].linked ? 0x1f8f80 : 0x1a4a40);
  const uc = uniColor(G);
  drawLines(progLbl.userData.tc, pr ? [`Program ${pr[0]}${pr[1].use ? ' (in use)' : pr[1].linked ? ' (linked)' : ''}`, ...Object.entries(G.uni).slice(0, 2).map(([n, v]) => `${n} ${v}`.slice(0, 26))] : ['Program —'], {size:22, bg:'#1c1b19', fg:'#ffffff', swatch: uc});
  // framebuffers: A/B identity follows the real swap count
  backId = (SWAPS[i] + (s.an === 'swap' ? 1 : 0)) % 2 === 0 ? 'A' : 'B'; const frontId = backId === 'A' ? 'B' : 'A';
  carG.rotation.y = (SWAPS[i] % 2) * Math.PI;
  paintAll(1);
  // printer + terminal pane
  const nNew = s.tm - (prev ? prev.tm : 0); drawPaper(P.term.slice(0, s.tm), nNew);
  $('termBox').innerHTML = s.tm ? P.term.slice(0, s.tm).map((l, k) => { const ty = l.charCodeAt(0) === 1; return `<div class="${k >= s.tm - nNew ? 'new' : ''}${ty ? ' typed' : ''}">${esc(ty ? l.slice(1) : l)}</div>`; }).join('') : '<span style="color:#6b7a70">(لسه مفيش طباعة)</span>';
  $('termBox').parentElement.scrollTop = 1e6;
  // panes
  drawGpuList(s); drawRamList(s);
  $('rStep').textContent = i + 1; $('rLine').textContent = lineOf(s.v); $('rUnit').textContent = s.u; $('rStack').textContent = s.st.length;
  $('rGpu').textContent = `${Object.keys(G.vaos).length} VAO · ${Object.keys(G.bufs).length} Buf · ${Object.keys(G.sh).length} Sh`;
  $('rLap').textContent = s.lap ? `${s.lap} / ${P.laps}` : s.cl ? 'خروج' : ST.slice(0, i).some(x => x.lap) ? 'بعد' : 'قبل';
  $('fbBackN').textContent = 'FB ' + backId; $('fbFrontN').textContent = 'FB ' + frontId;
  if (!soft) buildLive();
}
function paintAll(p){ // draw back / front for the current step at animation progress p
  const s = ST[i], prev = i ? ST[i-1] : null; const frontId = backId === 'A' ? 'B' : 'A';
  const backBefore = prev ? prev.bk : null; const wipe = (s.an === 'draw' || s.an === 'clear') && p < 1;
  const scanP = s.an === 'draw' ? Math.max(0, (p - .6) / .4) : p;
  texFrame(fbC[backId], s.gp.win ? s.bk : null, backBefore, wipe ? scanP : 1, true);
  texFrame(fbC[frontId], s.gp.win ? s.ft : null);
  const bg = $('fbBack').getContext('2d'), fg = $('fbFront').getContext('2d');
  paintFrame(bg, 320, 240, s.gp.win ? s.bk : null, backBefore, wipe ? scanP : 1, true);
  const showFront = s.an === 'swap' && p < .5 ? (prev ? prev.ft : null) : s.ft; paintFrame(fg, 320, 240, s.gp.win ? showFront : null);
  drawMonitor(showFront, s.ev, p);
}
function drawGpuList(s){
  const G = s.gp, hot = new Set((s.lv || []).map(l => l[1]));
  const h = [];
  if (!G.ctx) h.push('<p class="fine" style="margin:0">لسه مفيش وصلة بالكارت (Context). أوامر gl مش هتشتغل قبل <code>glfwMakeContextCurrent</code>.</p>');
  for (const [id, v] of Object.entries(G.vaos)){ const at = Object.entries(v.at).map(([l, a]) => `loc ${l}: ${a.size || '?'} float, stride ${a.stride || '?'} B, offset ${a.off || 0}${a.buf ? ', Buffer ' + a.buf : ''}${a.on ? '' : ' (off)'}`).join(' · ');
    h.push(`<div class="obj${hot.has('VAO ' + id) ? ' hot' : ''}"><span class="tg" style="background:#a3820d">VAO</span><b>${id}</b>${G.bvao == id ? ' ● مربوط' : ''}<small>${at || 'لسه مفيش وصف'}${v.ebo ? ' · EBO = Buffer ' + v.ebo : ''}</small></div>`); }
  for (const [id, b] of Object.entries(G.bufs)) h.push(`<div class="obj${hot.has('Buffer ' + id) ? ' hot' : ''}"><span class="tg" style="background:#8a6a3a">${b.t || 'Buffer'}</span><b>${id}</b> · ${b.bytes || 0} بايت${(G.bbuf.A == id || G.bbuf.E == id) ? ' ● مربوط' : ''}<small>${(b.vals || []).slice(0, 12).map(x => +x.toFixed(3)).join(', ') || '—'}</small></div>`);
  for (const [id, sh] of Object.entries(G.sh)) h.push(`<div class="obj${hot.has('Shader ' + id) ? ' hot' : ''}"><span class="tg" style="background:${sh.ty === 'Vertex' ? '#0f766e' : '#2c79a6'}">${sh.ty}</span><b>${id}</b> · ${({new:'فاضي', src:'فيه النص', ok:'مترجم ✓', del:'متعلّم للمسح'})[sh.st]}</div>`);
  for (const [id, p] of Object.entries(G.pr)){ const uc = uniColor(G);
    h.push(`<div class="obj${[...hot].some(x => /Program|uniform/.test(x)) ? ' hot' : ''}"><span class="tg" style="background:#1f8f80">Program</span><b>${id}</b> · ${p.use ? 'شغال ✓' : p.linked ? 'متربط' : 'بيتجمع'} · Shaders ${p.att.join(' + ') || '—'}${Object.keys(G.uni).length ? `<small>${Object.entries(G.uni).map(([n, v]) => `${n} = ${v}`).join(' · ')}</small>` : ''}${uc ? `<span class="sw" style="background:${uc}"></span>` : ''}</div>`); }
  if (G.win) h.push(`<div class="obj"><span class="tg" style="background:#555">state</span>glClear = (${G.clear.map(x => +(+x).toFixed(2)).join(', ')})${G.ps != 1 ? ' · point ' + G.ps + ' px' : ''}${G.depth ? ' · depth test' : ''}${G.cb ? ' · callback: ' + G.cb : ''}</div>`);
  $('gpuList').innerHTML = h.join('') || '<p class="fine" style="margin:0">الكارت لسه فاضي.</p>';
}
function drawRamList(s){
  const nxt = ST[i + 1]; const after = nxt && nxt.d === s.d && nxt.fn === s.fn ? Object.fromEntries(nxt.st[nxt.st.length - 1].v.map(x => [x[0], x])) : null;
  $('ramList').innerHTML = s.st.slice().reverse().map((f, k) => `<div class="frm${k ? ' dim' : ''}"><h4>${esc(f.fn)}()${k ? '' : ' ← شغالة'}</h4><table>${f.v.map(([n, v, u]) => { const a = !k && after && after[n]; const ch = a && (a[1] !== v || a[2] !== u) && !a[2];
    return `<tr${ch ? ' class="ch"' : ''}><td>${esc(n)}</td><td${u && !ch ? ' class="u"' : (String(v).length + (ch ? String(a[1]).length : 0) > 22 ? ' class="long"' : '')}>${ch ? esc(v) + ' → ' + esc(a[1]) : u ? 'لسه ما اتحطش' : esc(v)}</td></tr>`; }).join('')}</table></div>`).join('') || '<p class="fine">—</p>';
}
// per-step animations
function animateStep(dt){
  const s = ST[i]; if (!frozen) A.t += dt; const p = reduce ? 1 : Math.min(1, A.t / (A.dur * .8));
  tokens.forEach(m => m.visible = false);
  const wp = o => { const w = new T.Vector3(); o.getWorldPosition(w); return w; };
  const fly = (from, to, n, lift = .4) => tokens.slice(0, n).forEach((m, k) => { const q = Math.min(1, Math.max(0, p * 1.4 - k * .08)); m.visible = q > 0 && q < 1; m.position.lerpVectors(from, to, q); m.position.y += Math.sin(q * Math.PI) * lift; });
  if (s.an === 'upload'){ const m = /Buffer (\d+)/.exec((s.lv[0] || [])[1] || ''); const c = m && crates[m[1]]; if (c) fly(wp(parts.ram.g).add(new T.Vector3(0, .3, 0)), wp(c).add(new T.Vector3(0, .5, 0)), 6); }
  if (s.an === 'src'){ const to = /Fragment/.test(JSON.stringify(s.lv)) || (s.lv[0] && s.lv[0][0] === 'fs') ? parts.fs.g : parts.vs.g; fly(wp(parts.cpu.g).add(new T.Vector3(0, .9, 0)), wp(to).add(new T.Vector3(0, .6, 0)), 4); }
  if (s.an === 'uniform') fly(wp(parts.cpu.g).add(new T.Vector3(0, .9, 0)), wp(parts.prog.g).add(new T.Vector3(0, .3, 0)), 3);
  if (s.an === 'compile'){ const on = Math.sin(A.t * 12) > 0; if (s.lv[0] && s.lv[0][0] === 'fs') fsBar.material.emissive.setHex(on ? 0x6688ff : 0x202a60); else vsLamps.forEach(l => l.material.emissive.setHex(on ? 0xffd166 : 0x554400)); }
  if (s.an === 'link') progBar.material.emissive.setHex(Math.sin(A.t * 10) > 0 ? 0x3fd0bb : 0x1a4a40);
  if (s.an === 'attr'){ const m = /VAO (\d+)/.exec((s.lv[0] || [])[1] || ''); const tg = m && tags[m[1]]; if (tg){ tg.scale.setScalar(.75 + .25 * Math.min(1, p * 2)); } }
  else Object.values(tags).forEach(tg => tg.scale.setScalar(1));
  Object.values(crates).forEach(c => c.scale.setScalar(1));  // full size unless its own 'new' animation is running (it used to freeze small when stepping on early)
  if (s.an === 'new'){ const L = s.lv[0]; const g = L && anchor(L[0], L[1]); if (g && g !== bufG && g !== vaoG && (L[0] === 'buf' || L[0] === 'vao')) g.scale.setScalar(Math.min(1, .2 + p * 1.6)); }
  if (s.an === 'draw'){ const k = Math.min(3, Math.floor(p * 3.2 / .3 * .3 / .3)); const vp = Math.min(1, p / .3);
    vsLamps.forEach((l, j) => l.material.emissive.setHex(j < Math.floor(vp * 3.2) ? 0xffd166 : 0x332200));
    const crs = Object.values(crates); if (crs.length && p < .3) fly(wp(crs[0]).add(new T.Vector3(0, .5, 0)), wp(parts.vs.g).add(new T.Vector3(0, .5, 0)), 3, .3);
    drawRas(s.mk, Math.max(0, (p - .3) / .3), p < .3 ? 'off' : p < .6 ? 'scan' : 'done');
    fsBar.material.emissive.setHex(p >= .6 && p < 1 ? 0x3355ff : 0x202a60);
    paintAll(p); }
  else if (s.an === 'clear'){ paintAll(p); drawRas(null, 0, 'off'); }
  else if (s.an === 'swap'){ carG.rotation.y = (SWAPS[i] % 2) * Math.PI + ((1 - Math.cos(p * Math.PI)) / 2) * Math.PI; paintAll(p); }
  else if (s.an === 'click' && s.ev && s.ev.btn === 'key'){ fly(wp(parts.mouse.g).add(new T.Vector3(0, .4, 0)), wp(parts.cpu.g).add(new T.Vector3(0, .9, 0)), 2); drawMonitor(s.ft, s.ev, p); }
  else if (s.an === 'click'){ const b = s.ev && s.ev.btn === 'right' ? mBtnR : mBtnL; b.position.y = .32 - (s.ev && s.ev.act === 'press' ? .04 * Math.min(1, p * 3) : .04 * (1 - Math.min(1, p * 3)));
    fly(wp(parts.mouse.g).add(new T.Vector3(0, .4, 0)), wp(parts.cpu.g).add(new T.Vector3(0, .9, 0)), 2); drawMonitor(s.ft, s.ev, p); }
  else { mBtnL.position.y = mBtnR.position.y = .32; }
  if (s.an === 'check' || s.an === 'poll' || s.an === 'call' || s.an === 'ret') cpuLamp.material.emissive.setHex(Math.sin(A.t * 9) > 0 ? 0xff8a3d : 0x552200);
  if (playing && A.t >= A.dur){ if (i < ST.length - 1) go(i + 1); else play(false); }
}
let playing = false, frozen = false;
function play(on){ playing = on; if (on) frozen = false; $('key').setAttribute('aria-pressed', on); $('keyLabel').textContent = on ? 'إيقاف' : 'تشغيل'; syncPause(); }
function syncPause(){ const b = $('pause'); const paused = frozen || !playing; b.textContent = !paused ? '⏸ Pause' : frozen ? '▶ كمّل' : '▶ تشغيل'; b.setAttribute('aria-pressed', paused); }
$('pause').onclick = () => { if (playing){ playing = false; frozen = true; $('key').setAttribute('aria-pressed', false); $('keyLabel').textContent = 'تشغيل'; syncPause(); } else { frozen = false; play(true); } };
function go(k){ i = Math.max(0, Math.min(ST.length - 1, k)); if (!playing) frozen = false; applyStep(); }
$('key').onclick = () => { if (!playing && i >= ST.length - 1) go(0); if (playing){ playing = false; frozen = true; $('key').setAttribute('aria-pressed', false); $('keyLabel').textContent = 'تشغيل'; syncPause(); } else play(true); };
$('next').onclick = () => { play(false); go(i + 1); }; $('prev').onclick = () => { play(false); go(i - 1); }; $('replay').onclick = () => applyStep();
$('seek').oninput = e => { play(false); go(+e.target.value); };
const stepBy = d => { play(false); go(i + d); }; $('goDec').onclick = () => stepBy(-1); $('goInc').onclick = () => stepBy(1);
$('goStep').onsubmit = e => { e.preventDefault(); const inp = $('goN'), n = Math.round(+inp.value);
  if (!inp.value || isNaN(n) || n < 1 || n > ST.length){ inp.classList.add('bad'); inp.title = `اكتب رقم من 1 لـ ${ST.length}`; setTimeout(() => inp.classList.remove('bad'), 1200); return; }
  inp.blur(); play(false); go(n - 1); stage.scrollIntoView({behavior: reduce ? 'auto' : 'smooth', block: 'center'}); };
$('lever').oninput = () => { $('leverOut').textContent = secPerStep().toFixed(1) + ' s'; A.dur = secPerStep(); };
document.addEventListener('keydown', e => { if (e.target.tagName === 'INPUT' || !$('refbig').hidden) return; if (e.key === ' '){ e.preventDefault(); $('pause').click(); } if (e.key === 'ArrowLeft') $('next').click(); if (e.key === 'ArrowRight') $('prev').click(); if (e.key >= '1' && e.key <= '4') setMode(['painted','cutaway','flow','exploded'][+e.key - 1]); if (e.key === '+' || e.key === '=') zoom(.8); if (e.key === '-') zoom(1.25); });

// ------------------------------------------------------------------ modes & explode
function setMode(m){ mode = m; document.querySelectorAll('.modes button').forEach(b => b.setAttribute('aria-checked', b.dataset.mode === m)); $('callouts').classList.toggle('on', m === 'exploded'); }
document.querySelectorAll('.modes button').forEach(b => b.onclick = () => setMode(b.dataset.mode));
function applyModes(dt){
  const r = reduce ? 1 : Math.min(1, dt * 4);
  ex += ((mode === 'exploded' ? 1 : 0) - ex) * r; cut += ((mode !== 'painted' ? 1 : 0) - cut) * r; flow += ((mode === 'flow' ? 1 : 0) - flow) * r;
  for (const Pn of Object.values(parts)){ if (Pn.sub) continue; Pn.g.position.copy(Pn.home).addScaledVector(Pn.ex, ex); }
  lidMat.opacity = 1 - cut * .97; lidG.position.y = parts.lid.home.y + cut * .9 + ex * parts.lid.ex.y;
  wallMat.opacity = 1 - cut * .55; pipeMat.opacity = flow * .95;
}
const CALL = ['cpu','ram','buf','vao','vs','ras','fs','prog','car','mon','prn','mouse','ctx','lid'];
const callEls = CALL.map(n => { const d = document.createElement('div'); d.className = 'callout'; d.innerHTML = `${parts[n].label}<em>${parts[n].note}</em>`; $('callouts').appendChild(d); return d; });
const leadEls = CALL.map(() => { const p = document.createElementNS(svgNS, 'path'); p.setAttribute('fill', 'none'); p.setAttribute('stroke', cssv('--ink')); p.setAttribute('stroke-width', '.75'); $('leaders').appendChild(p); const c = document.createElementNS(svgNS, 'circle'); c.setAttribute('r', '2.2'); c.setAttribute('fill', cssv('--arancio')); $('leaders').appendChild(c); return [p, c]; });
function placeCallouts(rect){
  if (mode !== 'exploded') return;
  const pts = CALL.map((n, k) => { const w = new T.Vector3(); parts[n].g.getWorldPosition(w); const v = w.clone().project(cam); return {k, vis: parts[n].g.visible, x: rect.left + (v.x + 1) / 2 * rect.width, y: rect.top + (1 - v.y) / 2 * rect.height}; });
  const left = pts.filter(p => p.vis && p.x < rect.left + rect.width / 2).sort((a, b) => a.y - b.y), right = pts.filter(p => p.vis && p.x >= rect.left + rect.width / 2).sort((a, b) => a.y - b.y);
  pts.forEach(p => { callEls[p.k].style.display = p.vis ? '' : 'none'; leadEls[p.k][0].setAttribute('d', ''); leadEls[p.k][1].setAttribute('r', p.vis ? '2.2' : '0'); });
  const lay = (arr, lx) => { const step = Math.min(40, (rect.height - 40) / Math.max(1, arr.length)); let y0 = rect.top + 26;
    arr.forEach(p => { const ly = Math.max(y0, Math.min(rect.bottom - 20, p.y - 30)); y0 = ly + step; const el = callEls[p.k]; el.style.left = lx + 'px'; el.style.top = ly + 'px';
      const side = lx < p.x ? 1 : -1, e0 = lx + side * 70; leadEls[p.k][0].setAttribute('d', `M${p.x},${p.y} L${e0 + side * 14},${ly} L${e0},${ly}`); leadEls[p.k][1].setAttribute('cx', p.x); leadEls[p.k][1].setAttribute('cy', p.y); }); };
  lay(left, rect.left + 86); lay(right, rect.right - 86);
}

// ------------------------------------------------------------------ instruments
const I = { epath: $('epath').getContext('2d'), lmap: $('lmap').getContext('2d'), tach: $('tach').getContext('2d'), bytes: $('bytes').getContext('2d'), cycle: $('cycle').getContext('2d'), strip: $('strip').getContext('2d') };
function phaseOf(k){ // index into P.phases for step k (callbacks / nested calls map to the main-level line that is running)
  const s = ST[k]; if (!s.lap) return -1; for (let j = k; j >= 0 && ST[j].lap === s.lap; j--){ if (ST[j].d === 1){ const ix = P.phases.findIndex(p => p[0] === ST[j].v); if (ix >= 0) return ix; } } return -1; }
function shortName(t){ const m = /\b(gl\w+|glfw\w+)\s*\(/.exec(t); if (m) return m[1].replace(/^glfw/, '').replace(/^gl/, 'gl'); if (/^while/.test(t)) return 'check'; if (/^for/.test(t)) return 'for'; if (/^if/.test(t)) return 'if'; const n = /(\w+)\s*(\+\+|\+=|-=|=)/.exec(t); return n ? n[1] + (n[2] === '++' ? '++' : ' =') : t.slice(0, 10); }
function instr(){
  const ink = cssv('--ink'), ink3 = cssv('--ink-3'), ora = cssv('--arancio'), cel = cssv('--celeste-ink'), paper = cssv('--paper'), s = ST[i], G = s.gp;
  { const g = I.tach, c = 169, R = 150; g.clearRect(0,0,338,338); g.strokeStyle = ink; g.lineWidth = 1.2; g.beginPath(); g.arc(c, c, R, Math.PI * .75, Math.PI * 2.25); g.stroke(); g.font = '500 13px "IBM Plex Mono"'; g.fillStyle = ink; g.textAlign = 'center'; g.direction = 'ltr';
    for (let k = 0; k <= 4; k++){ const a = Math.PI * .75 + k / 4 * Math.PI * 1.5; g.beginPath(); g.moveTo(c + Math.cos(a) * (R - 18), c + Math.sin(a) * (R - 18)); g.lineTo(c + Math.cos(a) * R, c + Math.sin(a) * R); g.stroke(); g.fillText(k, c + Math.cos(a) * (R - 34), c + Math.sin(a) * (R - 34) + 5); }
    const v = s.st.length, a = Math.PI * .75 + Math.min(1, v / 4) * Math.PI * 1.5; g.strokeStyle = ora; g.lineWidth = 3; g.beginPath(); g.moveTo(c, c); g.lineTo(c + Math.cos(a) * (R - 24), c + Math.sin(a) * (R - 24)); g.stroke(); g.fillStyle = ink; g.beginPath(); g.arc(c, c, 7, 0, 7); g.fill();
    g.fillStyle = ink3; g.font = '500 12px "IBM Plex Mono"'; g.fillText('frames', c, c + 70); g.fillStyle = ink; g.font = '600 15px "IBM Plex Mono"'; g.fillText(s.fn ? s.fn.slice(0, 22) + '()' : 'idle', c, c + 100); }
  { const g = I.bytes, W = 338, H = 338; g.clearRect(0, 0, W, H); const bs = Object.entries(G.bufs); const max = Math.max(32, ...bs.map(([, b]) => b.bytes || 0));
    g.strokeStyle = ink; g.lineWidth = 1; g.beginPath(); g.moveTo(40, 30); g.lineTo(40, 270); g.lineTo(320, 270); g.stroke(); g.direction = 'ltr';
    if (!bs.length){ g.fillStyle = ink3; g.font = '500 14px "IBM Plex Mono"'; g.textAlign = 'center'; g.fillText('no buffers yet', 180, 160); }
    const bw = Math.min(70, 250 / Math.max(1, bs.length));
    bs.forEach(([id, b], k) => { const h = (b.bytes || 0) / max * 220, x = 52 + k * (bw + 10); const hot = (s.lv || []).some(l => l[1] === 'Buffer ' + id);
      g.fillStyle = b.t === 'EBO' ? cel : '#8a6a3a'; g.globalAlpha = hot ? 1 : .75; g.fillRect(x, 270 - h, bw, h); g.globalAlpha = 1; if (hot){ g.strokeStyle = ora; g.lineWidth = 3; g.strokeRect(x, 270 - h, bw, h); }
      g.fillStyle = ink; g.font = '700 14px "IBM Plex Mono"'; g.textAlign = 'center'; g.fillText((b.bytes || 0) + ' B', x + bw / 2, 262 - h); g.font = '500 12px "IBM Plex Mono"'; g.fillText('Buf ' + id, x + bw / 2, 288); g.fillText(b.t || '', x + bw / 2, 304); });
    g.fillStyle = ink3; g.font = '500 12px "IBM Plex Mono"'; g.textAlign = 'center'; g.fillText('bytes in VRAM (real glBufferData sizes)', 180, 328); }
  { const g = I.cycle, c = 169, R = 150, ph = P.phases, cur = phaseOf(i); g.clearRect(0,0,338,338); let a0 = -Math.PI / 2;
    if (!ph.length){ g.fillStyle = ink3; g.font = '500 13px "IBM Plex Mono"'; g.textAlign = 'center'; g.fillText('no loop', c, c); }
    ph.forEach((P_, k) => { const a1 = a0 + Math.PI * 2 / ph.length, on = k === cur; g.beginPath(); g.moveTo(c, c); g.arc(c, c, R, a0, a1); g.closePath();
      const u = LINE_UNIT[P_[0]]; g.fillStyle = on ? (u === 'GPU' ? '#0f766e' : u === 'CPU' ? ora : cel) : (k % 2 ? 'rgba(28,27,25,.05)' : 'rgba(28,27,25,.1)'); g.fill(); g.strokeStyle = ink; g.lineWidth = 1; g.stroke();
      const am = (a0 + a1) / 2; g.fillStyle = on ? paper : ink; g.direction = 'ltr';
      if (2 * Math.PI * R * .76 / ph.length >= 74){ g.textAlign = 'center'; g.font = '600 12px "IBM Plex Mono"'; g.fillText(lineOf(P_[0]), c + Math.cos(am) * R * .76, c + Math.sin(am) * R * .76);
        g.font = '500 10.5px "IBM Plex Mono"'; g.fillText(shortName(P_[1]).slice(0, 13), c + Math.cos(am) * R * .76, c + Math.sin(am) * R * .76 + 13); }
      else { // many lines: write each label along its spoke (radially), so neighbours never overlap
        const fs = Math.max(7.5, Math.min(11, 2 * Math.PI * 100 / ph.length * .62)), r0 = 52, r1 = R - 5, left = Math.cos(am) < 0;
        g.save(); g.translate(c, c); g.rotate(left ? am + Math.PI : am); g.textBaseline = 'middle';
        let lab = String(lineOf(P_[0])); g.font = `700 ${fs}px "IBM Plex Mono"`; const wNum = g.measureText(lab + ' ').width;
        g.font = `500 ${fs}px "IBM Plex Mono"`; let nm = shortName(P_[1]); while (nm.length > 1 && wNum + g.measureText(nm).width > r1 - r0) nm = nm.slice(0, -1);
        if (left){ g.textAlign = 'right'; g.font = `700 ${fs}px "IBM Plex Mono"`; g.fillText(lab, -r0, 0); g.font = `500 ${fs}px "IBM Plex Mono"`; g.fillText(nm, -r0 - wNum, 0); }
        else { g.textAlign = 'left'; g.font = `700 ${fs}px "IBM Plex Mono"`; g.fillText(lab, r0, 0); g.font = `500 ${fs}px "IBM Plex Mono"`; g.fillText(nm, r0 + wNum, 0); }
        g.restore(); }
      a0 = a1; });
    g.fillStyle = paper; g.beginPath(); g.arc(c, c, 46, 0, 7); g.fill(); g.strokeStyle = ink; g.stroke();
    if (cur >= 0){ const a = -Math.PI / 2 + (cur + .5) / ph.length * Math.PI * 2; g.strokeStyle = ora; g.lineWidth = 3; g.beginPath(); g.moveTo(c, c); g.lineTo(c + Math.cos(a) * R, c + Math.sin(a) * R); g.stroke();
      g.fillStyle = ink; g.font = '600 17px "IBM Plex Mono"'; g.textAlign = 'center'; g.fillText('lap ' + s.lap, c, c + 2); if (s.d > 1){ g.font = '500 10px "IBM Plex Mono"'; g.fillText('in ' + s.fn.slice(0, 10), c, c + 18); } }
    else { g.fillStyle = ink3; g.font = '500 13px "IBM Plex Mono"'; g.textAlign = 'center'; g.fillText(s.cl ? 'exit' : ST.slice(0, i).some(x => x.lap) ? 'after' : 'before', c, c + 5); } }
  { const g = I.strip, W = 704, H = 220, L = 30, B = 180; g.clearRect(0,0,W,H); g.strokeStyle = ink; g.lineWidth = 1.2; g.beginPath(); g.moveTo(L, 30); g.lineTo(L, B); g.lineTo(W - 20, B); g.stroke();
    const n = 60, bw = (W - 20 - L) / n, from = Math.max(0, i - n + 1);
    for (let k = from; k <= i; k++){ const q = ST[k], x = L + (k - from) * bw; const h = (q.u === 'CPU' ? .45 : q.u === 'GPU' ? 1 : .7) * (B - 50); g.fillStyle = unitCol(q.u); g.globalAlpha = k === i ? 1 : .55; g.fillRect(x + 1, B - h, Math.max(2, bw - 2), h);
      if (q.ev){ g.globalAlpha = 1; g.fillStyle = '#7d5cc4'; g.beginPath(); g.arc(x + bw / 2, B - h - 8, 4, 0, 7); g.fill(); } }
    g.globalAlpha = 1; g.fillStyle = ink3; g.font = '500 12px "IBM Plex Mono"'; g.textAlign = 'center'; g.direction = 'ltr'; g.fillText(`steps ${from + 1} – ${i + 1}   ·   orange = CPU, teal = GPU, blue = CPU→GPU, ● = mouse`, (L + W) / 2, B + 30); }
}

// line map over every source line (all files)
const LM = {L: 34, R: 690, T: 62, B: 222};
$('lmap').addEventListener('click', e => { const r = e.target.getBoundingClientRect(); const x = (e.clientX - r.left) / r.width * 704; const v = Math.floor((x - LM.L) / ((LM.R - LM.L) / NV)) + 1;
  if (v >= 1 && v <= NV){ let best = null; for (let d = 0; d < 4 && best === null; d++) for (const w of [v - d, v + d]) if (FIRST[w] !== undefined){ best = FIRST[w]; break; } if (best !== null){ play(false); go(best); } } });
function lmapLayout(){
  if (LM.pid === P.id) return; LM.pid = P.id;
  const c = $('lmap'), g = I.lmap, bw = (LM.R - LM.L) / NV, lanes = []; LM.lab = [];
  g.font = '600 14px "IBM Plex Mono"';
  P.regions.forEach(([a, b, n]) => { const x0 = LM.L + (a - 1) * bw, x1 = LM.L + b * bw, w = g.measureText(n).width;
    const tx = Math.min(LM.R - w / 2, Math.max(LM.L + w / 2, (x0 + x1) / 2)), box = [tx - w / 2 - 8, tx + w / 2 + 8];
    let L = 0; while (lanes[L] && lanes[L].some(([p, q]) => !(box[1] < p || box[0] > q))) L++;
    (lanes[L] = lanes[L] || []).push(box); LM.lab.push({n, tx, lane: L, mx: (x0 + x1) / 2}); });
  LM.fileY = 16; LM.T = (P.files.length > 1 ? 30 : 8) + 20 * Math.max(1, lanes.length) + 8; LM.B = LM.T + 160;
  const h = LM.B + 76; if (c.height !== h) c.height = h; }
function drawLineMap(){
  lmapLayout();
  const g = I.lmap, ink = cssv('--ink'), ink3 = cssv('--ink-3');
  g.clearRect(0, 0, 704, $('lmap').height); const bw = (LM.R - LM.L) / NV; g.direction = 'ltr';
  const counts = new Array(NV + 1).fill(0); for (let k = 0; k <= i; k++) counts[ST[k].v]++;
  const max = Math.max(4, ...counts);
  g.strokeStyle = ink; g.lineWidth = 1; g.beginPath(); g.moveTo(LM.L, LM.T); g.lineTo(LM.L, LM.B); g.lineTo(LM.R, LM.B); g.stroke();
  P.files.forEach((f, k) => { if (P.files.length < 2) return; const x0 = LM.L + f.off * bw; g.strokeStyle = ink; g.setLineDash([3, 3]); g.beginPath(); g.moveTo(x0, LM.fileY + 4); g.lineTo(x0, LM.B); g.stroke(); g.setLineDash([]); g.fillStyle = ink3; g.font = '600 12px "IBM Plex Mono"'; g.textAlign = 'left'; g.fillText(f.name, x0 + 3, LM.fileY); });
  g.font = '600 14px "IBM Plex Mono"'; g.textAlign = 'center';
  P.regions.forEach(([a, b, n, col], k) => { const x0 = LM.L + (a - 1) * bw, x1 = LM.L + b * bw; g.fillStyle = col; g.globalAlpha = .13; g.fillRect(x0, LM.T, x1 - x0, LM.B - LM.T); g.globalAlpha = 1;
    const lb = LM.lab[k], row = LM.T - 8 - lb.lane * 20;
    g.strokeStyle = ink3; g.lineWidth = 1; g.beginPath(); g.moveTo(lb.mx, row + 4); g.lineTo(lb.mx, LM.T); g.stroke(); g.fillStyle = col; g.fillText(n, lb.tx, row); });
  for (let v = 1; v <= NV; v++){ const u = LINE_UNIT[v], x = LM.L + (v - 1) * bw, c = counts[v];
    if (!u){ g.fillStyle = 'rgba(128,128,128,.35)'; g.fillRect(x + .5, LM.B - 3, Math.max(1, bw - 1), 3); continue; }
    const col = unitCol(u); g.globalAlpha = .25; g.fillStyle = col; g.fillRect(x + .5, LM.B - 8, Math.max(1, bw - 1), 8); g.globalAlpha = 1;
    if (c){ const h = 10 + (LM.B - LM.T - 14) * Math.sqrt(c / max); g.fillStyle = col; g.fillRect(x + .5, LM.B - h, Math.max(1, bw - 1), h); } }
  const cur = ST[i].v, cx = LM.L + (cur - .5) * bw; g.strokeStyle = ink; g.lineWidth = 1.5; g.beginPath(); g.moveTo(cx, LM.T); g.lineTo(cx, LM.B + 6); g.stroke();
  g.fillStyle = ink; g.beginPath(); g.moveTo(cx, LM.B + 2); g.lineTo(cx - 6, LM.B + 12); g.lineTo(cx + 6, LM.B + 12); g.fill();
  g.font = '700 17px "IBM Plex Mono"'; g.textAlign = cx > 560 ? 'right' : cx < 140 ? 'left' : 'center'; g.fillText(`line ${lineOf(cur)} · ${LINE_UNIT[cur] || '—'} · ×${counts[cur]}`, cx, LM.B + 32);
  const lg = [[cssv('--arancio'), 'CPU'], ['#0f766e', 'GPU'], [cssv('--celeste-ink'), 'CPU→GPU'], ['rgba(128,128,128,.6)', 'not executed']]; let lx = LM.L;
  g.textAlign = 'left'; g.font = '600 16px "IBM Plex Mono"'; lg.forEach(([c, t]) => { g.fillStyle = c; g.fillRect(lx, LM.B + 50, 16, 16); g.fillStyle = ink; g.fillText(t, lx + 21, LM.B + 64); lx += 34 + g.measureText(t).width; });
}

// execution path (virtual line over time)
function regionOf(v){ return P.regions.find(([a, b]) => v >= a && v <= b); }
function jumpNote(k){
  if (k === 0) return null; const a = ST[k-1], b = ST[k];
  if (b.ev) return b.ev.btn === 'key' ? `⌨ GLFW نده ${b.fn}() (زرار ${b.ev.key})` : `🖱 GLFW نده ${b.fn}() (ضغطة ${b.ev.btn === 'left' ? 'شمال' : 'يمين'})`;
  if (b.d > a.d) return `↕ نداء ${b.fn}(): من سطر ${lineOf(a.v)} لـ ${lineOf(b.v)}`;
  if (b.d < a.d) return `↩ رجعنا لـ ${b.fn}() بعد return: سطر ${lineOf(b.v)}`;
  if (b.an === 'check' && b.v < a.v) return `↑ رجع لأول الـ while (سطر ${lineOf(b.v)})`;
  const dv = b.v - a.v; if (Math.abs(dv) <= 2) return null;
  if (dv < 0) return `↑ نط لفوق لسطر ${lineOf(b.v)} (loop)`;
  return `↓ نط لتحت لسطر ${lineOf(b.v)} (تخطّى ${dv - 1} سطر)`;
}
const EP = {L: 74, R: 692, T: 24, B: 360};
function epFns(W, H, full){ const E = full ? {L: P.files.length > 1 ? 175 : 120, R: W - 30, T: 60, B: H - 110} : EP; const n = full ? ST.length : ST.length;
  return {E, X: k => E.L + k / Math.max(1, n - 1) * (E.R - E.L), Y: v => E.T + (v - 1) / Math.max(1, NV - 1) * (E.B - E.T)}; }
$('epath').addEventListener('click', e => { const r = e.target.getBoundingClientRect(); const x = (e.clientX - r.left) / r.width * 704; const k = Math.round((x - EP.L) / (EP.R - EP.L) * (ST.length - 1)); if (k >= 0 && k < ST.length){ play(false); go(k); } });
function refMarks(){ const seen = new Set(), marks = [];
  ST.forEach((q, k) => { if ((k === 0 || q.d !== ST[k-1].d) && !seen.has(q.fn) && (k === 0 || q.d > ST[k-1].d)){ seen.add(q.fn); marks.push({k, fn: q.fn, cb: !!q.ev}); } }); return marks; }
function refLegend(W){ const n = refMarks().length, cols = 3, fs = Math.round(W / 62); return {cols, cw: (W - 60) / cols, rh: fs * 2, fs, h: Math.ceil(n / cols) * fs * 2 + 24}; }
function drawPath(g, W, H, upto, full){
  if (full){ const want = H + refLegend(W).h; if (g.canvas.height !== want) g.canvas.height = want; }
  const ink = full ? '#1c1b19' : cssv('--ink'), ora = '#e0561c', paper = full ? '#ffffff' : cssv('--paper'); const {E, X, Y} = epFns(W, H, full); const sc = full ? 2 : 1;
  g.clearRect(0, 0, W, g.canvas.height); if (full){ g.fillStyle = '#fff'; g.fillRect(0, 0, W, g.canvas.height); } g.direction = 'ltr';
  let regLast = -1e9; const RL = [], RLB = []; P.regions.forEach(([a, b, n, c]) => { const y0 = Y(a - .5), y1 = Y(b + .5); g.fillStyle = c; g.globalAlpha = .13; g.fillRect(E.L, y0, E.R - E.L, y1 - y0); g.globalAlpha = 1;
    const ty = Math.max(y0 + 16 * sc, regLast + 18 * sc); if (ty <= y1 + 2 * sc && ty < E.B){ regLast = ty; g.font = `700 ${15 * sc}px "IBM Plex Mono"`; const twb = g.measureText(n).width; RLB.push({x0: E.R - 12 - twb, x1: E.R, y0: ty - 15 * sc, y1: ty + 5 * sc}); RL.push(() => { g.font = `700 ${15 * sc}px "IBM Plex Mono"`; g.textAlign = 'right'; const tw_ = g.measureText(n).width; g.fillStyle = full ? 'rgba(255,255,255,.88)' : paper; g.globalAlpha = full ? 1 : .88; g.fillRect(E.R - 10 - tw_, ty - 14 * sc, tw_ + 8, 18 * sc); g.globalAlpha = 1; g.fillStyle = c; g.fillText(n, E.R - 6, ty); }); } });
  if (P.files.length > 1) P.files.forEach(f => { const y = Y(f.off + .5); g.strokeStyle = ink; g.setLineDash([4, 4]); g.beginPath(); g.moveTo(E.L, y); g.lineTo(E.R, y); g.stroke(); g.setLineDash([]); g.fillStyle = ink; g.font = `600 ${12 * sc}px "IBM Plex Mono"`; g.textAlign = 'left'; g.fillText(f.name, E.L + 4, y + 13 * sc); });
  g.strokeStyle = ink; g.lineWidth = 1 * sc; g.beginPath(); g.moveTo(E.L, E.T); g.lineTo(E.L, E.B); g.lineTo(E.R, E.B); g.stroke();
  g.fillStyle = ink; g.font = `600 ${13 * sc}px "IBM Plex Mono"`; g.textAlign = 'right';
  const ticks = new Set([1, NV]); P.regions.forEach(([a]) => ticks.add(a)); let lastY = -99; [...ticks].sort((a, b) => a - b).forEach(v => { const y = Y(v); if (y - lastY < 14 * sc) return; lastY = y; g.fillText(lineOf(v, true), E.L - 6, y + 5); });
  g.textAlign = 'center'; const stepT = ST.length > 200 ? 50 : ST.length > 80 ? 20 : 10; for (let k = 0; k < ST.length - stepT / 2; k += stepT) g.fillText(k + 1, X(k), E.B + 20 * sc); g.fillText(ST.length, X(ST.length - 1), E.B + 20 * sc);
  g.font = `700 ${16 * sc}px "IBM Plex Sans Arabic", sans-serif`; g.direction = 'rtl'; g.fillText('ترتيب التنفيذ: خطوة 1، 2، 3 …  (الوقت ←)', (E.L + E.R) / 2, E.B + 48 * sc);
  g.save(); g.translate(20 * sc, (E.T + E.B) / 2); g.rotate(-Math.PI / 2); g.fillText(P.files.length > 1 ? 'رقم السطر (الملفات ورا بعض)' : 'رقم السطر في الملف', 0, 0); g.restore(); g.direction = 'ltr';
  // laps shading
  let l0 = null, lapRight = -1e9; ST.forEach((s, k) => { if (s.lap && (k === 0 || ST[k-1].lap !== s.lap)) l0 = k; if (s.lap && (k === ST.length - 1 || ST[k+1].lap !== s.lap)){ g.fillStyle = 'rgba(39,64,139,.06)'; g.fillRect(X(l0) - 2, E.T, X(k) - X(l0) + 4, E.B - E.T); g.fillStyle = '#27408b'; g.font = `600 ${11 * sc}px "IBM Plex Mono"`; g.textAlign = 'center'; const lt = 'lap ' + s.lap, lw = g.measureText(lt).width, lc = (X(l0) + X(k)) / 2; if (lc - lw / 2 > lapRight + 6 * sc){ g.fillText(lt, lc, E.T - 6); lapRight = lc + lw / 2; } } });
  if (!full){ g.strokeStyle = 'rgba(128,128,128,.28)'; g.lineWidth = 1; g.beginPath(); ST.forEach((x, k) => k ? g.lineTo(X(k), Y(x.v)) : g.moveTo(X(k), Y(x.v))); g.stroke(); }
  g.strokeStyle = ink; g.lineWidth = 1.5 * sc; g.beginPath(); for (let k = 0; k <= upto; k++){ const x = X(k), y = Y(ST[k].v); k ? g.lineTo(x, y) : g.moveTo(x, y); } g.stroke();
  for (let k = 0; k <= upto; k++){ const q = ST[k], c = q.u === 'GPU' ? '#0f766e' : q.u === 'CPU' ? ora : '#2c79a6'; const hollow = k && ST[k-1].v === q.v;
    g.beginPath(); g.arc(X(k), Y(q.v), (hollow ? 3.4 : 2.6) * (full ? 1.6 : 1), 0, 7); if (hollow){ g.fillStyle = paper; g.fill(); g.strokeStyle = c; g.lineWidth = 1.6; g.stroke(); } else { g.fillStyle = c; g.fill(); }
    if (q.ev){ g.fillStyle = '#7d5cc4'; g.font = `${13 * sc}px sans-serif`; g.textAlign = 'center'; g.fillText(q.ev.btn === 'key' ? '⌨' : '🖱', X(k), Y(q.v) - 8 * sc); } }
  RL.forEach(f => f());
  if (full){ // a ring + a small numbered badge at the first step of every function; the names go in a numbered list under the chart
    const marks = refMarks(), circ = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳', R = Math.round(W / 90), br = Math.round(W / 110), placed = [];
    const hit = (a, b) => !(a.x1 < b.x0 - 3 || a.x0 > b.x1 + 3 || a.y1 < b.y0 - 3 || a.y0 > b.y1 + 3);
    marks.forEach(m => { const px = X(m.k), py = Y(ST[m.k].v); placed.push({x0: px - R, x1: px + R, y0: py - R, y1: py + R}); });
    RLB.forEach(b => placed.push(b));
    marks.forEach((m, n) => {
      const px = X(m.k), py = Y(ST[m.k].v), col = m.fn === 'main' ? '#c2410c' : m.cb ? '#7d5cc4' : '#1f6fd1';
      g.lineWidth = Math.max(3, R / 4); g.strokeStyle = col; g.beginPath(); g.arc(px, py, R, 0, 7); g.stroke();
      g.globalAlpha = .15; g.fillStyle = col; g.beginPath(); g.arc(px, py, R, 0, 7); g.fill(); g.globalAlpha = 1;
      let bx = null, by = null;
      for (let dist = R + br + 4; dist < W / 3 && bx === null; dist += br * 1.2)
        for (let t = 0; t < 16; t++){ const a = -Math.PI / 2 + t * Math.PI / 8, cx = px + Math.cos(a) * dist, cy = py + Math.sin(a) * dist;
          if (cx - br < E.L || cx + br > E.R || cy - br < E.T || cy + br > E.B) continue;
          const b = {x0: cx - br, x1: cx + br, y0: cy - br, y1: cy + br}; if (placed.some(p => hit(p, b))) continue; bx = cx; by = cy; placed.push(b); break; }
      if (bx === null){ bx = px; by = py - R - br - 4; }
      const ang = Math.atan2(py - by, px - bx), ex = px - Math.cos(ang) * (R + 2), ey = py - Math.sin(ang) * (R + 2);
      g.lineWidth = Math.max(2, R / 7); g.strokeStyle = col; g.beginPath(); g.moveTo(bx + Math.cos(ang) * br, by + Math.sin(ang) * br); g.lineTo(ex, ey); g.stroke();
      g.fillStyle = col; g.beginPath(); g.arc(bx, by, br, 0, 7); g.fill();
      g.fillStyle = '#fff'; g.font = `700 ${Math.round(br * 1.25)}px "IBM Plex Mono"`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(String(n + 1), bx, by + 1); g.textBaseline = 'alphabetic';
    });
    // the numbered list under the chart
    const L = refLegend(W), y0 = H + 10;
    g.strokeStyle = '#d6d3cc'; g.lineWidth = 1; g.beginPath(); g.moveTo(30, H); g.lineTo(W - 30, H); g.stroke();
    marks.forEach((m, n) => { const col = m.fn === 'main' ? '#c2410c' : m.cb ? '#7d5cc4' : '#1f6fd1', r = Math.floor(n / L.cols), c = n % L.cols;
      const xr = W - 30 - c * L.cw, yy = y0 + r * L.rh + L.rh / 2;
      g.fillStyle = col; g.beginPath(); g.arc(xr - br, yy, br, 0, 7); g.fill();
      g.fillStyle = '#fff'; g.font = `700 ${Math.round(br * 1.25)}px "IBM Plex Mono"`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(String(n + 1), xr - br, yy + 1);
      g.fillStyle = '#1c1b19'; g.font = `600 ${L.fs}px "IBM Plex Sans Arabic", sans-serif`; g.direction = 'rtl'; g.textAlign = 'right';
      let t = `بداية ${m.fn}()\u200E` + (m.cb ? ' (GLFW ندهها)' : '') + ` · خطوة ${m.k + 1}`; const maxw = L.cw - 3 * br - 16;
      if (g.measureText(t).width > maxw){ t = `بداية ${m.fn}()\u200E · خطوة ${m.k + 1}`; }
      let fs2 = L.fs; while (g.measureText(t).width > maxw && fs2 > 10){ fs2--; g.font = `600 ${fs2}px "IBM Plex Sans Arabic", sans-serif`; }
      g.fillText(t, xr - 2 * br - 8, yy + 1); g.textBaseline = 'alphabetic'; g.direction = 'ltr'; });
    g.fillStyle = ink; g.font = `700 ${20}px "IBM Plex Sans Arabic"`; g.direction = 'rtl'; g.textAlign = 'right'; g.fillText(`${P.title} · ${ST.length} خطوة · ${P.files.map(f => f.name).join(' + ')}`, W - 30, 30); g.direction = 'ltr';
    return; }
  const x = X(i), y = Y(ST[i].v), pulse = 6 + 3 * Math.abs(Math.sin(performance.now() / 300));
  g.strokeStyle = ora; g.lineWidth = 2.5; g.beginPath(); g.arc(x, y, pulse, 0, 7); g.stroke();
  g.fillStyle = ink; g.font = '700 15px "IBM Plex Mono"'; g.textAlign = x > 450 ? 'right' : 'left'; g.fillText('line ' + lineOf(ST[i].v), x + (x > 450 ? -12 : 12), y - 10);
  for (let k = i; k > 0 && i - k < 4; k--){ const n = jumpNote(k); if (!n) continue;
    g.font = '600 15px "IBM Plex Sans Arabic", sans-serif'; g.direction = 'rtl'; const w = g.measureText(n).width + 20; const bx = Math.min(E.R - w, Math.max(E.L + 4, X(k) - w / 2)), by = Y(ST[k].v) > (E.T + E.B) / 2 ? E.T + 8 : E.B - 40;
    g.fillStyle = 'rgba(224,86,28,.92)'; g.fillRect(bx, by, w, 30); g.fillStyle = '#fff'; g.textAlign = 'center'; g.fillText(n, bx + w / 2, by + 21); g.direction = 'ltr';
    g.strokeStyle = 'rgba(224,86,28,.8)'; g.lineWidth = 1.2; g.setLineDash([4, 3]); g.beginPath(); g.moveTo(bx + w / 2, by + (by < 200 ? 30 : 0)); g.lineTo(X(k), Y(ST[k].v)); g.stroke(); g.setLineDash([]); break; }
}
// reference map (full path, hidden by default)
let refDirty = true;
function drawRefMaps(){ refDirty = true; if (!$('refbody').hidden) paintRef(); if (!$('refbig').hidden) paintRefBig(); }
function paintRef(){ drawPath($('refthumb').getContext('2d'), 1400, 860, ST.length - 1, true); }
function paintRefBig(){ drawPath($('refbigimg').getContext('2d'), 2800, 1720, ST.length - 1, true); }
$('reftoggle').onclick = () => { const b = $('refbody'); b.hidden = !b.hidden; if (!b.hidden) paintRef(); $('reftoggle').textContent = b.hidden ? '🗺️ اعرض الخريطة' : '✕ خبّي الخريطة'; $('reftoggle').setAttribute('aria-expanded', !b.hidden); };
let refZ = 100;
function setRefZoom(z, cx, cy){ const box = $('refscroll'), im = $('refbigimg'), old = refZ; z = Math.max(100, Math.min(500, Math.round(z))); if (z === old) return;
  const r = im.getBoundingClientRect(), br = box.getBoundingClientRect(); const px = cx === undefined ? br.left + br.width / 2 : cx, py = cy === undefined ? br.top + br.height / 2 : cy;
  const fx = (px - r.left) / r.width, fy = (py - r.top) / r.height; refZ = z; im.style.width = z + '%'; $('refzr').value = z; $('refzv').textContent = z + '%';
  const r2 = im.getBoundingClientRect(); box.scrollLeft += (r2.left + fx * r2.width) - px; box.scrollTop += (r2.top + fy * r2.height) - py; }
$('refin').onclick = () => setRefZoom(refZ * 1.25); $('refout').onclick = () => setRefZoom(refZ / 1.25); $('refzr').oninput = e => setRefZoom(+e.target.value);
$('refscroll').addEventListener('wheel', e => { e.preventDefault(); setRefZoom(refZ * (e.deltaY < 0 ? 1.12 : 1 / 1.12), e.clientX, e.clientY); }, {passive:false});
{ const pts = new Map(); let d0 = 0, z0 = 100, mid = [0, 0], pan = null; const im = $('refbigimg');
  im.addEventListener('pointerdown', e => { pts.set(e.pointerId, [e.clientX, e.clientY]); im.setPointerCapture(e.pointerId);
    if (pts.size === 2){ const [a, b] = [...pts.values()]; d0 = Math.hypot(a[0]-b[0], a[1]-b[1]); z0 = refZ; mid = [(a[0]+b[0])/2, (a[1]+b[1])/2]; pan = null; } else pan = {x: e.clientX, y: e.clientY, sl: $('refscroll').scrollLeft, st: $('refscroll').scrollTop}; });
  im.addEventListener('pointermove', e => { if (!pts.has(e.pointerId)) return; pts.set(e.pointerId, [e.clientX, e.clientY]);
    if (pts.size === 2 && d0){ const [a, b] = [...pts.values()]; setRefZoom(z0 * Math.hypot(a[0]-b[0], a[1]-b[1]) / d0, mid[0], mid[1]); }
    else if (pan && e.pointerType === 'mouse'){ $('refscroll').scrollLeft = pan.sl - (e.clientX - pan.x); $('refscroll').scrollTop = pan.st - (e.clientY - pan.y); } });
  const up = e => { pts.delete(e.pointerId); if (pts.size < 2) d0 = 0; if (!pts.size) pan = null; }; im.addEventListener('pointerup', up); im.addEventListener('pointercancel', up);
  im.addEventListener('dblclick', e => setRefZoom(refZ > 150 ? 100 : 250, e.clientX, e.clientY)); }
function fmSync(){ const ok = !!(P && P.fmap); $('fmFig').hidden = !ok; if (ok && !$('fmBody').hidden) $('fmImg').src = P.fmap; if (!ok && !$('fmBody').hidden){ $('fmBody').hidden = true; } }
$('fmToggle').onclick = () => { const b = $('fmBody'); b.hidden = !b.hidden; if (!b.hidden && P.fmap) $('fmImg').src = P.fmap; $('fmToggle').textContent = b.hidden ? '🖼️ اعرض الصورة' : '✕ خبّي الصورة'; $('fmToggle').setAttribute('aria-expanded', !b.hidden); };
let fmFull = false;
function fmSize(){ const im = $('fmBigImg'); im.style.width = fmFull ? (im.naturalWidth || 2400) + 'px' : '100%'; im.style.maxWidth = fmFull ? 'none' : '100%'; $('fmZoom').textContent = fmFull ? '↔️ على قد الشاشة' : '🔍 الحجم الكامل'; }
$('fmImg').onclick = () => { $('fmBigImg').src = P.fmap; fmFull = false; fmSize(); $('fmBig').hidden = false; document.body.style.overflow = 'hidden'; $('fmBig').scrollTo(0, 0); };
$('fmZoom').onclick = () => { fmFull = !fmFull; fmSize(); $('fmBig').scrollTo(0, 0); };
$('fmClose').onclick = () => { $('fmBig').hidden = true; document.body.style.overflow = ''; };
document.addEventListener('keydown', e => { if (e.key === 'Escape' && !$('fmBig').hidden) $('fmClose').click(); });
$('refthumb').onclick = () => { paintRefBig(); $('refbig').hidden = false; $('refbig').style.display = 'flex'; document.body.style.overflow = 'hidden'; refZ = 101; setRefZoom(100); $('refscroll').scrollTo(0, 0); };
$('refclose').onclick = () => { $('refbig').hidden = true; $('refbig').style.display = ''; document.body.style.overflow = ''; };
document.addEventListener('keydown', e => { if ($('refbig').hidden) return; if (e.key === 'Escape') $('refclose').click(); if (e.key === '+' || e.key === '='){ e.stopPropagation(); setRefZoom(refZ * 1.25); } if (e.key === '-'){ e.stopPropagation(); setRefZoom(refZ / 1.25); } }, true);

// ------------------------------------------------------------------ frame loop
let last = performance.now();
function frame(now){
  const dt = Math.min(.1, (now - last) / 1000); last = now;
  if (P){ animateStep(dt); applyModes(dt); placeCam();
    const W = innerWidth, H = innerHeight;
    if (canvas.width !== Math.floor(W * renderer.getPixelRatio()) || canvas.height !== Math.floor(H * renderer.getPixelRatio())) renderer.setSize(W, H, false);
    renderer.setViewport(0, 0, W, H); renderer.setScissor(0, 0, W, H); renderer.clear();
    const r = stage.getBoundingClientRect();
    if (r.width > 10 && r.height > 10 && r.bottom > 0 && r.top < H){ renderer.setViewport(r.left, H - r.bottom, r.width, r.height); renderer.setScissor(r.left, H - r.bottom, r.width, r.height); cam.aspect = r.width / r.height; cam.updateProjectionMatrix(); renderer.render(scene, cam); placeCallouts(r); }
    tickLive(); instr(); drawLineMap(); drawPath(I.epath, 704, 430, i, false); }
  requestAnimationFrame(frame);
}

// ------------------------------------------------------------------ glossary
%%GLOSS%%
function renderGloss(q){ q = (q || '').trim().toLowerCase();
  $('glList').innerHTML = Object.keys(G).filter(k => k !== 'ترجمة').filter(k => !q || k.toLowerCase().includes(q) || G[k][0].toLowerCase().includes(q) || G[k][1].toLowerCase().includes(q))
    .map(t => `<div><dt>${t}</dt><dd>${G[t][0]}<span class="eg">مثال من الحياة: ${G[t][1]}</span></dd></div>`).join('') || '<p class="fine">مفيش كلمة بالاسم ده.</p>'; }
function showGloss(on){ $('gloss').hidden = !on; if (on && $('cmdSheet') && !$('cmdSheet').hidden) showCmd(false); $('glossBtn').setAttribute('aria-expanded', on); $('glossBtn').textContent = on ? '✕ خبّي القاموس' : '📖 القاموس'; if (on){ renderGloss($('glq').value); if (!$('legend').hidden) showLegend(false); if ($('stepsSheet') && !$('stepsSheet').hidden) showSteps(false); } }
$('glossBtn').onclick = () => showGloss($('gloss').hidden); $('glX').onclick = () => showGloss(false);
$('glq').oninput = e => renderGloss(e.target.value);
document.addEventListener('keydown', e => { if (e.key === 'Escape' && !$('gloss').hidden) showGloss(false); });
renderGloss('');


// ------------------------------------------------------------------ device legend: picture + name + description (hidden until asked)
const LEG = [
  ['cpu', 'الـ CPU (المعالج)', 'CPU', 'بينفذ كود الـ C++ سطر سطر، وهو اللي بيبعت الأوامر للكارت. الأطباق اللي فوقه = إطارات الـ Stack: كل دالة شغالة ليها طبق مكتوب عليه اسمها، ولما الدالة تخلص الطبق بيتشال.', 'اللمبة اللي فوقه بتنور لما الـ CPU هو اللي شغال (السطر البرتقاني في المسجّل).'],
  ['ram', 'الرام', 'RAM · locals', 'ذاكرة الكمبيوتر العادية. الشاشة اللي عليها بتعرض متغيرات الدالة الشغالة دلوقتي بقيمها الحقيقية من التشغيل، زي <code>window</code> و <code>location</code> والمصفوفات. علامة ؟ = المتغير لسه ما اتحطش فيه قيمة.', 'بتتغير مع كل سطر بيكتب في متغير.'],
  ['gpu', 'كارت الشاشة', 'GPU', 'الصندوق الأزرق الكبير. أي أمر بيبدأ بـ <code>gl</code> بيروح هنا. جواه كل القطع اللي تحت: الـ Buffers والـ VAOs والـ Shaders والـ Rasterizer والـ Framebuffers.', 'بيبقى شغال بعد <code>glfwMakeContextCurrent</code>.'],
  ['ctx', 'لمبة الـ Context', 'Context', 'لمبة صغيرة في ركن الكارت. لما تنور معناها إن الوصلة بين برنامجك والكارت اتفتحت، ومن هنا أوامر gl تقدر تشتغل.', 'بتنور عند <code>glfwMakeContextCurrent</code>.'],
  ['buf', 'الصناديق: Buffers', 'VBO · EBO', 'كل صندوق خشب = Buffer على الكارت. مكتوب على وشه رقمه ونوعه: <b>VBO</b> للأركان، <b>EBO</b> لجدول أرقام الأركان. وعلى غطاه حجمه بالبايت وأول الأرقام اللي جواه.', 'بيظهر عند <code>glGenBuffers</code> ويتملي عند <code>glBufferData</code> (الكور الصفرا بتجري من الرام له).'],
  ['vao', 'اليفط الصفرا: VAOs', 'VAO', 'ورقة التعليمات اللي بتقول للكارت يقرا الصندوق (الـ Buffer) إزاي: كل خانة <code>loc</code> فيها كام رقم (<code>2f</code>)، والـ stride بالبايت، والـ offset، ومن أنهي Buffer، والـ EBO لو فيه. العلامة ● = الـ VAO المربوط دلوقتي.', 'بتظهر عند <code>glGenVertexArrays</code> وتتكتب عند <code>glVertexAttribPointer</code>.'],
  ['vs', 'محطة الـ Vertex Shader', 'Vertex Shader', 'محطة رمادي عليها 3 لمبات صفرا. الـ Vertex Shader برنامج صغير على الكارت بيحدد مكان كل ركن على الشاشة.', 'اللمبات بتنور لما يتترجم (<code>glCompileShader</code>)، ووقت الرسم بتنور واحدة ورا التانية = بيشتغل مرة لكل ركن.'],
  ['ras', 'شاشة الـ Rasterizer', 'Rasterizer', 'الشاشة الصغيرة المقسومة مربعات. جزء ثابت جوه الكارت، مش كود انت بتكتبه. بيقرر أنهي بكسلات جوه الشكل. المربعات اللي بتنور هي البكسلات الحقيقية اللي اتغيرت في التشغيل، ومكتوب عددها.', 'بيشتغل وقت <code>glDrawArrays</code> / <code>glDrawElements</code> (الخط الأصفر بيمسح من فوق لتحت).'],
  ['fs', 'محطة الـ Fragment Shader', 'Fragment Shader', 'محطة رمادي عليها شريط أزرق. الـ Fragment Shader بيلوّن كل بكسل الـ Rasterizer اختاره.', 'الشريط بينور وقت التلوين، وفي نفس الوقت الصورة بتتكتب في اللوحة اللي ورا.'],
  ['prog', 'شريط الـ Program', 'Program · uniforms', 'الشريط الأخضر واليافطة السودا. الـ Program = الـ Vertex والـ Fragment Shader مربوطين مع بعض. اليافطة بتكتب الـ uniforms زي <code>u_Color</code>، والمربع الملون = اللون الحقيقي اللي اتبعت.', 'بيتعمل عند <code>glCreateProgram</code> و <code>glLinkProgram</code>، ويبقى شغال عند <code>glUseProgram</code>، والـ uniform يتكتب عند <code>glUniform4f</code>.'],
  ['car', 'القرص: Framebuffers A و B', 'Back · Front', 'لوحتين رسم على قرص بيلف. اللوحة اللي بيترسم فيها في الخفا = <b>Back</b>، واللي على الشاشة = <b>Front</b>. الصور اللي عليهم اتقرت من الكارت فعلاً.', '<code>glClear</code> بيمسح اللي ورا، والرسم بيكتب فيه، و <code>glfwSwapBuffers</code> بيلف القرص نص لفة فاللوحتين يتبدلوا.'],
  ['mon', 'الشاشة', 'Window', 'الشباك اللي المستخدم شايفه. بيعرض اللوحة اللي قدام (Front) بس. علامة + الصفرا = مكان ضغطة الماوس.', 'بتظهر عند <code>glfwCreateWindow</code>، والصورة بتتغير بعد كل Swap.'],
  ['prn', 'الطابعة', 'Terminal · std::cout', 'كل حاجة البرنامج بيطبعها بـ <code>std::cout</code> بتطلع على الورقة دي، والسطر الجديد لونه مختلف.', 'بتطبع مع أي سطر فيه <code>std::cout</code>.'],
  ['mouse', 'الماوس', 'Mouse · events', 'الضغطات الحقيقية اللي اتبعتت للشباك وقت التشغيل. الزرار بينزل مع Press ويطلع مع Release.', 'لما GLFW يلاقي ضغطة جوه <code>glfwPollEvents</code> بينده <code>MouseButtonCallback</code> لوحده، والكورة الصفرا بتجري من الماوس للـ CPU.'],
  ['lid', 'غطا الكارت', 'lid', 'غطا الصندوق الأزرق. في وضع «مقفول» بيبان، وفي «مفتوح» و«مسار الداتا» و«مفكّك» بيتشال عشان تشوف جوه.', 'بيتحكم فيه أزرار العرض تحت.'],
  ['token', 'الكور الصفرا', 'data on the move', 'داتا بتتنقل من مكان لمكان: أرقام من الرام للصندوق، نص Shader من الـ CPU للمحطة، قيمة uniform للـ Program، أو ضغطة من الماوس للـ CPU.', 'بتظهر بس في الخطوات اللي فيها نقل.'],
  ['ring', 'الحلقة البرتقاني + الكارت', 'live callout', 'بتلف حوالين القطعة اللي اتغيرت في الخطوة دي، والكارت البرتقاني جنبها بيكتب اتغيرت إزاي وبسبب أنهي سطر.', 'بتتغير مع كل خطوة.'],
];
let legR = null;
function legShot(key){
  if (!legR){ const c = document.createElement('canvas'); legR = new T.WebGLRenderer({canvas: c, antialias: true, alpha: true, preserveDrawingBuffer: true}); legR.setPixelRatio(1); legR.setSize(264, 198, false); legR.setClearColor(0x000000, 0); }
  const vis = scene.children.map(o => o.visible);
  let target = null, temp = null;
  if (key === 'token'){ temp = new T.Mesh(new T.SphereGeometry(.09, 16, 16), tokMat); }
  else if (key === 'ring'){ temp = new T.Group(); const r = new T.Mesh(new T.RingGeometry(.45, .55, 40), new T.MeshBasicMaterial({color:0xe0561c, side:T.DoubleSide})); r.rotation.x = -Math.PI/2; temp.add(r); }
  else if ((key === 'buf' && !Object.keys(crates).length) || (key === 'vao' && !Object.keys(tags).length)){
    temp = new T.Group(); if (key === 'buf'){ temp.add(box(.68, .42, .62, M(0x8a6a3a, {roughness:.8}), 0, .21, 0)); const f = labelPlane(['Buffer 1 VBO'], .66, .2, 256, 76, {size:30, bg:'#4a3620', fg:'#ffd166'}); f.position.set(0, .22, .32); temp.add(f); }
    else { const p = labelPlane(['VAO 1 ●', 'loc0: 2f /8B @0'], .78, .62, 300, 236, {size:24, bg:'#fff6c9', fg:'#5c4400'}); p.position.y = .42; temp.add(p); temp.add(box(.05, .3, .05, M(0x3a362f), 0, .1, 0)); } }
  if (temp){ temp.position.set(40, 0, 40); scene.add(temp); target = temp; }
  else target = key === 'ctx' ? parts.gpu.g : parts[key].g;
  let top = target; while (top.parent && top.parent !== scene) top = top.parent;
  scene.children.forEach(o => { if (!(o.isLight)) o.visible = o === top; });
  const lidVis = lidG.visible; if (top === gpuG || key === 'ctx') lidG.visible = false; if (key === 'lid'){ lidG.visible = true; }
  const ringsVis = rings.map(r => r.visible);
  const bx = new T.Box3().setFromObject(key === 'gpu' || key === 'ctx' ? gpuG : target); const c = bx.getCenter(new T.Vector3()), sz = bx.getSize(new T.Vector3());
  const R = Math.max(.35, sz.length() / 2); const cm = new T.PerspectiveCamera(30, 264 / 198, .05, 200); const d = R / Math.sin(15 * Math.PI / 180) * .95;
  const yaw = key === 'mon' || key === 'prn' ? -.25 : -.5, pitch = key === 'ras' || key === 'mon' ? .25 : .55;
  cm.position.set(c.x + d * Math.cos(pitch) * Math.sin(yaw), c.y + d * Math.sin(pitch), c.z + d * Math.cos(pitch) * Math.cos(yaw)); cm.lookAt(c);
  if (key === 'ctx'){ const w = new T.Vector3(); ctxLamp.getWorldPosition(w); cm.position.copy(w).add(new T.Vector3(-1.6, 1.4, 2.6)); cm.lookAt(w); }
  legR.render(scene, cm); const url = legR.domElement.toDataURL('image/png');
  scene.children.forEach((o, k) => { if (vis[k] !== undefined) o.visible = vis[k]; }); lidG.visible = lidVis; rings.forEach((r, k) => r.visible = ringsVis[k]);
  if (temp) scene.remove(temp);
  return url;
}
function renderLegend(){
  const DX = devInfo();
  $('legList').innerHTML = LEG.map(([k, n, en, d, w]) => `<div class="lgw"><button type="button" class="lgc" data-k="${k}"><img class="im" alt="شكل ${n} في الماكينة" data-k="${k}"><span><h4>${n}<em>${en}</em></h4><p>${d}<span class="when">⏱ ${w}</span></p></span></button>${devDetails(k, DX)}</div>`).join('');
  fixBidi($('legList'));
  $('legList').querySelectorAll('[data-gk]').forEach(b => b.onclick = e => { e.stopPropagation(); showLegend(false); play(false); go(+b.dataset.gk); stage.scrollIntoView({behavior: reduce ? 'auto' : 'smooth', block: 'center'}); });
  requestAnimationFrame(() => document.querySelectorAll('#legList img').forEach(im => { try { im.src = legShot(im.dataset.k); } catch (e) { im.alt = ''; } }));
  document.querySelectorAll('#legList .lgc').forEach(b => b.onclick = () => { const k = b.dataset.k; if (!parts[k]) return; showLegend(false); stage.scrollIntoView({behavior: reduce ? 'auto' : 'smooth', block: 'center'});
    LIVE = [{pn: k, label: parts[k].label, what: LEG.find(x => x[0] === k)[1] + ': ' + parts[k].note, g: k === 'ctx' ? ctxLamp : parts[k].g}]; liveT0 = performance.now();
    liveEls.forEach((d, j) => { if (j){ d.style.display = 'none'; return; } d.style.display = ''; d.innerHTML = `<b>${esc(LIVE[0].label)}</b><span class="tw cur" data-full="${esc(LIVE[0].what)}"></span>`; }); });
}
// ------------------------------------------------------------------ device map details: per device, the code lines that act on it, its steps, and the named things inside it (attributes, buffers, uniforms...)
function vText(v){ for (const f of P.files){ if (v > f.off && v <= f.off + f.lines.length) return f.lines[v - f.off - 1]; } return ''; }
function vWhere(v){ for (const f of P.files){ if (v > f.off && v <= f.off + f.lines.length) return (P.files.length > 1 ? f.name + ' : ' : '') + (v - f.off); } return String(v); }
function shDecls(vs){ const out = [];
  for (const v of vs){ const t = vText(v).replace(/^\s*"|\\n"\s*$|"\s*$/g, '').replace(/^.*R"\(/, '').trim();
    let m = /layout\s*\(\s*location\s*=\s*(\d+)\s*\)\s*(in|out)\s+(\w+)\s+(\w+)/.exec(t);
    if (m){ out.push({kind: m[2], loc: +m[1], type: m[3], name: m[4], v, t}); continue; }
    m = /^(in|out|uniform)\s+(\w+)\s+(\w+)/.exec(t); if (m) out.push({kind: m[1], loc: null, type: m[2], name: m[3], v, t});
    if (/gl_Position\s*=/.test(t)) out.push({kind: 'gl', name: 'gl_Position', type: 'vec4', v, t}); }
  return out; }
// role of each device: what it takes, from whom; what it gives, to whom; what it links together
const ROLE = {
  cpu: {job: 'بينفّذ كود الـ C++ سطر سطر، وبيقرر إمتى يبعت أمر للكارت.', from: [['الرام', 'المتغيرات وقيمها'], ['الماوس / الكيبورد', 'الضغطات عن طريق <code>glfwPollEvents</code> والـ Callback']], to: [['الرام', 'يكتب قيم جديدة في المتغيرات'], ['كارت الشاشة', 'أي أمر <code>gl...</code> عن طريق الدرايفر'], ['الطابعة', 'أي <code>std::cout</code>']], link: 'بيربط برنامجك (الكود) بكل الأجهزة التانية. هو الوحيد اللي بيقرا الكود.'},
  ram: {job: 'بتشيل متغيرات البرنامج وهو شغال، زي <code>positions</code> و <code>window</code>.', from: [['الـ CPU', 'كل سطر فيه <code>=</code> بيكتب فيها']], to: [['الـ CPU', 'يقرا القيم'], ['الصندوق (Buffer)', 'الأرقام بتتنسخ منها للكارت عند <code>glBufferData</code>']], link: 'بتربط الـ CPU بالداتا. الكارت مايقدرش يقرا منها لوحده: لازم الـ CPU ينسخ.'},
  gpu: {job: 'الجهاز اللي بيرسم. جواه كل قطع الرسم.', from: [['الـ CPU (عن طريق الدرايفر)', 'أوامر <code>gl...</code> وأرقام وكود الـ Shaders']], to: [['الشاشة', 'الصورة النهائية بعد <code>glfwSwapBuffers</code>']], link: 'بيربط الأوامر اللي جاية من الـ CPU بالصورة اللي على الشاشة.'},
  ctx: {job: 'الوصلة المفتوحة بين برنامجك والكارت.', from: [['الـ CPU', '<code>glfwMakeContextCurrent</code>']], to: [['كل أوامر gl', 'من غيرها أي أمر gl مالوش مكان يروحله']], link: 'بتربط الشباك اللي GLFW عمله بالكارت.'},
  buf: {job: 'مساحة في ذاكرة الكارت فيها أرقام ورا بعض (بايتات). مش عارفة مين x ومين y.', from: [['الرام', 'الأرقام اتنسخت منها عند <code>glBufferData</code>']], to: [['ورقة التعليمات (VAO)', 'الـ attribute بيقرا منها حسب الـ stride والـ offset']], link: 'بتربط الداتا اللي كانت في الرام بالكارت. مكانها جوه الكارت.'},
  vao: {job: 'ورقة فيها خانات متنمّرة (attribute 0، 1، …). كل خانة بتقول: خد كام رقم لكل ركن، من أنهي صندوق، كل ركن بعد كام بايت (stride)، وابدأ منين (offset). <b>الـ attribute = خانة في الورقة دي</b>.', from: [['الـ CPU', 'بيكتب الخانات بـ <code>glEnableVertexAttribArray</code> و <code>glVertexAttribPointer</code>'], ['الصندوق (Buffer)', 'البايتات اللي هتتقطّع لأركان']], to: [['محطة الـ Vertex Shader', 'كل خانة بتدخل في المتغير اللي عنده نفس الرقم: <code>layout(location = N) in ...</code>']], link: 'بتربط الصندوق بالـ Vertex Shader. رقم الخانة في الورقة هو نفس رقم <code>location</code> في الـ Shader: خانة 0 = <code>layout(location = 0)</code>.'},
  vs: {job: 'برنامج صغير على الكارت بيشتغل مرة لكل ركن، وبيحدد مكانه على الشاشة (<code>gl_Position</code>).', from: [['ورقة التعليمات (VAO)', 'ركن واحد في كل مرة، في المتغيرات <code>in</code>'], ['شريط الـ Program', 'قيم الـ uniforms لو فيه']], to: [['الـ Rasterizer', '<code>gl_Position</code> لكل ركن، وأي متغير <code>out</code>']], link: 'بيربط أرقام الصندوق بأماكن على الشاشة.'},
  ras: {job: 'جزء ثابت في الكارت (مش كود منك). بيوصّل الأركان ويلاقي البكسلات اللي جوه الشكل.', from: [['محطة الـ Vertex Shader', 'مكان كل ركن']], to: [['محطة الـ Fragment Shader', 'كل بكسل جوه الشكل، ومعاه قيم <code>out</code> متخلطة بين الأركان']], link: 'بيربط الأركان بالبكسلات.'},
  fs: {job: 'برنامج صغير على الكارت بيشتغل مرة لكل بكسل، وبيطلّع لونه.', from: [['الـ Rasterizer', 'البكسل، وقيم <code>in</code>'], ['شريط الـ Program', 'قيم الـ uniforms زي <code>u_Color</code>']], to: [['اللوحة اللي ورا (Back)', 'لون البكسل في <code>out vec4 color</code> (location = 0 هنا = لوحة الرسم، مش attribute)']], link: 'بيربط البكسلات بالألوان.'},
  prog: {job: 'الـ Vertex والـ Fragment Shader مربوطين مع بعض في حتة واحدة.', from: [['الـ CPU', '<code>glAttachShader</code> و <code>glLinkProgram</code> و <code>glUseProgram</code> وقيم <code>glUniform...</code>']], to: [['المحطتين', 'الكود اللي هيشتغل، وقيم الـ uniforms']], link: 'بيربط الـ Vertex بالـ Fragment، وبيربط الـ CPU بالمحطتين عن طريق الـ uniforms.'},
  car: {job: 'لوحتين رسم: Back بيترسم فيها في الخفا، و Front هي اللي على الشاشة.', from: [['محطة الـ Fragment Shader', 'ألوان البكسلات'], ['الـ CPU', '<code>glClear</code> بيمسح، و <code>glfwSwapBuffers</code> بيبدّل']], to: [['الشاشة', 'اللوحة اللي قدام (Front)']], link: 'بتربط الرسم اللي بيحصل في الكارت بالشاشة اللي انت شايفها.'},
  mon: {job: 'الشباك اللي المستخدم شايفه.', from: [['القرص (Front)', 'الصورة بعد كل Swap']], to: [['المستخدم', 'الصورة'], ['الـ CPU', 'الضغطات اللي جوه الشباك (عن طريق GLFW)']], link: 'بيربط البرنامج بالمستخدم.'},
  prn: {job: 'الـ Terminal: أي نص البرنامج بيطبعه.', from: [['الـ CPU', '<code>std::cout</code> / <code>print</code>']], to: [['المستخدم', 'النص']], link: 'بتربط البرنامج بالمستخدم من غير شباك.'},
  mouse: {job: 'الضغطات الحقيقية اللي اتبعتت وقت التشغيل.', from: [['المستخدم', 'الإيد']], to: [['الـ CPU', 'GLFW بينده الـ Callback جوه <code>glfwPollEvents</code>']], link: 'بيربط المستخدم بالـ CPU.'},
  lid: {job: 'غطا الكارت في الرسم بس، عشان تشوف اللي جواه.', from: [], to: [], link: 'مالوش دور في البرنامج: ده جزء من شكل الماكينة.'},
  token: {job: 'داتا بتتنقل من جهاز لجهاز.', from: [['أي جهاز', 'اللي بيبعت']], to: [['أي جهاز', 'اللي بيستلم']], link: 'هي نفسها الوصلة: بتظهر في كل خطوة فيها نقل.'},
  ring: {job: 'علامة بتلف حوالين الجهاز اللي اتغير في الخطوة دي.', from: [], to: [], link: 'مالوش دور في البرنامج: ده للشرح بس.'},
};
function roleHtml(k){ const r = ROLE[k]; if (!r) return '';
  const li = a => a.length ? `<ul>${a.map(([w, t]) => `<li><b>${w}</b>: ${t}</li>`).join('')}</ul>` : '<p class="lgnone">-</p>';
  return `<p>${r.job}</p><h5>⬅️ بياخد من</h5>${li(r.from)}<h5>➡️ بيدي لـ</h5>${li(r.to)}<h5>🔗 بيربط بين</h5><p>${r.link}</p>`; }
let DXc = null;
function devInfo(){
  if (DXc && DXc.id === P.id) return DXc;
  const KEYS = LEG.map(x => x[0]), steps = {}, M = {vaos: {}, bufs: {}, sh: {}, pr: {}, uni: {}}, vars = new Map(), evs = [];
  KEYS.forEach(k => steps[k] = []);
  let g0 = null;
  ST.forEach((s, k) => {
    const ks = new Set((s.lv || []).map(l => l[0]));
    if (s.u === 'CPU') ks.add('cpu'); if (s.u !== 'CPU') ks.add('gpu'); if (s.ev) ks.add('mouse');
    if (s.lv && s.lv.length) ks.add('ring'); if (s.an === 'upload' || s.an === 'src' || s.ev) ks.add('token');
    ks.forEach(key => { if (steps[key]) steps[key].push(k); });
    const G = s.gp; if (G){ g0 = G; for (const t of ['vaos', 'bufs', 'sh', 'pr']) for (const [id, o] of Object.entries(G[t] || {})) M[t][id] = o; Object.assign(M.uni, G.uni || {}); }
    for (const fr of (s.st || [])) for (const [n, val] of (fr.v || [])) vars.set(fr.fn + '::' + n, {fn: fr.fn, n, val});
    if (s.ev) evs.push([k, s.ev]); });
  const vsD = shDecls(P.shl.vs || []), fsD = shDecls(P.shl.fs || []);
  DXc = {id: P.id, steps, M, vars, evs, vsD, fsD, g: g0 || {}};
  return DXc; }
function devDetails(k, DX){
  const S = DX.steps[k] || [], M = DX.M, sec = (icon, title, n, body) => body ? `<details class="lgd"><summary>${icon} ${title}${n != null ? ` <span class="n">${n}</span>` : ''}</summary><div class="lgb">${body}</div></details>` : '';
  const uCol = u => u === 'CPU' ? 'var(--arancio)' : u === 'GPU' ? 'var(--teal)' : 'var(--blueline)';
  // 1) code lines that act on this device (unique, in first-run order)
  const seen = new Map(); S.forEach(j => { const s = ST[j]; if (!seen.has(s.v)) seen.set(s.v, {j, s, n: 0}); seen.get(s.v).n++; });
  let codes = [...seen.values()].map(({j, s, n}) => `<li><button type="button" data-gk="${j}" title="روح لأول خطوة نفّذت السطر ده"><span class="ul" style="background:${uCol(s.u)}">${s.u}</span><span class="ln">سطر ${esc(fileLine(s))}</span><code>${esc(stepText(s))}</code>${n > 1 ? `<span class="x">اتنفذ ${n} مرة</span>` : ''}</button></li>`).join('');
  let codeTitle = 'الأكواد اللي بتشغّله';
  // shader stations: the code that lives INSIDE them
  let inside = '';
  if ((k === 'vs' || k === 'fs') && (P.shl[k] || []).length){
    inside = `<ol class="lgsrc">${P.shl[k].map(v => `<li><span class="ln">سطر ${esc(vWhere(v))}</span><code>${esc(vText(v))}</code></li>`).join('')}</ol>`; }
  // 2) steps
  const stepsHtml = S.map(j => { const s = ST[j], L = (s.lv || []).filter(l => l[0] === k).map(l => l[2]).join(' · ');
    return `<li><button type="button" data-gk="${j}"><span class="sn">خطوة ${j + 1}</span><span class="ul" style="background:${uCol(s.u)}">${s.u}</span><b>${esc(s.ti)}</b><span class="ln">سطر ${esc(fileLine(s))}</span>${L ? `<span class="wt">${esc(L)}</span>` : ''}</button></li>`; }).join('');
  // 3) named elements inside
  const row = (a, b) => `<li><b>${a}</b><span>${b}</span></li>`, C = t => `<code>${esc(String(t))}</code>`;
  let el = '';
  const attrName = loc => { const d = DX.vsD.find(x => x.kind === 'in' && x.loc === loc); return d ? ` · بتدخل في المتغير ${C(d.type + ' ' + d.name)} جوه الـ Vertex Shader (${C(vWhere(d.v).replace(' : ', ' سطر '))})` : ''; };
  if (k === 'vao') el = Object.entries(M.vaos).map(([id, o]) => `<li class="grp"><b>VAO ${id}</b>${o.ebo ? ` <span>مربوط بيه EBO = Buffer ${o.ebo}</span>` : ''}<ul>${Object.entries(o.at || {}).map(([loc, a]) =>
      row(`attribute ${loc} (خانة ${loc})`, `${a.on ? 'شغالة' : 'مقفولة'} · بتاخد ${a.size} رقم لكل ركن من ${C('Buffer ' + a.buf)} · ${C('stride = ' + a.stride)} بايت · ${C('offset = ' + a.off)} بايت (الركن 0 من بايت ${a.off}، والركن 1 من بايت ${+a.off + +a.stride}، وهكذا)${attrName(+loc)}`)).join('') || row('مفيش خانات', 'لسه ماتكتبش فيها')}</ul></li>`).join('');
  else if (k === 'buf') el = Object.entries(M.bufs).map(([id, b]) => row(`Buffer ${id} (${b.t || '?'})`, `${b.bytes || 0} بايت${b.vals && b.vals.length ? ` · الأرقام: ${C(b.vals.join(', '))}` : ''}`)).join('');
  else if (k === 'vs' || k === 'fs'){ const D = k === 'vs' ? DX.vsD : DX.fsD, kn = {in: 'مدخل (in)', out: 'مخرج (out)', uniform: 'uniform', gl: 'لازم يتكتب'};
    el = D.map(d => row(`${C(d.name)} · ${kn[d.kind]}${d.loc != null ? ` · location = ${d.loc}` : ''}`, `${C(d.type)} · سطر ${esc(vWhere(d.v))}${d.kind === 'in' && k === 'vs' && d.loc != null ? ` · بييجي من attribute ${d.loc}` : ''}${d.kind === 'out' && k === 'fs' ? ' · ده لون البكسل' : ''}`)).join('');
    el += Object.entries(M.sh).filter(([, o]) => o.ty === (k === 'vs' ? 'Vertex' : 'Fragment')).map(([id, o]) => row(`Shader ${id}`, `${o.ty}${o.st === 'del' ? ' · اتمسح بعد الربط (النسخة اللي في الـ Program لسه شغالة)' : o.st ? ' · ' + esc(o.st) : ''}`)).join(''); }
  else if (k === 'prog'){ el = Object.entries(M.pr).map(([id, o]) => row(`Program ${id}`, `فيه Shaders ${(o.att || []).join(' و ')}${o.linked ? ' · مربوط (Linked)' : ''}${o.use ? ' · شغال (glUseProgram)' : ''}`)).join('') + Object.entries(M.uni).map(([n, v]) => row(`uniform ${C(n)}`, `آخر قيمة اتبعتت: ${C(v)}`)).join(''); }
  else if (k === 'ram'){ const byFn = {}; for (const o of DX.vars.values()) (byFn[o.fn] = byFn[o.fn] || []).push(o);
    el = Object.entries(byFn).map(([fn, a]) => `<li class="grp"><b>${esc(fn)}()</b><ul>${a.map(o => row(C(o.n), C(o.val))).join('')}</ul></li>`).join(''); }
  else if (k === 'cpu') el = (P.regions || []).map(r => row(C(r[2]), `دالة: السطور ${r[0]}–${r[1]}`)).join('');
  else if (k === 'gpu'){ const g = DX.g; el = [row('VAOs', Object.keys(M.vaos).length), row('Buffers', Object.keys(M.bufs).length), row('Shaders', Object.keys(M.sh).length), row('Programs', Object.keys(M.pr).length), row('uniforms', Object.keys(M.uni).length)].join(''); }
  else if (k === 'ctx'){ const g = DX.g; el = [row('Context', g.ctx ? 'اتفتح' : 'لأ'), row('GLAD', g.glad ? 'جاب عناوين دوال OpenGL' : 'لأ'), row('VSync', g.vsync != null ? C(g.vsync) : '-')].join(''); }
  else if (k === 'car'){ const g = DX.g; el = [row('Back', 'اللوحة اللي بيترسم فيها في الخفا'), row('Front', 'اللوحة اللي على الشاشة'), row('لون المسح', C('(' + (g.clear || []).join(', ') + ')'))].join(''); }
  else if (k === 'mon') el = P.W ? [row('الشباك', `${P.W} × ${P.H} بكسل`), row('الصور', `${(P.frames || []).length} صورة اتقرت من الكارت`)].join('') : '';
  else if (k === 'prn') el = (P.term || []).length ? `<pre class="lgterm" dir="ltr">${esc(P.term.join('\n').replace(/\u0001/g, ''))}</pre>` : '';
  else if (k === 'mouse') el = DX.evs.map(([j, e]) => row(`خطوة ${j + 1}`, e.btn === 'key' ? `كيبورد: ${C(e.key)}` : `ماوس ${{left: 'شمال', right: 'يمين'}[e.btn] || esc(e.btn || '')} ${{press: 'اتداس', release: 'اتساب'}[e.act] || esc(e.act || '')}${e.x != null ? ` عند البكسل (${e.x}, ${e.y})` : ''}`)).join('');
  if (el) el = `<ul class="lgel">${el}</ul>`;
  const elTitle = {vao: 'العناصر جواه: الـ attributes (الخانات)', buf: 'العناصر جواه: الصناديق', vs: 'العناصر جواه: المدخلات والمخرجات', fs: 'العناصر جواه: المدخلات والمخرجات', prog: 'العناصر جواه: الـ Programs والـ uniforms', ram: 'العناصر جواه: المتغيرات', cpu: 'العناصر: الدوال', gpu: 'اللي جواه', ctx: 'الحالة', car: 'اللوحتين', mon: 'الشباك', prn: 'اللي اتطبع', mouse: 'الضغطات'}[k] || 'العناصر';
  const out = sec('🔗', 'دوره: بياخد من مين ويدي لمين', null, roleHtml(k)) + sec('📜', 'الكود المكتوب جواه', (P.shl[k] || []).length || null, inside) + sec('💻', codeTitle, seen.size || null, codes ? `<ul class="lgcode">${codes}</ul>` : '') + sec('🪜', 'الخطوات اللي بيشتغل فيها', S.length || null, stepsHtml ? `<ul class="lgst">${stepsHtml}</ul>` : '') + sec('🏷️', elTitle, null, el);
  return out ? `<div class="lgx">${out}</div>` : `<div class="lgx"><p class="lgnone">مالوش أوامر في البرنامج ده.</p></div>`; }
function showLegend(on){ $('legend').hidden = !on; if (on && $('cmdSheet') && !$('cmdSheet').hidden) showCmd(false); $('legBtn').setAttribute('aria-expanded', on); $('legBtn').textContent = on ? '✕ خبّي الخريطة' : '🧩 خريطة الأجهزة'; if (on){ showGloss(false); if (!$('story2').hidden) showStory(false); if ($('stepsSheet') && !$('stepsSheet').hidden) showSteps(false); if ($('bytesSheet') && !$('bytesSheet').hidden) showBytes(false); renderLegend(); } }
$('legBtn').onclick = () => showLegend($('legend').hidden); $('legX').onclick = () => showLegend(false);
document.addEventListener('keydown', e => { if (e.key === 'Escape' && !$('legend').hidden) showLegend(false); });

// ------------------------------------------------------------------ the bench story: what the program does, chapter by chapter (hidden until asked)
const STATIC_LOOP = 'الصورة هنا ثابتة، بس برضه لازم لوب. الشاشة مش بتفتكر الصورة لوحدها: كل فريم لازم يترسم من جديد (امسح ← ارسم ← بدّل اللوحتين). وكمان كل لفة <code>glfwPollEvents</code> بتسأل نظام التشغيل: حد داس على زرار القفل؟ حد حرّك الشباك؟ من غير اللوب البرنامج هيوصل لـ <code>return 0</code> في جزء من الثانية، والشباك يفتح ويقفل قبل ما تلحق تشوفه، ولو وقف من غير ما يسأل على الأحداث نظام التشغيل هيقول «البرنامج مش بيرد».';
const PSTORY = {
  d1_u1: {goal: "<b>السؤال:</b> إزاي نلوّن رسمة من الـ C++ من غير ما نلمس الـ Shader؟<br><b>الفكرة:</b> المستطيل = مثلثين. بدل ما نكتب 6 أركان، بنكتب 4 أركان بس، وجدول أرقام صغير (EBO) بيقول للكارت يوصّلهم إزاي: 0 و 1 و 2، ثم 2 و 3 و 0. واللون مش مكتوب جوه الـ Shader: بييجي من برا في متغير اسمه <code>u_Color</code> (uniform).<br><b>الأركان:</b> 4 أركان في <code>positions</code>، كل ركن رقمين (x, y).<br><b>الجدول (EBO):</b> 6 أرقام بتقول أنهي ركن مع أنهي.<br><b>اللون:</b> <code>glUniform4f(location, 0.2f, 0.3f, 0.8f, 1.0f)</code>: أحمر 0.2 وأخضر 0.3 وأزرق 0.8.<br><b>النتيجة الحقيقية:</b> مستطيل أزرق ثابت في نص الشباك.<br><b>المطلوب تفهمه:</b> الـ uniform قيمة واحدة لكل الرسمة جاية من الـ CPU. فلو عاوز تغيّر اللون بتغيّر سطر C++ واحد، والـ Shader زي ما هو.", loop: STATIC_LOOP + ' وكل لفة الـ CPU بيبعت نفس اللون تاني بـ <code>glUniform4f</code> قبل الرسم.'},
  d1_u2: {goal: "<b>السؤال:</b> نقدر نغيّر لون الرسمة وهي شغالة؟<br><b>الفكرة:</b> نفس المستطيل، بس اللون اللي بنبعته بـ <code>glUniform4f</code> بيتغير كل لفة.<br><b>r:</b> متغير في الرام بيزيد 0.05 كل لفة.<br><b>العكس:</b> لما <code>r</code> يعدّي 1 بيبدأ ينقص، ولما ينزل تحت 0 يبدأ يزيد.<br><b>الإرسال:</b> كل لفة: <code>glUniform4f(location, r, 0.3f, 0.8f, 1.0f)</code> قبل الرسم.<br><b>النتيجة الحقيقية:</b> اللون بيتحرك بين الأزرق والبنفسجي قدامك.<br><b>المطلوب تفهمه:</b> اللوب هي اللي بتعمل الحركة: كل لفة قيمة جديدة تتبعت للكارت قبل الرسم، والأركان نفسها ماتغيرتش.", loop: 'هنا اللوب ليها شغلانة واضحة: كل لفة الـ CPU بيبعت قيمة <code>r</code> الجديدة للكارت بـ <code>glUniform4f</code>، فكل فريم لونه مختلف. شكل المستطيل (الـ Buffers) اتبعت للكارت مرة واحدة قبل اللوب، واللي بيتبعت كل لفة هو رقم اللون بس. قارن بين صور اللفات في «الصورة الحقيقية»: الأحمر بيزيد.'},
  d1_cam: {goal: "<b>السؤال:</b> إزاي نشوف رسمة 3D من كاميرا نقدر نحركها؟<br><b>الفكرة:</b> هرم ملوّن 3D، وكل لفة بنحسب مصفوفة كاميرا ونبعتها للـ Vertex Shader، فالكارت يحوّل كل ركن 3D لمكان على الشاشة.<br><b>3 ملفات:</b> <code>main.cpp</code> بيستخدم كلاس <code>Shader</code> (في shaderClass.cpp) وكلاس <code>Camera</code> (في Camera.cpp). التنفيذ بينط بين الملفات، وده باين في «مسار التنفيذ».<br><b>Camera::Inputs:</b> كل لفة بتسأل: W A S D أو الماوس متداس؟ وتحرك الكاميرا.<br><b>Camera::Matrix:</b> بتحسب المصفوفة من مكان الكاميرا وتبعتها في <code>camMatrix</code>.<br><b>النتيجة الحقيقية:</b> هرم ملوّن 3D. محدش داس أثناء التسجيل، فالصورة فضلت ثابتة.<br><b>المطلوب تفهمه:</b> المصفوفة uniform بتتبعت كل لفة، وهي اللي بتحوّل 3D لـ 2D على الشاشة.", loop: 'كل لفة <code>Camera::Inputs</code> بتسأل: الكيبورد (W A S D) أو الماوس متداس؟ وتحرك الكاميرا. وبعدين <code>Camera::Matrix</code> بتحسب مصفوفة جديدة من مكان الكاميرا وتبعتها للـ Shader. عشان كده اللوب ضرورية: لو الكاميرا اتحركت، الهرم لازم يترسم من جديد من المكان الجديد. في التشغيل ده محدش داس، فالصورة فضلت زي ما هي.'},
  d2_va1: {goal: "<b>السؤال:</b> الكارت بيعرف منين إن كل ركن رقمين؟<br><b>الفكرة:</b> الأرقام في الصندوق (Buffer) مجرد بايتات. <code>glVertexAttribPointer</code> هو اللي بيقول: «الخانة 0 = رقمين float، وكل ركن بعد 8 بايت من اللي قبله».<br><b>الأركان:</b> 3 أركان × رقمين = 6 أرقام = 24 بايت.<br><b>Layout:</b> <code>glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 8, 0)</code>.<br><b>النتيجة الحقيقية:</b> مثلث برتقاني.<br><b>المطلوب تفهمه:</b> الـ Layout هو وصف البايتات. من غيره الكارت مايعرفش يقرا الصندوق.", loop: STATIC_LOOP},
  d2_va2: {goal: "<b>السؤال:</b> إزاي نحط لون لكل ركن؟<br><b>الفكرة:</b> كل ركن بقى 5 أرقام: x و y ثم r و g و b (20 بايت). فيه خانتين في الـ Layout.<br><b>خانة 0:</b> المكان: رقمين من بايت 0.<br><b>خانة 1:</b> اللون: 3 أرقام من بايت 8.<br><b>الـ Rasterizer:</b> الكارت بيخلط الألوان بين الأركان لوحده.<br><b>النتيجة الحقيقية:</b> مثلث ألوانه متدرجة.<br><b>المطلوب تفهمه:</b> نفس الصندوق ممكن يشيل أكتر من معلومة لكل ركن، والـ offset بيقول كل واحدة بتبدأ فين.", loop: STATIC_LOOP},
  d3_s1: {goal: "<b>السؤال:</b> ينفع نكتب الـ Shader في ملف لوحده؟<br><b>الفكرة:</b> الـ Shaders في <code>Basic.shader</code>، والبرنامج بيقراه سطر سطر بـ <code>getline</code> ويقسمه نصين عند سطر <code>#shader</code>.<br><b>ParseShader:</b> لوب <code>while (getline(...))</code> لفّت 19 مرة، مرة لكل سطر في الملف.<br><b>الباقي:</b> زي أي برنامج: ترجمة وربط ورسم.<br><b>النتيجة الحقيقية:</b> مثلث أزرق.<br><b>المطلوب تفهمه:</b> الـ Shader مجرد نص، فممكن ييجي من ملف وتعدّله من غير ما تعيد ترجمة الـ C++.", loop: STATIC_LOOP + ' وخلي بالك إن فيه لوب تاني قبلها خالص: <code>while (getline(stream, line))</code> جوه <code>ParseShader</code>. دي بتلف مرة لكل سطر في الملف (19 سطر) وتقف لما الملف يخلص، لأن <code>getline</code> بترجع false.'},
  d3_l1: {goal: "<b>السؤال:</b> إزاي نرسم أول أمر CAD: خط بين نقطتين؟<br><b>الفكرة:</b> نفس الصندوق (نقطتين) بيترسم مرتين بنوعين.<br><b>GL_LINES:</b> خط أبيض.<br><b>GL_POINTS:</b> النقطتين كمربعات برتقاني.<br><b>اللون:</b> uniform بيتغير بين الرسمتين.<br><b>النتيجة الحقيقية:</b> خط أبيض وطرفيه برتقاني.<br><b>المطلوب تفهمه:</b> الأركان نفسها، ونوع الرسم هو اللي بيحدد الشكل.", loop: 'كل لفة فيها رسمتين: الـ CPU يبعت لون أبيض ويقول «ارسم خط»، وبعدين يبعت برتقاني ويقول «ارسم نقط». ده أساس أي برنامج CAD: نفس الداتا بتتعرض بأكتر من شكل. والصورة لازم تتعاد كل فريم زي أي شباك.'},
  d3_l2: {goal: "<b>السؤال:</b> إزاي الماوس يرسم خطوط؟<br><b>الفكرة:</b> كل ضغطة = نقطة جديدة في vector، وكل نقطتين = خط.<br><b>MouseButtonCallback:</b> GLFW بينده الدالة دي لوحده لما تدوس.<br><b>الصندوق:</b> بيتبعت من جديد للكارت بعد كل ضغطة.<br><b>النتيجة الحقيقية:</b> 5 ضغطات حقيقية: خطين ونقطة لوحدها مستنية شريكتها.<br><b>المطلوب تفهمه:</b> الحدث بيوصل جوه glfwPollEvents، والرسم الجديد بيبان في اللفة اللي بعدها.", loop: 'هنا اللوب هي اللي بتخلي البرنامج «يسمع». كل لفة <code>glfwPollEvents</code> بتسأل نظام التشغيل: حد داس؟ لو أيوه، GLFW بينده <code>MouseButtonCallback</code> لوحده، فالنقطة بتتحول من بكسل لـ ‎-1..+1 وتتضاف للـ vector وتتبعت للكارت تاني، وفي اللفة اللي بعدها تترسم. من غير لوب مفيش حد يسأل على الماوس أصلاً. وكمان GLFW بينده الدالة تاني لما الزرار يطلع (Release)، بس السطر الأول بيرجّعها على طول، فالمرة دي مش ظاهرة في الخطوات.'},
  d4_e1: {goal: "<b>السؤال:</b> المستطيل محتاج كام ركن من غير جدول؟<br><b>الفكرة:</b> كل مثلث لازم 3 أركان كاملين، فالمستطيل = 6 أركان، منهم ركنين متكررين.<br><b>glDrawArrays:</b> بيمشي على الأركان بالترتيب.<br><b>النتيجة الحقيقية:</b> مستطيل أزرق.<br><b>المطلوب تفهمه:</b> التكرار ده هو اللي الـ EBO بيوفّره في البرنامج اللي بعده.", loop: STATIC_LOOP},
  d4_e2: {goal: "<b>السؤال:</b> نوفّر الأركان المتكررة إزاي؟<br><b>الفكرة:</b> 4 أركان بس + جدول (EBO) فيه 6 أرقام: 0 و 1 و 2، ثم 2 و 3 و 0.<br><b>glDrawElements:</b> بيمشي على الجدول بدل الأركان.<br><b>النتيجة الحقيقية:</b> نفس المستطيل بالظبط.<br><b>المطلوب تفهمه:</b> وفّرنا ركنين هنا، وفي الأشكال الكبيرة التوفير ضخم.", loop: STATIC_LOOP},
  d4_v1: {goal: "<b>السؤال:</b> إزاي نرسم أكتر من حاجة في نفس الشباك؟<br><b>الفكرة:</b> كل رسمة ليها VAO و Buffer خاصين بيها، وقبل كل رسمة بنربط الـ VAO بتاعها.<br><b>البيت:</b> 6 خطوط بيضا.<br><b>الشمس:</b> صليب أصفر.<br><b>النتيجة الحقيقية:</b> بيت وشمس.<br><b>المطلوب تفهمه:</b> VAO لكل حاجة = سطر ربط واحد قبل رسمها.", loop: 'كل لفة: امسح ← اربط VAO البيت + لون أبيض + ارسم ← اربط VAO الشمس + لون أصفر + ارسم ← بدّل. الـ VAO هو اللي مخلي التبديل بين الرسمتين سطر واحد (<code>glBindVertexArray</code>) بدل ما نعيد وصف الأركان كل مرة.'},
  d4_v2: {goal: "<b>السؤال:</b> إزاي نعمل Polyline بالماوس؟<br><b>الفكرة:</b> ضغطة شمال = نقطة في الخط الشغال، ضغطة يمين = اقفل الخط وابدأ واحد جديد. كل خط محفوظ كـ (أول نقطة، عدد النقط).<br><b>اللوب جوه اللفة:</b> <code>for (const Polyline& line : polylines)</code> بترسم كل خط بـ GL_LINE_STRIP.<br><b>النتيجة الحقيقية:</b> 10 ضغطات حقيقية: 3 خطوط.<br><b>المطلوب تفهمه:</b> نفس الصندوق فيه كل النقط، والجدول الصغير بيقول كل خط بيبدأ فين وطوله كام.", loop: 'كل لفة: ارسم كل خط لوحده بـ <code>GL_LINE_STRIP</code> (فعدد الرسمات بيزيد كل ما الخطوط تزيد)، وبعدين ارسم كل النقط، وبعدين اسأل على الماوس. الضغطة اللي بتحصل في لفة بتبان في اللفة اللي بعدها، لأن الرسم حصل قبل السؤال.'},
  d5_p1: {goal: "<b>السؤال:</b> إزاي swap تبدّل متغيرين بتوع main؟<br><b>الفكرة:</b> بتاخد عنوانهم (<code>&x</code> و <code>&y</code>) فتكتب جوه الصناديق الأصلية.<br><b>temp:</b> شايلة الـ 10 لحد ما تتحط في y.<br><b>النتيجة الحقيقية:</b> <code>x = 20</code> و <code>y = 10</code>.<br><b>المطلوب تفهمه:</b> اتفرج على الرام: a و b فيهم نفس عناوين x و y.", loop: 'البرنامج ده مافيهوش لوب <code>while</code> خالص: بيمشي من أول <code>main</code> لآخرها مرة واحدة ويخلص. مفيش شباك يفضل مفتوح ويستنى، فمفيش حاجة محتاجة تتكرر.'},
  d5_p2: {goal: "<b>السؤال:</b> أنهي طريقة swap بتشتغل؟<br><b>الفكرة:</b> نفس التبديل بالقيمة وبالـ Pointer وبالـ Reference، وكل دالة بتطبع العناوين اللي استلمتها.<br><b>SwapValue:</b> عناوين مختلفة (نسخ).<br><b>SwapPointer و SwapReference:</b> نفس عناوين x و y.<br><b>النتيجة الحقيقية:</b> بالقيمة مافيش تبديل، والاتنين التانيين بدّلوا.<br><b>المطلوب تفهمه:</b> لو العنوان اللي استلمته الدالة مختلف، يبقى بتشتغل على نسخة.", loop: 'البرنامج ده مافيهوش لوب <code>while</code> خالص: بيمشي من أول <code>main</code> لآخرها مرة واحدة ويخلص. مفيش شباك يفضل مفتوح ويستنى، فمفيش حاجة محتاجة تتكرر.'},
  d5_n1: {goal: "<b>السؤال:</b> إيه أساسيات NumPy؟<br><b>الفكرة:</b> مصفوفة بتحسب على كل العناصر مرة واحدة من غير لوب.<br><b>الشكل والنوع:</b> shape و dtype والحجم بالبايت.<br><b>الوصول:</b> عنصر وصف وعمود.<br><b>تحذير:</b> <code>c = a</code> مش نسخة: c اتغيرت فـ a اتغيرت. و <code>copy()</code> هي النسخة.<br><b>النتيجة الحقيقية:</b> كل سطر طبع نتيجته في الـ Terminal.<br><b>المطلوب تفهمه:</b> الـ = في NumPy زي Reference، مش نسخة.", loop: 'البرنامج ده مافيهوش لوب خالص: Python بتمشي على السطور من فوق لتحت مرة واحدة وتخلص. مفيش شباك يفضل مفتوح ويستنى، فمفيش حاجة محتاجة تتكرر.'},
  d5_n2: {goal: "<b>السؤال:</b> dot و cross بـ NumPy؟<br><b>الفكرة:</b> نفس مثال Khan في سطر لكل عملية.<br><b>np.dot:</b> [1,‎-7,1] · [5,2,4] = ‎-5.<br><b>np.cross:</b> [‎-30, 1, 37]، والتأكد إنه عمودي.<br><b>زيادة:</b> الطول والزاوية، و x × y = z، وكذا متجه مرة واحدة.<br><b>النتيجة الحقيقية:</b> نفس أرقام Khan.<br><b>المطلوب تفهمه:</b> NumPy بتعمل نفس القانون اللي كتبناه بإيدنا.", loop: 'البرنامج ده مافيهوش لوب خالص: Python بتمشي على السطور من فوق لتحت مرة واحدة وتخلص. مفيش شباك يفضل مفتوح ويستنى، فمفيش حاجة محتاجة تتكرر.'},
  d5_c1: {goal: "<b>السؤال:</b> push_back و pop_back بيشتغلوا إزاي؟<br><b>الفكرة:</b> كود الفيديو: أسماء من الكيبورد لحد Q.<br><b>اللوب:</b> <code>while (name != \"Q\")</code> لفّت 4 مرات.<br><b>pop_back:</b> شالت Q اللي اتضافت.<br><b>النتيجة الحقيقية:</b> كتبنا Braden و Jeff و Katie و Q، وطبع 3 أسماء.<br><b>المطلوب تفهمه:</b> الـ vector بيضيف ويشيل من الآخر بس بالدالتين دول.", loop: 'هنا اللوب مش عشان شباك: عشان نفضل نقرا أسماء لحد ما المستخدم يكتب Q (الـ Sentinel). كل لفة: <code>cin</code> يقرا كلمة، و <code>push_back</code> يضيفها في الآخر، وبعدين الشرط يتشاف من جديد. ولاحظ في الرام إن capacity بقت 1 ثم 2 ثم 4: لما الـ vector يتملي بيحجز مكان أكبر وينقل الأسماء. واللوب التانية <code>for</code> بتلف على الأسماء عشان تطبعها.'},
  d5_r1: {goal: "<b>السؤال:</b> إزاي نكتب الـ Shader كنص ونفحص الترجمة؟<br><b>الفكرة:</b> كود The Cherno: الـ Shaders في <code>std::string</code>، و <code>CompileShader</code> بتفحص: لو فيه غلطة بتطبع رسالتها وتمسح الـ Shader.<br><b>الفحص:</b> هنا مفيش غلطة، فالـ if مادخلتش.<br><b>النتيجة الحقيقية:</b> مثلث أحمر.<br><b>المطلوب تفهمه:</b> الكارت مش هيقولك الغلطة لوحده: لازم تسأله بـ glGetShaderiv.", loop: STATIC_LOOP},
  d5_r2: {goal: "<b>السؤال:</b> نقدر نغيّر الشكل من الـ Shader بس؟<br><b>الفكرة:</b> نفس البرنامج، والتعديل جوه نص الـ Shader بس.<br><b>Vertex:</b> بيضرب كل ركن في 1.5 فالمثلث يكبر، ويبعت المكان للـ Fragment.<br><b>Fragment:</b> بيلوّن كل بكسل حسب مكانه.<br><b>النتيجة الحقيقية:</b> مثلث أكبر بألوان متدرجة، وأرقام الأركان في الكارت زي ما هي.<br><b>المطلوب تفهمه:</b> الـ Shader بيعدّل وقت الرسم، والبيانات نفسها ماتغيرتش.", loop: STATIC_LOOP},
  d6_p1: {goal: "<b>السؤال:</b> الـ Compiler بيشتغل إزاي من جوه؟<br><b>الفكرة:</b> الكود <code>var x = 1 + 2 * 3; x * 2;</code> بيعدّي على 4 مراحل، وكل مرحلة بتطبع نتيجتها.<br><b>Scan:</b> الحروف ← Tokens.<br><b>Parser:</b> Tokens ← شجرة (الضرب تحت الجمع).<br><b>Compile:</b> الشجرة ← أوامر Bytecode.<br><b>Run:</b> الأوامر بتتنفذ على Stack.<br><b>النتيجة الحقيقية:</b> <code>x = 7</code>، والنتيجة 14.<br><b>المطلوب تفهمه:</b> الأولوية جاية من ترتيب الدوال: الجمع بينده الضرب.", loop: 'البرنامج ده مافيهوش لوب <code>while</code> للشباك: بيمشي من أول <code>main</code> لآخرها مرة واحدة ويخلص.' + ' بس جواه لوبات كتير: <code>while</code> بيلف على كل حرف في الـ Scanner، و <code>while (Match(...))</code> في الـ Parser، و <code>for</code> بيلف على الأوامر في الـ VM. ودالتين بيندهوا نفسهم (<code>PrintTree</code> و <code>Compile</code>)، فالـ Stack بتاع الـ CPU بيطلع وينزل.'},
  d6_p2: {goal: "<b>السؤال:</b> السنة دي كبيسة؟ (تمرين Leap)<br><b>الفكرة:</b> كبيسة لو بتقبل على 4، إلا لو بتقبل على 100، إلا لو بتقبل على 400.<br><b>check:</b> بتقارن بالإجابة الصح وتطبع PASS أو FAIL، زي exercism.<br><b>النتيجة الحقيقية:</b> 6 سنين والـ 6 PASS.<br><b>المطلوب تفهمه:</b> الاختبار بيمسك الغلطة في ثانية.", loop: 'البرنامج ده مافيهوش لوب <code>while</code> للشباك: بيمشي من أول <code>main</code> لآخرها مرة واحدة ويخلص.'},
  d6_p3: {goal: "<b>السؤال:</b> الرقم يتحوّل لصوت إزاي؟ (تمرين Raindrops)<br><b>الفكرة:</b> 3 = Pling و 5 = Plang و 7 = Plong، ولو مفيش يرجع الرقم.<br><b>3 if منفصلة:</b> عشان الرقم ممكن يقبل على أكتر من واحد.<br><b>النتيجة الحقيقية:</b> 7 أرقام والـ 7 PASS.<br><b>المطلوب تفهمه:</b> else if كانت هتوقف عند أول صوت.", loop: 'البرنامج ده مافيهوش لوب <code>while</code> للشباك: بيمشي من أول <code>main</code> لآخرها مرة واحدة ويخلص.'},
  d6_m1: {goal: "<b>السؤال:</b> dot والطول بـ Python من غير مكتبات؟<br><b>الفكرة:</b> dot بلوب، والطول = جذر (a · a).<br><b>أمثلة Khan:</b> [2,5] · [7,1] و [1,2,3] · [‎-2,0,5].<br><b>50 عنصر:</b> نفس الدالة لأي طول.<br><b>النتيجة الحقيقية:</b> 19 و 13، و ‖[2,5]‖ = √29.<br><b>المطلوب تفهمه:</b> القانون واحد مهما كان عدد الأرقام.", loop: 'البرنامج بيمشي مرة واحدة ويخلص. واللوب الوحيد <code>for</code> جوه <code>dot</code>: بيلف مرة لكل عنصر.'},
  d6_m2: {goal: "<b>السؤال:</b> خصائص الضرب النقطي بأرقام؟<br><b>الفكرة:</b> نفس الأرقام بـ NumPy، و 3 خصائص بنتأكد منها.<br><b>الخصائص:</b> الترتيب مش بيفرق، والتوزيع، والرقم يطلع برا.<br><b>Unit vector:</b> نقسم على الطول.<br><b>النتيجة الحقيقية:</b> 13 و 13، و 21 و 21، و 39 و 39، ومتجه طوله 1.<br><b>المطلوب تفهمه:</b> الخصائص دي هي اللي بتخلي الحسابات بعدين أسهل.", loop: 'مفيش لوب: كل سطر بيتنفذ مرة واحدة، و NumPy هي اللي بتلف جواها.'},
  d6_r1: {goal: "<b>السؤال:</b> إزاي نحرّك اللون بـ uniform؟ (كود The Cherno)<br><b>الفكرة:</b> مستطيل بـ Index Buffer، ولونه من <code>u_Color</code>. كل فريم الـ CPU بيغيّر الأحمر 0.05 ويبعته.<br><b>العكس:</b> عند 0 و 1 الاتجاه بيتعكس.<br><b>الفحص:</b> لو الاسم مش موجود بيطبع تحذير.<br><b>النتيجة الحقيقية:</b> لون بيطلع وينزل، والأحمر بيتطبع كل 10 فريمات.<br><b>المطلوب تفهمه:</b> الأركان اتبعتت مرة، واللي بيتبعت كل فريم 4 أرقام بس.", loop: 'هنا اللوب هي اللي بتعمل الحركة: كل لفة <code>r</code> بيتغير ويتبعت للكارت قبل الرسم. الأركان (الصناديق) اتبعتت مرة واحدة قبل اللوب، واللي بيتبعت كل لفة 4 أرقام بس.'},
  d6_r2: {goal: "<b>السؤال:</b> رقم واحد من الـ CPU يلوّن كل بكسل بشكل مختلف؟<br><b>الفكرة:</b> الـ CPU بيبعت الوقت بس (<code>glUniform1f</code>)، والـ Fragment بيحسب لكل بكسل لون بـ sin من الوقت ومكان البكسل.<br><b>النوع:</b> float ← 1f.<br><b>النتيجة الحقيقية:</b> ألوان بتتحرك وتختلف من مكان لمكان.<br><b>المطلوب تفهمه:</b> الشغل التقيل على الكارت، والـ CPU بيبعت رقم.", loop: 'كل لفة: هات الوقت، وابعته، وارسم. رقم واحد بيتبعت، والكارت بيحسب آلاف الألوان.'},
  d6_c1: {goal: "<b>السؤال:</b> نقدر نرتّب الكود من غير ما نغيّر سلوكه؟ (Refactoring)<br><b>الفكرة:</b> نفس برنامج مسح آخر خط، والكود متقسم: ثوابت فوق، و 3 أفعال (AddPoint و FinishLine و DeleteLastLine)، والرسم كله في DrawScene.<br><b>الإثبات:</b> نفس الدوسات = نفس الرسايل بالحرف ونفس الصور.<br><b>النتيجة الحقيقية:</b> نفس الـ 11 حدث، ونفس النتيجة بالظبط.<br><b>المطلوب تفهمه:</b> الـ Callback بقى يترجم الضغطة لفعل بس، وكل فعل دالة صغيرة.", loop: 'اللوب بقى 3 سطور: <code>DrawScene</code> ثم Swap ثم <code>glfwPollEvents</code>. ولما حد يدوس، GLFW بينده الـ Callback، وهو بينده الفعل المناسب.'},
  d7_p1: {goal: "<b>السؤال:</b> مراجعة: الـ Pointer بيعمل إيه بالظبط؟ (كل أمثلة The Cherno)<br><b>الفكرة:</b> رقم فيه عنوان، والنوع بيقول كام بايت.<br><b>void*:</b> بيشيل عنوان var.<br><b>int*:</b> بيكتب فيه 10.<br><b>الحجم:</b> كل الـ Pointers 8 بايت.<br><b>الـ Heap:</b> 8 بايت فيهم Hi.<br><b>char**:</b> بيشاور على buffer نفسه.<br><b>النتيجة الحقيقية:</b> var بقى 10، والعناوين في الـ Terminal حقيقية.<br><b>المطلوب تفهمه:</b> & = هات العنوان، و * = روح للعنوان."},
  d7_p2: {goal: "<b>السؤال:</b> اختبر نفسك: 4 دوال بالـ Pointers تشتغل صح؟<br><b>الفكرة:</b> كل دالة ليها اختبار PASS أو FAIL.<br><b>Swap:</b> بتبدّل من خلال العناوين.<br><b>SetToZero:</b> بتفحص nullptr.<br><b>MakeText:</b> بتاخد char** عشان تغيّر text بتاع main.<br><b>Sum:</b> بتمشي بـ <code>*(values + i)</code> 4 مرات.<br><b>النتيجة الحقيقية:</b> الـ 4 PASS.<br><b>المطلوب تفهمه:</b> عشان دالة تغيّر حاجة: ابعتلها عنوانها."},
  d7_m1: {goal: "<b>السؤال:</b> اختبر نفسك: الضرب الاتجاهي بإيدك صح؟<br><b>الفكرة:</b> دالة cross بالقانون (الصف الأوسط معكوس)، و 7 أسئلة بتصحّح نفسها.<br><b>الأسئلة:</b> مثال Khan، والعمودية (<code>dot = 0</code>)، و i × j = k، والترتيب بيعكس الإشارة، و a × a = 0.<br><b>النتيجة الحقيقية:</b> الـ 7 PASS.<br><b>المطلوب تفهمه:</b> لو الصف الأوسط مش معكوس، 4 أسئلة بيفشلوا."},
  d7_m2: {goal: "<b>السؤال:</b> np.cross والـ Normal؟<br><b>الفكرة:</b> نفس المثال بـ NumPy، وأول استخدام حقيقي: الـ Normal بتاع مثلث.<br><b>على خط واحد:</b> [1,2,3] × [2,4,6] = صفر.<br><b>Normal:</b> الضرب الاتجاهي لضلعين من نفس الركن.<br><b>النتيجة الحقيقية:</b> الـ Normal = [0, 0, 6]، وبعد القسمة على الطول [0, 0, 1].<br><b>المطلوب تفهمه:</b> الـ Normal هو اللي هنحسب بيه الإضاءة بعدين."},
  d7_r1: {goal: "<b>السؤال:</b> ليه لازم VAO، وإيه اللي بيفتكره؟ (كود The Cherno)<br><b>الفكرة:</b> في الـ Core Profile مفيش VAO افتراضي. البرنامج بيجرب ربط من غير VAO، وبعدين بيفك كل حاجة ويربط قبل الرسم.<br><b>التجربة:</b> أول <code>glVertexAttribPointer</code> قبل الـ VAO اترفض: 1282.<br><b>الفك:</b> الـ Program والـ VAO والصندوقين.<br><b>اللوب:</b> بيربط الـ Program والـ VAO بس قبل الرسم.<br><b>النتيجة الحقيقية:</b> مستطيل لونه بيتحرك، و <code>glGetError</code> = 0 في كل الفريمات.<br><b>المطلوب تفهمه:</b> سطر <code>glBindVertexArray(vao)</code> بيرجّع الصندوق والـ Layout وصندوق الترتيب مرة واحدة.", loop: 'كل لفة: الـ Program والـ VAO بيترابطوا من جديد (لأننا فكّيناهم قبل اللوب)، والأحمر بيتغير 0.05 ويتبعت، وكل 10 لفات بنسأل <code>glGetError</code>. سطر <code>glBindVertexArray(vao)</code> لوحده بيرجّع الصندوق والـ Layout وصندوق الترتيب.'},
  d7_r2: {goal: "<b>السؤال:</b> The Cherno قال فيه طريقتين نقول بيهم للكارت «اقرا أركان الشكل ده إزاي». أنهي أحسن؟<br><b>الفكرة:</b> الكارت بياخد الأرقام في صندوق، ومحتاج ورقة تعليمات (VAO) تقوله كل ركن كام رقم. المربع كل ركن رقمين (x و y)، والمثلث 3 أرقام (x و y و z): Layout مختلف.<br><b>الطريقة 2 (البيت الشمال):</b> لكل شكل VAO لوحده، زي ورقة تعليمات مكتوبة مرة واحدة. قبل الرسم بنمسك الورقة بس: <code>glBindVertexArray(squareVao)</code>.<br><b>الطريقة 1 (البيت اليمين):</b> VAO واحد بس، زي ورقة واحدة: قبل كل رسمة بنمسحها ونكتب التعليمات من جديد: <code>glBindBuffer</code> + <code>glVertexAttribPointer</code>.<br><b>u_Offset:</b> مالوش دعوة بالتجربة، بيزحزح الرسمة عشان البيتين يبانوا جنب بعض.<br><b>النتيجة الحقيقية:</b> البيتين نفس البكسلات بالظبط (قارناهم بالكمبيوتر). الفرق في الكود بس: الطريقة 2 = سطرين ربط في الفريم، والطريقة 1 = 6 سطور.<br><b>المطلوب تفهمه:</b> الـ VAO بيحفظ «يقرا إزاي»، فالطريقة 2 أبسط، وعشان كده The Cherno بينصح بيها. وفي الطريقة 1 لو نسيت تكتب التعليمات قبل رسمة، الشكل بيبوظ (جربناها في ملف اليوم 7).", loop: 'كل لفة 4 رسمات: المربع والمثلث مرتين. الشمال بيربط VAO لكل رسمة، واليمين بيعيد <code>glBindBuffer</code> و <code>glVertexAttribPointer</code> قبل كل رسمة. الصورة ثابتة، فكل اللفات نفس الصورة.'},
  d7_c1: {goal: "<b>السؤال:</b> الـ ID بتاع الـ Commit (84180e1) جاي منين؟<br><b>الفكرة:</b> مش رقم عشوائي: بصمة SHA-1 للمحتوى.<br><b>blob:</b> بصمة الملف <code>refactored.cpp</code> = d088e29.<br><b>tree:</b> بصمة الفولدر = c298df0.<br><b>commit:</b> بصمة نص الـ Commit (الفولدر والاسم والوقت والرسالة).<br><b>النتيجة الحقيقية:</b> 84180e1 = نفس اللي <code>git log --oneline</code> طبعه في الجلسة الحقيقية.<br><b>المطلوب تفهمه:</b> أي تغيير، حتى حرف أو ثانية، بيطلّع ID مختلف خالص."},
  d5_c2: {goal: "<b>السؤال:</b> إزاي نمسح آخر خط بـ Backspace؟<br><b>الفكرة:</b> نفس Polylines بالماوس، و Backspace بيشيل آخر خط من القايمتين.<br><b>KeyCallback:</b> pop_back للخط، ولوب بتعمل pop_back لكل رقم من نقطه (عدد النقط × 2).<br><b>النتيجة الحقيقية:</b> 10 ضغطات ماوس و Backspace واحد: الخط التاني اتمسح، وبعدين اترسم خط جديد بنقطتين.<br><b>المطلوب تفهمه:</b> المسح لازم يحصل في الاتنين: النقط والجدول.", loop: 'كل لفة: ارسم كل خط بـ <code>GL_LINE_STRIP</code>، وبعدين النقط، وبعدين <code>glfwPollEvents</code> تسأل: حد داس على الماوس أو الكيبورد؟ لو أيوه GLFW بينده <code>MouseButtonCallback</code> أو <code>KeyCallback</code> لوحده. والتغيير بيبان في اللفة اللي بعدها. وكمان GLFW بينده الدالة تاني لما الزرار يطلع (Release)، بس السطر الأول بيرجّعها على طول، فالمرة دي مش ظاهرة في الخطوات.'},
  d1_p1: {goal: "<b>السؤال:</b> إزاي نعمل Pointer مش بيشاور على حاجة؟<br><b>الفكرة:</b> الـ Pointer رقم فيه عنوان. العنوان 0 معناه «مفيش حاجة».<br><b>3 طرق:</b> <code>void* a = 0;</code> و <code>= NULL;</code> و <code>= nullptr;</code>.<br><b>النتيجة الحقيقية:</b> الـ 3 طبعوا 0.<br><b>المطلوب تفهمه:</b> الـ 3 نفس الحاجة، و <code>nullptr</code> هي الطريقة الحديثة في C++."},
  d1_p2: {goal: "<b>السؤال:</b> الـ Pointer بيشيل إيه بالظبط؟<br><b>الفكرة:</b> كل متغير له بيت في الرام وله عنوان. <code>&var</code> = «هات عنوان var».<br><b>var:</b> جواه 8.<br><b>ptr:</b> <code>void* ptr = &var;</code>: جواه عنوان var.<br><b>النتيجة الحقيقية:</b> <code>&var</code> و <code>ptr</code> طبعوا نفس الرقم (0x7fffffff95ac).<br><b>المطلوب تفهمه:</b> الـ Pointer مش القيمة، هو رقم البيت اللي فيه القيمة."},
  d1_p3: {goal: "<b>السؤال:</b> لو العنوان رقم وخلاص، ليه فيه <code>int*</code> و <code>double*</code>؟<br><b>الفكرة:</b> نفس العنوان ممكن يتشاف بنوعين. النوع بيقول للـ compiler: هنقرا كام بايت من هنا.<br><b>ptr:</b> <code>int*</code> على var.<br><b>ptr2:</b> <code>double*</code> على نفس var.<br><b>النتيجة الحقيقية:</b> الاتنين طبعوا نفس العنوان، و <code>int = 4</code> بايت و <code>double = 8</code> بايت.<br><b>المطلوب تفهمه:</b> العنوان واحد، والنوع هو اللي بيحدد حجم القراية والكتابة."},
  d1_p4: {goal: "<b>السؤال:</b> نقدر نغيّر متغير من غير ما نكتب اسمه؟<br><b>الفكرة:</b> النجمة قبل الـ Pointer = «روح للعنوان ده». فـ <code>*ptr = 10;</code> بتكتب في بيت var نفسه.<br><b>قبل:</b> <code>var = 8</code>.<br><b>الكتابة:</b> <code>*ptr = 10;</code><br><b>النتيجة الحقيقية:</b> var بقى 10.<br><b>المطلوب تفهمه:</b> ده أساس كل اللي جاي: الدالة اللي بتاخد عنوان تقدر تغيّر المتغير الأصلي."},
  d1_p5: {goal: "<b>السؤال:</b> إزاي نحجز ذاكرة وقت التشغيل؟<br><b>الفكرة:</b> <code>new char[8]</code> بيحجز 8 بايت على الـ Heap ويرجّع عنوان أولهم. و <code>memset</code> بيملاهم أصفار.<br><b>الطباعة:</b> لوب بتلف 8 مرات وتطبع كل بايت.<br><b>المسح:</b> <code>delete[] buffer;</code> بيرجّع الـ 8 بايت.<br><b>النتيجة الحقيقية:</b> العنوان (0x55555559d2b0) وبعده 8 أصفار.<br><b>المطلوب تفهمه:</b> اللي يتحجز بـ <code>new[]</code> لازم يترجع بـ <code>delete[]</code>."},
  d1_p6: {goal: "<b>السؤال:</b> الـ Pointer نفسه ليه عنوان؟<br><b>الفكرة:</b> <code>buffer</code> متغير زي أي متغير، فليه بيت وعنوان. <code>char** ptr = &buffer;</code> = Pointer لـ Pointer.<br><b>ptr:</b> عنوان buffer.<br><b>*ptr:</b> اللي جوه buffer = عنوان الـ 8 بايت.<br><b>(*ptr)[0]:</b> أول بايت (0).<br><b>النتيجة الحقيقية:</b> <code>ptr</code> = <code>&buffer</code>، و <code>*ptr</code> = <code>buffer</code>.<br><b>المطلوب تفهمه:</b> كل نجمة = خطوة على السلسلة: ptr ← buffer ← البايتات."},
  d1_dot: {goal: "<b>السؤال:</b> إزاي نحسب الضرب النقطي، ونعرف منه الاتجاه؟<br><b>الفكرة:</b> dot = اضرب المتقابلين واجمع، والنتيجة رقم واحد.<br><b>بإيدنا:</b> دالة <code>dot</code> بلوب على 2D و 4D.<br><b>glm::dot:</b> نفس الحساب بالمكتبة على متجهات في نفس الاتجاه، وعمودية، وعكس بعض.<br><b>النتيجة الحقيقية:</b> [1,2] · [3,4] = 11، و [6,2,8,3] · [1,8,5,3] = 71. ونفس الاتجاه = 7، وعمودي = 0، وعكس = ‎-7.<br><b>المطلوب تفهمه:</b> الإشارة بتقول الاتجاه: موجب = نفس الناحية، صفر = عمودي، سالب = عكس."},
  d2_c1: {goal: "<b>السؤال:</b> إيه شكل أول برنامج بلغة C؟<br><b>الفكرة:</b> C هي أصل C++. بدل <code>std::cout</code> بنستخدم <code>printf</code>، و <code>%d</code> مكان الرقم.<br><b>year:</b> 1972.<br><b>النتيجة الحقيقية:</b> «C was born in 1972» و «Hello from C!».<br><b>المطلوب تفهمه:</b> نفس الفكرة بكتابة مختلفة: النص فيه مكان للرقم، والرقم بييجي بعده."},
  d2_c2: {goal: "<b>السؤال:</b> إزاي نحجز مصفوفة في C؟<br><b>الفكرة:</b> <code>malloc</code> بيحجز بايتات ويرجّع عنوان (زي <code>new</code>)، و <code>free</code> بيرجّعها (زي <code>delete</code>).<br><b>الحجز:</b> <code>malloc(5 * sizeof(int))</code> = 20 بايت.<br><b>الفحص:</b> لو رجع NULL يبقى فشل.<br><b>لوبين:</b> واحدة بتملا (i × 10)، وواحدة بتطبع.<br><b>النتيجة الحقيقية:</b> <code>numbers[0] = 0</code> لحد <code>numbers[4] = 40</code>.<br><b>المطلوب تفهمه:</b> في C إنت اللي بتحسب الحجم بالبايت، وإنت اللي بترجّع الذاكرة."},
  d2_c3: {goal: "<b>السؤال:</b> لما أزوّد Pointer بـ 1 بيروح فين؟<br><b>الفكرة:</b> <code>p++</code> على <code>int*</code> بينط 4 بايت (حجم int)، مش بايت واحد.<br><b>المصفوفة:</b> {10, 20, 30, 40}.<br><b>اللوب:</b> تطبع العنوان والقيمة، وبعدين <code>p++</code>.<br><b>النتيجة الحقيقية:</b> العناوين 95a0 ← 95a4 ← 95a8 ← 95ac، والقيم 10 و 20 و 30 و 40.<br><b>المطلوب تفهمه:</b> حساب العناوين بيمشي بحجم النوع، عشان كده النوع مهم."},
  d2_c4: {goal: "<b>السؤال:</b> إزاي دالة تغيّر متغير بتاع main؟<br><b>الفكرة:</b> نبعتلها العنوان، وهي تكتب من خلاله.<br><b>doubleIt:</b> <code>*number = *number * 2;</code><br><b>النداء:</b> <code>doubleIt(&score);</code><br><b>النتيجة الحقيقية:</b> score كان 21 وبقى 42.<br><b>المطلوب تفهمه:</b> الدالة استلمت نسخة من العنوان، بس العنوان لسه بيشاور على score الأصلي."},
  d2_d1: {goal: "<b>السؤال:</b> إزاي نحسب طول متجه؟<br><b>الفكرة:</b> الطول = جذر (v · v)، يعني فيثاغورس.<br><b>dot:</b> بلوب.<br><b>length:</b> <code>std::sqrt(dot(a, a, n))</code>.<br><b>النتيجة الحقيقية:</b> [2,5] · [7,1] = 19، و [1,2,3] · [‎-2,0,5] = 13، و [2,5] · [2,5] = 29، والطول = 5.38516 = √29.<br><b>المطلوب تفهمه:</b> الطول مبني على الضرب النقطي للمتجه في نفسه."},
  d2_v1: {goal: "<b>السؤال:</b> إزاي نخزن عدد أركان مش معروف من الأول؟<br><b>الفكرة:</b> <code>std::vector</code> قايمة بتكبر لوحدها.<br><b>push_back:</b> بيضيف في الآخر.<br><b>[0] و at(1):</b> الوصول لعنصر برقمه.<br><b>النتيجة الحقيقية:</b> الحجم 0 ثم 3، و <code>vertices[0].x = 1</code>، و <code>vertices.at(1).y = 5</code>.<br><b>المطلوب تفهمه:</b> الـ vector بيبدأ فاضي ويكبر مع كل push_back."},
  d2_v2: {goal: "<b>السؤال:</b> إزاي نلف على كل عناصر الـ vector؟<br><b>الفكرة:</b> 3 طرق.<br><b>بالرقم:</b> <code>for (size_t i = 0; ...)</code><br><b>for-each:</b> <code>for (const Vertex& v : vertices)</code>: قراية بس.<br><b>بالـ Reference:</b> <code>for (Vertex& v : vertices)</code>: بيعدّل الأصل.<br><b>النتيجة الحقيقية:</b> x بقى 10 و 40 بعد الضرب في 10.<br><b>المطلوب تفهمه:</b> من غير <code>&</code> اللوب بتشتغل على نسخة، والتعديل يضيع."},
  d2_v3: {goal: "<b>السؤال:</b> إزاي نمسح من الـ vector؟<br><b>الفكرة:</b> <code>erase</code> بيشيل عنصر من مكانه، و <code>clear</code> بيفضّيه كله.<br><b>الطباعة:</b> <code>operator<<</code> عشان نطبع Vertex بسطر واحد.<br><b>النتيجة الحقيقية:</b> بعد erase فضل (1, 2, 3)، وبعد clear الحجم 0.<br><b>المطلوب تفهمه:</b> الـ vector بيتحكم في الحجم لوحده وإنت بتضيف وتشيل."},
  d2_v4: {goal: "<b>السؤال:</b> إزاي نخزن نقط رسمة CAD؟<br><b>الفكرة:</b> كل نقطة struct فيه x و y، وكلهم في vector.<br><b>addPoint:</b> بتاخد الـ vector بـ Reference وتضيف.<br><b>printPoints:</b> بتاخده <code>const&</code> وتطبع.<br><b>pop_back:</b> بيشيل آخر نقطة.<br><b>النتيجة الحقيقية:</b> 3 نقط ثم نقطتين.<br><b>المطلوب تفهمه:</b> ده نفس اللي هيحصل في برامج الـ CAD بالماوس بعد كده."},
  d2_v5: {goal: "<b>السؤال:</b> الـ vector بيكبر إزاي من جوه؟<br><b>الفكرة:</b> الـ vector حاجز مكان (capacity) أكبر من اللي مستخدمه (size). لما المكان يخلص، بيحجز ضعفه وينقل كل حاجة.<br><b>اللوب:</b> 9 مرات push_back، وكل مرة نطبع size و capacity، ونشوف العنوان اتغير ولا لأ.<br><b>النتيجة الحقيقية:</b> capacity: 1 ← 2 ← 4 ← 8 ← 16، والنقل حصل عند 1 و 2 و 3 و 5 و 9.<br><b>المطلوب تفهمه:</b> العنوان بيتغير لما الـ vector يتنقل، فأي Pointer قديم على عناصره يبوظ."},
  d3_r1: {goal: "<b>السؤال:</b> يعني إيه Reference؟<br><b>الفكرة:</b> <code>int& ref = a;</code> = اسم تاني لنفس الصندوق، مش صندوق جديد.<br><b><code>ref = 2</code>:</b> كتبنا في ref.<br><b>النتيجة الحقيقية:</b> a بقى 2، و <code>&a</code> و <code>&ref</code> نفس العنوان.<br><b>المطلوب تفهمه:</b> الـ Reference مالوش بيت لوحده: هو نفس المتغير باسم تاني."},
  d3_r2: {goal: "<b>السؤال:</b> أنهي طريقة بتخلّي الدالة تغيّر المتغير؟<br><b>الفكرة:</b> نفس الزيادة بـ 3 طرق.<br><b>نسخة:</b> زوّدت النسخة بس.<br><b>Pointer:</b> <code>(*value)++</code>.<br><b>Reference:</b> <code>value++</code> على الأصل.<br><b>النتيجة الحقيقية:</b> a: 5 (النسخة ماغيرتش) ثم 6 ثم 7.<br><b>المطلوب تفهمه:</b> الـ Pointer والـ Reference الاتنين بيغيّروا الأصل، والـ Reference كتابته أسهل."},
  d3_r3: {goal: "<b>السؤال:</b> ينفع أخلّي Reference يشاور على متغير تاني؟<br><b>الفكرة:</b> لأ. <code>ref = b;</code> مش «ref بقى b»، دي «اكتب قيمة b جوه a».<br><b>Reference:</b> نسخ 8 جوه a.<br><b>Pointer:</b> اتنقل من a لـ b عادي.<br><b>النتيجة الحقيقية:</b> بعد <code>ref = b</code>: <code>a = 8</code>. وبعد الـ Pointer: <code>a = 2</code> و <code>b = 1</code>.<br><b>المطلوب تفهمه:</b> الـ Reference مربوط بمتغير واحد للأبد، والـ Pointer ممكن يتنقل."},
  d3_r4: {goal: "<b>السؤال:</b> إزاي The Cherno بيستخدم الـ References؟<br><b>الفكرة:</b> نفس كود الفيديو، و <code>LOG</code> اختصار للطباعة.<br><b>Increment:</b> بـ Reference.<br><b>Pointer:</b> بيكتب في a وبعدين يتنقل لـ b.<br><b>النتيجة الحقيقية:</b> 2 ثم 3 ثم 2 ثم 1.<br><b>المطلوب تفهمه:</b> لو مش محتاج تتنقل لحاجة تانية: استخدم Reference."},
  d3_h1: {goal: "<b>السؤال:</b> كام حرف مختلف بين سلسلتين DNA؟ (تمرين Hamming)<br><b>الفكرة:</b> نقارن حرف حرف في نفس المكان ونعد المختلف.<br><b>strlen:</b> لو الطولين مختلفين: ‎-1.<br><b>اللوب:</b> بالـ index.<br><b>النتيجة الحقيقية:</b> 7، و 0، و ‎-1 (طولين مختلفين).<br><b>المطلوب تفهمه:</b> الحل الأول بالـ index زي أي لغة."},
  d3_h2: {goal: "<b>السؤال:</b> نفس التمرين بالـ Pointers؟<br><b>الفكرة:</b> الـ Pointers هي اللي بتمشي على الحروف: <code>lhs++</code> لحد ما نوصل لصفر آخر النص.<br><b>الفحص:</b> NULL ← ‎-1.<br><b>النهاية:</b> لو واحد خلص قبل التاني ← ‎-1.<br><b>النتيجة الحقيقية:</b> 7، و 0، و ‎-1، و ‎-1.<br><b>المطلوب تفهمه:</b> النص في C = عنوان أول حرف، والصفر في الآخر بيقول خلص."},
  d3_x1: {goal: "<b>السؤال:</b> إيه الضرب الاتجاهي؟<br><b>الفكرة:</b> في 2D بيطلّع رقم، وفي 3D بيطلّع متجه عمودي على الاتنين.<br><b>2D:</b> <code>v1 * w2 - v2 * w1</code>.<br><b>3D:</b> القانون بـ 3 صفوف.<br><b>النتيجة الحقيقية:</b> 2D: ‎-5، والعكس 5، و 3v × w = ‎-15. و 3D: [0,0,2] × [0,2,0] = (‎-4, 0, 0)، والضرب النقطي معاهم 0 و 0.<br><b>المطلوب تفهمه:</b> الترتيب بيعكس الإشارة، والناتج في 3D عمودي."},
  d4_st1: {goal: "<b>السؤال:</b> إيه فايدة <code>static</code> برا الكلاس؟<br><b>الفكرة:</b> متغير أو دالة <code>static</code> = تخص الملف ده بس، فملف تاني يقدر يستخدم نفس الاسم من غير تعارض.<br><b>main.cpp:</b> <code>s_Variable = 10</code>.<br><b>static.cpp:</b> <code>s_Variable = 5</code> (static).<br><b>النتيجة الحقيقية:</b> كل ملف شاف بتاعه: 10 و 5، وكل Function طبعت اسم ملفها.<br><b>المطلوب تفهمه:</b> static = مخفي عن باقي الملفات."},
  d4_st2: {goal: "<b>السؤال:</b> إزاي ملف يستخدم متغير متعرّف في ملف تاني؟<br><b>الفكرة:</b> <code>extern int s_Variable;</code> = «المتغير ده موجود في حتة تانية».<br><b>static.cpp:</b> <code>s_Variable = 5</code>.<br><b>النتيجة الحقيقية:</b> 5.<br><b>المطلوب تفهمه:</b> extern عكس static: بيدوّر في الملفات التانية."},
  d4_c1: {goal: "<b>السؤال:</b> <code>const</code> مع الـ Pointer معناها إيه؟<br><b>الفكرة:</b> مكان الـ const بيفرق.<br><b>const int*:</b> مينفعش تغيّر القيمة، ينفع تنقل الـ Pointer.<br><b>int* const:</b> ينفع تغيّر القيمة، مينفعش تنقله.<br><b>const int* const:</b> ولا ده ولا ده.<br><b>النتيجة الحقيقية:</b> <code>*a = 2</code>، و <code>*b = 90</code>، و <code>*c = 2</code>، و <code>*d = 90</code>.<br><b>المطلوب تفهمه:</b> اقرا من اليمين للشمال: الـ const بيمسك اللي قبله."},
  d4_c2: {goal: "<b>السؤال:</b> يعني إيه دالة <code>const</code>؟<br><b>الفكرة:</b> <code>GetX() const</code> = بتوعد إنها مش هتغيّر الـ object. و <code>mutable</code> استثناء لعداد debug.<br><b>PrintEntity:</b> بتاخد <code>const Entity&</code>، فمش هتقدر تنده غير دوال const.<br><b>النتيجة الحقيقية:</b> <code>x = 7</code> مرتين، و GetX اتندهت مرتين.<br><b>المطلوب تفهمه:</b> const بتحمي البيانات، و mutable للحاجات اللي مش جزء من «البيانات الحقيقية»."},
  d4_x1: {goal: "<b>السؤال:</b> حل تمارين Khan في الضرب الاتجاهي؟<br><b>الفكرة:</b> دالة cross بالقانون، و check بتطبع الناتج وتتأكد إنه عمودي (<code>dot = 0</code>).<br><b>5 أمثلة:</b> مثال الفيديو و i × j و j × i ومثالين كمان.<br><b>النتيجة الحقيقية:</b> [1,‎-7,1] × [5,2,4] = [‎-30, 1, 37]، و [2,3,4] × [5,6,7] = [‎-3, 6, ‎-3]، و [3,‎-3,1] × [4,9,2] = [‎-15, ‎-2, 39]. وكل الضرب النقطي = 0.<br><b>المطلوب تفهمه:</b> لو الضرب النقطي مش صفر، يبقى غلطت في القانون."},
};
const CAT = {win:'تجهيز الشباك والوصلة بالكارت', data:'تجهيز الداتا في الرام', buf:'شحن الداتا للكارت', sh:'تجهيز الـ Shaders', loop:'اللوب: ارسم كل فريم', end:'الخروج والتنضيف'};
function stepText(s){ return (P.files[s.f].lines[s.ln - 1] || '').trim(); }
function catOf(s, k, exitK){
  if (s.lap) return 'loop'; if (exitK >= 0 && k >= exitK) return 'end';
  const t = stepText(s), f = s.fn || '';
  if (/Shader|Program/.test(f) || /Shader|Program|glUseProgram|glGetUniformLocation|getline|ss\[/.test(t)) return 'sh';
  if (/glfw|glad|glViewport/.test(t)) return 'win';
  if (/VertexArray|glGenBuffers|glBindBuffer|glBufferData|VertexAttrib|glDeleteBuffers/.test(t) || /^(VAO|VBO|EBO)/.test(f)) return 'buf';
  return 'data';
}
function chapters(){
  const exitK = ST.findIndex(s => s.cl); const raw = [];
  ST.forEach((s, k) => { const c = catOf(s, k, exitK); const L = raw[raw.length - 1]; if (L && L.c === c) L.to = k; else raw.push({c, from:k, to:k}); });
  const out = []; // fold tiny chapters into the previous one, then merge equal neighbours
  raw.forEach((ch, n) => { const small = ch.to - ch.from < 2 && ch.c !== 'loop' && ch.c !== 'end'; const L = out[out.length - 1];
    if (small && L){ L.to = ch.to; return; } if (L && L.c === ch.c){ L.to = ch.to; return; } out.push(Object.assign({}, ch)); });
  if (out.length > 1 && out[0].to - out[0].from < 2 && out[0].c !== out[1].c){ out[1].from = out[0].from; out.shift(); }
  return out;
}
function nd(t, c){ return `<span class="nd${c ? ' ' + c : ''}">${t}</span>`; }
const AR = '<span class="ar">←</span>';
function chapText(ch){
  const a = ST[ch.from], b = ST[ch.to], G = b.gp, G0 = ch.from ? ST[ch.from - 1].gp : {vaos:{}, bufs:{}, sh:{}, pr:{}, uni:{}};
  const newBufs = Object.entries(G.bufs).filter(([id]) => !G0.bufs[id]), newVaos = Object.keys(G.vaos).filter(id => !G0.vaos[id]);
  const bytes = newBufs.reduce((n, [, x]) => n + (x.bytes || 0), 0);
  const fns = [...new Set(ST.slice(ch.from, ch.to + 1).filter(s => s.d > 1).map(s => s.fn))];
  const calls = fns.length ? ` التنفيذ نط لـ ${fns.map(f => `<code>${esc(f)}()</code>`).join(' و ')} ورجع.` : '';
  const vars = [...new Set(ST.slice(ch.from, ch.to + 1).filter(s => s.d === 1 && /متغير جديد/.test(s.ti)).map(s => (/\b(\w+)\s*(\[[^\]]*\])?\s*(=|\{|;)/.exec(stepText(s)) || [])[1]).filter(Boolean))];
  switch (ch.c){
    case 'win': return {t: `البرنامج بيبدأ من <code>main()</code>. الـ CPU بيطلب من GLFW يجهز نفسه، وبعدين يفتح شباك ${P.W} × ${P.H}. بعدين <code>glfwMakeContextCurrent</code> بيوصّل الشباك ده بكارت الشاشة (Context)، و GLAD بيجيب من الدرايفر عناوين دوال OpenGL.${calls}`,
      who: `${nd('الكود بتاعك')} ${AR} ${nd('CPU', 'c')} ${AR} ${nd('GLFW')} ${AR} ${nd('نظام التشغيل')} ${AR} ${nd('🪟 الشباك')}، و ${nd('GLAD')} ${AR} ${nd('درايفر الكارت')}`,
      why: 'قبل الفصل ده مفيش أي دالة من دوال OpenGL (اللي بتبدأ بـ <code>gl</code> زي <code>glClear</code>) تنفع تشتغل: لازم يبقى فيه شباك وكارت متوصل بيه الأول.'};
    case 'data': return {t: `الـ CPU لوحده بيجهز الأرقام في الرام: ${vars.length ? vars.map(v => `<code>${esc(v)}</code>`).join('، ') : 'متغيرات ومصفوفات'}. الكارت لسه ما يعرفش عنها أي حاجة.${calls}`,
      who: `${nd('CPU', 'c')} ${AR} ${nd('الرام')}`, why: 'الأركان والألوان لازم تبقى موجودة في الرام الأول عشان نعرف ننسخها للكارت بعد كده.'};
    case 'buf': { const ups = ST.slice(ch.from, ch.to + 1).map((s, j) => [s, ch.from + j]).filter(([s]) => /glBufferData/.test(stepText(s)));
      const brk = bufBreakdown(G, newBufs.map(([id]) => id));
      return {t: `الـ CPU بيطلب من الكارت يحجز ${newVaos.length ? nVao(newVaos.length) : ''}${newVaos.length && newBufs.length ? ' و ' : ''}${newBufs.length ? nBuf(newBufs.length) : ''}. <b>الـ Buffer</b> (هنسميه «الصندوق») = مساحة في ذاكرة الكارت بنحط فيها أرقام الأركان. <b>الـ VAO</b> (هنسميه «ورقة التعليمات») = ورقة بتقول للكارت الأرقام اللي في الصندوق مترتبة إزاي. بعدين <code>glBufferData</code> ${ups.length ? `(${ups.map(([s, k]) => lnk(k)).join(' و ')})` : ''} ${bytes ? `بينسخ <b>${bytes} بايت</b> من الرام للصندوق اللي على الكارت` : 'بيحجز الصندوق <b>فاضي (0 بايت)</b> لأن لسه مفيش نقط، وهيتملي بعدين في اللوب'}، و <code>glVertexAttribPointer</code> بيكتب في ورقة التعليمات (الـ VAO) إزاي الكارت يقرا الصندوق: كل ركن فيه كام رقم، وبعد كام بايت ييجي الركن اللي بعده.${calls}${brk}${linkMap()}`,
      who: `${nd('CPU', 'c')} ${AR} ${nd('glGenBuffers / glBufferData')} ${AR} ${nd('الدرايفر')} ${AR} ${nd('GPU: Buffers و VAOs', 'g')}`,
      why: 'الكارت مش بيقرا من رام الكمبيوتر وهو بيرسم. لازم الداتا تتنقل لذاكرته مرة واحدة هنا، وبعد كده كل فريم يرسم منها على طول من غير ما الـ CPU يبعتها تاني.'}; }
    case 'sh': { const pr = Object.keys(G.pr)[0]; const un = Object.keys(G.uni);
      return {t: `نص الـ Shaders بيتبعت للدرايفر، يترجمه لأوامر الكارت (Compile)، ويربط الاتنين في برنامج واحد${pr ? ` (Program ${pr})` : ''} (Link).${calls} ${un.length ? `وبعدين بنجيب رقم خانة الـ uniform ${un.map(u => `<code>${esc(u)}</code>`).join(' و ')}.` : ''}`,
      who: `${nd('CPU', 'c')} ${AR} ${nd('نص GLSL')} ${AR} ${nd('الدرايفر يترجم')} ${AR} ${nd('GPU: Vertex + Fragment = Program', 'g')}`,
      why: 'الكارت مش بيفهم C++. الـ Shaders هما البرامج الصغيرة اللي هتشتغل على الكارت نفسه: الـ Vertex مرة لكل ركن، والـ Fragment مرة لكل بكسل.'}; }
    case 'loop': { const laps = P.laps, clicks = ST.filter(s => s.ev).length, keys = ST.filter(s => s.ev && s.ev.btn === 'key').length, draws = ST.slice(ch.from, ch.to + 1).filter(s => s.an === 'draw').length;
      const order = P.phases.map(p => { const t = p[1]; const m = /\b(gl\w+)\s*\(/.exec(t) || /([A-Za-z_]\w*(?:\.|->)\w+)\s*\(/.exec(t); return `<code>${esc(/^while/.test(t) ? 'while (!glfwWindowShouldClose)' : m ? m[1] + '()' : t.replace(/;$/, ''))}</code>`; }).join(' ← ');
      return {t: `${(PSTORY[P.id] || {}).loop || STATIC_LOOP}<br>ترتيب اللفة الواحدة: ${order}. في التشغيل ده لفّت <b>${laps}</b> مرات، واتعمل فيها ${draws} أمر رسم${clicks ? (keys ? `، والماوس نده دالته <b>${times(clicks - keys)}</b>، والكيبورد نده دالته <b>${times(keys)}</b>` : `، والماوس نده الدالة <b>${times(clicks)}</b>`) : ''}.`,
        who: `${nd('CPU', 'c')} ${AR} ${nd('glClear و glDrawArrays')} ${AR} ${nd('GPU يرسم في Back', 'g')} ${AR} ${nd('Swap')} ${AR} ${nd('🖥 الشاشة')}` + (clicks ? `، وبالعكس: ${nd(keys ? '🖱 الماوس و ⌨ الكيبورد' : '🖱 الماوس')} ${AR} ${nd('نظام التشغيل')} ${AR} ${nd('GLFW')} ${AR} ${nd('دالتك (Callback)', 'c')}` : ''),
        why: 'عشان الصورة تفضل على الشاشة وتتحدث، والبرنامج يفضل يسمع للماوس والكيبورد وزرار القفل. اللوب بتقف لما الشباك يتطلب يتقفل.'}; }
    case 'end': return {t: `الشرط <code>glfwWindowShouldClose</code> بقى true (في التشغيل ده إحنا اللي طلبنا القفل بعد آخر لفة)، فالـ while وقفت. بعدها البرنامج بيمسح اللي حجزه على الكارت ويقفل GLFW، وبعدين <code>return 0</code>.${calls}`,
      who: `${nd('CPU', 'c')} ${AR} ${nd('glDeleteProgram')} ${AR} ${nd('GPU يفضّي', 'g')}، و ${nd('CPU', 'c')} ${AR} ${nd('glfwTerminate')} ${AR} ${nd('نظام التشغيل يقفل الشباك')}`,
      why: 'أي حاجة اتحجزت لازم تترجع. الكارت ونظام التشغيل مش هيعرفوا لوحدهم إن البرنامج خلص بالأدب.'};
  }
}

function lnk(k){ return `<a href="#" class="sl" data-go="${k}">سطر ${lineOf(ST[k].v)}</a>`; }

const SHAPE_AR = {square: 'المربع', triangle: 'المثلث', positions: 'الشكل', vertices: 'الشكل', house: 'البيت', sun: 'الشمس', points: 'النقط', rect: 'المستطيل', rectangle: 'المستطيل', quad: 'المربع', line: 'الخط', lines: 'الخطوط', cube: 'المكعب', grid: 'الشبكة', pyramid: 'الهرم'};
function vaoNames(){ const R = {}; ST.forEach(s => { const m = /glBindVertexArray\s*\(\s*([A-Za-z_]\w*)\s*\)/.exec(stepText(s)); const g = s.gp || {}; if (m && g.bvao && !R[g.bvao]) R[g.bvao] = m[1]; }); return R; }
// program-specific closing note for the «مين بتاع مين؟» box
function goLine(n, lap){ const k = ST.findIndex(s => s.ln === n && (lap ? s.lap === lap : true)); return k < 0 ? `سطر ${n}` : `<a href="#" class="sl" data-go="${k}">سطر ${n}</a>`; }
const LINK_EXTRA = {
  d7_r2: () => `<details class="sub"><summary><b>الطريقتين جنب بعض: كام VAO في كل طريقة؟</b></summary>
<div class="tw"><table class="mtab"><thead><tr><th></th><th>الطريقة 1 (اليمين)</th><th>الطريقة 2 (الشمال)</th></tr></thead><tbody>
<tr><td>عدد الـ VAO</td><td><b>عدد 1</b></td><td><b>عدد 2</b></td></tr>
<tr><td>رقمه</td><td>VAO رقم 3</td><td>VAO رقم 1 و VAO رقم 2</td></tr>
<tr><td>اسمه في الكود</td><td><code>globalVao</code></td><td><code>squareVao</code> و <code>triangleVao</code></td></tr>
<tr><td>مين بيستخدمه</td><td>المربع والمثلث بالدور</td><td>كل شكل ليه واحد</td></tr>
<tr><td>الـ Layout بيتكتب</td><td>جوه اللوب، قبل كل رسمة</td><td>مرة واحدة قبل اللوب</td></tr>
<tr><td>أوامر التجهيز كل لفة</td><td><b>عدد 6</b></td><td><b>عدد 2</b></td></tr>
<tr><td>الـ Buffers</td><td colspan="2">نفس الـ Buffers، وعددهم 3</td></tr>
</tbody></table></div>
<p>أوامر التجهيز في الطريقة 1 (عدد 6): <code>glBindVertexArray</code> عدد 1 مرة، و <code>glBindBuffer</code> عدد 3 مرات، و <code>glVertexAttribPointer</code> عدد 2 مرة. وفي الطريقة 2 (عدد 2): <code>glBindVertexArray</code> قبل كل شكل بس.</p>
<p>المجموع: عدد 1 + عدد 2 = <b>عدد 3 VAO</b> في البرنامج كله. ومفيش ولا VAO مستخدم في الطريقتين مع بعض. اللي مشترك بين الطريقتين هو الـ Buffers بس.</p>
<p><b>«مشترك» في VAO رقم 3 يعني إيه؟</b> يعني مشترك بين <b>المربع والمثلث</b> جوه الطريقة 1، مش بين الطريقتين. هو ورقة تعليمات واحدة، بنكتب فيها المربع وبعدين المثلث بالدور، في كل لفة:</p>
<ol>
<li>نشغّل VAO رقم 3 (${goLine(164, 1)}).</li>
<li><b>نكتب فيه المربع:</b> «اقرا من <code>squareBuffer</code>، كل ركن رقمين، وخد الترتيب من <code>squareIbo</code>» (${goLine(165, 1)} لـ ${goLine(167, 1)}).</li>
<li>نرسم المربع (${goLine(169, 1)}).</li>
<li><b>نكتب فوقه المثلث:</b> «اقرا من <code>triangleBuffer</code>، كل ركن 3 أرقام» (${goLine(170, 1)} و ${goLine(171, 1)}). الكتابة دي بتمسح بتاعة المربع.</li>
<li>نرسم المثلث (${goLine(173, 1)}).</li>
</ol>
<p>وفي اللفة اللي بعدها نرجع نكتب المربع تاني، وهكذا. الورقة مش بتشيل الاتنين مع بعض: كل مرة شكل واحد بس. ولو نسيت تكتب واحد منهم قبل رسمته، الورقة هتفضل شايلة اللي قبله، والمثلث يترسم بأرقام المربع ويطلع نص مربع أزرق.</p>
<p><b>والطريقة 2؟</b> VAO رقم 1 اتكتب فيه المربع مرة واحدة قبل اللوب، و VAO رقم 2 اتكتب فيه المثلث مرة واحدة قبل اللوب. جوه اللوب بنشغّل الورقة بس ونرسم (${goLine(155, 1)} و ${goLine(158, 1)}). عشان كده The Cherno بيفضّلها: الكود جوه اللوب أقصر، وأصعب تغلط فيه.</p>
</details><details class="sub"><summary><b>✍️ أوامر الكتابة والمسح في VAO رقم 3</b></summary>
<p>مفيش أمر «امسح» للـ VAO. الكتابة الجديدة هي اللي بتمسح القديمة. الـ VAO جواه <b>خانات</b>، وكل أمر بيكتب في خانة بيشيل اللي كان فيها ويحط الجديد مكانه. الخانتين اللي بيتغيروا في VAO رقم 3:</p>
<ul>
<li><b>خانة المدخل 0:</b> فيها «اقرا من أنهي صندوق، وكام رقم لكل ركن». الأمر اللي بيكتب فيها هو <code>glVertexAttribPointer</code> بس.</li>
<li><b>خانة صندوق الترتيب:</b> الأمر اللي بيكتب فيها هو <code>glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, …)</code>.</li>
</ul>
<p><b>الترتيب في كل لفة، وحالة VAO رقم 3 بعد كل أمر</b> (كلمة «بعده» في العمود = بعد ما الأمر اللي في نفس الصف يتنفذ):</p>
<div class="tw"><table class="mtab wtab"><thead><tr><th>السطر</th><th>الأمر</th><th>بيعمل إيه</th><th>خانة المدخل 0 بعده</th><th>خانة الترتيب بعده</th></tr></thead><tbody>
<tr><td>${goLine(164, 1)}</td><td><code>glBindVertexArray(globalVao)</code></td><td>يشغّل VAO رقم 3</td><td>زي ما هي من اللفة اللي فاتت</td><td>زي ما هي</td></tr>
<tr><td>${goLine(165, 1)}</td><td><code>glBindBuffer(GL_ARRAY_BUFFER, squareBuffer)</code></td><td>يختار الصندوق الحالي، <b>ومبيكتبش في الـ VAO</b></td><td>زي ما هي</td><td>زي ما هي</td></tr>
<tr><td>${goLine(166, 1)}</td><td><code>glVertexAttribPointer(0, 2, …, 8, 0)</code></td><td>✍️ <b>يكتب المربع ويمسح المثلث</b></td><td><code>squareBuffer</code>، رقمين لكل ركن</td><td>زي ما هي</td></tr>
<tr><td>${goLine(167, 1)}</td><td><code>glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, squareIbo)</code></td><td>✍️ يكتب ترتيب المربع</td><td>المربع</td><td><code>squareIbo</code></td></tr>
<tr><td>${goLine(169, 1)}</td><td><code>glDrawElements(…)</code></td><td>🎨 يرسم المربع</td><td>المربع</td><td><code>squareIbo</code></td></tr>
<tr><td>${goLine(170, 1)}</td><td><code>glBindBuffer(GL_ARRAY_BUFFER, triangleBuffer)</code></td><td>يختار صندوق المثلث، ولسه مكتبش حاجة</td><td>لسه المربع</td><td><code>squareIbo</code></td></tr>
<tr><td>${goLine(171, 1)}</td><td><code>glVertexAttribPointer(0, 3, …, 12, 0)</code></td><td>✍️ <b>يكتب المثلث ويمسح المربع</b></td><td><code>triangleBuffer</code>، 3 أرقام لكل ركن</td><td><code>squareIbo</code></td></tr>
<tr><td>${goLine(173, 1)}</td><td><code>glDrawArrays(…)</code></td><td>🎨 يرسم المثلث</td><td>المثلث</td><td><code>squareIbo</code>، بس مش بيتقري</td></tr>
</tbody></table></div>
<p><b>مين الأول؟</b> المربع بيتكتب الأول (${goLine(166, 1)}) ويمسح المثلث اللي فضل من اللفة اللي فاتت، والمثلث بيتكتب بعده (${goLine(171, 1)}) ويمسح المربع. يعني كل شكل بيمسح اللي قبله، وكل ده جوه اللوب.</p>
<p><b>3 حاجات مهمة:</b></p>
<ol>
<li><code>glBindBuffer(GL_ARRAY_BUFFER, …)</code> لوحده <b>مبيكتبش في الـ VAO</b>: بيحدد «الصندوق الحالي» بس. الكتابة الفعلية بتحصل في <code>glVertexAttribPointer</code>، اللي بياخد الصندوق الحالي ويكتبه في الخانة. ودي الغلطة اللي اتمسكت: لو شلت ${goLine(171, 1)}، المدخل 0 هيفضل شايل المربع حتى لو ${goLine(170, 1)} اختار صندوق المثلث.</li>
<li><b>خانة الترتيب مبتتمسحش خالص.</b> <code>squareIbo</code> بيفضل فيها وقت رسم المثلث، بس <code>glDrawArrays</code> مبيقراهاش، فمفيش مشكلة.</li>
<li><b>المسح الحقيقي في البرنامج نوعين، وولا واحد فيهم بيمسح الـ VAO:</b> <code>glClear</code> في أول كل لفة بيمسح <b>الصورة</b> اللي على الشاشة. و <code>glDeleteProgram(shader)</code> في الآخر بيمسح الـ Shaders، والـ VAO والـ Buffers بيتمسحوا لوحدهم لما <code>glfwTerminate</code> يقفل كل حاجة. البرنامج مفيهوش <code>glDeleteVertexArrays</code> ولا <code>glDeleteBuffers</code>.</li>
</ol>
</details><details class="sub"><summary><b>🗂️ يعني إيه «خانة المدخل 0» و«خانة الترتيب»؟</b></summary>
<p>الـ VAO عامل زي ورقة فيها خانات فاضية بنملاها:</p>
<p><b>1. خانات المدخلات (0، 1، 2 …):</b> الـ Shader بتاعنا أول سطر فيه <code>layout(location = 0) in vec4 position;</code>، ومعناه: «أنا محتاج مدخل اسمه <code>position</code>، وهييجي من <b>المدخل رقم 0</b>». <b>خانة المدخل 0</b> في الـ VAO هي اللي بترد عليه وبتقوله: «المدخل رقم 0 اقراه من صندوق كذا، كل ركن فيه كام رقم، وبعد كام بايت ييجي الركن اللي بعده». ورقم 0 هنا هو أول رقم في <code>glVertexAttribPointer(0, …)</code> و <code>glEnableVertexAttribArray(0)</code>.</p>
<p>البرنامج ده مستخدم <b>مدخل واحد بس، رقم 0</b>، للمكان (x, y). لو كان فيه لون لكل ركن، كان هيبقى فيه <b>مدخل رقم 1</b> للون، زي برنامج «Vertex Attributes: مكان + لون» في اليوم 2: <code>glVertexAttribPointer(0, …)</code> للمكان، و <code>glVertexAttribPointer(1, …)</code> للون، والـ Shader فيه <code>location = 0</code> و <code>location = 1</code>. الكارت بيسمح بخانات مدخلات كتير في الـ VAO، عادةً عدد 16 على الأقل، وبتترقّم من 0، واحنا بنستخدم منها اللي محتاجينه بس.</p>
<p><b>2. خانة الترتيب:</b> خانة واحدة بس في كل VAO، ومالهاش رقم. فيها صندوق الترتيب (EBO)، اللي بنكتبه بـ <code>glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, …)</code>.</p>
<p>ورقة VAO رقم 3 بعد ${goLine(167, 1)} شكلها كده:</p>
<div class="tw"><table class="mtab"><thead><tr><th>الخانة</th><th>فيها إيه</th></tr></thead><tbody>
<tr><td>المدخل 0</td><td>اقرا من <code>squareBuffer</code>، عدد 2 أرقام لكل ركن، الركن 8 بايت</td></tr>
<tr><td>المدخل 1</td><td>فاضية، مش مستخدمة</td></tr>
<tr><td>…</td><td>فاضية</td></tr>
<tr><td>الترتيب</td><td><code>squareIbo</code></td></tr>
</tbody></table></div>
</details><details class="sub"><summary><b>📋 خانة الترتيب لوحدها، سطر سطر</b></summary>
<div class="tw"><table class="mtab"><thead><tr><th>السطر</th><th>خانة الترتيب بعده</th><th>ليه</th></tr></thead><tbody>
<tr><td>${goLine(164, 1)}</td><td>زي ما هي (<code>squareIbo</code> من اللفة اللي فاتت)</td><td>لسه محدش كتب فيها</td></tr>
<tr><td>${goLine(165, 1)}</td><td>زي ما هي</td><td>الأمر ده بيختار صندوق الأركان، مالوش دعوة بالترتيب</td></tr>
<tr><td>${goLine(166, 1)}</td><td>زي ما هي</td><td><code>glVertexAttribPointer</code> بيكتب في خانة المدخل 0 بس</td></tr>
<tr><td>${goLine(167, 1)}</td><td><b><code>squareIbo</code></b> ✍️</td><td>ده الأمر الوحيد اللي بيكتب في خانة الترتيب</td></tr>
<tr><td>${goLine(169, 1)}</td><td><code>squareIbo</code></td><td><code>glDrawElements</code> بيقرا منها الترتيب <code>0, 1, 2, 2, 3, 0</code></td></tr>
<tr><td>${goLine(170, 1)} و ${goLine(171, 1)}</td><td><code>squareIbo</code></td><td>الأمرين دول لأركان المثلث، مش للترتيب</td></tr>
<tr><td>${goLine(173, 1)}</td><td><code>squareIbo</code>، بس محدش بيقراها</td><td><code>glDrawArrays</code> مبيستخدمش ترتيب</td></tr>
</tbody></table></div>
<p>الخلاصة: في الطريقة 1، خانة الترتيب <b>بتتكتب مرة واحدة بس في كل لفة</b> (${goLine(167, 1)})، وفيها <code>squareIbo</code> على طول، لأن المثلث مش محتاج ترتيب فمحدش بيغيّرها.</p></details>`};
function linkMap(){
  const BN = bufNames(), VN = vaoNames(), seenLine = new Set(), shapes = {}, vaoUse = {};
  ST.forEach((s, k) => { const t = stepText(s); const m = /^\s*(glDraw\w+)\s*\(/.exec(t); if (!m) return; if (seenLine.has(s.v)) return; seenLine.add(s.v);
    const g = s.gp || {}, va = (g.vaos || {})[g.bvao]; if (!va) return;
    const a = Object.values(va.at || {}).find(x => x.on); if (!a) return;
    const vb = a.buf, eb = /Elements/.test(m[1]) ? va.ebo : 0, src = (BN[vb] || {}).src || `Buffer ${vb}`;
    const key = src + '|' + (eb || 0);
    (shapes[key] = shapes[key] || {src, vb, eb, draws: []}).draws.push({k, vao: g.bvao, fn: m[1]});
    (vaoUse[g.bvao] = vaoUse[g.bvao] || new Set()).add(key); });
  const keys = Object.keys(shapes); if (!keys.length || keys.length > 8) return '';
  const bn = id => `<bdi dir="ltr">Buffer ${id}${BN[id] && BN[id].v ? ` (<code>${esc(BN[id].v)}</code>)` : ''}</bdi>`;
  const vn = id => `<bdi dir="ltr">VAO ${id}${VN[id] ? ` (<code>${esc(VN[id])}</code>)` : ''}</bdi>`;
  const shapeName = sh => { const base = sh.src.replace(/\W.*$/, ''); const ar = SHAPE_AR[base] || SHAPE_AR[base.toLowerCase()]; return ar ? `${ar} <bdi dir="ltr">(<code>${esc(sh.src)}</code>)</bdi>` : `<code>${esc(sh.src)}</code>`; };
  const times = n => n === 1 ? 'مرة واحدة' : n === 2 ? 'مرتين' : `${n} مرات`;
  const rows = keys.map(key => { const sh = shapes[key];
    return `<li><b>${shapeName(sh)}:</b> أركانه في ${bn(sh.vb)}${sh.eb ? `، وترتيبه في ${bn(sh.eb)}` : ''}. بيترسم ${times(sh.draws.length)} في كل لفة: ` +
      sh.draws.map(d => `بـ ${vn(d.vao)} في <a href="#" class="sl" data-go="${d.k}">سطر ${lineOf(ST[d.k].v)}</a>`).join('، و') + '.</li>'; });
  const vrows = Object.keys(vaoUse).sort((a, b) => a - b).map(id => { const ks = [...vaoUse[id]];
    return `<li>${vn(id)}: ` + (ks.length === 1 ? `بتاع ${shapeName(shapes[ks[0]])} بس، ومتسجّل فيه مرة واحدة قبل اللوب.` : `<b>مشترك</b> بين ${ks.map(x => shapeName(shapes[x])).join(' و ')}. نفس الورقة، بس بنكتب فيها من جديد (<code>glBindBuffer</code> + <code>glVertexAttribPointer</code>) قبل كل رسمة.`) + '</li>'; });
  const allV = Object.keys(G0().vaos || {}).filter(id => !vaoUse[id]);
  return `<details class="brk"><summary><b>🔗 مين بتاع مين؟</b></summary><ul>${rows.join('')}</ul>` + (vrows.length > 1 || allV.length ? `<b>وأوراق التعليمات (VAO):</b><ul>${vrows.join('')}${allV.map(id => `<li>${vn(id)}: اتعملت بس مفيش رسمة استخدمتها.</li>`).join('')}</ul>` : '') + (LINK_EXTRA[P.id] ? LINK_EXTRA[P.id]() : '') + '</details>'; }
function G0(){ return (ST[ST.length - 1] || {}).gp || {}; }
function bufNames(){ const R = {};
  ST.forEach(s => { const t = stepText(s), g = s.gp || {};
    let m = /glBindBuffer\s*\(\s*(GL_\w+)\s*,\s*(\w+)\s*\)/.exec(t);
    if (m && g.bbuf){ const id = g.bbuf[/ELEMENT/.test(m[1]) ? 'E' : 'A']; if (id && !/^\d+$/.test(m[2])) (R[id] = R[id] || {}).v = R[id].v || m[2]; }
    m = /glBufferData\s*\(\s*(GL_\w+)\s*,[^,]+,\s*([A-Za-z_][\w.]*)/.exec(t);
    if (m && g.bbuf){ const id = g.bbuf[/ELEMENT/.test(m[1]) ? 'E' : 'A']; if (id && m[2] !== 'nullptr' && m[2] !== 'NULL') (R[id] = R[id] || {}).src = R[id].src || m[2]; } });
  return R; }
function bufBreakdown(G, ids){
  if (!ids.length) return '';
  if (ids.every(id => !G.bufs[id].bytes)){ const F = ST[ST.length - 1].gp; const fin = ids.map(id => [id, (F.bufs[id] || {}).bytes || 0]);
    const eq = t => `<span class="eq" dir="ltr">${t}</span>`;
    return `<details class="brk"><summary><b>ليه 0 بايت؟</b></summary> البرنامج ده بيرسم النقط اللي بتدوسها بالماوس، ووقت الفصل ده لسه محدش داس، فالصندوق (الـ Buffer) اتحجز فاضي. مع كل ضغطة ماوس، الـ CPU بيضيف النقطة (رقمين x و y) ويبعت الأرقام كلها للصندوق تاني بـ <code>glBufferData</code>.<ul>${fin.map(([id, b]) => `<li>في آخر التشغيل Buffer ${id} بقى <b>${b} بايت</b> = ${b / 8} ${b / 8 >= 3 && b / 8 <= 10 ? 'نقاط' : 'نقطة'} × رقمين × 4 بايت ${eq(`${b / 8} × 2 × 4 = ${b}`)}.</li>`).join('')}</ul></details>`; }
  let total = 0;
  const eq = t => `<span class="eq" dir="ltr">${t}</span>`;
  const DUAL = {'رقم':'رقمين','مثلث':'مثلثين','ركن':'ركنين'}; const num = (n, one, many) => n === 1 ? `${one} واحد` : n === 2 ? DUAL[one] : `${n} ${n >= 3 && n <= 10 ? many : one}`;
  const BN = bufNames(); const who = id => BN[id] && BN[id].v ? ` <span class="bwho">— اسمه في الكود <code>${esc(BN[id].v)}</code>${BN[id].src ? ` واتملا من <code>${esc(BN[id].src)}</code>` : ''}</span>` : '';
  const rows = ids.map(id => { const b = G.bufs[id]; const n = (b.bytes || 0) / 4; total += b.bytes || 0;
    if (b.t === 'EBO') return `<li><b>Buffer ${id} = جدول الأرقام (EBO)</b>${who(id)}<b>:</b> فيه <b>${num(n, 'رقم', 'أرقام')}</b> صحيحة (نوعها <code>unsigned int</code>)، وكل رقم بياخد 4 بايت، يعني ${eq(`${n} × 4 = ${b.bytes}`)} بايت.${n % 3 ? '' : ` والـ ${n} دول = ${num(n / 3, 'مثلث', 'مثلثات')}، كل مثلث 3 أركان ${eq(`${n / 3} × 3 = ${n}`)}`}: <code>${(b.vals || []).slice(0, 12).map(x => +x).join(', ')}</code>.</li>`;
    let at = null; for (const v of Object.values(G.vaos)) for (const a of Object.values(v.at)) if (String(a.buf) === String(id) && a.stride) at = at || a;
    const per = at ? (+at.stride) / 4 : 0, corners = per ? n / per : 0;
    return `<li><b>Buffer ${id} = الأركان (VBO)</b>${who(id)}<b>:</b> فيه <b>${num(n, 'رقم', 'أرقام')}</b> (نوعها <code>float</code>)، وكل رقم بياخد 4 بايت، يعني ${eq(`${n} × 4 = ${b.bytes}`)} بايت.${per ? ` الأرقام دي = <b>${num(corners, 'ركن', 'أركان')}</b>، وكل ركن فيه ${num(per, 'رقم', 'أرقام')} ${per === 2 ? '(x و y)' : per === 5 ? '(x و y ثم r و g و b)' : per === 6 ? '(x و y و z ثم r و g و b)' : per === 3 ? '(x و y و z)' : ''}، يعني ${eq(`${corners} × ${per} = ${n}`)}. ومن هنا الـ stride: كل ركن ${eq(`${per} × 4 = ${at.stride}`)} بايت.` : ''} الأرقام نفسها: <code>${(b.vals || []).slice(0, 12).map(x => +(+x).toFixed(3)).join(', ')}</code>.</li>`; });
  return `<details class="brk"><summary><b>ليه ${total} بايت بالظبط؟</b></summary> القاعدة: كل رقم (float أو int) بياخد <b>4 بايت</b> في الذاكرة.<ul>${rows.join('')}</ul>${ids.length > 1 ? `والمجموع: ${eq(`${ids.map(id => G.bufs[id].bytes).join(' + ')} = ${total}`)} بايت.` : ''}</details>`;
}
function chapLines(ch){ // the real source lines this chapter ran, in order (first lap only for the loop)
  const seen = new Set(), rows = [];
  for (let k = ch.from; k <= ch.to; k++){ const s = ST[k];
    if (ch.c === 'loop' && s.lap > 1 && s.d === 1) continue; // lap 1 shows the loop; later laps only add the callback lines
    if (seen.has(s.v)) continue; seen.add(s.v);
    const t = stepText(s); if (t === '{' || t === '}') continue;
    rows.push(`<li><button type="button" data-go="${k}" title="روح للخطوة ${k + 1}"><span class="n">${lineOf(s.v)}</span><code>${esc(t)}</code><span class="d"><b>${esc(s.ti)}</b>${s.ex ? ' — ' + s.ex : ''}${s.dy && s.dy.length ? `<span class="dy">${s.dy.slice(0, 3).join('<br>')}</span>` : ''}</span></button>${whyHtml(k) ? `<div class="wy">${whyHtml(k)}</div>` : ''}</li>`); }
  return rows.length ? `<details class="cl" open><summary>السطور اللي اتنفذت في الفصل ده (${rows.length}) · دوس على سطر تروحله</summary><ol>${rows.join('')}</ol></details>` : '';
}

// every term the story uses, defined before the story uses it (only the ones that actually appear are shown)
const DICT = [
  [/CPU/, 'CPU', 'المعالج اللي في الكمبيوتر. بينفذ الكود بتاعك سطر سطر، ومش هو اللي بيرسم.'],
  [/الرام/, 'الرام', 'ذاكرة الكمبيوتر. فيها المتغيرات بتاعة الكود زي المصفوفات والأرقام.'],
  [/GPU|الكارت/, 'الكارت (GPU)', 'كارت الشاشة. هو اللي بيرسم، وليه ذاكرة لوحده منفصلة عن الرام.'],
  [/الدرايفر/, 'الدرايفر', 'برنامج بيجي مع كارت الشاشة. بيستلم أوامر الـ CPU (الدوال اللي بتبدأ بـ <code>gl</code>) وينفذها على الكارت.'],
  [/نظام التشغيل/, 'نظام التشغيل', 'ويندوز أو لينكس: هو اللي بيدير الشبابيك والماوس والكيبورد.'],
  [/GLFW/, 'GLFW', 'مكتبة بتفتح الشباك وتكلم نظام التشغيل عن الماوس والكيبورد.'],
  [/Context/, 'Context', 'الوصلة بين الشباك والكارت. من غيرها دوال <code>gl</code> مش بتشتغل.'],
  [/GLAD/, 'GLAD', 'مكتبة بتجيب من الدرايفر عناوين دوال OpenGL عشان الكود يقدر يندهها.'],
  [/Buffer|الصندوق/, 'Buffer = «الصندوق»', 'مساحة في ذاكرة الكارت بنحط فيها أرقام (أماكن الأركان مثلاً). في القصة بنسميه «الصندوق»، وفي الماكينة هو الصندوق الخشب.'],
  [/VAO|ورقة التعليمات/, 'VAO = «ورقة التعليمات»', 'ورقة على الكارت بتقول الأرقام اللي في الصندوق مترتبة إزاي (كل ركن كام رقم). في الماكينة هي اليافطة الصفرا.'],
  [/stride/, 'stride', 'المسافة بالبايت من أول ركن لأول الركن اللي بعده جوه الصندوق.'],
  [/EBO|جدول الأرقام/, 'EBO = «جدول الأرقام»', 'صندوق تاني فيه أرقام الأركان بترتيب الرسم، بدل ما نكتب الركن المكرر مرتين.'],
  [/Shader/, 'Shader', 'برنامج صغير بيشتغل على الكارت نفسه، مش على الـ CPU. فيه نوعين: Vertex و Fragment.'],
  [/Vertex/, 'Vertex Shader', 'الـ Shader اللي بيشتغل مرة لكل ركن، وبيحدد الركن ده يتحط فين على الشاشة.'],
  [/Fragment/, 'Fragment Shader', 'الـ Shader اللي بيشتغل مرة لكل بكسل جوه الشكل، وبيحدد لونه.'],
  [/GLSL/, 'GLSL', 'اللغة اللي بيتكتب بيها الـ Shader. شبه C.'],
  [/Compile|Link|تترجم|يترجم/, 'Compile و Link', 'الدرايفر بيترجم نص الـ Shader لأوامر الكارت (Compile)، وبعدين يربط الاتنين في برنامج واحد (Link).'],
  [/Program/, 'Program', 'الـ Vertex والـ Fragment Shader بعد ما اتربطوا مع بعض. ده اللي الكارت بيرسم بيه.'],
  [/uniform/, 'uniform', 'قيمة واحدة (زي اللون) الـ CPU بيبعتها للـ Shader، وبتفضل ثابتة لكل الرسمة.'],
  [/مصفوفة الكاميرا|camMatrix/, 'مصفوفة الكاميرا', 'جدول 4×4 أرقام بيحوّل مكان كل ركن في العالم لمكانه على الشاشة حسب الكاميرا واقفة فين.'],
  [/Rasterizer/, 'Rasterizer', 'جزء ثابت جوه الكارت (مش كود بتكتبه) بيحدد أنهي بكسلات جوه الشكل.'],
  [/بكسل/, 'بكسل', 'نقطة واحدة ملوّنة في الشاشة. الشباك 640 × 480 فيه 307,200 بكسل.'],
  [/Framebuffer/, 'Framebuffer', 'لوحة الرسم: صورة في ذاكرة الكارت بحجم الشباك.'],
  [/Back|Front/, 'Back و Front', 'لوحتين للرسم: الكارت بيرسم في اللي ورا (Back)، والشاشة بتعرض اللي قدام (Front).'],
  [/\bSwap\b|SwapBuffers/, 'Swap', 'تبديل اللوحتين: اللي اترسم ورا يبقى قدام ويظهر على الشاشة.'],
  [/لوب|while|لفة|لفّت/, 'اللوب (while) و«اللفة»', 'جزء من الكود بيتكرر طول ما شرطه صح، وكل مرة بيتكرر فيها اسمها «لفة». في برامج الرسم الشرط = «الشباك لسه مفتوح»، وكل لفة = صورة جديدة على الشاشة.'],
  [/فريم/, 'فريم', 'صورة واحدة من الصور اللي بتتعرض ورا بعض على الشاشة (حوالي 60 في الثانية).'],
  [/glfwPollEvents/, 'glfwPollEvents', 'سطر بيسأل نظام التشغيل: حد داس على الماوس أو الكيبورد أو زرار القفل؟'],
  [/KeyCallback|Backspace|BackSpace/, 'KeyCallback و Backspace', 'دالة الكيبورد: GLFW بيندهها لوحده لما زرار يتداس. هنا بتمسح آخر خط لما الزرار يبقى Backspace (زرار المسح اللي فوق Enter).'],
  [/Callback|MouseButtonCallback/, 'Callback', 'دالة انت كاتبها بس مش انت اللي بتندهها: GLFW بيندهها لوحده لما يحصل حاجة زي ضغطة ماوس.'],
  [/Press|Release/, 'Press و Release', 'الضغطة الواحدة بالماوس = حدثين: الزرار نزل (Press) والزرار طلع (Release).'],
  [/-1\.\.\+1|‎-1/, 'الإحداثيات من ‎-1 لـ +1', 'OpenGL بيقيس الشباك من ‎-1 (أول الشمال أو تحت) لـ +1 (آخر اليمين أو فوق)، مهما كان مقاسه بالبكسل.'],
  [/GL_TRIANGLES/, 'GL_TRIANGLES', 'نوع رسم: كل 3 أركان ورا بعض = مثلث مليان.'],
  [/GL_LINES/, 'GL_LINES', 'نوع رسم: كل ركنين ورا بعض = خط لوحده.'],
  [/GL_POINTS/, 'GL_POINTS', 'نوع رسم: كل ركن = نقطة لوحدها.'],
  [/GL_LINE_STRIP/, 'GL_LINE_STRIP', 'نوع رسم: الأركان كلها متوصلة ورا بعض في خط واحد مكسّر.'],
  [/getline/, 'getline', 'دالة بتقرا سطر واحد من الملف. لما الملف يخلص بترجّع false.'],
  [/Pointer|عنوانهم|عناوين|&amp;x/, 'Pointer و &amp; و *', 'الـ Pointer متغير شايل <b>عنوان</b> متغير تاني في الرام. <code>&amp;x</code> = عنوان x، و <code>*a</code> = القيمة اللي في العنوان a.'],
  [/Reference/, 'Reference', 'اسم تاني لنفس الصندوق في الرام، مش نسخة. بيتكتب <code>int&amp; a</code>.'],
  [/Terminal/, 'الـ Terminal', 'الشباك الأسود اللي البرنامج بيطبع فيه، وانت بتكتب فيه للبرنامج.'],
  [/\bcin\b/, 'cin', 'بيقرا كلمة من الكيبورد (من الـ Terminal) لحد ما تدوس مسافة أو Enter.'],
  [/Sentinel/, 'Sentinel', 'قيمة خاصة بتوقّف اللوب لما تتكتب، هنا Q.'],
  [/push_back|pop_back/, 'push_back و pop_back', '<code>push_back</code> بيضيف عنصر في آخر الـ vector، و <code>pop_back</code> بيمسح آخر عنصر.'],
  [/capacity/, 'size و capacity', 'size = عدد العناصر اللي في الـ vector، و capacity = عدد الأماكن المحجوزة فعلاً. لما يتملي بيحجز مكان أكبر وينقل العناصر.'],
  [/Python/, 'Python', 'لغة برمجة، كودها بيتنفذ سطر سطر ببرنامج اسمه Interpreter، من غير ما يتحول لـ exe الأول.'],
  [/NumPy|np\./, 'NumPy', 'مكتبة Python للمصفوفات: الأرقام جنب بعض في الذاكرة، والحساب على كلها مرة واحدة.'],
  [/np\.dot|النقطي/, 'الضرب النقطي (dot)', 'اضرب الأماكن المتقابلة في المتجهين واجمع: الناتج رقم واحد.'],
  [/np\.cross|الاتجاهي/, 'الضرب الاتجاهي (cross)', 'بيطلّع متجه عمودي على المتجهين، وموجود في 3D بس.'],
  [/vector/, 'vector', 'قايمة في الرام بتكبر لوحدها كل ما تضيف فيها حاجة.'],
  [/مسار التنفيذ/, 'مسار التنفيذ', 'الرسمة اللي في الصفحة بتوريك رقم السطر اللي اتنفذ في كل خطوة، فتشوف الكود نط فين ورجع امتى.'],
  [/الكروت البرتقاني/, 'الكروت البرتقاني', 'الكروت اللي بتظهر على الماكينة في كل خطوة وبتقول إيه اللي اتغير وبسبب أنهي سطر.'],
];
function storyWords(text){ return DICT.filter(([re]) => re.test(text)).map(([, w, d]) => [w, d]); }

// lines where the driver receives a command (read from the source itself; the run tells how many times each one executed)
const DRV_KIND = [
  [/^(glfwMakeContextCurrent)$/, 'الوصلة', 'GLFW بيطلب من نظام التشغيل يشغّل الدرايفر ويوصّله بالشباك (Context).'],
  [/^(gladLoadGLLoader)$/, 'الوصلة', 'GLAD بيسأل الدرايفر عن مكان كل دالة gl جواه.'],
  [/^gl(Viewport|ClearColor|Clear)$/, 'لوحة الرسم', 'الدرايفر بيجهّز أو بيمسح لوحة الرسم (Framebuffer).'],
  [/^gl(Gen|Bind|Delete)(VertexArrays?|Buffers?)$|^gl(BufferData|BufferSubData|VertexAttribPointer|EnableVertexAttribArray)$/, 'الصندوق وورقة التعليمات', 'الدرايفر بيحجز أو بيملا Buffer («الصندوق») أو بيكتب VAO («ورقة التعليمات») في ذاكرة الكارت.'],
  [/^gl(CreateShader|ShaderSource|CompileShader|CreateProgram|AttachShader|LinkProgram|ValidateProgram|DeleteShader|UseProgram|GetShaderiv|GetShaderInfoLog|GetProgramiv|DeleteProgram)$/, 'الـ Shader', 'الدرايفر بيترجم الـ Shader أو بيربطه أو بيختاره للرسم.'],
  [/^gl(GetUniformLocation|Uniform\w+)$/, 'uniform', 'الدرايفر بيدوّر على uniform أو بيحط فيه قيمة.'],
  [/^gl(Draw\w+|PointSize|LineWidth)$/, 'أمر رسم', 'الدرايفر بيخلّي الكارت يرسم فعلاً في اللوحة اللي ورا (Back).'],
  [/^(glfwSwapBuffers)$/, 'عرض الصورة', 'GLFW بيطلب من الدرايفر يبدّل اللوحتين (Swap) فالصورة تظهر.'],
  [/^gl[A-Z]\w*$/, 'أمر تاني', 'أمر OpenGL بيروح للدرايفر.'],
];

// what the driver does for each specific call (A = the arguments as written in that line)
const cnt = (n, one, two, many) => { const x = +n; return isNaN(x) ? `${n} ${many}` : x === 1 ? `${one} واحد` : x === 2 ? two : x <= 10 ? `${x} ${many}` : `${x} ${one}`; };
const DRV_DO = {
  glfwMakeContextCurrent: A => `GLFW بيطلب من نظام التشغيل يشغّل الدرايفر ويربطه بالشباك <code>${A[0]}</code>. من هنا الدرايفر بقى عارف هيرسم فين.`,
  gladLoadGLLoader: A => `GLAD بيسأل الدرايفر عن عنوان كل دالة gl جواه ويحفظها. من غير السطر ده أي سطر gl بعده هيوقّع البرنامج.`,
  glViewport: A => `الدرايفر بيعرف إن الرسم هيتحط في مستطيل من (${A[0]}، ${A[1]}) بعرض ${A[2]} وطول ${A[3]} بكسل، وده اللي بيحوّل الإحداثيات من ‎-1..+1 لبكسلات.`,
  glClearColor: A => `الدرايفر بيحفظ اللون اللي هيمسح بيه اللوحة: أحمر ${A[0]}، أخضر ${A[1]}، أزرق ${A[2]}. لسه مامسحش حاجة.`,
  glClear: A => `الدرايفر بيخلّي الكارت يمسح اللوحة اللي ورا (Back) كلها باللون اللي اتحفظ في glClearColor.`,
  glEnable: A => `الدرايفر بيشغّل خاصية <code>${A[0]}</code> في الكارت.`,
  glPointSize: A => `الدرايفر بيحفظ إن كل نقطة هتترسم بحجم ${A[0]} بكسل.`,
  glGenVertexArrays: A => `الدرايفر بيعمل ${nVao(A[0])} فاضية ويكتب رقمها في <code>${A[1].replace('&', '')}</code>.`,
  glBindVertexArray: A => A[0] === '0' ? `الدرايفر بيشيل ورقة التعليمات من على الترابيزة، فمفيش VAO شغال دلوقتي.` : `الدرايفر بيخلّي <code>${A[0]}</code> هي ورقة التعليمات الشغالة. أي إعداد بعده هيتكتب فيها، وأي رسم بعده هيقرا منها.`,
  glGenBuffers: A => `الدرايفر بيعمل ${nBuf(A[0])} فاضي ويكتب رقمه في <code>${A[1].replace('&', '')}</code>. لسه ماحجزش بايتات.`,
  glBindBuffer: A => A[1] === '0' ? `الدرايفر بيفك أي صندوق من خانة <code>${A[0]}</code>${A[0] === 'GL_ELEMENT_ARRAY_BUFFER' ? '. ولو فيه VAO شغال وقتها، الـ VAO كمان بينسى صندوق الترتيب بتاعه' : ''}.` : `الدرايفر بيخلّي <code>${A[1]}</code> هو الصندوق الشغال في خانة <code>${A[0]}</code>${A[0] === 'GL_ELEMENT_ARRAY_BUFFER' ? ' (جدول الأرقام EBO)' : ' (الأركان VBO)'}. السطر اللي بعده هيحط الأرقام فيه.`,
  glBufferData: A => `الدرايفر بيحجز في ذاكرة الكارت <code>${A[1]}</code> بايت وينسخ فيها الأرقام من <code>${A[2]}</code> اللي في الرام. ده السطر اللي البيانات بتعدّي فيه فعلاً من الرام للكارت.`,
  glVertexAttribPointer: A => `الدرايفر بيكتب في ورقة التعليمات: الخانة رقم ${A[0]} = ${cnt(A[1], 'رقم', 'رقمين', 'أرقام')} من نوع ${A[2] === 'GL_FLOAT' ? 'float' : A[2]}، والمسافة بين كل ركن والتاني (stride) = <code>${A[4]}</code>، وتبدأ من <code>${A[5]}</code>.`,
  glEnableVertexAttribArray: A => `الدرايفر بيشغّل الخانة رقم ${A[0]} في ورقة التعليمات. من غيره الـ Shader مش هيشوف الأرقام دي.`,
  glCreateShader: A => `الدرايفر بيعمل Shader فاضي من نوع ${/VERTEX/.test(A[0]) ? 'Vertex' : /FRAGMENT/.test(A[0]) ? 'Fragment' : A[0]} ويرجّع رقمه.`,
  glShaderSource: A => `الدرايفر بياخد نص الـ GLSL من <code>${A[2].replace('&', '')}</code> ويحفظه جوه الـ Shader <code>${A[0]}</code>. لسه ماترجمش.`,
  glCompileShader: A => `الدرايفر بيترجم نص الـ GLSL اللي في <code>${A[0]}</code> لأوامر يفهمها الكارت (Compile). لو فيه غلط في النص، هنا بيطلع.`,
  glGetShaderiv: A => `الدرايفر بيرد على سؤال: الترجمة نجحت ولا لأ؟ ويكتب الإجابة في <code>${A[2].replace('&', '')}</code>.`,
  glGetShaderInfoLog: A => `الدرايفر بيرجّع رسالة الغلط بتاعة الترجمة عشان تتطبع.`,
  glCreateProgram: A => `الدرايفر بيعمل Program فاضي هيتجمع فيه الـ Vertex والـ Fragment Shader.`,
  glAttachShader: A => `الدرايفر بيضيف الـ Shader <code>${A[1]}</code> ${A[1] === 'vs' ? '(الـ Vertex)' : A[1] === 'fs' ? '(الـ Fragment)' : ''} للـ Program <code>${A[0]}</code>.`,
  glLinkProgram: A => `الدرايفر بيربط الـ Shaders اللي اتضافوا في Program واحد (Link)، ويتأكد إن خرج الـ Vertex راكب على دخل الـ Fragment.`,
  glValidateProgram: A => `الدرايفر بيتأكد إن الـ Program <code>${A[0]}</code> ينفع يشتغل على الكارت بالإعدادات الحالية.`,
  glDeleteShader: A => `الدرايفر بيمسح نسخة الـ Shader <code>${A[0]}</code> ${A[0] === 'vs' ? '(الـ Vertex)' : A[0] === 'fs' ? '(الـ Fragment)' : ''} لوحدها، عشان خلاص بقت جوه الـ Program ومش محتاجينها.`,
  glUseProgram: A => A[0] === '0' ? `الدرايفر بيفك الـ Program: مفيش Shader شغال لحد ما حد يختار واحد تاني.` : `الدرايفر بيخلّي <code>${A[0]}</code> هو الـ Program اللي أي رسم بعده هيترسم بيه.`,
  glGetUniformLocation: A => `الدرايفر بيدوّر جوه الـ Program على uniform اسمه <code>${A[1]}</code> ويرجّع رقم مكانه (أو ‎-1 لو مش موجود).`,
  glUniform2f: A => `الدرايفر بيحط رقمين في الـ uniform اللي مكانه <code>${A[0]}</code>: <code>${A[1]}</code> و <code>${A[2]}</code>.`,
  glGetError: A => `الدرايفر بيرد بآخر غلطة سجّلها ويصفّرها: 0 = مفيش، و 1282 = أمر اترفض (GL_INVALID_OPERATION).`,
  glUniform1f: A => `الدرايفر بيحط رقم واحد (float) في الـ uniform اللي مكانه <code>${A[0]}</code>: <code>${A[1]}</code>.`,
  glUniform4f: A => `الدرايفر بيحط 4 أرقام في الـ uniform اللي مكانه <code>${A[0]}</code>: ${A.slice(1).map(x => `<code>${x}</code>`).join(' و ')}.`,
  glUniformMatrix4fv: A => `الدرايفر بينسخ مصفوفة 4×4 (16 رقم) من الرام للـ uniform اللي مكانه <code>${A[0]}</code>.`,
  glDrawArrays: A => `الدرايفر بيخلّي الكارت يرسم ${cnt(A[2], 'ركن', 'ركنين', 'أركان')} بنوع <code>${A[0]}</code> بداية من الركن رقم ${A[1]}، من الصندوق اللي ورقة التعليمات الشغالة شاورت عليه.`,
  glDrawElements: A => `الدرايفر بيخلّي الكارت يرسم <code>${A[0]}</code> بـ ${cnt(A[1], 'رقم', 'رقمين', 'أرقام')} من جدول الأرقام (EBO)، وكل رقم بيشاور على ركن في الصندوق.`,
  glfwSwapBuffers: A => `GLFW بيطلب من الدرايفر يبدّل اللوحتين (Swap): اللي اترسم ورا (Back) يبقى قدام (Front) ويظهر على الشاشة.`,
  glDeleteVertexArrays: A => `الدرايفر بيمسح ورقة التعليمات (VAO) من الكارت.`,
  glDeleteBuffers: A => `الدرايفر بيفضّي الصندوق (Buffer) ويرجّع البايتات بتاعته للكارت.`,
  glDeleteProgram: A => `الدرايفر بيمسح الـ Program <code>${A[0]}</code> من الكارت قبل ما البرنامج يقفل.`,
};
function callArgs(t, fn){ const i = t.indexOf(fn + '('); if (i < 0) return []; let d = 0, s = i + fn.length + 1, cur = '', out = [];
  for (let k = s; k < t.length; k++){ const c = t[k]; if (c === '(') d++; if (c === ')'){ if (!d) { out.push(cur.trim()); break; } d--; } if (c === ',' && !d){ out.push(cur.trim()); cur = ''; } else cur += c; }
  return out.map(x => x.replace(/^\(GLADloadproc\)/, '')); }

// keep latin / code runs (main(), glClear, x, y) in their own direction inside Arabic sentences
const BIDI_RE = /\([^()\u0600-\u06FF]*[A-Za-z_][^()\u0600-\u06FF]*\)|[A-Za-z_&#][\w:.&*\[\]<>-]*(?:\([^()؀-ۿ]*\))?(?: (?:= )?[A-Za-z0-9_][\w:.&*\[\]<>-]*(?:\([^()؀-ۿ]*\))?)*;?/g;
function fixBidi(root){ if (!root) return; const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {acceptNode: n => n.parentElement.closest('code,bdi,pre,.c,.eq,[dir="ltr"],script,style') ? NodeFilter.FILTER_REJECT : (/[؀-ۿ]/.test(n.parentElement.textContent) && /[A-Za-z_]/.test(n.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT)});
  const nodes = []; while (w.nextNode()) nodes.push(w.currentNode);
  for (const n of nodes){ const t = n.nodeValue; BIDI_RE.lastIndex = 0; if (!BIDI_RE.test(t)) continue; BIDI_RE.lastIndex = 0;
    const frag = document.createDocumentFragment(); let last = 0, m; while ((m = BIDI_RE.exec(t))){ if (m.index > last) frag.appendChild(document.createTextNode(t.slice(last, m.index))); const b = document.createElement('bdi'); b.dir = 'ltr'; b.textContent = m[0]; frag.appendChild(b); last = m.index + m[0].length; }
    if (last < t.length) frag.appendChild(document.createTextNode(t.slice(last))); n.parentNode.replaceChild(frag, n); } }
function driverLines(){
  if (P._drv) return P._drv; const out = [];
  P.files.forEach(f => f.lines.forEach((l, k) => { const t = l.trim(); if (!t || t.startsWith('//')) return;
    const names = [...t.replace(/\/\/.*$/, '').matchAll(/\b(gl[A-Z]\w*|glfwMakeContextCurrent|glfwSwapBuffers|gladLoadGLLoader)\s*\(/g)].map(m => m[1]);
    if (!names.length) return; const n = names[0]; const K = DRV_KIND.find(([re]) => re.test(n));
    const v = f.off + k + 1; const runs = []; ST.forEach((s, j) => { if (s.v === v) runs.push(j); });
    let what = names.map(nm => { const A = callArgs(t, nm); try { return DRV_DO[nm] ? DRV_DO[nm](A.map(x => esc(x.replace(/^&/, '')))) : ''; } catch (e) { return ''; } }).filter(Boolean).join(' ') || K[2];
    out.push({v, file: f.name, ln: k + 1, t, fn: names.join(' و '), kind: K[1], what, runs}); }));
  return P._drv = out;
}
function times(n){ return n === 1 ? 'مرة واحدة' : n === 2 ? 'مرتين' : n <= 10 ? `${n} مرات` : `${n} مرة`; }
// ===== laps: why the render loop exists (real experiments in lapexp/) =====
const LAPIMG = {"swap": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZoAAACsCAMAAAB1jJpVAAAAYFBMVEX//////f35+vf64uLysbGk27hrp3EZpE3qenrjX2ezUty8UsDiT0+pTc/ITIamTMymTMulTMviS0ujS8jgPz/dLy/cJyfcJiaaRr1TJmY5GkYKBQ0DAQQDAQMBAAEAAAB7ToP7AAAEOElEQVR42u3d21LbMBCAYeuQRO4o0+JaFh2gvP9bdiXLp+CWkGJPhvn3ggQfJGc/rSS4SVURBEEQBEEQRInT6bBfZ220K2+vvlPXIfpPehTtpC0jDTpohgTXfTL+QVOvpCtf7qJXF/ltu9C+n1wfYwzNokOb2nKxVlTNZeJvo3GXV1pt7DU0rjLdosfcVr1vzUiujznf+nCSV12OHIYTcvSoKnnXo2xNI6Oz0l1nJD02JbiJaQSnXLs6tDaPfBn48pgpdSZGM1yRQmacxsqxUm8SftaeGrO96EVqpEslkrvItZJo0q9TJ7mtHDY9QGNVud5WtpHnMdvQnBKK1snlmBjkiMknjjrZ6KLRv25NY2KnbUpANya4VE1jbOyMaqLTeaYasjYby+VkuTOP9EV7IQZnzWUvcp/4poHQGpu8ZlUzdjJWTekj27UmNeWvqsQbZyjJukk8ffpL9tNLPngsGofTcYcJTZLq2tbZ2L5Za7TkSHh0n6wVGsl2OTlNaPP2bJfGvVPLo8N8le/JjflcH16v0ZQHkB/9HGtjsFZXG9Kkiatao6kyTZrsTrvQSA58XTdDWt/SyNylZMCv04TqkmbeXmWs7LHKqeGokhlJIOrhnrqvGu3TuzWaPkoflXLi3bmNafRfaQ5pjjvuQmNj01n5Ee07VROuq5p5e3nGzBPV7Kh4GuUGmlI12VScwwpNUMv9vDYu9bsdzXytWaUx+1SNTP/RmDws84cvG9aBZlprxnVl2tKurDWL9rw12nbBLI4mGtNmmtaYca3pq2bWyXytkeobaIyTNkeuTWiqtOYPO7RLGpX2aftUjeQlKCWrfvEwPsR6opl2aHLC591YueLNDq1snmft1W3o2tose1EuhLqvmmmHJnu+vO0aO5k2z9qVLVmZ0KyX+21FXLfH+9//PRCfv1DJn5T+1r8Lodm0YmS281ZBQxAE8Qnx+kXiC34iaKCBBhpooIEGGmiggQYaaKCBBhpooIEGGmiggQYaaKCBBhpooIEGGmiggQYaaKCBBhpooIEGGmiggQYaaKCBBhpooNmS5uV583iBhqr5UjTPv3aIZ2g+TPP79en8bfM4P0lH0HyY5vHHz43jxyM0t9GcH75vGg9naKCBBhpooIEGGmiggQYaaKCBBhpooIEGGmiggQYaaKCBBhpooIEGGmiggQYaaKCBBhpooIEGGmiggQYaaKCBBhpooIEGGmiggQYaaKCBBhpooIEGGmiggQYaaKCBBhpooIEGGmiggQYaaKCBBhpooIEGGmiggQYaaKCBBhpooIEGGmiggQYaaKCB5n0avvzxXmn4ytT7pOGLhu+Y5l4/CDR8qT1VAw000EADDTTQQAMNNNBAAw000EADDTTQQAMNNNBAAw000EADDTTQQAMNNNBAAw000EADDTTQQAMNNNBAAw000EADDTTQXB1/AFfPzpx4EcTQAAAAAElFTkSuQmCC", "clear": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZoAAACsCAMAAAB1jJpVAAAAYFBMVEX////+//77+Pfc8eTF4Mr0vLx7y5k7smf1ilXMZ1B0TEIgp1IWo0pEREXeNTXcJiZEOzQuLi4aFxQHBwcEAgACAgICAgEBAgICAQABAQIBAQEBAQAAAQMAAAIBAAAAAABg0hYlAAAH/0lEQVR42u2d63qCOBCG5SjIQeTQdXFr7v8uNwlBUFEgJBroNz+0DUngmzczE6iP3e1gMBgMBoPBYNuwKHbFT27s99ptP4r3C2ecbPvYUakpPXoDP84cOX+wPjT7O5f68d6iTf5LZ8ZxtPcVoXElV8EbB4fHYMS7oscAGidIj2nqGYPGuXePz6i8Q+PvnGEIEmisSG3YdI6XQePRV9v2AuVootjfR3uXpST67tuixW0P+FHks3gQi/7mSM7i1s6iIo74i5jIuk3UomlfxEy2OC+b0Y8jh49yehf01PM2sTj5AvOO4c4+Hm3qcL7a0yO1lPk6CFkA7OwgTdOAeuNIO9CeTtuDZ2/W59iM3Nlpy4yj4QM9i05Mu3s7MaUnh2bvuHHsWNRxNk9LrKU5QH+PfbHYLYdnsBuaNp+J9i5qxET+rp3oMWqaEbybw3u59LQOjULbcf3ugp56dhMvR8OwMOcyp98ntJS128zfdnAMrRuaXtRYzUGBhjO6oRHHWFfL5qzolI501OzsOHapN2yapWIeLu0B3timKeFu97HU8PYOjRtHfCK7naitNTF1fjeCTy3WBkNIh/muLc57d862ZzexgmJDvUaXd+A1oXJXaygIj+HhPwyh4Qe9YTTtMX7FHJF8mmO+ZmhoTqGgGzRue8BljdRNFk0lzLWPaLr2Do0fN+b0qwg7YlME3Qh+vuY8MQ82Pq6F7/fO2fbsJlaAhnotDMP05rwnNOnuDZr24CAabo6XshQYqkDTj5onNPTdob57QtO130WN9VTgBbSoG9GLGr/paNPl0cZa/5y9qLH6gbqw2KQcQJNyRqLGexc197WGTmmJ+R0rUIOmX2sG0TjRHRpfYBDtIqvR4U1pcP3dYNTcRvRrDXW+6/iOzZ3f1pqnnt3ECtBQtx8958gzD3Merysdmq7WiLritD2aWuN1tYZDuu3QeK2xvZCisenWQQma/g5tIKHRfdp91PDNc9fOneXsmSvtbq/lPtzXOL0R/R0aY+PuI/F7c+C5521iFZvnkC5v6sdU8HDCW/bhwWKzexW2Q6OJKeRRI3o87dAe7muarR2NGDpuYdRI237+/YiqpwOKbzklM+LRNvWRjbs4qUij2Su/45yJhSawoTvQv/OUzlhjSSv0LDxRhcFgsBEjG7ENKgIaoAEaoAEaoAEaoAEaoAEaoAEaoAEaoAEaoAEaoAEaoAGa76G5XC5Ag6gBmulWV+QQhvm/ZQ00JqGhXAipwiDI+C810JiBpuGSJwlFc0iyvG0Cmu+iuXFJ8n/yLCvyLGnoVBXQfBFNw+VEuZx6IHLacGro1EDzDTQPXCiGc1lemkJTMDqFzroDNNO59I9V/djRQwdoxurLExdhDZ227mjYFQCNFBdBp+7TUb0rAJoZeWyod61tVwA08lz6dDTsCoBmEReduwKgmVlfXtYd5bsCoFHBRcuuAGjk85jmXcEfR6OSi+pdwR9FczlfdHB5uSu4ns9XoJmq6B8l9WXiruAXUTMRzTnPc41cnncFZZ4XQDOu6EyKIAiU57F3u4JDEBxICTTjaHKKRjeXu10B0MyJmoJUn/n4RV2VBGjm1Jryk1dXoNbgc2jbuK/5oOG+BlEDNEADNEADNEADNEADNEADNEADNEADNEADNEADNEADNEADNEADNEADNEADNEADNEADNEADNEADNEADNEADNEADNEADNEADNEADNEADNEADNEDzXSvLcmNoFitC1CBq3tmVlFmWleS6GTQqFBkhpPlqkpy+bwWNCkVmCKmLraFRoMgIIT8kD8Ow2BAaFYpM0FGRPPlvU9sAJYoM0VFfF341iVFo1CgyREd93VDUKFJkiI4t3deoUrQRHQahUabIBB2behqgTtFGdBiDRqGiRaOX/t9dVbGvDo1JiraQlc2JGqWKFjyLIMWyG16VOpSgMUzRAiH8MVFRn5foULZelaAxS5H80J/mm6wJqQ3QoQSNYYoWpdWMWlJIKVEa+2rQmKZIdmBNTgn/Vuk8kVlmqnWo+F9ppimSlUGSjP/5uyJFQhVVX9axGI2BiiRDv6Arq/lO/lpimSnOygrQmKhIboUVSd4tq9nLTIOOhWiMVCRZ7+4q5cxlpj72l6IxU9H8BVbxclk9XFs1eZlp0bEEjamKJMplljwvp+nLTI+OBWiMVSSRlE+DlzsxP+vIyovQmKto/kYmf3Gxk5aZLh3SaAxWtKxcDi6z+uOxL4/GZEXzdJyS6t11ji0zfTok0RitaFa5PGVjZfFtftaoQwqN4YoUlMupy0xbVpZEY7qiOUk5n7TNf7XMtOqQQGO8IuU6Xi0znbEvg8Z8RVNjf6RckrFbac06ZqNZgaKp5XLek9inZaZbx0w0q1A06aqqKeXyXX7Wm5Vno1mHIrVJ+cUy069jFpqVKNKlo1tml+uP7tifh2YtiqaUy0LyIybNMvv9/YCOGWhWo2j0UjLpD/+IZXZIw0N9JoagWZGiCeWyWjA/VXAIggMpDUGzJkVjTzLyRToIKX9MQrMqRSPlsliog1xInmU5uRiBZl2KXrSfy/K8oFx+3kbRrE/R60O/SUZU6OA+ISZEzcoUDZ+bZIfDof3I3BaiZo2KhivdhzYhn0OzRkVvhNSbQ1OvHw0P/4yct4NmjYrIRuzvfFXdZzYhH988E0QNogZogAZogAZogAZogAZogAZogAZogAZogAZogAZogAZogAZogAZogAZogAZogAZogOa9/Q/oSlFI8rfGfAAAAABJRU5ErkJggg==", "poll": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZoAAACsCAMAAAB1jJpVAAAAYFBMVEX////+//799/fr9/D2yMi348eT1KtXvX3xjnTqcWWuVkk3i1Yhp1IWo0rgPz/dLi7cJiZOQjc4NjUgHx8NCggEAgECAgIBAgICAQABAQIBAQEBAQAAAQMAAAIBAAAAAADvLvl7AAAHi0lEQVR42u3di5aiOBAG4OZOOICAwri4Le//llsJgXDTDkpsdvhzzowSMGh9VFLYfWa+vtDQ0NDQ0NDQ0P6+FieefOYlwaDfCeLRtvZgasCv0XPegsR5462mmbvwVPuVNjtlTOPAlWN/giYYxdFPAou6/AcvI7k49tfSeOu1J3FjWfgDjTxiThNmqT3pzbJTGtpLNHxflqXP3s7SiczQOEk8vsCDr8c0Fu1x5nunFNNtK34rbVQ8XqFh05xJqcNNR4cPaJjmW1kVaz8QF7Tj8wvbkT1e+xB41CvyIUnEVd9HzxdXdNfPH5NY/CUHsvqBxOVPMfaT2JKsfFBPZc1wm46iQ+VbeZyGy82lC9fOMvuLR5BiJi7mE49cyE4pn6XCtL3wMwooHdkfId4WHRNmMtqM72Dj8ZjIpcEoM5qQP7r0ivYQS51anqh7pR5N7PDIiQtbTEu8R+wIaJs6Ww2rfexpuqjJfpU1KkPkQIpG5gAdETiO39MMt4WMI7b9zl+/ORQUCoxrqwDLrEltETAKlE3hs3qawcVs8Z2se6XImsl4kkaNMqNxs5PNfeRYoTp1eyK6dmzbDbWzhkKReBQ9WzwRPXKH6OwQRJx6GjX5+K1KRyNeIyzi/pq3Y8ElabzuiaQZbPPrgR8Q+57zymJDcQrTNOTZM6YJBYSIkYjzAo3Y6Y5oJuPJCU2NMllrhIRLLK4gcrt8Uyei/tC1VywediIuV7pwErUw8wePd1LALZqZaLKa0ah+ReMnbXOGSwcvA3oav1umJM1gOxGalpgf/RdowixMGUtDGdbhWtPS0Nz1mKbbqWjG48kyYHzgeK1xM0aOlpu1ze1P3Z7IYpJwDc0wa2Y09OhY46yRGdL1D7OmW1Imq3of5ydZE8hMczy/nQNX0lBYspAmnTZcCzTd9X6iP+7PWTMejw0OfEBjU8UtEutkqUpheA3QdMZfvobGitVas0jjxCMaETXVL2no5WKtcbxgRON7ttdvPltrPJ4tXuDYQnhtGcCDIAAyu6Nh1iA+cpVI+Soh1xV5xPJaMxmvC/9glFmFxsTBYizbZSMaOpFL05li06QZVmgLExrNR8GIRhTPql/81d53ioEC52s2oamtJxUat7G89vAXiueUPjfFJZUebnrKhvHpays3ldWYPGJWocnieTReF/6lCq2r9MiRdYcwd3BqcSLLZacTM32PGkxuQgy09245X2qu7myz5/aBuAXv3nGurCFc2zF+z472ShOTkGshEGhoaGjvtOYvaX/hJwINaEADGtCABjSgAQ1oQAMa0IAGNKABDWhAAxrQgOb/Q3O73UCDrAGNfqurJoqi8z9lDZo90ZBL01QpY7nYqEGzD5rW5ZznRBPlxaXrAs3v0vQu+fnPuSgulyJvdaoKNL9IM3AZQAx0atD8Bs3EhRiuZXlrF5pex9i6Axp9l+G+yrwOaFa7yDbVAc0HaDRcpE49XndAY5RG20UeXRurCkDzusuiznbrDmjecjFZFYDmXRdjVQFotnAxUhWAZiOX7auCg9Ns6bJ1VXBQmtv1ZsLlYVVwv17voNH9IH/MuCxXBd/IGk2a6+VyMegyrwpKfkLQ/AzTXNI0NesyWXeilEVNCRodGsZMu4x0IgYa/ayhWeYzv35RV2WTg2bFWlN+8k1dsNY0+D20v+K+5oMN9zXIGtCABjSgAQ1oQAMa0IAGNKABDWhAAxrQgAY0oAENaEADGtCABjSgAQ1oQAMa0IAGNKABDWhAAxrQgAY0oAENaEADGtCABjSgAQ1oQLNtK8sSNMga0Oi3e1Oei3PZ3EGzN5prc2GMXegRNHujqUGzU5qyOUdpBJr90VTNufgXZcAOaUgmr+9v/mMroDElU9+RNbujaWVwX7M/mo1kQGNGBt8G7JBmMxnQTNq7/5PwVrMZaPa6zoBm0q7N5b1b+C1lQDOiab/4qq/vyGz3QUCjWim+Li6apt6BDGgmoc2LIs8vL9lsOpuBZthqCq34d7LP+fmFxNlaBjQKpikK8QP9qil54lS/LAOaPrIXypX2f3+oX0icjdcZ0AxyRsioQJfFqsQxIAOaPrKjtX9l4mw/m4GmdWhlqkm0K+3EMSIDmr4AqOfdmoljRgY0cpmpF0OuVaqZWGdAo0qzR/n0c+KYkjk8zawAmCVO8fzLAUOzGWgqWmaqZ5H/KXHMyRyb5kEBsGLFMShzaJqagl78XIE9SRxj68zBaZ4VAIsrTvVRmQPTVCIXKs38Wkock7PZkWnqpsgr/W8wF74cMCxzVBqtAuB54piWOShN3VQ6BcCzUs3sOnNYmjXLzIPEMS9zSJqlL5q1E4evOLe78dnsmDS8AChf/KWZNnG+vz8gczya9QXAPHGiNIrqawOaTWmoACCZ6o3xySRiLGpK0GxKU2t/A/C4lRVotqd5vQAYtFtzLopzcwPNVjTXsrw+/+HM3j7IkbLm+60CYKIMmo1ork0RRf0vASJrdkRTfqisAs2LNDVodjqhFc0VNPv9NgA0Oy2eQYOsAQ1oQAMa0IAGNKABDWhAAxrQgAY0oAENaEADGtCABjSgAQ1oQAMa0IAGNKA5HM1/ikh+POVg1EgAAAAASUVORK5CYII="};
function lapLineInfo(t, ph){
  const pre = ST.filter(s => !s.lap).map(s => stepText(s)).join('\n');
  const vaoOff = /glBindVertexArray\(0\)/.test(pre), progOff = /glUseProgram\(0\)/.test(pre);
  if (/glBindVertexArray/.test(t) && ph.filter(p => /glBindVertexArray/.test(p[1])).length > 1) return ['بيختار الـ VAO بتاع الرسمة الجاية.', 'الرسمة هتتقري من الـ VAO اللي كان مربوط قبلها (أركان رسمة تانية و Layout تاني)، فالشكل يبوظ.'];
  if (/glBindVertexArray/.test(t) && vaoOff) return ['بيرجّع الـ VAO قبل الرسم: الصندوق والـ Layout وصندوق الترتيب في سطر واحد.', 'إحنا فكّينا الـ VAO قبل اللوب، فالرسم مالوش أركان: شاشة سودا و <code>glGetError</code> = 1282 كل فريم (جربناها في ملف اليوم 7).'];
  if (/glUseProgram/.test(t) && progOff) return ['بيختار الـ Shader قبل الرسم.', 'إحنا فكّيناه بـ <code>glUseProgram(0)</code> قبل اللوب، فالرسم مالوش Shader يرسم بيه.'];
  if (/glBindBuffer\(GL_ELEMENT_ARRAY_BUFFER/.test(t)) return ['بيربط صندوق الترتيب (Index Buffer).', /globalVao|squareIbo/.test(t) ? 'في الطريقة 1 الـ VAO الواحد ممكن يكون فاكر صندوق ترتيب تاني، فالأحسن يتربط قبل الرسمة.' : 'الـ VAO فاكره من وقت الإعداد، فالصورة نفسها (جربناها في ملف اليوم 7). The Cherno كاتبه للتأكيد.'];
  if (/glBindBuffer\(GL_ARRAY_BUFFER/.test(t)) return ['بيختار صندوق الأركان اللي الـ Layout الجاي هيقرا منه.', 'الـ <code>glVertexAttribPointer</code> اللي بعده هيربط الصندوق القديم: الأرقام تتقري غلط والشكل يبوظ (جربناها في ملف اليوم 7).'];
  if (/glVertexAttribPointer/.test(t)) return ['بيكتب الـ Layout من جديد في الـ VAO الواحد (الطريقة 1).', 'الرسمة هتتقري بالـ Layout والصندوق بتوع الرسمة اللي قبلها: المثلث طلع نص مربع (جربناها في ملف اليوم 7).'];
  if (/glUniform2f/.test(t)) return ['بيبعت الزحزحة (<code>u_Offset</code>) قبل الرسم.', 'الرسمتين هيترسموا في نفس المكان فوق بعض.'];
  if (/glGetError/.test(t)) return ['بيسأل الكارت: رفض أي أمر؟', 'مفيش طباعة، والرسمة زي ما هي.'];
  const nU = ph.filter(p => /glUniform/.test(p[1])).length, nB = ph.filter(p => /glBindVertexArray/.test(p[1])).length;
  if (/^while\b/.test(t)) return ['بيسأل: حد قفل الشباك؟ لو لأ، لفة كمان.', 'البرنامج يكمّل لـ <code>return 0</code> ويخلص في أقل من ثانية (التجربة الأولى تحت).'];
  if (/glClearColor/.test(t)) return ['بيختار لون المسح.', 'يفضل اللون اللي اتحدد آخر مرة. لو اتحدد قبل اللوب، الشكل مش هيفرق.'];
  if (/glClear\b/.test(t)) return ['بيمسح اللوحة الخلفية قبل ما نرسم عليها.', 'الرسمة القديمة تفضل تحت الجديدة: أي حاجة اتمسحت أو اتحركت تسيب أثر (تجربة <code>glClear</code> تحت).'];
  if (/glUniform/.test(t)) { const lit = !/\(\s*\w+\s*,[^)]*[A-Za-z_]\w*\s*[,)]/.test(t.replace(/\d+\.\d*f/g, '1')) ;
    return ['بيبعت قيمة للـ Shader (uniform) قبل الرسم.', nU > 1 ? 'كل رسمة ليها لونها، فلو اتشال الرسمتين ياخدوا نفس اللون.' : lit ? 'القيمة هنا ثابتة، فلو اتبعتت مرة واحدة قبل اللوب الشكل هيبقى زي ما هو. اتكتبت جوه اللوب عشان تبقى جنب الرسم.' : 'الكارت يفضل بالقيمة القديمة، فالحركة تقف.']; }
  if (/glDraw/.test(t)) return ['بيقول للكارت: ارسم دلوقتي.', 'مفيش رسم: الشباك يبقى بلون المسح بس.'];
  if (/glBindVertexArray/.test(t)) return ['بيختار أنهي صندوق (VAO) هيترسم منه.', nB > 1 ? 'الرسمتين يترسموا من نفس الصندوق.' : 'لو الصندوق اتربط قبل اللوب ومحدش غيّره، الشكل مش هيفرق.'];
  if (/glUseProgram|\.Activate\(/.test(t)) return ['بيختار برنامج الـ Shader.', 'لو اتختار قبل اللوب ومحدش غيّره، الشكل مش هيفرق.'];
  if (/^for\b/.test(t)) return ['بيلف على كل الخطوط اللي اترسمت.', 'ولا خط يترسم (النقط بس).'];
  if (/glfwSwapBuffers/.test(t)) return ['بيقلب اللوحة الخلفية اللي رسمنا عليها لقدام، فتبان على الشاشة.', 'الشباك يفضل أسود مع إن الرسم بيحصل (تجربة <code>glfwSwapBuffers</code> تحت).'];
  if (/glfwPollEvents/.test(t)) return ['بيسأل نظام التشغيل: حد داس على الماوس أو الكيبورد أو زرار القفل؟ وينده الدوال بتاعتك.', 'ولا دوسة توصل، وزرار القفل ✕ مش بيقفل (تجربتين تحت).'];
  if (/glfwGetTime/.test(t)) return ['بيقرا الوقت من أول التشغيل بالثواني.', 'الوقت ميتغيرش، فالألوان تقف.'];
  if (/^(else\s+)?if\s*\(\s*r\b|\br\s*\+=/.test(t)) return ['بيحسب قيمة <code>r</code> الجديدة على الـ CPU.', 'القيمة متتغيرش، فاللون يقف.'];
  if (/std::cout|frame\s*(%|==)|^frame\+\+/.test(t)) return ['بيعد الفريمات ويطبع كل شوية في الـ Terminal.', 'مفيش طباعة، والرسمة زي ما هي.'];
  if (/\.Inputs\(/.test(t)) return ['بيقرا W A S D والماوس ويحرك الكاميرا.', 'الكاميرا متتحركش مهما دوست.'];
  if (/\.Matrix\(/.test(t)) return ['بيحسب مصفوفة الكاميرا ويبعتها للـ Shader.', 'الكارت يفضل بالمصفوفة القديمة، فحتى لو الكاميرا اتحركت الصورة متتغيرش.'];
  if (/DrawScene\(/.test(t)) return ['دالة بتاعتك جواها المسح والألوان والرسم.', 'مفيش مسح ولا رسم.'];
  if (/count\s*=/.test(t)) return ['بيعد النقط اللي في الـ vector.', 'الرسم مش هيعرف يرسم كام نقطة.'];
  return ['سطر على الـ CPU بيتنفذ كل لفة.', 'يتشال أثره بس.'];
}

function lapInfo(l){
  const isLoop = s => { const t = stepText(s); return /^(for|while)\b/.test(t) && !/glfwWindowShouldClose/.test(t); };
  const evName = e => e.btn === 'key' ? (e.key === 'BackSpace' ? 'Backspace' : 'زرار ' + e.key) : e.btn === 'right' ? 'دوسة يمين' : `دوسة شمال عند (${e.x}, ${e.y})`;
  const why = t => {
    if (/polylines/.test(t)) {
      const ev = ST.filter(s => s.ev && s.lap < l).map(s => s.ev), R = ev.filter(e => e.btn === 'right').length, B = ev.filter(e => e.btn === 'key' && e.key === 'BackSpace').length;
      return `عدد الخطوط في <code>polylines</code> وقت الرسم = 1 (الخط المفتوح) + ${R} دوسة يمين${B ? ` − ${B} Backspace` : ''} قبل اللفة دي = <b>${1 + R - B}</b>.`;
    }
    if (/last\.count \* 2/.test(t)) return 'عدد أرقام آخر خط = عدد نقطه × 2 (x و y لكل نقطة). اللوب دي بتشتغل بس في اللفة اللي اتداس فيها Backspace، جوه دالة الكيبورد.';
    return 'اللوب بتفضل تلف لحد ما شرطها يبقى غلط.';
  };
  const ks = ST.map((s, k) => [s, k]).filter(([s]) => s.lap === l); if (!ks.length) return null;
  const loops = new Map();
  ks.forEach(([s]) => { if (isLoop(s)) { const o = loops.get(s.v) || {n: 0, t: stepText(s), fn: s.fn}; o.n++; loops.set(s.v, o); } });
  const ev = ks.filter(([s]) => s.ev).map(([s]) => evName(s.ev));
  const loopsHtml = [...loops.entries()].map(([v, o]) => `<div class="ilp">لوب <code>${esc(o.t)}</code> (سطر ${lineOf(v)}${o.fn && o.fn !== 'main' ? `، جوه دالة <code>${esc(o.fn)}</code>` : ''}): لفّت <b>${times(Math.max(0, o.n - 1))}</b>. <span class="ilw">السبب: ${why(o.t)}</span></div>`).join('') || '<div class="ilp">مفيش لوب جوه اللفة دي: كل سطر فيها اتنفذ مرة واحدة.</div>';
  const evHtml = ev.length ? `<div class="ile">في آخر اللفة (جوه <code>glfwPollEvents</code>) وصلت: ${ev.join('، ')}. أثرها هيبان من اللفة ${l + 1}.</div>` : '';
  // executed lines in order, consecutive repeats merged
  const seq = []; ks.forEach(([s, k]) => { const L = seq[seq.length - 1]; if (L && L.v === s.v && L.last === k - 1) { L.n++; L.last = k; } else seq.push({v: s.v, n: 1, k, last: k, fn: s.fn, t: stepText(s)}); });
  const linesHtml = `<ol class="ilseq">${seq.map(x => `<li><button type="button" class="ilgo" data-go="${x.k}">سطر ${lineOf(x.v)}</button> <code>${esc(x.t)}</code>${x.fn && x.fn !== 'main' ? ` <small>(جوه دالة <code>${esc(x.fn)}</code>)</small>` : ''}${x.n > 1 ? ` <b>× ${x.n}</b>` : ''}</li>`).join('')}</ol>`;
  return {l, first: ks[0][1], steps: ks.length, loopsHtml, evHtml, linesHtml, nLoops: loops.size};
}
function innerLoopsHtml(){
  const L = P.laps; if (!L) return '';
  const usesPoly = ST.some(s => /for \(const Polyline& line : polylines\)/.test(stepText(s)));
  const rows = [];
  for (let l = 1; l <= L; l++){ const x = lapInfo(l); if (!x) continue;
    rows.push(`<li><button type="button" class="ilgo" data-go="${x.first}">اللفة ${l}</button> <small>${x.steps} خطوة</small>${x.loopsHtml}${x.evHtml}</li>`); }
  const intro = usesPoly
    ? '<p>اللوب اللي جوه اللفة هنا هي <code>for (const Polyline& line : polylines)</code>: بتلف مرة لكل خط في القايمة، وفي كل مرة بترسم الخط ده. فعددها مش ثابت: <b>بيساوي عدد الخطوط اللي في <code>polylines</code> وقتها</b>. القايمة بتبدأ بخط واحد مفتوح (فاضي)، ودوسة يمين بتقفله وتفتح خط جديد (+1)، و Backspace بيمسح آخر خط (‎−1)، ودوسة شمال بتزوّد نقطة بس (العدد مايتغيرش). والعدد مش بيتأثر بالوقت: لو سبت الشباك دقيقة من غير ما تدوس، كل اللفات بنفس العدد.</p><p>العدد ده متعدّ من التشغيل الحقيقي: سطر الـ for بيتسأل مرة زيادة في الآخر (لما الشرط يبقى غلط)، فعدد اللفات = مرات السؤال − 1، ونفس عدد مرات الرسم بـ <code>GL_LINE_STRIP</code> في اللفة.</p>'
    : '<p>البرنامج ده <b>مافيهوش لوب جوه اللفة</b>: كل سطر من سطور اللفة بيتنفذ مرة واحدة بس في كل لفة، والعدد هو هو في كل اللفات. اللي بيتكرر هو اللفة كلها (الـ <code>while</code>).</p>';
  return intro + `<ol class="ill">${rows.join('')}</ol>`;
}
let LAPNOW = -1;
function syncLapNow(force){
  const box = $('lapNow'); if (!box || !P) return;
  const s = ST[i]; const l = s && s.lap ? s.lap : 0;
  if (!l || !P.laps){ box.hidden = true; LAPNOW = -1; return; }
  box.hidden = false;
  if (l === LAPNOW && !force) return;
  LAPNOW = l; const x = lapInfo(l); if (!x) { box.hidden = true; return; }
  $('lapNowSum').innerHTML = `🔁 جوه اللفة ${l} من ${P.laps}: إيه اللي حصل فيها؟`;
  $('lapNowBody').innerHTML = `<p class="ilhead">اللفة دي فيها <b>${x.steps} خطوة</b>${x.nLoops ? ` و ${x.nLoops === 1 ? 'لوب واحدة جواها' : x.nLoops + ' لوب جواها'}` : ''}.</p>`
    + `<h6>🔂 اللوب اللي جوه اللفة دي</h6>${x.loopsHtml}`
    + (x.evHtml ? `<h6>🖱 الدوسات</h6>${x.evHtml}` : `<h6>🖱 الدوسات</h6><div class="ile">مفيش دوسة وصلت في اللفة دي.</div>`)
    + `<details class="lw"><summary>📋 السطور اللي اتنفذت في اللفة ${l} بالترتيب</summary>${x.linesHtml}</details>`
    + `<p class="ilnav">${l > 1 ? `<button type="button" class="ilgo" data-go="${lapInfo(l - 1).first}">→ اللفة ${l - 1}</button>` : ''} ${l < P.laps && lapInfo(l + 1) ? `<button type="button" class="ilgo" data-go="${lapInfo(l + 1).first}">اللفة ${l + 1} ←</button>` : ''}</p>`;
  fixBidi($('lapNowBody'));
  $('lapNowBody').querySelectorAll('[data-go]').forEach(b => b.onclick = () => { play(false); go(+b.dataset.go); });
}
function lapWhyHtml(){
  const ph = P.phases; if (!ph.length) return '';
  const S = PSTORY[P.id] || {}, ev = ST.filter(s => s.ev), keys = ev.filter(s => s.ev.btn === 'key').length, cl = ev.length - keys;
  const hasDyn = ph.some(p => /glfwGetTime|\br\s*\+=|\.Inputs\(/.test(p[1])) || ev.length;
  const sub = (t, b, open) => `<details class="lw"${open ? ' open' : ''}><summary>${t}</summary>${b}</details>`;
  const lines = `<ol class="lwl">${ph.map(p => { const [a, b] = lapLineInfo(p[1], ph); return `<li><span class="lwn">سطر ${lineOf(p[0])}</span> <code>${esc(p[1])}</code><div>شغلته: ${a}</div><div class="lwx">لو شلناه: ${b}</div></li>`; }).join('')}</ol>`;
  const fig = (k, cap) => `<figure class="lwf"><img src="${LAPIMG[k]}" alt="${cap}"><figcaption>${cap}</figcaption></figure>`;
  return sub('١. يعني إيه «لفة»؟', `<p>اللفة = مرة واحدة الـ CPU بيمشي فيها على كل السطور اللي جوه <code>while (!glfwWindowShouldClose(window))</code> من أولها لآخرها، وبعدين يرجع يسأل الشرط تاني. في البرنامج ده اللفة الواحدة فيها ${ph.length} سطور، بالترتيب ده:</p>${lines}`, true)
   + sub('٢. فايدتها في البرنامج ده', `<p>${S.loop || STATIC_LOOP}</p><p>${hasDyn ? 'يعني هنا كل لفة بتطلّع صورة مختلفة شوية عن اللي قبلها.' : 'يعني هنا كل اللفات بتطلّع نفس الصورة بالظبط، ومع ذلك لازم تتكرر (السبب في ٤).'}${ev.length ? ` وكمان الدوسات: ${cl ? `الماوس وصل <b>${times(cl)}</b>` : ''}${cl && keys ? ' و' : ''}${keys ? `الكيبورد وصل <b>${times(keys)}</b>` : ''}، وكل دوسة وصلت جوه لفة من <code>glfwPollEvents</code>، واللفة اللي بعدها رسمت النتيجة.` : ''}</p>`)
   + sub('٣. مطلوبة ولا لأ؟', `<p><b>أيوه، إجبارية</b> في أي برنامج بيفتح شباك ويرسم فيه، حتى لو الصورة ثابتة. اللي مش مطلوب هو عدد معين من اللفات: اللوب مالهاش عدد، بتفضل تلف لحد ما حد يقفل الشباك (الشرط <code>glfwWindowShouldClose</code> يبقى true).</p><p>الحاجة الوحيدة اللي بتتغير من برنامج لبرنامج هي <b>اللي جوه</b> اللفة: لازم يبقى فيها رسم (أو دالة بترسم)، و <code>glfwSwapBuffers</code>، و <code>glfwPollEvents</code>. باقي السطور حسب البرنامج.</p>`)
   + sub('٤. وجودها سببه إيه؟', `<ol class="lwr"><li><b>الشباك يفضل مفتوح.</b> الكود بيتنفذ من فوق لتحت. من غير لوب، الـ CPU يوصل لـ <code>glfwTerminate</code> و <code>return 0</code> في جزء من الثانية، والشباك يتقفل.</li><li><b>الشاشة مش بتفتكر الصورة.</b> الشاشة بتتحدث حوالي 60 مرة في الثانية، والكارت بيعرض اللي في اللوحة الأمامية. أي تغيير (لون، حركة، خط جديد) محتاج رسم جديد من الأول: امسح ← ارسم ← اقلب اللوحتين.</li><li><b>الدوسات مش بتوصل لوحدها.</b> نظام التشغيل بيحط كل دوسة في طابور (Queue) مستني. <code>glfwPollEvents</code> هي اللي بتفضّي الطابور وتنده دوالك. ولو برنامج مسألش فترة، نظام التشغيل يعتبره «مش بيرد».</li>${hasDyn ? '<li><b>الحركة.</b> كل لفة بنحسب قيمة جديدة (وقت أو لون أو مكان كاميرا) ونبعتها قبل الرسم، فالصور ورا بعض بتبان كأنها بتتحرك.</li>' : ''}</ol>`)
   + sub('٥. من غيرها إيه اللي هيحصل؟ (تجارب حقيقية)', `<p>شلنا حتة من الكود في برنامجين من اليوم 6 (<code>animated_color.cpp</code> و <code>refactored.cpp</code>) وشغّلناهم فعلاً على نفس الجهاز اللي سجّل البنش ده. ده اللي حصل:</p>
     <div class="lwe"><h6>تجربة 1: شلنا الـ <code>while</code> كلها (السطور اللي جواها تتنفذ مرة واحدة)</h6><p>اتطبع سطر واحد بس <code>frame 0: r = 0.05</code> بدل ما يفضل يطبع، والبرنامج كله خلص في أقل من ثانية (بين 0.14 و 0.77 ثانية في كذا تشغيل). الشباك فضل ظاهر حوالي عُشر ثانية واتقفل لوحده. يعني فتح ورسم صورة واحدة وقفل قبل ما العين تلحق.</p></div>
     <div class="lwe"><h6>تجربة 2: شلنا <code>glfwSwapBuffers</code> بس</h6>${fig('swap', 'شمال: البرنامج العادي. يمين: من غير glfwSwapBuffers')}<p>الشباك فضل <b>أسود</b> طول الوقت، مع إن الرسم بيحصل (الـ Terminal كمّل يطبع <code>frame 0</code> و <code>frame 10</code> وهكذا). السبب: الرسم بيحصل على اللوحة الخلفية، ومحدش بيقلبها لقدام. وكمان اللوب بقت تلف أسرع 6.5 مرة (في ثانيتين: 24470 لفة بدل 3730) لأن مفيش تبديل لوحات بيتعمل.</p></div>
     <div class="lwe"><h6>تجربة 3: شلنا <code>glfwPollEvents</code> من <code>animated_color.cpp</code></h6><p>اللون فضل يتحرك عادي. بس لما بعتنا للشباك رسالة «اقفل» (نفس اللي زرار ✕ بيبعته)، البرنامج <b>فضل شغال</b> بعد 3 ثواني ولازم قفلناه بالعافية. البرنامج العادي قفل بعد 0.02 ثانية. السبب: الرسالة قعدت في الطابور ومحدش قراها، فـ <code>glfwWindowShouldClose</code> فضلت false. على ويندوز الشباك كان هيكتب «Not Responding».</p></div>
     <div class="lwe"><h6>تجربة 4: شلنا <code>glfwPollEvents</code> من <code>refactored.cpp</code></h6>${fig('poll', 'شمال: العادي بعد 9 دوسات. يمين: من غير glfwPollEvents')}<p>بعتنا نفس الـ 17 دوسة (ماوس و Backspace): ولا واحدة وصلت. <code>MouseButtonCallback</code> و <code>KeyCallback</code> ماتندهوش خالص، الـ Terminal فاضي، والشاشة سودا.</p></div>
     <div class="lwe"><h6>تجربة 5: شلنا <code>glClear</code> من <code>DrawScene</code> في <code>refactored.cpp</code></h6>${fig('clear', 'شمال: العادي بعد Backspace. يمين: من غير glClear')}<p>لحد أول Backspace الصورة كانت زي العادي. بعد Backspace الخط اللي اتمسح من الـ vector <b>فضل باين</b> على الشاشة، لأن بكسلاته القديمة محدش مسحها. والـ Terminal طبع نفس الكلام بالظبط زي العادي، فالغلطة دي مش هتلاقيها غير لو بصيت على الصورة.</p></div>`)
   + sub('٦. اللوب اللي جوه كل لفة: كام مرة وليه؟', innerLoopsHtml())
   + sub('٧. اللفات اللي في البنش ده', `<p>في التسجيل ده سجّلنا ${P.laps === 2 ? '<b>لفتين</b>' : `<b>${P.laps}</b> ${P.laps < 11 ? 'لفات' : 'لفة'}`} بس، وبعدها الـ gdb قفل الشباك بنفسه (نده <code>glfwSetWindowShouldClose</code>) عشان البنش مايبقاش طويل. في التشغيل العادي على شاشة 60Hz اللوب بتلف حوالي <b>60 مرة في الثانية</b> لحد ما تقفل الشباك.${ev.length ? ' وهنا اللفات أكتر لأن كل دوسة محتاجة لفة توصل فيها، ولفة ترسم نتيجتها.' : ''}</p><p>الأزرار اللي فوق («اللفة 1» و «اللفة 2» وهكذا) بتوديك لأول خطوة في كل لفة. 🖱 = اللفة دي وصلت فيها دوسة ماوس، و ⌨ = دوسة كيبورد. وفي «مسار التنفيذ» كل لفة بتبان كتكرار لنفس أرقام السطور.</p>`);
}
function driverSection(){
  const D = driverLines(); if (!D.length) return '';
  const ran = D.filter(d => d.runs.length), tot = ran.reduce((s, d) => s + d.runs.length, 0); const files = new Set(D.map(d => d.file)).size;
  const rows = D.map(d => `<tr${d.runs.length ? '' : ' class="no"'}><td class="n">${files > 1 ? esc(d.file) + ' : ' : ''}${d.ln}</td><td><code>${esc(d.t)}</code></td><td>${(() => { const s = d.runs.length ? ST[d.runs[0]] : null; return `<span class="tag">${d.kind}</span>${s ? ` <b>${esc(s.ti)}</b>` : ''}<br><small>${d.what}</small>`; })()}</td><td class="r">${d.runs.length ? `<button type="button" data-go="${d.runs[0]}" title="روح لأول مرة اتنفذ فيها">${times(d.runs.length)} ▶</button>` : '<small>ما اتنفذش في التشغيل ده</small>'}</td></tr>`).join('');
  return `<h4>⚙️ السطور اللي الدرايفر بياخد فيها أوامر</h4>
    <p>الدرايفر هو البرنامج اللي بيجي مع كارت الشاشة وبينفذ دوال OpenGL. الكود مابيكتبش اسمه أبداً، بس أي سطر فيه دالة بتبدأ بـ <code>gl</code> هو أمر رايح للدرايفر، وكمان 3 سطور من GLFW و GLAD بتكلّمه (<code>glfwMakeContextCurrent</code> و <code>gladLoadGLLoader</code> و <code>glfwSwapBuffers</code>). في البرنامج ده فيه <b>${D.length}</b> سطر زي كده، اتنفذ منهم ${ran.length} سطر، والدرايفر استلم <b>${tot}</b> أمر في التشغيل كله (عشان سطور اللوب بتتكرر كل لفة). السطور دي عليها علامة ⚙ في الكود جنب رقم السطر.</p>
    <div class="drvt"><table><thead><tr><th>السطر</th><th>الكود</th><th>الأمر ده بيعمل إيه في الدرايفر</th><th>اتنفذ كام مرة</th></tr></thead><tbody>${rows}</tbody></table></div>`;
}
function renderStory(){
  const S = PSTORY[P.id] || {}; const CH = chapters(); const lastFr = P.frames.length - 1;
  const hasCb = ST.some(s => s.ev && s.ev.btn !== 'key'), hasKey = ST.some(s => s.ev && s.ev.btn === 'key');
  const noGLs = document.body.classList.contains('nogl'), isPyS = P.files.some(f => /\.py$/.test(f.name));
  $('stoSub').textContent = `${P.title} · ${CH.length} فصول · ${ST.length} خطوة`;
  const curCh = CH.findIndex(c => i >= c.from && i <= c.to);
  $('stoBody').innerHTML = `
    <h4>🎯 هنوصل لإيه؟</h4>
    <div class="goal"><p>${S.goal || esc(P.desc)}</p>${lastFr >= 0 ? `<figure style="margin:0"><img src="${P.frames[lastFr]}" alt="آخر صورة اتقرت من الكارت في التشغيل الحقيقي"><figcaption>آخر صورة حقيقية من الكارت</figcaption></figure>` : `<figure style="margin:0"><div class="term" style="max-height:220px;overflow:auto;padding:8px">${P.term.map(l => l.charCodeAt(0) === 1 ? `<div class="typed">${esc(l.slice(1))}</div>` : `<div>${esc(l)}</div>`).join('')}</div><figcaption>اللي ظهر في الـ Terminal في التشغيل الحقيقي</figcaption></figure>`}</div>
    <h4>🧭 مين بيوجّه أوامر لمين؟</h4>
    <div class="chain">
      ${noGLs ? `<div class="row"><b>الحساب</b>${nd('الكود بتاعك')} ${AR} ${nd('CPU', 'c')} ${AR} ${nd('الرام (المتغيرات)')}</div><div class="row"><b>الطباعة</b>${nd('CPU', 'c')} ${AR} ${nd(isPyS ? 'print' : 'std::cout')} ${AR} ${nd('🖥 الـ Terminal')}</div>${P.term.some(l => l.charCodeAt(0) === 1) ? `<div class="row"><b>الكيبورد</b>${nd('⌨ الكيبورد')} ${AR} ${nd('الـ Terminal')} ${AR} ${nd('cin', 'c')} ${AR} ${nd('الرام (المتغيرات)')}</div>` : ''}` : `
      <div class="row"><b>الشباك</b>${nd('الكود بتاعك')} ${AR} ${nd('CPU', 'c')} ${AR} ${nd('GLFW')} ${AR} ${nd('نظام التشغيل')} ${AR} ${nd('🪟 الشباك')}</div>
      <div class="row"><b>الرسم</b>${nd('CPU', 'c')} ${AR} ${nd('دوال gl (glClear و glDrawArrays …)')} ${AR} ${nd('الدرايفر')} ${AR} ${nd('GPU', 'g')} ${AR} ${nd('Framebuffer')} ${AR} ${nd('🖥 الشاشة')}</div>`}
      ${hasCb ? `<div class="row"><b>الماوس (بالعكس)</b>${nd('🖱 الماوس')} ${AR} ${nd('نظام التشغيل')} ${AR} ${nd('GLFW')} ${AR} ${nd('MouseButtonCallback', 'c')} ${AR} ${nd('الرام + الكارت')}</div>` : ''}
      ${hasKey ? `<div class="row"><b>الكيبورد (بالعكس)</b>${nd('⌨ الكيبورد')} ${AR} ${nd('نظام التشغيل')} ${AR} ${nd('GLFW')} ${AR} ${nd('KeyCallback', 'c')} ${AR} ${nd('الرام + الكارت')}</div>` : ''}
    </div>
    <p>${noGLs ? `البرنامج ده مالوش شباك ومش بيكلّم كارت الشاشة خالص: الـ CPU بينفذ كل سطر لوحده، والمتغيرات في الرام، واللي بيطلع بيتكتب في الـ Terminal بـ <code>${isPyS ? 'print' : 'std::cout'}</code>.${isPyS ? ' والفرق إن Python نفسها برنامج بيقرا الكود ده سطر سطر وينفذه (Interpreter)، مش compiler بيحوّله لـ exe الأول. و NumPy جواها كود C سريع بيشتغل على المصفوفات.' : ''}</p><p style="display:none">` : ''}الـ CPU هو المدير: بينفذ الكود سطر سطر، ومش بيرسم بنفسه. أي سطر فيه دالة بتبدأ بـ <code>gl</code> (زي <code>glBufferData</code> أو <code>glDrawArrays</code>) هو أمر بيتبعت للكارت، والكارت هو اللي بيرسم.${hasCb ? (hasKey ? ' الحالة الوحيدة اللي الأمر بييجي فيها بالعكس هي الماوس والكيبورد: محدش من الكود بينده <code>MouseButtonCallback</code> ولا <code>KeyCallback</code>، GLFW هو اللي بيندههم لما تدوس.' : ' الحالة الوحيدة اللي الأمر بييجي فيها بالعكس هي الماوس: محدش من الكود بينده <code>MouseButtonCallback</code>، GLFW هو اللي بيندهها لما تدوس.') : ''}</p>
    ${driverSection()}
    <h4>📚 فصول القصة بالترتيب</h4>
    ${CH.map((c, n) => { const x = chapText(c); const a = ST[c.from], b = ST[c.to];
      return `<div class="chap${n === curCh ? ' now' : ''}"><h5><span>${n + 1}. ${CAT[c.c]}${n === curCh ? ' ← انت هنا' : ''}</span><small>steps ${c.from + 1}–${c.to + 1} · lines ${lineOf(a.v)}–${lineOf(b.v)}</small></h5><p>${x.t}</p>${chapLines(c)}<span class="who">${x.who}</span><span class="why">${x.why}</span><button type="button" class="gochap" data-go="${c.from}">▶ روح لأول الفصل ده (خطوة ${c.from + 1})</button></div>`; }).join('')}
    <h4>🔁 ${noGLs && !ST.some(s => /^(while|for)\b/.test(stepText(s))) ? 'فين اللوب؟' : 'ليه بنعمل لوب؟'}</h4><p>${S.loop || (noGLs ? (ST.some(s => /^(while|for)\b/.test(stepText(s))) ? `البرنامج ده مالوش شباك، فاللوب هنا مش عشان الشاشة: بتكرر نفس السطور (زي اللف على عناصر مصفوفة أو حروف نص) لحد ما شرطها يبقى غلط. اتفرج على «مسار التنفيذ»: كل لفة بتبان كتكرار لنفس أرقام السطور.` : (isPyS ? 'البرنامج ده مافيهوش لوب خالص: Python بتمشي على السطور من فوق لتحت مرة واحدة وتخلص. مفيش شباك يفضل مفتوح ويستنى، فمفيش حاجة محتاجة تتكرر.' : 'البرنامج ده مافيهوش لوب <code>while</code> خالص: بيمشي من أول <code>main</code> لآخرها مرة واحدة ويخلص. مفيش شباك يفضل مفتوح ويستنى، فمفيش حاجة محتاجة تتكرر.')) : STATIC_LOOP)}</p>
    <h4>👀 تتفرج إزاي؟</h4>
    <p>اضغط «تشغيل» وسيبه يمشي، أو امشي بـ «اللي بعده». كل خطوة = سطر واحد اتنفذ فعلاً بالترتيب ده. اللون البرتقاني = الـ CPU شغال لوحده، الأخضر = الكارت شغال، الأزرق = الـ CPU بيبعت أمر للكارت. الكروت البرتقاني على الماكينة بتقولك إيه اللي اتغير في الخطوة دي وبسبب أنهي سطر، و «مسار التنفيذ» بيوريك امتى الكود نط لدالة ورجع، وامتى لف في اللوب.</p>`;
  { const body = $('stoBody'), txt = body.innerText; const W = storyWords(txt);
    body.insertAdjacentHTML('afterbegin', `<h4>📝 قبل ما تبدأ: معنى الكلمات اللي في القصة</h4><dl class="words">${W.map(([w, d]) => `<div><dt>${w}</dt><dd>${d}</dd></div>`).join('')}</dl>`); }
  { const body = $('stoBody'); const kids = [...body.childNodes]; const frag = document.createDocumentFragment(); let cur = null;
    for (const n of kids){ if (n.nodeName === 'H4'){ cur = document.createElement('details'); cur.className = 'sec'; const sm = document.createElement('summary'); sm.innerHTML = n.innerHTML; cur.appendChild(sm); frag.appendChild(cur); }
      else if (cur) cur.appendChild(n); else frag.appendChild(n); }
    body.innerHTML = ''; body.appendChild(frag); }
  fixBidi($('stoBody'));
  $('stoBody').querySelectorAll('[data-go]').forEach(bn => bn.onclick = (e) => { e.preventDefault(); showStory(false); play(false); go(+bn.dataset.go); stage.scrollIntoView({behavior: reduce ? 'auto' : 'smooth', block: 'center'}); });
}
function showStory(on){ if (on && $('bytesSheet') && !$('bytesSheet').hidden) showBytes(false); if (on && $('cmdSheet') && !$('cmdSheet').hidden) showCmd(false); $('story2').hidden = !on; $('stoBtn').setAttribute('aria-expanded', on); $('stoBtn').textContent = on ? '✕ خبّي القصة' : '📜 قصة البنش';
  if (on){ if (!$('legend').hidden) showLegend(false); if (!$('gloss').hidden) showGloss(false); if ($('stepsSheet') && !$('stepsSheet').hidden) showSteps(false); renderStory(); $('story2').scrollTop = 0; } }
$('stoBtn').onclick = () => showStory($('story2').hidden); $('stoX').onclick = () => showStory(false);
document.addEventListener('keydown', e => { if (e.key === 'Escape' && !$('story2').hidden) showStory(false); });



// ------------------------------------------------------------------ jump to a code line (like the step box, but for source lines)
let selLine = null; // global line id (file offset + line)
function lnFile(){ return P.files.length > 1 ? +$('lnF').value || 0 : 0; }
function setupLineNav(){ const sel = $('lnF'); sel.hidden = P.files.length < 2; sel.innerHTML = P.files.map((f, k) => `<option value="${k}">${esc(f.name)}</option>`).join(''); sel.value = '0';
  selLine = null; $('lnN').value = ''; syncLineNav(); }
function syncLineNav(){ const f = P.files[lnFile()]; $('lnN').max = f.lines.length; $('lnN').placeholder = `1–${f.lines.length}`;
  const n = selLine ? selLine - f.off : 0; $('lnDec').disabled = n <= 1; $('lnInc').disabled = n >= f.lines.length && n > 0; }
function showLine(fk, n){ const f = P.files[fk]; n = Math.max(1, Math.min(f.lines.length, n)); const v = f.off + n; const L = $('L' + v); if (!L) return;
  document.querySelectorAll('#code div.sel').forEach(e => e.classList.remove('sel')); L.classList.add('sel'); selLine = v; $('lnN').value = n;
  const bx = $('code'); bx.scrollTop = Math.max(0, L.offsetTop - bx.clientHeight / 2); L.classList.remove('flash'); void L.offsetWidth; L.classList.add('flash');
  const runs = []; ST.forEach((s, j) => { if (s.v === v) runs.push(j); }); const txt = f.lines[n - 1].trim();
  const after = runs.find(j => j > i);
  $('lnInfo').innerHTML = !txt ? `سطر ${n} فاضي.` : runs.length ? `سطر ${n} اتنفذ ${times(runs.length)} في التشغيل ده. <button type="button" data-go="${runs[0]}">أول مرة: خطوة ${runs[0] + 1} ▶</button>${after !== undefined && after !== runs[0] ? `<button type="button" data-go="${after}">اللي بعد خطوتك: ${after + 1} ▶</button>` : ''}` : `سطر ${n} ما اتنفذش في التشغيل ده${/^[{}]$|^\/\/|^#/.test(txt) ? ' (قوس أو تعليق أو سطر للمترجم، مش أمر بيتنفذ)' : ''}.`;
  $('lnInfo').querySelectorAll('[data-go]').forEach(b => b.onclick = () => { play(false); go(+b.dataset.go); });
  syncLineNav(); }
$('goLine').onsubmit = e => { e.preventDefault(); const inp = $('lnN'), f = P.files[lnFile()], n = Math.round(+inp.value);
  if (!inp.value || isNaN(n) || n < 1 || n > f.lines.length){ inp.classList.add('bad'); setTimeout(() => inp.classList.remove('bad'), 1200); $('lnInfo').textContent = `اكتب رقم من 1 لـ ${f.lines.length}`; return; }
  inp.blur(); showLine(lnFile(), n); };
const lineBy = d => { const f = P.files[lnFile()]; const cur = selLine && selLine > f.off && selLine <= f.off + f.lines.length ? selLine - f.off : (ST[i].f === lnFile() ? ST[i].ln : 0); showLine(lnFile(), cur + d); };
$('lnDec').onclick = () => lineBy(-1); $('lnInc').onclick = () => lineBy(1); $('lnF').onchange = () => { selLine = null; $('lnN').value = ''; $('lnInfo').textContent = ''; syncLineNav(); };
// ------------------------------------------------------------------ every step, in order, fully described (hidden until asked)
let stBuilt = null;
function renderSteps(){
  if (stBuilt !== P.id){ stBuilt = P.id;
    $('stList').innerHTML = ST.map((s, k) => {
      const lapTag = s.lap ? `<span class="u" style="background:var(--blueline)">لفة ${s.lap}</span>` : s.cl ? '<span class="u" style="background:var(--blueline)">خروج من while</span>' : '';
      const evTag = s.ev ? (s.ev.btn === 'key' ? `<span class="u ev">⌨ ${esc(s.ev.key)}</span>` : '<span class="u ev">🖱 ماوس</span>') : '';
      const code = stepText(s);
      return `<li id="stp${k}" data-k="${k}"><div class="sh"><span class="n">خطوة ${k + 1}</span><span class="tags">${lapTag}${evTag}${unitBadge(s.u)}<button type="button" data-go="${k}">روح ▶</button></span></div>
        <div class="tt">سطر ${esc(fileLine(s))}: ${esc(s.ti)}</div>
        <code class="c">${esc(code)}</code>
        <p class="ex">${s.ex || ''}</p>${s.dy && s.dy.length ? `<span class="dy">${s.dy.join('<br>')}</span>` : ''}${whyHtml(k) ? `<div class="wy">${whyHtml(k)}</div>` : ''}
        <span class="wh">${esc(P.files[s.f].name)} : ${s.ln}${s.fn ? ` · ${esc(s.fn)}()` : ''}</span></li>`; }).join('');
    fixBidi($('stList'));
    $('stList').querySelectorAll('[data-go]').forEach(bn => bn.onclick = () => { showSteps(false); play(false); go(+bn.dataset.go); stage.scrollIntoView({behavior: reduce ? 'auto' : 'smooth', block: 'center'}); });
    $('stq').value = ''; }
  $('stSub').textContent = `${P.title} · ${ST.length} خطوة بالترتيب اللي اتنفذت بيه فعلاً · انت دلوقتي في خطوة ${i + 1}`;
  $('stList').querySelectorAll('li').forEach(li => { const k = +li.dataset.k; li.classList.toggle('now', k === i); li.classList.toggle('past', k < i); });
}
function filterSteps(q){ q = q.trim().toLowerCase(); $('stList').querySelectorAll('li').forEach(li => { li.hidden = !!q && !li.textContent.toLowerCase().includes(q) && String(+li.dataset.k + 1) !== q; }); }
function showSteps(on){ const sh = $('stepsSheet'); sh.hidden = !on; if (on && $('cmdSheet') && !$('cmdSheet').hidden) showCmd(false); $('stepsBtn').setAttribute('aria-expanded', on); $('stepsBtn').textContent = on ? '✕ خبّي الخطوات' : '📋 كل الخطوات';
  if (on){ if (!$('legend').hidden) showLegend(false); if (!$('gloss').hidden) showGloss(false); if (!$('story2').hidden) showStory(false); if ($('bytesSheet') && !$('bytesSheet').hidden) showBytes(false);
    renderSteps(); filterSteps($('stq').value); const cur = $('stp' + i); if (cur) requestAnimationFrame(() => { sh.scrollTop = Math.max(0, cur.offsetTop - 140); }); } }
$('stepsBtn').onclick = () => showSteps($('stepsSheet').hidden); $('stX').onclick = () => showSteps(false); $('stq').oninput = e => filterSteps(e.target.value);
document.addEventListener('keydown', e => { if (e.key === 'Escape' && !$('stepsSheet').hidden) showSteps(false); });


// ------------------------------------------------------------------ commands table: how many CPU / CPU→GPU / GPU steps, and which GPU commands (only where window.CMD_TABLE)
const FAM = [
  ['draw', 'أوامر رسم', '#e0561c', /^gl(DrawArrays|DrawElements)$/],
  ['fb', 'لوحة الرسم (مسح وعرض)', '#c78512', /^(glClear|glClearColor|glViewport|glfwSwapBuffers)$/],
  ['buf', 'الصندوق (Buffer)', '#3a8fbf', /^gl(GenBuffers|BindBuffer|BufferData|BufferSubData|DeleteBuffers)$/],
  ['vao', 'ورقة التعليمات (VAO)', '#0f766e', /^gl(GenVertexArrays|BindVertexArray|EnableVertexAttribArray|VertexAttribPointer|DeleteVertexArrays)$/],
  ['sh', 'الـ Shader', '#7d5cc4', /^gl(CreateShader|ShaderSource|CompileShader|GetShaderiv|GetShaderInfoLog|CreateProgram|AttachShader|LinkProgram|ValidateProgram|DeleteShader|UseProgram|DeleteProgram|GetProgramiv)$/],
  ['uni', 'uniform', '#b0406a', /^gl(GetUniformLocation|Uniform\w+)$/],
  ['set', 'إعدادات تانية', '#5a7d2a', /^gl[A-Z]\w*$/],
];
const OTHER = [
  ['win', 'الشباك و GLFW', s => /\b(glfw\w+|gladLoadGLLoader)\s*\(/.test(stepText(s)) && !/glfwSwapBuffers/.test(stepText(s))],
  ['ev', 'أحداث ماوس وكيبورد', s => !!s.ev],
  ['call', 'نداء دالة من دوالك', (s, k, P) => { const n = P.steps[k + 1]; return n && n.d > s.d && !n.ev; }],
  ['print', 'طباعة في الـ Terminal', s => /\b(cout|printf|print)\b/.test(stepText(s))],
  ['cin', 'قراية من الكيبورد (cin)', s => /\bcin\s*>>/.test(stepText(s))],
  ['loop', 'فحص شرط لوب (while / for)', s => /^(while|for)\b/.test(stepText(s))],
  ['brace', 'دخول أو خروج من دالة (أقواس)', s => /^[{}];?$/.test(stepText(s))],
];
function gfn(t){ const m = /\b(gl[A-Z]\w*|glfwSwapBuffers)\s*\(/.exec(t); return m ? m[1] : null; }
// CPU steps: every step goes to exactly ONE of these (first match wins), so they add up to the CPU total
const CPUCAT = [
  ['ev', 'دخول دالة الماوس أو الكيبورد', '#7d5cc4', s => !!s.ev],
  ['brace', 'أقواس (دخول وخروج من دالة)', '#8a8f98', s => /^[{}];?$/.test(stepText(s))],
  ['win', 'الشباك و GLFW', '#3a8fbf', s => /\b(glfw\w+|gladLoadGLLoader)\s*\(/.test(stepText(s))],
  ['cin', 'قراية من الكيبورد (cin)', '#c78512', s => /\bcin\s*>>/.test(stepText(s))],
  ['print', 'طباعة في الـ Terminal', '#0f766e', s => /\b(cout|printf|print)\b/.test(stepText(s))],
  ['loop', 'فحص شرط لوب (while / for)', '#b0406a', s => /^(while|for)\b/.test(stepText(s))],
  ['call', 'نداء دالة من دوالك', '#e0561c', (s, k) => { const n = ST[k + 1]; return n && n.d > s.d && !n.ev; }],
  ['ret', 'return (رجوع بقيمة)', '#5a7d2a', s => /^return\b/.test(stepText(s))],
  ['calc', 'حساب ومتغيرات', '#d0a248', () => true],
];
function cmdStats(){
  const r = {n: ST.length, CPU: 0, 'CPU→GPU': 0, GPU: 0, fam: {}, fns: {}, famU: {}, cpu: {}, cpuL: {}};
  ST.forEach((s, k) => { r[s.u] = (r[s.u] || 0) + 1; const t = stepText(s);
    if (s.u === 'CPU'){ const C = CPUCAT.find(c => c[3](s, k)); r.cpu[C[0]] = (r.cpu[C[0]] || 0) + 1;
      const m = C[0] === 'win' ? /\b(glfw\w+|gladLoadGLLoader)\s*\(/.exec(t) : null; const key = m ? m[1] : 'L' + s.v;
      const L = (r.cpuL[C[0]] = r.cpuL[C[0]] || {}); (L[key] = L[key] || [0, k, m ? m[1] : null, s.v])[0]++; return; }
    const f = gfn(t); const F = f && FAM.find(([, , , re]) => re.test(f)); if (!F) return;
    r.fam[F[0]] = (r.fam[F[0]] || 0) + 1; (r.famU[F[0]] = r.famU[F[0]] || {})[s.u] = ((r.famU[F[0]] || {})[s.u] || 0) + 1;
    const fn = (r.fns[F[0]] = r.fns[F[0]] || {}); (fn[f] = fn[f] || [0, k])[0]++; });
  return r;
}
function renderCmd(){
  const s = cmdStats(), pct = (v, n) => n ? Math.round(v * 100 / n) : 0;
  $('cmdSub').textContent = `${P.title} · ${ST.length} خطوة اتنفذت فعلاً`;
  const U = [['CPU', 'var(--arancio)', 'الـ CPU لوحده'], ['CPU→GPU', 'var(--blueline)', 'أمر للدرايفر'], ['GPU', 'var(--teal)', 'الكارت شغال']];
  const bar = (parts, n) => `<div class="bar">${parts.map(([v, c, ttl]) => `<i style="width:${pct(v, n)}%;background:${c}" title="${ttl}"></i>`).join('')}</div>`;
  const t1 = `<table><thead><tr><th class="pn">مين</th><th>الخطوات</th><th>النسبة</th></tr></thead><tbody>
    ${U.map(([u, c, d]) => `<tr><td class="pn"><span class="sw" style="background:${c}"></span><b>${u}</b><br><small>${d}</small></td><td${s[u] ? '' : ' class="z"'}>${s[u] || 0}</td><td>${pct(s[u] || 0, s.n)}%</td></tr>`).join('')}
    <tr class="tot"><td class="pn">المجموع</td><td>${s.n}</td><td>100%</td></tr></tbody></table>${bar(U.map(([u, c]) => [s[u] || 0, c, u]), s.n)}`;
  const chipsCPU = id => Object.values(s.cpuL[id] || {}).sort((x, y) => y[0] - x[0]).map(([n, k, name, v]) => `<button type="button" class="fn" dir="ltr" data-k="${k}" title="${esc(stepText(ST[k]))}">${name ? name : 'line ' + lineOf(v)} <b>× ${n}</b>${name ? '' : `<small class="cs">${esc(stepText(ST[k]))}</small>`}</button>`).join('');
  const cats = CPUCAT.filter(c => s.cpu[c[0]]);
  const t2 = s.CPU ? `<table><thead><tr><th class="pn">النوع</th><th>الخطوات</th><th>النسبة من الـ CPU</th></tr></thead><tbody>
    ${cats.map(([id, name, c]) => `<tr><td class="pn"><span class="sw" style="background:${c}"></span>${name}</td><td>${s.cpu[id]}</td><td>${pct(s.cpu[id], s.CPU)}%</td></tr>`).join('')}
    <tr class="tot"><td class="pn">كل خطوات الـ CPU</td><td>${s.CPU}</td><td>100%</td></tr></tbody></table>${bar(cats.map(([id, n, c]) => [s.cpu[id], c, n]), s.CPU)}
    <p class="note">كل خطوة اتعدت في نوع واحد بس، فالمجموع = خطوات الـ CPU بالظبط. دوس على أي سطر أو دالة تروح لأول مرة اتنفذ فيها.</p>
    ${cats.map(([id, name, c]) => `<div class="grp" style="border-inline-start:4px solid ${c}"><b>${name}</b> <small>(${s.cpu[id]})</small><br>${chipsCPU(id)}</div>`).join('')}` : '<p class="note">مفيش خطوات CPU.</p>';
  const fams = FAM.filter(([id]) => s.fam[id]); const gpuN = (s['CPU→GPU'] || 0) + (s.GPU || 0);
  const t3 = gpuN ? `<table><thead><tr><th class="pn">النوع</th><th>CPU→GPU</th><th>GPU</th><th>المجموع</th></tr></thead><tbody>
    ${fams.map(([id, name, c]) => `<tr><td class="pn"><span class="sw" style="background:${c}"></span>${name}</td><td${(s.famU[id] || {})['CPU→GPU'] ? '' : ' class="z"'}>${(s.famU[id] || {})['CPU→GPU'] || 0}</td><td${(s.famU[id] || {}).GPU ? '' : ' class="z"'}>${(s.famU[id] || {}).GPU || 0}</td><td><b>${s.fam[id]}</b></td></tr>`).join('')}
    <tr class="tot"><td class="pn">كل أوامر الـ GPU</td><td>${s['CPU→GPU'] || 0}</td><td>${s.GPU || 0}</td><td>${gpuN}</td></tr></tbody></table>${bar(fams.map(([id, n, c]) => [s.fam[id], c, n]), gpuN)}
    ${fams.map(([id, name, c]) => `<div class="grp" style="border-inline-start:4px solid ${c}"><b>${name}</b> <small>(${s.fam[id]})</small><br>${Object.entries(s.fns[id]).sort((x, y) => y[1][0] - x[1][0]).map(([f, [n, k]]) => `<button type="button" class="fn" dir="ltr" style="border-color:${c}" data-k="${k}">${f} <b>× ${n}</b></button>`).join('')}</div>`).join('')}`
    : '<p class="note">البرنامج ده مش بيكلّم كارت الشاشة خالص: مفيش ولا أمر <code>gl</code>.</p>';
  $('cmdBody').innerHTML = `
    <p class="note">كل خطوة = سطر واحد اتنفذ في التشغيل الحقيقي. <b style="color:var(--arancio)">CPU</b> = سطر الـ CPU نفذه لوحده. <b>CPU→GPU</b> = أمر <code>gl</code> الـ CPU بعته للدرايفر يجهّز حاجة على الكارت. <b style="color:var(--teal)">GPU</b> = الكارت نفسه اشتغل: مسح أو رسم أو عرض الصورة.</p>
    <details open><summary>1. مين اشتغل كام خطوة</summary>${t1}</details>
    <details open><summary>2. أوامر الـ CPU بالتفصيل (كل نوع بلون)</summary>${t2}</details>
    <details open><summary>3. أوامر الـ GPU بالتفصيل (كل نوع بلون)</summary>${t3}</details>`;
  $('cmdBody').querySelectorAll('.fn').forEach(b => b.onclick = () => { showCmd(false); play(false); go(+b.dataset.k); stage.scrollIntoView({behavior: reduce ? 'auto' : 'smooth', block: 'center'}); });
}
function showCmd(on){ const sh = $('cmdSheet'); sh.hidden = !on; $('cmdBtn').setAttribute('aria-expanded', on); $('cmdBtn').textContent = on ? '✕ خبّي الأوامر' : '📊 الأوامر';
  if (on){ ['legend', 'gloss', 'story2', 'stepsSheet', 'bytesSheet'].forEach(id => { const e = $(id); if (e && !e.hidden){ const b = {legend: showLegend, gloss: showGloss, story2: showStory, stepsSheet: showSteps, bytesSheet: showBytes}[id]; b(false); } }); renderCmd(); sh.scrollTop = 0; } }
if (window.CMD_TABLE){ $('cmdBtn').hidden = false; $('cmdBtn').onclick = () => showCmd($('cmdSheet').hidden); $('cmdX').onclick = () => showCmd(false); }

// ------------------------------------------------------------------ bytes table (hidden until asked)
function showBytes(on){ const sh = $('bytesSheet'); if (!sh) return; if (on && $('cmdSheet') && !$('cmdSheet').hidden) showCmd(false); sh.hidden = !on; $('bytBtn').setAttribute('aria-expanded', on); $('bytBtn').textContent = on ? '✕ خبّي البايتات' : '🧮 البايتات';
  if (on){ if (!$('legend').hidden) showLegend(false); if (!$('gloss').hidden) showGloss(false); if (!$('story2').hidden) showStory(false); if ($('stepsSheet') && !$('stepsSheet').hidden) showSteps(false);
    sh.querySelectorAll('tr.cur').forEach(r => r.classList.remove('cur')); const r = sh.querySelector(`tr[data-pid="${P.id}"]`);
    if (r){ r.classList.add('cur'); sh.scrollTop = Math.max(0, r.offsetTop - 120); } } }
if ($('bytBtn')){ $('bytBtn').onclick = () => showBytes($('bytesSheet').hidden); $('bytX').onclick = () => showBytes(false);
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !$('bytesSheet').hidden) showBytes(false); }); }
// ------------------------------------------------------------------ program picker
{ const pk = $('picker'); const DAYN = {1:'اليوم 1', 2:'اليوم 2', 3:'اليوم 3', 4:'اليوم 4', 5:'اليوم 5', 6:'اليوم 6', 7:'اليوم 7', 8:'الأسبوع 3 · اليوم 1', 9:'الأسبوع 3 · اليوم 2'};
  const days = [...new Set(PROGS.map(p => p.day))]; const multi = days.length > 1;
  days.forEach(d => { const ps = PROGS.filter(p => p.day === d);
    const row = document.createElement(multi ? 'details' : 'div'); row.className = 'pk-day'; row.dataset.day = d;
    row.innerHTML = multi ? `<summary><span>${DAYN[d] || ('اليوم ' + d)}</span><small>عدد ${ps.length} برامج</small></summary><div class="pk-list"></div>` : `<span>${DAYN[d] || ('اليوم ' + d)}</span><div class="pk-list"></div>`;
    const list = row.querySelector('.pk-list');
    ps.forEach(p => { const b = document.createElement('button'); b.type = 'button'; b.dataset.id = p.id; b.setAttribute('aria-pressed', 'false');
      b.innerHTML = `<i class="${p.kind === 'CAD' ? 'cad' : p.kind === 'رسم' ? '' : 'cli'}">${esc(p.kind)}</i>${esc(p.title)}`; b.onclick = () => loadProgram(p.id); list.appendChild(b); });
    if (multi){ const wk = d >= 8 ? 3 : 2; let w = pk.querySelector(`details.pk-week[data-week="${wk}"]`);
      if (!w){ w = document.createElement('details'); w.className = 'pk-week'; w.dataset.week = wk;
        w.innerHTML = `<summary><span>الأسبوع ${wk}</span><small></small></summary><div class="pk-days"></div>`; pk.appendChild(w); }
      if (wk === 3) row.querySelector('summary span').textContent = 'اليوم ' + (d - 7);
      w.querySelector('.pk-days').appendChild(row);
      const n = w.querySelectorAll('.pk-day').length, np = w.querySelectorAll('.pk-list button').length;
      w.querySelector('summary small').textContent = `عدد ${n} أيام · عدد ${np} برنامج`;
    } else pk.appendChild(row); }); }
addEventListener('hashchange', () => { const h = location.hash.slice(1); if (h && (!P || h !== P.id) && PROGS.some(p => p.id === h)) loadProgram(h); });
setMode('cutaway');
const fromFile = (/__(d\d_\w+?)\.html?$/i.exec(decodeURIComponent(location.pathname)) || [])[1];
const start = location.hash.slice(1) || window.BENCH_START || fromFile || ''; loadProgram(PROGS.some(p => p.id === start) ? start : (store.get('bench06') && PROGS.some(p => p.id === store.get('bench06')) ? store.get('bench06') : PROGS[0].id));
syncPause();
requestAnimationFrame(frame);
})();
