# Week 3 Day 6 storyboards: each frame = the line that just ran + the state after it (values from the real runs).
import sys
sys.path.insert(0, '/home/claude/day2')
from sb import cell, lbl, arr, region, cross, termbox, frame, story, BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, RED, GREEN, PINK


def d13_life():
    def st(books, heap=None, term=None):
        s = region(6, 16, 190, 100, 'STACK (books)', TEAL, '#ecfdf5')
        for i, (t, stt) in enumerate(books):
            s += cell(14, 92 - i * 24, 174, 20, t, stt, 9.5)
        s += region(204, 16, 110, 100, 'HEAP', ORANGE, '#fff7ed')
        if heap: s += cell(212, 40, 94, 24, heap[0], heap[1], 9.5)
        if term: s += termbox(6, 122, 308, term)
        return s
    f = [frame(1, 'Entity a("a");   {  Entity b("b");', st([('main: a', 'n'), ('{ }: b', 'new')], None, ['Created Entity a', 'Created Entity b']), 'كتابين: main وفوقه الـ Scope الفاضي.', 152),
         frame(2, '}   // end of the empty scope', st([('main: a', 'n'), ('{ }: b', 'free')], None, ['end of the empty scope', 'Destroyed Entity b']), 'الكتاب اللي فوق اتشال، و b مات معاه.', 152),
         frame(3, '{  Entity* h = new Entity("heap");  }', st([('main: a', 'n'), ('{ }: h (pointer)', 'free')], ('Entity heap', 'warn'), ['Created Entity heap', 'end of the scope with new: heap ...']), 'الـ Pointer مات، والـ Entity لسه على الـ Heap ومحدش يعرف عنوانه.', 152),
         frame(4, 'return 0;  }   // end of main', st([('main: a', 'free')], ('Entity heap', 'warn'), ['main ends', 'Destroyed Entity a']), 'a مات آخر حاجة. و heap عمره ما اتمسح.', 152)]
    return story('الكتب على الـ Stack', 'البرنامج 1 · lifetime.cpp', f)


def d13_scoped():
    def sc(stack, heap, term, extra=''):
        s = region(6, 16, 150, 70, 'STACK', TEAL, '#ecfdf5') + region(164, 16, 150, 70, 'HEAP', ORANGE, '#fff7ed')
        if stack: s += cell(14, 36, 134, 30, stack[0], stack[1], 10)
        if heap: s += cell(172, 36, 134, 30, heap[0], heap[1], 10)
        if stack and heap and stack[1] != 'free': s += arr(148, 51, 172, 51, ORANGE)
        return s + termbox(6, 94, 308, term) + extra
    f = [frame(1, 'ScopedPtr e = new Entity();', sc(('ScopedPtr e', 'new'), ('Entity', 'new'), ['Created Entity']), 'new على الـ Heap، والعنوان جوه ScopedPtr على الـ Stack.', 136),
         frame(2, '}   // ~ScopedPtr() -> delete m_Ptr', sc(('ScopedPtr e', 'free'), ('Entity', 'free'), ['inside the scope', 'Destroyed Entity']), 'عند القوس: Destructor بتاع ScopedPtr عمل delete.', 136),
         frame(3, 'std::unique_ptr<Entity> u = std::make_unique<Entity>();', sc(('unique_ptr u', 'new'), ('Entity', 'new'), ['after the scope (ScopedPtr)', 'Created Entity']), 'نفس الحاجة بالمكتبة.', 136),
         frame(4, '{  Timer t("loop");  ...  }', sc(('Timer t', 'free'), None, ['sum = 4950', 'Timer loop: more than 0 ns']), 'الـ Timer وقف وطبع لوحده عند القوس.', 136)]
    return story('ScopedPtr و Timer', 'البرنامج 2 · scoped_ptr.cpp', f)
