# Day 7 storyboards: each frame = the line that just ran + the state after it.
import sys
sys.path.insert(0, '/home/claude/day2')
from sb import cell, lbl, arr, region, cross, termbox, frame, story, BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, RED, GREEN, PINK


def d7_ptr():
    STK = region(10, 18, 150, 118, 'STACK')
    HEAP = region(172, 18, 140, 70, 'HEAP', ORANGE, '#fffaf5')
    def var(v, st): return cell(20, 36, 60, 26, v, st, 12) + lbl(110, 53, 'var', BLUE, 9.5, 'middle', True)
    def heap(vals, st='n'):
        s = HEAP
        for k, v in enumerate(vals): s += cell(180 + k * 16, 44, 14, 24, v, 'chg' if st == 'chg' and k < 2 else 'new' if st == 'new' else 'n', 8.5)
        return s
    f = [frame(1, 'int* intPtr = &var;  *intPtr = 10;', STK + var(10, 'chg') + cell(20, 72, 60, 26, '&var', 'ptr', 9) + lbl(115, 89, 'intPtr', BLUE, 9.5, 'middle', True) + arr(50, 72, 50, 64, GREEN),
               'النجمة مشيت على السهم وكتبت 10 في <code>var</code>.', 145),
         frame(2, 'char* buffer = new char[8];  memset(buffer, 0, 8);', STK + var(10, 'n') + cell(20, 104, 60, 26, 'addr', 'ptr', 9) + lbl(115, 121, 'buffer', BLUE, 9.5, 'middle', True) + heap('00000000', 'new') + arr(80, 117, 180, 62, ORANGE),
               '8 بايت جداد على الـ Heap، كلهم صفر. <code>buffer</code> على الـ Stack شايل عنوانهم.', 145),
         frame(3, "buffer[0] = 'H';  *(buffer + 1) = 'i';", STK + var(10, 'n') + cell(20, 104, 60, 26, 'addr', 'ptr', 9) + lbl(115, 121, 'buffer', BLUE, 9.5, 'middle', True) + heap('Hi000000', 'chg') + arr(80, 117, 180, 62, ORANGE),
               'طريقتين لنفس الحاجة: <code>[0]</code> و <code>*(buffer + 1)</code>. النص بقى <code>Hi</code> (الصفر بعده = آخر النص).', 145),
         frame(4, 'delete[] buffer;  buffer = nullptr;', STK + var(10, 'n') + cell(20, 104, 60, 26, 'nullptr', 'n', 9) + lbl(115, 121, 'buffer', BLUE, 9.5, 'middle', True) + region(172, 18, 140, 70, 'HEAP', GRAY, '#f3f4f6') + lbl(242, 60, 'returned', GRAY, 10, 'middle', True),
               'الـ 8 بايت رجعوا للنظام، و <code>buffer</code> بقى nullptr (صفر) عشان محدش يستخدم العنوان القديم.', 145)]
    return story('العناوين والـ Heap', 'البرنامج 1 · pointers_review.cpp', f)


def d7_vao():
    def scene(bound_vao, bound_ibo, bound_prog, note_draw=None):
        s = region(10, 16, 150, 112, 'CURRENT (bound)')
        s += lbl(20, 40, 'program', GRAY, 9, 'start') + cell(80, 28, 70, 20, bound_prog, 'chg' if bound_prog != '0' else 'free', 9)
        s += lbl(20, 66, 'VAO', GRAY, 9, 'start') + cell(80, 54, 70, 20, bound_vao, 'chg' if bound_vao != '0' else 'free', 9)
        s += lbl(20, 92, 'element', GRAY, 9, 'start') + cell(80, 80, 70, 20, bound_ibo, 'chg' if bound_ibo != '0' else 'free', 9)
        s += region(172, 16, 140, 112, 'inside vao', TEAL, '#ecfdf5') + cell(180, 36, 124, 22, 'attr 0 -> buffer', 'gpu', 9) + cell(180, 64, 124, 22, 'element -> ibo', 'gpu', 9)
        if note_draw: s += termbox(172, 98, 140, [note_draw])
        return s
    f = [frame(1, 'glBindVertexArray(vao);  glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo);', scene('vao', 'ibo', 'shader'), 'وقت الإعداد: كل ربط اتسجل جوه الـ VAO.', 140),
         frame(2, 'glUseProgram(0);  glBindVertexArray(0);  glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0);', scene('0', '0', '0'), 'فكّينا كل حاجة. اللي جوه الـ VAO لسه محفوظ.', 140),
         frame(3, 'glUseProgram(shader); glBindVertexArray(vao);', scene('vao', 'ibo', 'shader'), 'في اللوب: سطرين رجّعوا كل حاجة. صندوق الترتيب رجع لوحده مع الـ VAO.', 140),
         frame(4, 'glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, nullptr);', scene('vao', 'ibo', 'shader', 'glGetError() = 0'), 'الرسم شغال، ومفيش ولا أمر اترفض.', 140)]
    return story('نفك كل حاجة ونرجعها بسطر', 'البرنامج 1 · vertex_array.cpp', f)


def d7_git():
    def scene(work, stage, repo, out=None):
        s = region(8, 16, 96, 70, 'folder', ORANGE, '#fff7ed') + region(112, 16, 96, 70, 'staging', BLUE, '#eff6ff') + region(216, 16, 96, 70, '.git', GREEN, '#ecfdf5')
        if work: s += cell(14, 40, 84, 24, work, 'hot', 8.5)
        if stage: s += cell(118, 40, 84, 24, stage, 'new', 8.5)
        for k, r in enumerate(repo): s += cell(222, 32 + k * 26, 84, 22, r, 'chg', 8.5)
        if out: s += termbox(8, 92, 304, out)
        return s
    f = [frame(1, 'git init  ·  git status', scene('refactored.cpp', '', [], ['Untracked files: refactored.cpp']), 'الملف موجود في الفولدر، و Git لسه مش متابعه (Untracked).', 135),
         frame(2, 'git add .', scene('', 'refactored.cpp', [], ['new file:   refactored.cpp']), 'اتنقل للـ Staging: جاهز للـ Commit.', 135),
         frame(3, 'git commit -m "add refactored polyline tool"', scene('', '', ['84180e1'], ['[master (root-commit) 84180e1]', ' 1 file changed, 227 insertions(+)']), 'نقطة حفظ أولى: 227 سطر اتضافوا.', 148),
         frame(4, 'edit 10.0f -> 12.0f  ·  git add .  ·  git commit', scene('', '', ['84180e1', 'ed785af'], ['[master ed785af]', ' 1 insertion(+), 1 deletion(-)']), 'سطر واحد اتغير = سطر اتشال وسطر اتضاف. ونقطة حفظ تانية فوق الأولى.', 148)]
    return story('الملف بيتنقل من صندوق لصندوق', 'المحاضرة 4 · جلسة Git حقيقية', f)
