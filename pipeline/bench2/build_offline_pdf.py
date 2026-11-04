import os, pymupdf as fitz
from PIL import Image
src=open('/home/claude/sim/three.min.js').read()
tag='<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>'
cells={'d1_u1':(1,'bench_day1_draw_uniforms'),'d1_cam':(1,'bench_day1_cad_camera'),'d2_va1':(2,'bench_day2_draw_vertex_colors'),'d3_s1':(3,'bench_day3_draw_shader_file'),'d3_l1':(3,'bench_day3_cad_line'),'d4_e1':(4,'bench_day4_draw_ebo_rect'),'d4_v1':(4,'bench_day4_cad_lines'),'d5_r2':(5,'bench_day5_draw_shader_edit'),'d5_c2':(5,'bench_day5_cad_delete_last_line'),'d5_p1':(5,'bench_day5_prog_swap'),'d5_n2':(5,'bench_day5_math_numpy'),'d1_p1':(1,'bench_day1_prog_pointers'),'d1_dot':(1,'bench_day1_math_dot'),'d2_c1':(2,'bench_day2_prog_c'),'d2_d1':(2,'bench_day2_math_dot_length'),'d2_v4':(2,'bench_day2_cad_vector_points'),'d3_r1':(3,'bench_day3_prog_references'),'d3_x1':(3,'bench_day3_math_cross'),'d4_st1':(4,'bench_day4_prog_static_const'),'d4_x1':(4,'bench_day4_math_cross_khan'),'d6_p1':(6,'bench_day6_prog_compiler'),'d6_r1':(6,'bench_day6_draw_animated_colors'),'d6_m1':(6,'bench_day6_math_dot_length'),'d6_c1':(6,'bench_day6_cad_refactoring'),'d7_p1':(7,'bench_day7_prog_pointers_review'),'d7_r2':(7,'bench_day7_draw_vertex_arrays'),'d7_m1':(7,'bench_day7_math_cross_quiz'),'d7_c1':(7,'bench_day7_cad_commit_id'),'d8_p1':(8,'bench_week3_day1_prog_classes'),'d8_t1':(8,'bench_week3_day1_draw_textures'),'d8_m1':(8,'bench_week3_day1_math_matrices'),'d8_c1':(8,'bench_week3_day1_cad_brep'),'d9_p1':(9,'bench_week3_day2_prog_struct_class'),'d9_t1':(9,'bench_week3_day2_draw_stb_image'),'d9_m1':(9,'bench_week3_day2_math_transformations'),'d9_c1':(9,'bench_week3_day2_cad_triangle_mesh')}
def make(d, start=None):
    h=open(f'bench_day{d}.html').read(); assert tag in h
    h=h.replace(tag,'<script>'+src.replace('</script','<\\/script')+'</script>')
    h=h.replace('<title>', '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>',1)
    if start: h=h.replace('<script id="data"', f'<script>window.BENCH_START="{start}"</script>\n<script id="data"',1)
    if start:
        import json as _j
        i=h.index('<script id="data" type="application/json">')+len('<script id="data" type="application/json">'); k=h.index('</script>', i)
        D=_j.loads(h[i:k].replace('<\\/','</'))
        for pp in D['programs']:
            if pp['id']!=start: pp.pop('fmap',None)
        h=h[:i]+_j.dumps(D,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+h[k:]
    return h
os.makedirs('offline',exist_ok=True)
for f in os.listdir('offline'): os.remove('offline/'+f)
DAYFILE={d:f'bench_day{d}' for d in range(1,8)}; DAYFILE[8]='bench_week3_day1'; DAYFILE[9]='bench_week3_day2'
for d in [1,2,3,4,5,6,7,8,9]: open(f'offline/{DAYFILE[d]}.html','w').write(make(d))
for pid,(d,fn) in cells.items(): open(f'offline/{fn}.html','w').write(make(d,pid))
W='/tmp/claude-0/wk/'; OFF='offline/'
d=fitz.open(W+'w.pdf'); PG={k:d[2] for k in range(1,8)}; PG[8]=d[3]; PG[9]=d[3]
rows={1:(87,238.5,110.9),2:(238.5,410.2,263.1),3:(410.2,683.2,434.1),4:(683.2,865.5,707.1),5:(865.5,1025.8,890.1),6:(1025.8,1197.0,1051.4),7:(1197.0,1360.5,1222.4),8:(87,238.5,110.9),9:(238.5,390.0,263.1)}
WORDS={k:PG[k].get_text('words') for k in PG}  # PG 8 and 9 share page 3: read words before any insert
cl=[(1,131,194,'bench_day1_draw_uniforms','اليوم 1 · رسم: Uniforms'),(1,5.8,68,'bench_day1_cad_camera','اليوم 1 · CAD: الكاميرا والماوس'),
    (2,131,194,'bench_day2_draw_vertex_colors','اليوم 2 · رسم: ألوان بالـ vertex'),(3,131,194,'bench_day3_draw_shader_file','اليوم 3 · رسم: الـ Shader من ملف'),
    (3,5.8,68,'bench_day3_cad_line','اليوم 3 · CAD: خط بين نقطتين'),(4,131,194,'bench_day4_draw_ebo_rect','اليوم 4 · رسم: EBO مستطيل'),(4,5.8,68,'bench_day4_cad_lines','اليوم 4 · CAD: عدة خطوط'),
    (5,131,194,'bench_day5_draw_shader_edit','اليوم 5 · رسم: تعديل الـ Shader'),(5,5.8,68,'bench_day5_cad_delete_last_line','اليوم 5 · CAD: مسح آخر خط'),
    (5,194,257,'bench_day5_prog_swap','اليوم 5 · برمجة: swap بالـ Pointers'),(5,68,131,'bench_day5_math_numpy','اليوم 5 · رياضيات: dot و cross في NumPy'),
    (1,194,257,'bench_day1_prog_pointers','اليوم 1 · برمجة: Pointers'),(1,68,131,'bench_day1_math_dot','اليوم 1 · رياضيات: الضرب النقطي'),
    (2,194,257,'bench_day2_prog_c','اليوم 2 · برمجة: لغة C و Pointers'),(2,68,131,'bench_day2_math_dot_length','اليوم 2 · رياضيات: الضرب النقطي والطول'),(2,5.8,68,'bench_day2_cad_vector_points','اليوم 2 · CAD: النقط في vector'),
    (3,194,257,'bench_day3_prog_references','اليوم 3 · برمجة: References و Hamming'),(3,68,131,'bench_day3_math_cross','اليوم 3 · رياضيات: الضرب الاتجاهي'),
    (4,194,257,'bench_day4_prog_static_const','اليوم 4 · برمجة: Static و Const'),(4,68,131,'bench_day4_math_cross_khan','اليوم 4 · رياضيات: Cross product تمارين'),
    (6,194,257,'bench_day6_prog_compiler','اليوم 6 · برمجة: Compiler صغير و exercism'),(6,131,194,'bench_day6_draw_animated_colors','اليوم 6 · رسم: ألوان متحركة'),(6,68,131,'bench_day6_math_dot_length','اليوم 6 · رياضيات: مراجعة dot والطول'),(6,5.8,68,'bench_day6_cad_refactoring','اليوم 6 · CAD: تنظيف الكود'),
    (7,194,257,'bench_day7_prog_pointers_review','اليوم 7 · برمجة: مراجعة الـ Pointers'),(7,131,194,'bench_day7_draw_vertex_arrays','اليوم 7 · رسم: تجربة حرة بالـ Vertex Arrays'),(7,68,131,'bench_day7_math_cross_quiz','اليوم 7 · رياضيات: اختبر نفسك Cross product'),(7,5.8,68,'bench_day7_cad_commit_id','اليوم 7 · CAD: الـ ID بتاع الـ Commit'),
    (8,194,257,'bench_week3_day1_prog_classes','الأسبوع 3 · اليوم 1 · برمجة: الـ Classes'),(8,131,194,'bench_week3_day1_draw_textures','الأسبوع 3 · اليوم 1 · رسم: الـ Textures'),(8,68,131,'bench_week3_day1_math_matrices','الأسبوع 3 · اليوم 1 · رياضيات: المصفوفات'),(8,5.8,68,'bench_week3_day1_cad_brep','الأسبوع 3 · اليوم 1 · CAD: الـ B-Rep'),
    (9,194,257,'bench_week3_day2_prog_struct_class','الأسبوع 3 · اليوم 2 · برمجة: struct مقابل class'),(9,131,194,'bench_week3_day2_draw_stb_image','الأسبوع 3 · اليوم 2 · رسم: تحميل صورة بـ stb_image'),(9,68,131,'bench_week3_day2_math_transformations','الأسبوع 3 · اليوم 2 · رياضيات: التحويلات الخطية'),(9,5.8,68,'bench_week3_day2_cad_triangle_mesh','الأسبوع 3 · اليوم 2 · CAD: vertex و edge و face')]
T=[]
for day,(y0,y1,tb) in rows.items():
    p=PG[day]; r=fitz.Rect(258.8, tb+8, 286.8, tb+8+44); p.insert_image(r, filename=W+f'btn/day{day}.png', overlay=True); T.append((p,r,DAYFILE[day],({8: 'بنش الأسبوع 3 · اليوم 1 (كل البرامج)', 9: 'بنش الأسبوع 3 · اليوم 2 (كل البرامج)'}.get(day, f'بنش اليوم {day} (كل البرامج)'))))
pw,ph=Image.open(W+'btn/pill.png').size
for day,x0,x1,fn,desc in cl:
    p=PG[day]; y0,y1,_=rows[day]; ws=[w for w in WORDS[day] if x0<=(w[0]+w[2])/2<=x1 and y0<=(w[1]+w[3])/2<=y1]; free=y1-max(w[3] for w in ws)
    if free >= 12:
        H=13 if free >= 16 else 10.5; Wd=H*pw/ph; m=(free-H)/2 if free < 16 else 2.5
        r=fitz.Rect(x1-3-Wd, y1-m-H, x1-3, y1-m); p.insert_image(r, filename=W+'btn/pill.png', overlay=True)
    else:
        c=fitz.Point(x0+8,y0+7.6); R=5.6; sh=p.new_shape(); sh.draw_circle(c,R); sh.finish(color=(1,.69,.54), fill=(.878,.337,.11), width=.6)
        sh.draw_polyline([fitz.Point(c.x-1.6,c.y-2.6),fitz.Point(c.x+2.8,c.y),fitz.Point(c.x-1.6,c.y+2.6)]); sh.finish(fill=(1,1,1), color=(1,1,1), width=.2, closePath=True); sh.commit(overlay=True)
        r=fitz.Rect(c.x-R-1.5,c.y-R-1.5,c.x+R+1.5,c.y+R+1.5)
    T.append((p,r,fn,desc))
for p,r,fn,desc in T:
    Hh=p.rect.height
    a=p.add_file_annot(r.tl, open(OFF+fn+'.html','rb').read(), fn+'.html', desc=desc, icon='Paperclip')
    a.set_info(content=desc); a.set_opacity(0); a.update()
    d.xref_set_key(a.xref,'Rect',f'[{r.x0} {Hh-r.y1} {r.x1} {Hh-r.y0}]')
d.save(W+'year1_weeks_mobile.pdf', garbage=3, deflate=True)
print(os.path.getsize(W+'year1_weeks_mobile.pdf')/1e6,'MB', len(T))
