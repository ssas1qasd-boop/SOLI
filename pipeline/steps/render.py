# HTML for the "write it yourself, step by step" section.
import html, os, shutil

CSS = '''
.wline .wcode > span.ltr { display:inline; }
.wsteps .chips { display:block; }
.wsteps .chip { display:inline-block; vertical-align:top; margin:0 1.5mm 1.5mm 0; }
.wkw { margin:2.5mm 0 1.5mm; font-weight:bold; color:#3730a3; font-size:10pt; border-bottom:1px dashed #a5b4fc; padding-bottom:1mm; }
.wbacks { display:block; text-align:left; direction:ltr; margin:0 0 0.8mm; }
.wbacks .wl-back { float:none !important; display:inline-block; direction:rtl; margin:0 0 0 3mm !important; font-size:8.5pt; }
.wbacks .wl-back2 { color:#0f766e !important; }
.wsteps { margin:3mm 0 6mm; border:1px solid #fcd34d; border-radius:3mm; background:#fffdf5; padding:2.5mm 3.5mm 1mm; }
.wsteps .wsh { font-weight:bold; color:#92400e; font-size:11pt; margin:0 0 1mm; }
.wsteps .wsub { color:#78716c; font-size:9.5pt; margin:0 0 2.5mm; }
.wstep { background:#fff; border:1px solid #f1e3b5; border-radius:2mm; margin:0 0 3mm; padding:2mm 3mm; }
.wres { page-break-inside:avoid; }
.wsth { font-weight:bold; font-size:10.5pt; color:#1f2937; margin-bottom:1mm; }
.wsth .n { display:inline-block; min-width:5.5mm; height:5.5mm; line-height:5.5mm; border-radius:50%; background:#d97706; color:#fff; text-align:center; font-size:9pt; margin-left:2mm; }
.wwhy { font-size:9.6pt; color:#374151; margin:0 0 1.5mm; line-height:1.55; }
.wfile { direction:rtl; text-align:right; font-family:"DejaVu Sans Mono",monospace; font-size:8pt; color:#6b7280; margin:1mm 0 0.5mm; }
.wcode { direction:ltr; text-align:left; background:#0f1521; border-radius:1.5mm; padding:1.5mm 2.5mm; font-family:"DejaVu Sans Mono",monospace; font-size:8.2pt; line-height:1.4; white-space:pre-wrap; word-break:break-word; color:#e5e7eb; }
.wcode > span { display:block; min-height:1.2em; }
.wcode > .old { color:#aeb6c4; }
.wcode > .new { background:#3b3204; color:#fde68a; display:block; margin:0 -2.5mm; padding:0 2.5mm; border-right:3px solid #f59e0b; }
.wcode .gap { color:#4b5563; }
.wcode .ln { font-style:normal; color:#6b7280; user-select:none; }
.wcode > .new .ln { color:#d97706; }
.wwhere { background:#fff7ed; border:1px dashed #fdba74; border-radius:1.5mm; padding:1mm 2.5mm; margin:1mm 0 1.2mm; font-size:9.4pt; line-height:1.6; }
.wwhere .pin { font-weight:bold; color:#9a3412; }
.wwhere ul { margin:0.5mm 0 0; padding-right:5mm; }
.wres { display:flex; gap:3mm; align-items:flex-start; margin-top:1.5mm; }
.wres .lbl { font-size:9pt; font-weight:bold; color:#15803d; white-space:nowrap; }
.wres .wterm { flex:1; direction:ltr; text-align:left; background:#0b0f17; color:#b8f2c4; font-family:"DejaVu Sans Mono",monospace; font-size:8pt; border-radius:1.5mm; padding:1.5mm 2.5mm; white-space:pre-wrap; }
.wres img { width:52mm; border-radius:1.5mm; border:1px solid #d1d5db; }
.wres .none { font-size:9pt; color:#6b7280; }
.wfull summary { cursor:pointer; font-size:9pt; color:#2563eb; margin-top:1.5mm; }
'''

