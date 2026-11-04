KW = r'\b(void|int|float|double|char|bool|const|class|public|return|if|else|while|for|new|delete|nullptr|true|false|uniform|in|out|layout|vec2|vec3|vec4|mat4)\b'
def hl(line):
    t = html.escape(line, quote=False)
    m = re.search(r'(//.*$|#\w.*$)', t)
    tail = ''
    if m: t, tail = t[:m.start()], f'<span class="cm">{m.group(0)}</span>'
    parts = re.split(r'("[^"]*")', t)
    out = []
    for p in parts:
        if p.startswith('"'): out.append(f'<span class="st">{p}</span>'); continue
        p = re.sub(KW, r'<span class="kw">\1</span>', p)
        p = re.sub(r'(?<![\w#.])(\d+\.?\d*f?)\b', r'<span class="nu">\1</span>', p)
        out.append(p)
    return ''.join(out) + tail
