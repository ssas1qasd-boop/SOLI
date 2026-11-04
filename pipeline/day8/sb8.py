# Week 3 Day 1 storyboards: each frame = the line that just ran + the state after it.
import sys
sys.path.insert(0, '/home/claude/day2')
from sb import cell, lbl, arr, region, cross, termbox, frame, story, BLUE, TEAL, ORANGE, PURPLE, GRAY, INK, RED, GREEN, PINK


def d8_player():
    def obj(y, name, vals, st):
        s = lbl(20, y + 17, name, BLUE, 10, 'start', True)
        for k, (n, v) in enumerate(zip(('x', 'y', 'speed'), vals)):
            s += cell(80 + k * 74, y, 70, 26, v, st[k], 11) + lbl(115 + k * 74, y + 38, n, GRAY, 8.5)
        return s
    STK = region(10, 16, 300, 112, 'STACK')
    f = [frame(1, 'Player player;  player.x = 0; player.y = 0; player.speed = 2;', STK + obj(34, 'player', ('0', '0', '2'), ('new', 'new', 'new')),
               '12 بايت على الـ Stack: x و y و speed جنب بعض.', 135),
         frame(2, 'player.Move(1, -1);', STK + obj(34, 'player', ('2', '-2', '2'), ('chg', 'chg', 'n')) + termbox(10, 92, 300, ['this = &player  ->  x += 1*2, y += -1*2']),
               'جوه الدالة <code>x</code> = <code>player.x</code>، لأن <code>this</code> = عنوان player.', 135),
         frame(3, 'Move(player, 1, -1);', STK + obj(34, 'player', ('4', '-4', '2'), ('chg', 'chg', 'n')) + termbox(10, 92, 300, ['player& -> the same 12 bytes']),
               'نفس النتيجة بالدالة اللي برّه: الـ Reference بيشاور على نفس الـ 12 بايت.', 135),
         frame(4, 'Player enemy; …  enemy.Move(-1, 0);', region(10, 16, 300, 124, 'STACK') + obj(34, 'player', ('4', '-4', '2'), ('n', 'n', 'n')) + obj(84, 'enemy', ('5', '10', '5'), ('chg', 'new', 'new')),
               'Object تاني ليه متغيراته. نفس الدالة <code>Move</code> غيّرت enemy بس.', 150)]
    return story('Object في الرام والـ Method', 'البرنامج 1 · player.cpp', f)


def d8_texture():
    def scene(ram, gpu, slot, shader, note=None):
        s = region(8, 16, 96, 96, 'RAM', BLUE, '#eff6ff') + region(112, 16, 96, 96, 'GPU texture', TEAL, '#ecfdf5') + region(216, 16, 96, 96, 'slot / shader', PURPLE, '#f5f3ff')
        if ram: s += cell(14, 44, 84, 40, ram, 'new' if ram != 'freed' else 'free', 9)
        if gpu: s += cell(118, 44, 84, 40, gpu, 'chg' if gpu.startswith('id') else 'gpu', 9)
        if slot: s += cell(222, 36, 84, 24, slot, 'hot', 9)
        if shader: s += cell(222, 70, 84, 24, shader, 'pink', 8.5)
        if note: s += termbox(8, 118, 304, [note])
        return s
    f = [frame(1, 'stbi_load("res/logo.png", …, 4)', scene('128x128x4 B', '', '', '', 'width = 128, height = 128, channels = 4'), '64 ألف بايت (128 × 128 × 4) في الرام، والصورة مقلوبة فوق-تحت.', 145),
         frame(2, 'glGenTextures · glBindTexture · glTexParameteri x4', scene('128x128x4 B', 'id 1 (empty)', '', ''), 'Texture فاضية في الكارت رقمها 1، والإعدادات الأربعة اتحطت.', 120),
         frame(3, 'glTexImage2D(…, pixels);  stbi_image_free(pixels);', scene('freed', 'id 1: pixels', '', ''), 'البكسلات اتنسخت للكارت، فرجّعنا الرام.', 120),
         frame(4, 'texture.Bind(0);  glUniform1i(location, 0);', scene('freed', 'id 1: pixels', 'slot 0 = id 1', 'u_Texture = 0', 'frame 0 drawn, glGetError() = 0'), 'الخانة 0 فيها الـ Texture، والـ Shader بيقرا من الخانة 0.', 145)]
    return story('الصورة من الملف للكارت', 'البرنامج 1 · texture.cpp', f)


def d8_brep():
    def scene(v, e, fc, res, st='n'):
        s = cell(10, 24, 92, 34, f'V = {v}', 'new', 11) + cell(114, 24, 92, 34, f'E = {e}', 'new', 11) + cell(218, 24, 92, 34, f'F = {fc}', st, 11)
        s += termbox(10, 72, 300, res)
        return s
    f = [frame(1, 'cube.Report();', scene(8, 12, 6, ['F - E + V = 2', 'edges not shared by 2 faces = 0']), 'مكعب مقفول: أويلر = 2، ومفيش ضلع مكشوف.', 130),
         frame(2, 'pyramid.Report();', scene(5, 8, 5, ['F - E + V = 2', 'edges not shared by 2 faces = 0']), 'هرم: أعداد مختلفة، ونفس الـ 2.', 130),
         frame(3, 'open.faces.erase(open.faces.begin() + 1);  open.Report();', scene(8, 12, 5, ['F - E + V = 1', 'edges not shared by 2 faces = 4'], 'warn'), 'شلنا الغطا: أويلر بقى 1، والـ 4 أضلاع اللي حوالين الفتحة بقت مكشوفة.', 130)]
    return story('الفحص بيمسك الجسم المفتوح', 'البرنامج 1 · brep.cpp', f)