import re as _re

def _short(t, n=48):
    t = t.strip()
    return t if len(t) <= n else t[:n - 1] + '…'

def _scopes(rows):
    """For every row index: (scope_owner_text_or_None, in_raw_string, owner_of_brace_line)."""
    stack, info, in_raw, prev_text = [], [], False, ''
    for i, (_, t, _) in enumerate(rows):
        owner_here = stack[-1] if stack else None
        brace_owner = None
        raw_now = in_raw
        line = t
        if not in_raw and 'R"(' in t:
            in_raw = True; raw_now = True
            line = t.split('R"(')[0]
            if ')"' in t.split('R"(', 1)[1]: in_raw = False
        elif in_raw:
            if ')"' in t:
                in_raw = False
                line = t.split(')"', 1)[1]
                tail = t.split(')"', 1)[0]
            else:
                line = ''
        st = t.strip()
        if not raw_now or line:
            for ch in line:
                if ch == '{':
                    own = prev_text if st == '{' else st
                    stack.append(own); brace_owner = own
                elif ch == '}':
                    if stack: brace_owner = stack.pop()
        info.append((owner_here, raw_now and not line, brace_owner))
        if st: prev_text = st
    return info

def _describe_scope(owner, in_raw, before_main):
    if in_raw:
        return 'جوه نص الـ Shader'
    if owner is None:
        if before_main is None:
            return 'برا أي دالة'
        return 'برا أي دالة، ' + ('فوق <code>main</code>' if before_main else 'تحت <code>main</code>')
    o = owner
    if _re.search(r'\bmain\s*\(', o): return 'جوه <code>main</code>'
    if o.startswith('while'): return 'جوه اللوب (<code>while</code>)'
    if o.startswith('for'): return 'جوه الـ <code>for</code>'
    if o.startswith(('if', 'else')): return 'جوه الـ <code>' + html.escape(_short(o, 30)) + '</code>'
    m = _re.match(r'(class|struct|enum class)\s+(\w+)', o)
    if m: return f'جوه <code>{m.group(1)} {m.group(2)}</code>'
    if '=' in o and o.rstrip().endswith('{') or o.endswith('=') or o.endswith('[] ='):
        return 'جوه المصفوفة <code>' + html.escape(_short(o.split('=')[0], 28)) + '</code>'
    m = _re.search(r'([\w:~]+)\s*\(', o)
    if m: return f'جوه الدالة <code>{html.escape(m.group(1))}</code>'
    return 'جوه <code>' + html.escape(_short(o, 30)) + '</code>'

def _anchor(rows, info, j):
    t = rows[j][1].strip()
    if t.startswith('})"'):
        return f'السطر {j + 1} (<code>{html.escape(t)}</code>: نهاية نص الـ Shader)'
    if t in ('{', '}', '};'):
        own = info[j][2]
        word = 'فتحة' if t == '{' else 'قفلة'
        return f'{word} <code>{html.escape(t)}</code> بتاعة <code>{html.escape(_short(own or "", 36))}</code> (السطر {j + 1})'
    return f'السطر {j + 1} (<code>{html.escape(_short(t))}</code>)'

