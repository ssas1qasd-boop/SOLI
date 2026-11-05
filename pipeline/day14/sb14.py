# Week 3 Day 7 storyboards (values from the real runs).
import sys, re
sys.path.insert(0, '/home/claude/day2')
from sb import cell, lbl, arr, region, cross, termbox, frame, story, BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, RED, GREEN, PINK

T = open('/home/claude/day14/src/p2_string.txt').read()
B1, B2 = re.search(r'buffers: (0x[0-9a-f]+) and (0x[0-9a-f]+)', T).groups()
def short(a): return '…' + a[-4:]


def d14_string():
    def sc(objs, bufs, term):
        s = region(6, 16, 120, 96, 'STACK', TEAL, '#ecfdf5') + region(134, 16, 180, 96, 'HEAP', ORANGE, '#fff7ed')
        for i, (n, st) in enumerate(objs):
            s += cell(14, 32 + i * 40, 104, 30, n, st, 9.5)
        for i, (v, st) in enumerate(bufs):
            s += cell(144, 32 + i * 40, 160, 30, v, st, 10)
            s += arr(118, 47 + i * 40, 144, 47 + i * 40, ORANGE)
        return s + termbox(6, 118, 308, term)
    f = [frame(1, 'String string = "Cherno";', sc([('string', 'new')], [('C h e r n o \\0  ' + short(B1), 'new')], ['(nothing printed)']), 'strlen = 6، و Buffer من 7 بايت.', 150),
         frame(2, 'String second = string;', sc([('string', 'n'), ('second', 'new')], [('C h e r n o \\0  ' + short(B1), 'n'), ('C h e r n o \\0  ' + short(B2), 'new')], ['Copied!']), 'الـ Copy Constructor عمل Buffer جديد.', 150),
         frame(3, "second[2] = 'a';", sc([('string', 'n'), ('second', 'n')], [('C h e r n o', 'n'), ('C h a r n o', 'chg')], ['Cherno / Charno']), 'النسخة بس اتغيرت.', 150),
         frame(4, 'PrintByValue(string);  PrintByReference(string);', sc([('string', 'n'), ('copy (dies)', 'free')], [('C h e r n o', 'n'), ('C h e r n o', 'free')], ['Copied!', 'by value: Cherno', 'by const reference: Cherno']), 'بالقيمة: نسخة اتعملت وماتت. بالـ Reference: ولا حاجة.', 150)]
    return story('Deep Copy خطوة خطوة', 'البرنامج 2 · string.cpp', f)


def d14_git():
    def g(commits, file, term):
        s = region(6, 16, 308, 60, 'commits', PURPLE, '#f5f3ff')
        for i, (h, c) in enumerate(commits):
            s += cell(14 + i * 74, 32, 68, 30, h, c, 9.5)
        s += lbl(14, 92, 'site.css: ' + file, INK, 10, 'start', True)
        return s + termbox(6, 100, 308, term)
    f = [frame(1, 'git add site.css', g([], 'blue', ['?? site.css', 'A  site.css']), '?? = مش متابع، و A = في الـ Staging.', 140),
         frame(2, 'git commit -m "v1: blue"', g([('372ae88', 'new')], 'blue', ['(commit made)']), 'أول لقطة.', 140),
         frame(3, 'v2, v3, v4 (commit -a)', g([('372ae88', 'n'), ('a25f620', 'new'), ('e846659', 'new'), ('c03766c', 'new')], 'orange', ['M site.css', '-body { color: blue; }', '+body { color: pink; }']), 'العميل غيّر 3 مرات، وكل مرة Commit.', 140),
         frame(4, 'git checkout 372ae88 -- site.css', g([('372ae88', 'hot'), ('a25f620', 'n'), ('e846659', 'n'), ('c03766c', 'n')], 'blue', ['site.css now: body { color: blue; }', "files: ['site.css']"]), 'رجعنا الأصل، وفي الفولدر ملف واحد بس.', 140)]
    return story('من الملف للـ Commit', 'البرنامج 1 · git_record.py', f)
