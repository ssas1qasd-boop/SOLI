// ------------------------------------------------------------------ the bench story: what the program does, chapter by chapter (hidden until asked)
const STATIC_LOOP = 'الصورة هنا ثابتة، بس برضه لازم لوب. الشاشة مش بتفتكر الصورة لوحدها: كل فريم لازم يترسم من جديد (امسح ← ارسم ← بدّل اللوحتين). وكمان كل لفة <code>glfwPollEvents</code> بتسأل نظام التشغيل: حد داس على زرار القفل؟ حد حرّك الشباك؟ من غير اللوب البرنامج هيوصل لـ <code>return 0</code> في جزء من الثانية، والشباك يفتح ويقفل قبل ما تلحق تشوفه، ولو وقف من غير ما يسأل على الأحداث نظام التشغيل هيقول «البرنامج مش بيرد».';
const PSTORY = {
  d1_u1: {goal: 'مستطيل أزرق ثابت. المستطيل = مثلثين، بس الأركان متخزنة مرة واحدة بس (4 أركان)، وجدول أرقام صغير (EBO) بيقول للكارت يوصّلهم إزاي (0,1,2 و 2,3,0). اللون مش متكتب جوه الـ Shader: بييجي من برا في uniform اسمه <code>u_Color</code>.', loop: STATIC_LOOP + ' وكل لفة الـ CPU بيبعت نفس اللون تاني بـ <code>glUniform4f</code> قبل الرسم.'},
  d1_u2: {goal: 'نفس المستطيل، بس لونه بيتغير قدامك. فيه متغير <code>r</code> في الرام بيزيد 0.05 كل لفة لحد ما يعدّي 1، وبعدين يبدأ ينقص، وهكذا.', loop: 'هنا اللوب ليها شغلانة واضحة: كل لفة الـ CPU بيبعت قيمة <code>r</code> الجديدة للكارت بـ <code>glUniform4f</code>، فكل فريم لونه مختلف. شكل المستطيل (الـ Buffers) اتبعت للكارت مرة واحدة قبل اللوب، واللي بيتبعت كل لفة هو رقم اللون بس. قارن بين صور اللفات في «الصورة الحقيقية»: الأحمر بيزيد.'},
  d1_cam: {goal: 'هرم ملوّن 3D بنشوفه من كاميرا. الكود متقسم على 3 ملفات: <code>main.cpp</code> بيستخدم كلاس <code>Shader</code> (في shaderClass.cpp) وكلاس <code>Camera</code> (في Camera.cpp)، فالتنفيذ بينط بين الملفات، وده باين في «مسار التنفيذ».', loop: 'كل لفة <code>Camera::Inputs</code> بتسأل: الكيبورد (W A S D) أو الماوس متداس؟ وتحرك الكاميرا. وبعدين <code>Camera::Matrix</code> بتحسب مصفوفة جديدة من مكان الكاميرا وتبعتها للـ Shader. عشان كده اللوب ضرورية: لو الكاميرا اتحركت، الهرم لازم يترسم من جديد من المكان الجديد. في التشغيل ده محدش داس، فالصورة فضلت زي ما هي.'},
  d2_va1: {goal: 'مثلث برتقاني. كل ركن فيه رقمين بس (x, y)، يعني 8 بايت، و <code>glVertexAttribPointer</code> بيقول للكارت بالظبط كده: «خانة 0: رقمين float، وكل ركن بعد 8 بايت من اللي قبله».', loop: STATIC_LOOP},
  d2_va2: {goal: 'مثلث ألوانه متدرجة. كل ركن فيه 5 أرقام: x, y ثم r, g, b (20 بايت). فيه خانتين: خانة 0 = المكان (من بايت 0)، وخانة 1 = اللون (من بايت 8). الكارت بيخلط الألوان بين الأركان لوحده في الـ Rasterizer، عشان كده التدرج.', loop: STATIC_LOOP},
  d3_s1: {goal: 'مثلث أزرق، بس الـ Shaders مش مكتوبين جوه الكود: متكتبين في ملف لوحده اسمه <code>Basic.shader</code>. البرنامج بيفتح الملف ويقراه سطر سطر بـ <code>getline</code>، ويقسمه نصين (Vertex و Fragment) حسب سطر <code>#shader</code>، وبعدين يبعتهم للكارت.', loop: STATIC_LOOP + ' وخلي بالك إن فيه لوب تاني قبلها خالص: <code>while (getline(stream, line))</code> جوه <code>ParseShader</code>. دي بتلف مرة لكل سطر في الملف (19 سطر) وتقف لما الملف يخلص، لأن <code>getline</code> بترجع false.'},
  d3_l1: {goal: 'أول أمر CAD: خط أبيض بين نقطتين، والنقطتين نفسهم مرسومين مربعات برتقاني. نفس الـ Buffer (نفس النقطتين) بيترسم مرتين: مرة <code>GL_LINES</code> ومرة <code>GL_POINTS</code>، وكل مرة بلون uniform مختلف.', loop: 'كل لفة فيها رسمتين: الـ CPU يبعت لون أبيض ويقول «ارسم خط»، وبعدين يبعت برتقاني ويقول «ارسم نقط». ده أساس أي برنامج CAD: نفس الداتا بتتعرض بأكتر من شكل. والصورة لازم تتعاد كل فريم زي أي شباك.'},
  d3_l2: {goal: 'تدوس بالماوس في الشباك، وكل ضغطتين = خط. في التشغيل ده اتبعت للشباك 5 ضغطات حقيقية، فاتعمل خطين ونقطة لوحدها مستنية شريكتها.', loop: 'هنا اللوب هي اللي بتخلي البرنامج «يسمع». كل لفة <code>glfwPollEvents</code> بتسأل نظام التشغيل: حد داس؟ لو أيوه، GLFW بينده <code>MouseButtonCallback</code> لوحده، فالنقطة بتتحول من بكسل لـ ‎-1..+1 وتتضاف للـ vector وتتبعت للكارت تاني، وفي اللفة اللي بعدها تترسم. من غير لوب مفيش حد يسأل على الماوس أصلاً. وكمان GLFW بينده الدالة تاني لما الزرار يطلع (Release)، بس السطر الأول بيرجّعها على طول، فالمرة دي مش ظاهرة في الخطوات.'},
  d4_e1: {goal: 'مستطيل أزرق من مثلثين بـ <code>glDrawArrays</code>: 6 أركان، منهم ركنين متكررين، عشان كل مثلث لازم ياخد 3 أركان كاملين.', loop: STATIC_LOOP},
  d4_e2: {goal: 'نفس المستطيل بـ 4 أركان بس + جدول أرقام (EBO) فيه 6 أرقام: 0,1,2 و 2,3,0. <code>glDrawElements</code> بيمشي على الجدول بدل ما يمشي على الأركان بالترتيب. وفّرنا ركنين هنا، وفي الأشكال الكبيرة التوفير بيبقى ضخم.', loop: STATIC_LOOP},
  d4_v1: {goal: 'رسمتين في نفس الشباك: بيت (خطوط بيضا) وشمس (صليب أصفر). كل رسمة ليها VAO و Buffer خاصين بيها.', loop: 'كل لفة: امسح ← اربط VAO البيت + لون أبيض + ارسم ← اربط VAO الشمس + لون أصفر + ارسم ← بدّل. الـ VAO هو اللي مخلي التبديل بين الرسمتين سطر واحد (<code>glBindVertexArray</code>) بدل ما نعيد وصف الأركان كل مرة.'},
  d4_v2: {goal: 'Polyline بالماوس: ضغطة شمال = نقطة جديدة في الخط الشغال، ضغطة يمين = اقفل الخط ده وابدأ واحد جديد. اتبعت 10 ضغطات حقيقية، فاتعمل 3 خطوط.', loop: 'كل لفة: ارسم كل خط لوحده بـ <code>GL_LINE_STRIP</code> (فعدد الرسمات بيزيد كل ما الخطوط تزيد)، وبعدين ارسم كل النقط، وبعدين اسأل على الماوس. الضغطة اللي بتحصل في لفة بتبان في اللفة اللي بعدها، لأن الرسم حصل قبل السؤال.'},
};
const CAT = {win:'تجهيز الشباك والوصلة بالكارت', data:'تجهيز الداتا في الرام', buf:'شحن الداتا للكارت', sh:'تجهيز الـ Shaders', loop:'اللوب: ارسم كل فريم', end:'الخروج والتنضيف'};
function stepText(s){ return (P.files[s.f].lines[s.ln - 1] || '').trim(); }
function catOf(s, k, exitK){
  if (s.lap) return 'loop'; if (exitK >= 0 && k >= exitK) return 'end';
  const t = stepText(s), f = s.fn || '';
  if (/Shader|Program/.test(f) || /Shader|Program|glUseProgram|glGetUniformLocation|getline|ss\[/.test(t)) return 'sh';
  if (/glfw|glad|glViewport/.test(t)) return 'win';
  if (/VertexArray|glGenBuffers|glBindBuffer|glBufferData|VertexAttrib|glDeleteBuffers/.test(t) || /^(VAO|VBO|EBO)/.test(f)) return 'buf';
  return 'data';
}
function chapters(){
  const exitK = ST.findIndex(s => s.cl); const raw = [];
  ST.forEach((s, k) => { const c = catOf(s, k, exitK); const L = raw[raw.length - 1]; if (L && L.c === c) L.to = k; else raw.push({c, from:k, to:k}); });
  const out = []; // fold tiny chapters into the previous one, then merge equal neighbours
  raw.forEach((ch, n) => { const small = ch.to - ch.from < 2 && ch.c !== 'loop' && ch.c !== 'end'; const L = out[out.length - 1];
    if (small && L){ L.to = ch.to; return; } if (L && L.c === ch.c){ L.to = ch.to; return; } out.push(Object.assign({}, ch)); });
  return out;
}
function nd(t, c){ return `<span class="nd${c ? ' ' + c : ''}">${t}</span>`; }
const AR = '<span class="ar">←</span>';
function chapText(ch){
  const a = ST[ch.from], b = ST[ch.to], G = b.gp, G0 = ch.from ? ST[ch.from - 1].gp : {vaos:{}, bufs:{}, sh:{}, pr:{}, uni:{}};
  const newBufs = Object.entries(G.bufs).filter(([id]) => !G0.bufs[id]), newVaos = Object.keys(G.vaos).filter(id => !G0.vaos[id]);
  const bytes = newBufs.reduce((n, [, x]) => n + (x.bytes || 0), 0);
  const fns = [...new Set(ST.slice(ch.from, ch.to + 1).filter(s => s.d > 1).map(s => s.fn))];
  const calls = fns.length ? ` التنفيذ نط لـ ${fns.map(f => `<code>${esc(f)}()</code>`).join(' و ')} ورجع.` : '';
  const vars = [...new Set(ST.slice(ch.from, ch.to + 1).filter(s => s.d === 1 && /متغير جديد/.test(s.ti)).map(s => (/\b(\w+)\s*(\[[^\]]*\])?\s*(=|\{|;)/.exec(stepText(s)) || [])[1]).filter(Boolean))];
  switch (ch.c){
    case 'win': return {t: `البرنامج بيبدأ من <code>main()</code>. الـ CPU بيطلب من GLFW يجهز نفسه، وبعدين يفتح شباك ${P.W} × ${P.H}. بعدين <code>glfwMakeContextCurrent</code> بيوصّل الشباك ده بكارت الشاشة (Context)، و GLAD بيجيب من الدرايفر عناوين دوال OpenGL.${calls}`,
      who: `${nd('الكود بتاعك')} ${AR} ${nd('CPU', 'c')} ${AR} ${nd('GLFW')} ${AR} ${nd('نظام التشغيل')} ${AR} ${nd('🪟 الشباك')}، و ${nd('GLAD')} ${AR} ${nd('درايفر الكارت')}`,
      why: 'قبل الفصل ده مفيش أي أمر <code>gl…</code> ينفع يشتغل: لازم يبقى فيه شباك وكارت متوصل بيه الأول.'};
    case 'data': return {t: `الـ CPU لوحده بيجهز الأرقام في الرام: ${vars.length ? vars.map(v => `<code>${esc(v)}</code>`).join('، ') : 'متغيرات ومصفوفات'}. الكارت لسه ما يعرفش عنها أي حاجة.${calls}`,
      who: `${nd('CPU', 'c')} ${AR} ${nd('الرام')}`, why: 'الأركان والألوان لازم تبقى موجودة في الرام الأول عشان نعرف ننسخها للكارت بعد كده.'};
    case 'buf': return {t: `الـ CPU بيطلب من الكارت يحجز ${newVaos.length ? `${newVaos.length} VAO` : ''}${newVaos.length && newBufs.length ? ' و ' : ''}${newBufs.length ? `${newBufs.length} Buffer` : ''}، وبعدين <code>glBufferData</code> بينسخ ${bytes ? `<b>${bytes} بايت</b>` : 'البايتات'} من الرام لذاكرة الكارت، و <code>glVertexAttribPointer</code> بيكتب على الـ VAO «اقرا الصندوق إزاي».${calls}`,
      who: `${nd('CPU', 'c')} ${AR} ${nd('أوامر gl')} ${AR} ${nd('الدرايفر')} ${AR} ${nd('GPU: Buffers و VAOs', 'g')}`,
      why: 'الكارت مش بيقرا من رام الكمبيوتر وهو بيرسم. لازم الداتا تتنقل لذاكرته مرة واحدة هنا، وبعد كده كل فريم يرسم منها على طول من غير ما الـ CPU يبعتها تاني.'};
    case 'sh': { const pr = Object.keys(G.pr)[0]; const un = Object.keys(G.uni);
      return {t: `نص الـ Shaders بيتبعت للدرايفر، يترجمه لأوامر الكارت (Compile)، ويربط الاتنين في برنامج واحد${pr ? ` (Program ${pr})` : ''} (Link).${calls} ${un.length ? `وبعدين بنجيب رقم خانة الـ uniform ${un.map(u => `<code>${esc(u)}</code>`).join(' و ')}.` : ''}`,
      who: `${nd('CPU', 'c')} ${AR} ${nd('نص GLSL')} ${AR} ${nd('الدرايفر يترجم')} ${AR} ${nd('GPU: Vertex + Fragment = Program', 'g')}`,
      why: 'الكارت مش بيفهم C++. الـ Shaders هما البرامج الصغيرة اللي هتشتغل على الكارت نفسه: الـ Vertex مرة لكل ركن، والـ Fragment مرة لكل بكسل.'}; }
    case 'loop': { const laps = P.laps, clicks = ST.filter(s => s.ev).length, draws = ST.slice(ch.from, ch.to + 1).filter(s => s.an === 'draw').length;
      const order = P.phases.map(p => `<code>${esc(shortName(p[1]))}</code>`).join(' ← ');
      return {t: `${(PSTORY[P.id] || {}).loop || STATIC_LOOP}<br>ترتيب اللفة الواحدة: ${order}. في التشغيل ده لفّت <b>${laps}</b> مرات، واتعمل فيها ${draws} أمر رسم${clicks ? `، والماوس نده الدالة <b>${clicks}</b> مرة` : ''}.`,
        who: `${nd('CPU', 'c')} ${AR} ${nd('glClear / glDraw…')} ${AR} ${nd('GPU يرسم في Back', 'g')} ${AR} ${nd('Swap')} ${AR} ${nd('🖥 الشاشة')}` + (clicks ? `، وبالعكس: ${nd('🖱 الماوس')} ${AR} ${nd('نظام التشغيل')} ${AR} ${nd('GLFW')} ${AR} ${nd('دالتك (Callback)', 'c')}` : ''),
        why: 'عشان الصورة تفضل على الشاشة وتتحدث، والبرنامج يفضل يسمع للماوس والكيبورد وزرار القفل. اللوب بتقف لما الشباك يتطلب يتقفل.'}; }
    case 'end': return {t: `الشرط <code>glfwWindowShouldClose</code> بقى true (في التشغيل ده إحنا اللي طلبنا القفل بعد آخر لفة)، فالـ while وقفت. بعدها البرنامج بيمسح اللي حجزه على الكارت ويقفل GLFW، وبعدين <code>return 0</code>.${calls}`,
      who: `${nd('CPU', 'c')} ${AR} ${nd('glDelete…')} ${AR} ${nd('GPU يفضّي', 'g')}، و ${nd('CPU', 'c')} ${AR} ${nd('glfwTerminate')} ${AR} ${nd('نظام التشغيل يقفل الشباك')}`,
      why: 'أي حاجة اتحجزت لازم تترجع. الكارت ونظام التشغيل مش هيعرفوا لوحدهم إن البرنامج خلص بالأدب.'};
  }
}
function renderStory(){
  const S = PSTORY[P.id] || {}; const CH = chapters(); const lastFr = P.frames.length - 1;
  const hasCb = ST.some(s => s.ev);
  $('stoSub').textContent = `${P.title} · ${CH.length} فصول · ${ST.length} خطوة`;
  const curCh = CH.findIndex(c => i >= c.from && i <= c.to);
  $('stoBody').innerHTML = `
    <h4>🎯 هنوصل لإيه؟</h4>
    <div class="goal"><p>${S.goal || esc(P.desc)}</p><figure style="margin:0"><img src="${P.frames[lastFr]}" alt="آخر صورة اتقرت من الكارت في التشغيل الحقيقي"><figcaption>آخر صورة حقيقية من الكارت</figcaption></figure></div>
    <h4>🧭 مين بيوجّه أوامر لمين؟</h4>
    <div class="chain">
      <div class="row"><b>الشباك</b>${nd('الكود بتاعك')} ${AR} ${nd('CPU', 'c')} ${AR} ${nd('GLFW')} ${AR} ${nd('نظام التشغيل')} ${AR} ${nd('🪟 الشباك')}</div>
      <div class="row"><b>الرسم</b>${nd('CPU', 'c')} ${AR} ${nd('أوامر gl…')} ${AR} ${nd('الدرايفر')} ${AR} ${nd('GPU', 'g')} ${AR} ${nd('Framebuffer')} ${AR} ${nd('🖥 الشاشة')}</div>
      ${hasCb ? `<div class="row"><b>الماوس (بالعكس)</b>${nd('🖱 الماوس')} ${AR} ${nd('نظام التشغيل')} ${AR} ${nd('GLFW')} ${AR} ${nd('MouseButtonCallback', 'c')} ${AR} ${nd('الرام + الكارت')}</div>` : ''}
    </div>
    <p>الـ CPU هو المدير: بينفذ الكود سطر سطر، ومش بيرسم بنفسه. أي سطر فيه <code>gl…</code> هو أمر بيتبعت للكارت، والكارت هو اللي بيرسم.${hasCb ? ' الحالة الوحيدة اللي الأمر بييجي فيها بالعكس هي الماوس: محدش من الكود بينده <code>MouseButtonCallback</code>، GLFW هو اللي بيندهها لما تدوس.' : ''}</p>
    <h4>📚 فصول القصة بالترتيب</h4>
    ${CH.map((c, n) => { const x = chapText(c); const a = ST[c.from], b = ST[c.to];
      return `<div class="chap${n === curCh ? ' now' : ''}"><h5><span>${n + 1}. ${CAT[c.c]}${n === curCh ? ' ← انت هنا' : ''}</span><small>steps ${c.from + 1}–${c.to + 1} · lines ${lineOf(a.v)}…${lineOf(b.v)}</small></h5><p>${x.t}</p><span class="who">${x.who}</span><span class="why">${x.why}</span><button type="button" data-go="${c.from}">▶ روح لأول الفصل ده (خطوة ${c.from + 1})</button></div>`; }).join('')}
    <h4>🔁 ليه بنعمل لوب؟</h4><p>${S.loop || STATIC_LOOP}</p>
    <h4>👀 تتفرج إزاي؟</h4>
    <p>اضغط «تشغيل» وسيبه يمشي، أو امشي بـ «اللي بعده». كل خطوة = سطر واحد اتنفذ فعلاً بالترتيب ده. اللون البرتقاني = الـ CPU شغال لوحده، الأخضر = الكارت شغال، الأزرق = الـ CPU بيبعت أمر للكارت. الكروت البرتقاني على الماكينة بتقولك إيه اللي اتغير في الخطوة دي وبسبب أنهي سطر، و «مسار التنفيذ» بيوريك امتى الكود نط لدالة ورجع، وامتى لف في اللوب.</p>`;
  $('stoBody').querySelectorAll('[data-go]').forEach(bn => bn.onclick = () => { showStory(false); play(false); go(+bn.dataset.go); stage.scrollIntoView({behavior: reduce ? 'auto' : 'smooth', block: 'center'}); });
}
function showStory(on){ $('story2').hidden = !on; $('stoBtn').setAttribute('aria-expanded', on); $('stoBtn').textContent = on ? '✕ خبّي القصة' : '📜 قصة البنش';
  if (on){ if (!$('legend').hidden) showLegend(false); if (!$('gloss').hidden) showGloss(false); renderStory(); $('story2').scrollTop = 0; } }
$('stoBtn').onclick = () => showStory($('story2').hidden); $('stoX').onclick = () => showStory(false);
document.addEventListener('keydown', e => { if (e.key === 'Escape' && !$('story2').hidden) showStory(false); });
