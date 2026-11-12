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