def _where(rows, k):
    """List of (first_line_no, last_line_no, text) for each block of new lines."""
    info = _scopes(rows)
    main_at = next((i for i, (_, t, _) in enumerate(rows) if _re.search(r'\bmain\s*\(', t) and not t.strip().endswith(';') and not info[i][1] and 'R"(' not in t), None)
    hunks, i = [], 0
    while i < len(rows):
        if rows[i][2] == k:
            j = i
            while j + 1 < len(rows) and (rows[j + 1][2] == k or (rows[j + 1][2] is None and j + 2 < len(rows) and rows[j + 2][2] == k)):
                j += 1
            hunks.append((i, j)); i = j + 1
        else:
            i += 1
    out = []
    for a, b in hunks:
        prev = next((x for x in range(a - 1, -1, -1) if rows[x][1].strip() and rows[x][2] != k), None)
        nxt = next((x for x in range(b + 1, len(rows)) if rows[x][1].strip() and rows[x][2] != k), None)
        owner, raw, _ = info[a]
        scope = _describe_scope(owner, raw, None if main_at is None else a < main_at)
        if prev is None and nxt is None:
            pos = 'ده أول كود في الملف'
        elif prev is None:
            pos = 'في أول الملف، قبل ' + _anchor(rows, info, nxt)
        else:
            pos = 'بعد ' + _anchor(rows, info, prev)
            if nxt is None:
                pos += '، في آخر الملف'
            elif rows[nxt][1].strip() not in ('{',):
                pos += '، وقبل ' + _anchor(rows, info, nxt)
        lines = f'السطر {a + 1}' if a == b else f'السطور {a + 1}–{b + 1}'
        out.append(f'<b>{lines}:</b> {scope}، {pos}.')
    return out

import sys as _s2
_s2.path.insert(0, '/home/claude/steps/wordsdata')
import lookup as WL
def _day(path):
    m = _re.search(r'/day(\d)/', path); return int(m.group(1)) if m else 1
def anchor(pid, f, ln):
    return _re.sub(r'[^A-Za-z0-9_-]', '-', f'{pid}-{f}-{ln}')

def _code_view(prog, k, hl, mode='pdf'):
    blocks = []
    for f in prog.files_at(k):
        rows = prog.code_at(f, k)
        new_idx = [i for i, (_, _, s) in enumerate(rows) if s == k]
        newfile = all(s == k or s is None for _, _, s in rows)
        # ranges of new lines (for the one-line summary)
        rng, i = [], 0
        while i < len(rows):
            if rows[i][2] == k:
                j = i
                while j + 1 < len(rows) and (rows[j + 1][2] == k or (rows[j + 1][2] is None and j + 2 < len(rows) and rows[j + 2][2] == k)):
                    j += 1
                rng.append(f'{i + 1}' if i == j else f'{i + 1}–{j + 1}'); i = j + 1
            else:
                i += 1
        out, words = [], []
        day = _day(prog.files[f])
        for i, (ln, text, s) in enumerate(rows):
            cls = 'new' if s == k else 'old'
            body = hl(text) if s == k else (html.escape(text) or '&nbsp;')
            wd = WL.get(text, day) if s == k else None
            if wd:
                a = anchor(prog.pid, f, ln)
                out.append(f'<span class="{cls}" id="sl-{a}"><i class="ln">{i + 1:>3}</i> {body} <a class="wl-go" href="#sw-{a}">🔍</a></span>')
                words.append(f'<div class="wline" id="sw-{a}"><div class="wbacks"><a class="wl-back" href="#sl-{a}">↩ ارجع للسطر في الخطوة</a>'
                             f'<a class="wl-back wl-back2" href="#tr-{a}">↩ ارجع لجدول البرنامج</a></div>'
                             f'<div class="wcode"><i class="ln">{i + 1}</i><span class="ltr">{html.escape(text.strip())}</span></div>{wd}</div>')
            else:
                out.append(f'<span class="{cls}"><i class="ln">{i + 1:>3}</i> {body}</span>')
        if newfile and new_idx:
            tag = '<div class="wwhere"><span class="pin">📄 ملف جديد:</span> اعمله واكتب فيه الكود ده كله.</div>'
        elif new_idx:
            tag = '<div class="wwhere"><span class="pin">🟨 الجديد في الخطوة دي:</span> ' + ('السطر ' if len(rng) == 1 and '–' not in rng[0] else 'السطور ') + '، '.join(rng) + '. والباقي زي ما هو من الخطوة اللي فاتت.</div>'
        else:
            tag = '<div class="wwhere" style="background:#f8fafc;border-color:#cbd5e1"><span class="pin" style="color:#475569">الملف ده ماتغيرش في الخطوة دي.</span></div>'
        if not new_idx and len(prog.src) > 1:
            continue  # unchanged file in a multi-file project: skip to keep it short
        aid = _re.sub(r'[^A-Za-z0-9_-]', '-', f'st-{prog.pid}-s{k}-{f}')
        raw = '\n'.join(t for _, t, _ in rows) + '\n'
        label = html.escape(f)
        if mode == 'web':
            head = (f'<div class="copybar" id="{aid}"><span class="fname"><span class="ltr">{label}</span></span>'
                    f'<button type="button" class="copy" data-src="src-{aid}">📋 نسخ الكود كامل</button></div>'
                    f'<pre class="rawsrc" id="src-{aid}" hidden>{html.escape(raw)}</pre>')
        else:
            import steps_hook as _STH
            link = _STH.copylink(aid, label, raw, k)
            head = f'<div class="wfile"><span class="ltr">{label}</span>{link}</div>'
        blocks.append(head + tag + '<div class="wcode">' + ''.join(out) + '</div>')
        if words:
            blocks.append('<div class="wkw">🔍 كلمة كلمة: كل سطر جديد في الخطوة دي</div>' + ''.join(words))
    return ''.join(blocks)

