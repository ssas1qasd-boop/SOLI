#!/usr/bin/env python3
"""جسر صغير بين البنش و Claude Code اللي على الموبايل.
البنش (صفحة GitHub) بيبعت السؤال هنا على 127.0.0.1:8081، والجسر بيشغّل `claude -p` جوه Ubuntu
ويرجّع الرد. كده Claude بيرد جوه البنش نفسه، بنفس اشتراكك، من غير مفتاح API.
التشغيل (في Termux العادي):  python ~/claude_bridge.py
"""
import json, os, subprocess, shutil, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = 8081
ALLOWED = {'https://ssas1qasd-boop.github.io', 'http://localhost:8090', 'http://127.0.0.1:8090'}
WORK = os.path.expanduser('~/.claude_bridge_empty')  # فولدر فاضي: Claude مايشوفش ملفاتك
os.makedirs(WORK, exist_ok=True)

def claude_cmd():
    # Claude Code متسطّب جوه Ubuntu (proot-distro). لو متسطّب في Termux نفسه، بنستخدمه على طول.
    if shutil.which('claude'):
        return ['claude']
    return ['proot-distro', 'login', 'ubuntu', '--', 'bash', '-lc', 'cd /root && exec claude "$@"', 'claude']

BASE = claude_cmd()

def ask(prompt, timeout=240):
    cmd = BASE + ['-p', '--output-format', 'text', '--max-turns', '1']
    r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=timeout, cwd=WORK)
    out = (r.stdout or '').strip()
    if r.returncode != 0 and not out:
        raise RuntimeError((r.stderr or 'claude failed').strip()[-400:])
    return out

class H(BaseHTTPRequestHandler):
    def _cors(self):
        o = self.headers.get('Origin', '')
        if o in ALLOWED:
            self.send_header('Access-Control-Allow-Origin', o)
            self.send_header('Vary', 'Origin')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Private-Network', 'true')
    def _json(self, code, obj):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code); self._cors()
        self.send_header('Content-Type', 'application/json; charset=utf-8'); self.send_header('Content-Length', str(len(b)))
        self.end_headers(); self.wfile.write(b)
    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()
    def do_GET(self):
        if self.path.startswith('/ping'):
            return self._json(200, {'ok': True, 'who': 'claude-code-bridge'})
        self._json(404, {'error': 'not found'})
    def do_POST(self):
        if self.headers.get('Origin', '') not in ALLOWED:
            return self._json(403, {'error': 'origin not allowed'})
        if not self.path.startswith('/ask'):
            return self._json(404, {'error': 'not found'})
        try:
            n = int(self.headers.get('Content-Length', '0'))
            p = json.loads(self.rfile.read(n) or b'{}').get('prompt', '')
            if not p.strip():
                return self._json(400, {'error': 'empty prompt'})
            print(f'→ سؤال ({len(p)} حرف)…', flush=True)
            t = ask(p)
            print(f'← رد ({len(t)} حرف)', flush=True)
            self._json(200, {'text': t})
        except subprocess.TimeoutExpired:
            self._json(504, {'error': 'Claude اتأخر أكتر من 4 دقايق'})
        except Exception as e:
            self._json(500, {'error': str(e)})
    def log_message(self, *a):
        pass

if __name__ == '__main__':
    print('🌉 جسر Claude شغال على http://127.0.0.1:%d  (سيبه مفتوح، وCTRL+c يقفله)' % PORT, flush=True)
    print('   بيستخدم: ' + ' '.join(BASE[:4]) + (' …' if len(BASE) > 4 else ''), flush=True)
    ThreadingHTTPServer(('127.0.0.1', PORT), H).serve_forever()
