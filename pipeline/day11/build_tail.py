css += STH.CSS
css += Q.CSS + SB.CSS
P.insert(1, Q.quick_section(Q11.DAY11_CARDS, Q11.DAY11_QA, MODE))
if MODE != 'web':
    P.append(Q.answers_section(Q11.DAY11_QA))
P = [Q.tag_reference(x) for x in P]
import linenums as LN
if MODE != 'web': P.append(STH.copy_appendix())
P = [JUMP.apply(''.join(P), LN, ART if MODE != 'web' else '')]
css += STH.CSS if MODE != 'web' else ''
css += LN.CSS + JUMP.CSS
if MODE == 'web':
    body = "".join(P)
    body = re.sub(r'src="(img/[^"]+\.png)"', lambda m: 'src="data:image/png;base64,' + base64.b64encode(open(m.group(1), 'rb').read()).decode() + '"', body)
    webcss = open('/home/claude/day1/web.css', encoding='utf-8').read()
    js = open('/home/claude/day1/web.js', encoding='utf-8').read()
    page = ('<title>محاضرات الأسبوع 3 · اليوم الرابع</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=JetBrains+Mono:wght@400;600&display=swap">'
            f'<style>{css}\n{webcss}</style>\n<div class="page" dir="rtl" lang="ar">{body}</div>\n<div class="toast" id="toast" role="status" aria-live="polite" hidden></div>\n<script>{js}</script>\n')
    open('week3_day4_web.html', 'w', encoding='utf-8').write(page)
    print('built web', len(page))
else:
    doc = f'<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>الأسبوع 3 - اليوم الرابع</title><style>{css}</style></head><body>{"".join(P)}</body></html>'
    open('week3_day4.html', 'w', encoding='utf-8').write(doc)
    weasyprint.HTML('week3_day4.html', base_url='.').write_pdf('Week3_Day4_Wednesday.pdf')
    import fixpdf; fixpdf.fix('Week3_Day4_Wednesday.pdf')
    print('built pdf')
if STH.missing(): print('STEPS NOT PLACED:', STH.missing())
