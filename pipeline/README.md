# سكربتات بناء ملفات الأيام والبنش والخرايط

دي كل السكربتات اللي اتبنى بيها كل حاجة لحد الأسبوع 3 اليوم 4: ملف كل يوم (PDF)، والبنش، وصفحة الخرايط، وخطة السنة. وفيها كمان البرامج نفسها (`dayN/src`) والصور الصغيرة اللي بتحتاجها (`dayN/src/res`).

**مش موجود هنا:** الحاجات اللي بتتعمل من التشغيل (`work/` و `out_days/` و `img/` و ملفات الـ PDF)، والملفات الكبيرة. كلها بتتعمل تاني لما تشغّل السكربتات.

## مهم: المسارات

السكربتات مكتوب فيها مسارات كاملة زي `/home/claude/day11/...`. عشان كده لازم الفولدرات تبقى في `/home/claude`:

```bash
sudo mkdir -p /home/claude && sudo chown $USER /home/claude
cp -r pipeline/* /home/claude/
mkdir -p /tmp/claude-0 && cp -r /home/claude/tmp_tools/* /tmp/claude-0/
```

## المكتبات (Ubuntu / Debian)

```bash
sudo apt install -y g++ gdb valgrind python3 python3-pip libglfw3-dev xvfb xdotool imagemagick nodejs npm ffmpeg
pip install numpy matplotlib pillow weasyprint pymupdf --break-system-packages
npm install playwright && npx playwright install chromium
gcc -shared -fPIC /tmp/claude-0/vsync.c -o /tmp/claude-0/vsync.so -ldl
cd /home/claude/day1/full && gcc -c glad/src/glad.c -Iglad/include -o glad.o
```

- **`vsync.so`**: مكتبة صغيرة بتتحمّل قبل البرامج (LD_PRELOAD) عشان الشباك مايستناش الشاشة وهو شغال على Xvfb.
- **Xvfb**: شاشة وهمية. برامج الرسم بتفتح شبابيكها عليها عشان نصوّرها.

## الأجزاء

| الفولدر | بيعمل إيه |
|---|---|
| `dayN/` | ملف اليوم: `src/` البرامج، و `exp/mkN.py` التجارب الغلط، و `dataN.py` شرح كل سطر، و `wordsN.py` و `diagN.py` و `sbN.py` و `quickN.py` و `why_dayN.py` و `bodyN.py`، و `build_dayN.py` بيطلّع الـ PDF |
| `day1/` و `day2/` و `day3/` | دوال مشتركة: `words.py` و `why.py` و `diagrams.py` و `sb.py` و `quick.py` و `diag3.py` |
| `steps/` | قسم «اكتبه بنفسك خطوة بخطوة»: `specs_dN.py` بيقسم كل برنامج لخطوات، و `engine.py` بيترجم ويشغّل كل خطوة |
| `bench2/` | البنش: `run1.sh` و `gdbtrace.py` للـ C++ و `pytrace.py` للـ Python، و `build_steps.py` و `goals.py` و `edicts.py`، و `assemble.py` بيعمل الصفحة |
| `maps/` | الخرايط: `specs/dN.txt` (وصف الصناديق والأسهم)، و `cmap.py` بيبني الصفحات، و `page.js` الحركة والكور |
| `bridge/` | جسر Claude بين البنش والموبايل (`claude_bridge.py`) |
| `tmp_tools/` | `vsync.c`، وسكربتات Playwright للاختبار والتسجيل، و `yr/compose.py` لخطة السنة |

## الخطوات ليوم جديد (مثال: اليوم 12)

1. **البرامج:** اكتب `day12/src/*.cpp` و `*.py`. شغّل كل برنامج واحفظ اللي طبعه في ملف `.txt` بنفس الاسم:
   ```bash
   g++ -Wall p1.cpp -o p1 && ./p1 > p1.txt
   ```
   برامج الرسم بتتشغّل وتتصوّر بـ `glrun.py`.
2. **التجارب الغلط:** انسخ `day11/exp/mk11.py` لـ `day12/exp/mk12.py` وغيّر التجارب، وبعدين شغّله.
3. **الشرح:** `data12.py` لازم يكون فيه شرح لكل سطر مش موجود في الأيام اللي قبله. السكربت اللي في `day11` بيقف ويقولك لو سطر ناقص.
4. **الخطوات:** اعمل `steps/specs_d12.py` زي `specs_d11.py`، واتأكد إن كل خطوة بتترجم وبتشتغل.
5. **الـ PDF:**
   ```bash
   cd /home/claude/day12 && python3 build_day12.py
   ```
6. **البنش:** اعمل trace لكل برنامج:
   ```bash
   cd /home/claude/bench2
   STDIN_FILE=work/enter.in bash run1.sh d12_p1 0 x "" "[]" /home/claude/day12/src/p1.cpp
   bash run1.sh d12_t1 2 "اسم الشباك" "" "[]" /home/claude/day12/src/t1.cpp /home/claude/day12/src/stb.cpp
   mkdir -p work/d12_m1 && (cd work/d12_m1 && python3 ../../pytrace.py /home/claude/day12/src/m1.py /home/claude/bench2/work/d12_m1)
   ```
   الرقم `0` أو `2` في `run1.sh` هو عدد اللفات اللي هتتسجّل لبرامج الرسم.

   لو البرنامج فيه لوب بكسلات كبير (زي صورة 256 × 256)، البنش هيقف عند عدد 20000 خطوة. عشان كده فيه `SKIP`: السطر اللي اللوب بيبدأ عنده، والسطر اللي بعده، والبنش بيعدي اللوب مرة واحدة:
   ```bash
   SKIP='[["t1_mipmaps.cpp",98,107]]' bash run1.sh d12_t1 2 "Mipmaps" "" "[]" /home/claude/day12/src/t1_mipmaps.cpp
   ```

   بعد كده زوّد البرامج في `PROGS` جوه `build_steps.py`، وفي `goals.py`، وزوّد `('day12','data12')` في `edicts.py`، وشغّل:
   ```bash
   python3 build_steps.py && python3 assemble.py
   ```
7. **الخرايط:** اكتب `maps/specs/d12.txt`، وزوّد اليوم في `DAYN` جوه `mapgen.py`، وكبّر الأرقام في `cmap.py` و `assemble.py`، وبعدين:
   ```bash
   cd /home/claude/maps && python3 cmap.py && rm -rf out && cp -r out2 out
   ```
8. **الاختبار:** `node /tmp/claude-0/alldays.js` بيفتح كل الخرايط ويتأكد إن مفيش أخطاء.

## ملاحظات

- البرامج بتتسجّل من التشغيل الحقيقي: الأرقام والصور مش مكتوبة بالإيد.
- `gh_publish.sh` بيرفع البنش على GitHub Pages. هو محتاج إن الريبو يكون متسجّل دخول عليه بـ git.
- `sim/three.min.js` هي مكتبة three.js اللي البنش بيستخدمها. في الصفحة بتتحمّل من CDN، والنسخة دي للاختبار من غير نت.
