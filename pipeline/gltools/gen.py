import json, base64, html, re, io
from PIL import Image
A = '/home/claude/day7/apitrace/'
SRC = open('/home/claude/day7/src/r2_two_methods.cpp').read().split('\n')
def img(path, w=320):
    im = Image.open(path).convert('RGB').resize((w, w * 3 // 4)); b = io.BytesIO(); im.save(b, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()
LINE = {3977: 89, 3978: 90, 3979: 91, 3980: 95, 3981: 96, 3982: 97, 3983: 98, 3984: 99, 3985: 100, 3986: 101, 3987: 102, 3988: 105, 3989: 106, 3990: 107, 3991: 108,
        3992: 109, 3993: 110, 3994: 114, 3995: 115, 3996: 116, 3997: 117, 4014: 143, 4015: 144, 4016: 145, 4017: 151, 4018: 154, 4019: 155, 4020: 156, 4021: 157,
        4022: 158, 4023: 159, 4024: 160, 4025: 163, 4026: 164, 4027: 165, 4028: 166, 4029: 167, 4030: 168, 4031: 169, 4032: 170, 4033: 171, 4034: 172, 4035: 173, 4037: 179}
calls = []
for l in open(A + 'frame1_calls.txt'):
    m = re.match(r'^(\d+) (gl\w+)\((.*)$', l.rstrip('\n'))
    if not m: continue
    n = int(m.group(1)); fn = m.group(2); args = m.group(3)
    if fn.startswith('glShaderSource'): args = 'shader = %s, count = 1, string = &"#version 330 core ..."' % re.match(r'shader = (\d+)', args).group(1)
    if fn == 'glGetShaderiv' or n < 3977: continue
    calls.append((n, fn, args.rstrip(')') if args.endswith(')') and args.count('(') < args.count(')') else args))
def st(c, f='state_%d.json'):
    d = json.loads(open(A + (f % c if '%' in f else f)).read(), strict=False); P = d['parameters']
    at = next((v for k, v in P.items() if isinstance(v, dict) and 'GL_VERTEX_ATTRIB_ARRAY_SIZE' in v), {})
    return dict(vao=P['GL_VERTEX_ARRAY_BINDING'], abuf=P['GL_ARRAY_BUFFER_BINDING'], ebuf=P['GL_ELEMENT_ARRAY_BUFFER_BINDING'], prog=P['GL_CURRENT_PROGRAM'],
                size=at.get('GL_VERTEX_ATTRIB_ARRAY_SIZE'), stride=at.get('GL_VERTEX_ATTRIB_ARRAY_STRIDE'), attrbuf=at.get('GL_VERTEX_ATTRIB_ARRAY_BUFFER_BINDING'),
                uni=d['uniforms'], verts=[v['position'] for v in d['buffers'].get('vertices', [])])
DRAWS = [(4021, 'المربع الشمال', 'الطريقة 2: VAO 1 لوحده', 'fb_4021.png'), (4024, 'المثلث الشمال', 'الطريقة 2: VAO 2 لوحده', 'fb_4024.png'),
         (4031, 'المربع اليمين', 'الطريقة 1: VAO 3 بعد ما اتكتب فيه Layout المربع', 'fb_4031.png'), (4035, 'المثلث اليمين', 'الطريقة 1: نفس VAO 3 بعد ما اتكتب فيه Layout المثلث', 'fb_4035.png')]
S = {c: st(c) for c, *_ in DRAWS}
BUG = st(0, 'bug_state.json')
json.dump(dict(calls=calls, line=LINE, src=SRC, S=S, BUG=BUG, draws=[(c, a, b, img(A + p)) for c, a, b, p in DRAWS], bugimg=img(A + 'bug_fb.png'), okimg=img(A + 'fb_4035.png')),
          open('data.json', 'w'), ensure_ascii=False)
print(len(calls), S[4031], BUG)
# ---- RenderDoc part ----
R = '/home/claude/day7/rd/'
d = json.load(open('data.json'))
tm = json.load(open(R + 'tm.json')); bug = json.load(open(R + 'bug.json'))
NAMES = {'Buffer 26': 'squareBuffer', 'Buffer 27': 'squareIbo', 'Buffer 28': 'triangleBuffer', 'Vertex Array 29': 'squareVao', 'Vertex Array 30': 'triangleVao', 'Vertex Array 31': 'globalVao', 'Program 32': 'shader'}
RDLINE = {2: 151, 3: 154, 4: 155, 5: 156, 6: 157, 7: 158, 8: 159, 9: 160, 10: 163, 11: 164, 12: 165, 13: 166, 14: 167, 15: 168, 16: 169, 17: 170, 18: 171, 19: 172, 20: 173, 21: 179}
for x in tm['draws'] + bug['draws']:
    x['img'] = img(R + x['png']); c = x['attr0']['comp']; s = x['attr0']['stride'] // 4
    x['vsin'] = [x['vbuf'][i * s:i * s + c] for i in range(len(x['vbuf']) // s)]
TITLES = {6: ('المربع الشمال', 'الطريقة 2'), 9: ('المثلث الشمال', 'الطريقة 2'), 16: ('المربع اليمين', 'الطريقة 1'), 20: ('المثلث اليمين', 'الطريقة 1')}
d['rd'] = dict(events=[e for e in tm['events'] if e[0] > 1], draws=tm['draws'], bug=bug['draws'][-1], names=NAMES, line=RDLINE, titles=TITLES)
json.dump(d, open('data.json', 'w'), ensure_ascii=False)
open('gl_tools.html', 'w').write(open('tpl.html').read().replace('%%DATA%%', json.dumps(d, ensure_ascii=False).replace('</', '<\\/')))
print('rd ok', len(d['rd']['events']))