def render(prog, hl, mode, imgdir, imgprefix='img/'):
    res = prog.results
    n = len(prog.steps)
    h = [f'<div class="wsteps"><div class="wsh">✍️ اكتبه بنفسك خطوة خطوة · {n} خطوات</div>'
         '<div class="wsub">ابدأ من ملف فاضي. كل خطوة فيها <b>الكود كامل</b> زي ما المفروض يبقى عندك بعدها: السطور <b>بالأصفر</b> هي اللي هتزوّدها، والرمادي موجود عندك من قبل. والأرقام على الشمال = رقم السطر في الملف. '
         'وبعد كل خطوة اعمل Run: لازم تشوف نفس النتيجة اللي تحت، لأننا شغّلنا كل خطوة فعلاً.</div>']
    for k, st in enumerate(prog.steps, 1):
        r = res[k - 1]
        assert r['build_ok'], (prog.pid, k, r['build'][:300])
        body = f'<div class="wstep"><div class="wsth"><span class="n">{k}</span>{st["title"]}</div>'
        if st.get('why'):
            body += f'<div class="wwhy">{st["why"]}</div>'
        body += _code_view(prog, k, hl, mode)
        # result
        out = (r.get('out') or '').rstrip('\n')
        parts = ''
        if r.get('shot'):
            name = f'steps_{prog.pid}_s{k}.png'
            os.makedirs(imgdir, exist_ok=True)
            shutil.copy(r['shot'], os.path.join(imgdir, name))
            parts += f'<img src="{imgprefix}{name}">'
        if out:
            parts += f'<div class="wterm">{html.escape(out)}</div>'
        if not st.get('note') and ('unused variable' in r.get('build', '') or 'defined but not used' in r.get('build', '')):
            st = dict(st, note='الـ compiler ممكن يطلّع تحذير (warning) إن فيه متغير لسه مش مستخدم. ده عادي: هيتستخدم في الخطوة الجاية.')
        if not parts:
            note = st.get('note') or ('البرنامج اشتغل وقفل على طول، ومطبعش حاجة.' if prog.kind == 'cli' else 'البرنامج اشتغل وقفل على طول: لسه مفيش شباك.')
            parts = f'<div class="none">{note}</div>'
        elif st.get('note'):
            parts += f'<div class="none" style="flex-basis:100%">{st["note"]}</div>'
        body += f'<div class="wres" style="flex-wrap:wrap"><span class="lbl">▶ Run:</span>{parts}</div>'
        body += '</div>'
        h.append(body)
    h.append('</div>')
    return ''.join(h)
