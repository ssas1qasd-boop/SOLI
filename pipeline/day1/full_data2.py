from full_data import E
E.update({
 # p1
 '#include <cstddef>': 'مكتبة فيها تعريف <code>NULL</code>.',
 'void* a = 0;': 'Pointer قيمته صفر = مش بيشاور على حاجة.',
 'void* b = NULL;': 'نفس الكلام بالاسم القديم <code>NULL</code>.',
 'void* c = nullptr;': 'نفس الكلام بالطريقة الحديثة. دي اللي تستخدمها.',
 'std::cout << "a = " << a << std::endl;': 'اطبع <code>a</code>.',
 'std::cout << "b = " << b << std::endl;': 'اطبع <code>b</code>.',
 'std::cout << "c = " << c << std::endl;': 'اطبع <code>c</code>. التلاتة هيطلعوا صفر.',
 # p2
 'void* ptr = &var;': 'علامة <code>&amp;</code> = «هات العنوان». فـ <code>ptr</code> شايل عنوان <code>var</code>.',
 'std::cout << "var  = " << var << std::endl;': 'اطبع القيمة: 8.',
 'std::cout << "&var = " << &var << std::endl;': 'اطبع العنوان: رقم طويل.',
 'std::cout << "ptr  = " << ptr << std::endl;': 'اطبع <code>ptr</code>: نفس العنوان بالظبط.',
 # p3
 'double* ptr2 = (double*)&var;': 'نفس العنوان، بس قلنا «اللي هناك double» (غيّرنا النوع بالعافية).',
 'std::cout << "int*    : " << ptr << std::endl;': 'اطبع العنوان من الـ <code>int*</code>.',
 'std::cout << "double* : " << ptr2 << std::endl;': 'واطبعه من الـ <code>double*</code>: هيطلع نفس الرقم.',
 'std::cout << "int size    = " << sizeof(int) << " bytes" << std::endl;': 'حجم <code>int</code>: 4 بايت.',
 'std::cout << "double size = " << sizeof(double) << " bytes" << std::endl;': 'حجم <code>double</code>: 8 بايت.',
 # p4
 'std::cout << "before: var = " << var << std::endl;': 'اطبع القيمة قبل: 8.',
 'std::cout << "after:  var = " << var << std::endl;': 'اطبعها بعد: 10، مع إننا ما لمسناش <code>var</code> نفسه.',
 # p5
 'std::cout << "buffer = " << (void*)buffer << std::endl;': 'اطبع عنوان الـ 8 بايت. (حوّلناه لـ <code>void*</code> عشان <code>cout</code> يطبعه كعنوان مش كنص)',
 'for (int i = 0; i < 8; i++)': 'لف على الـ 8 بايت…',
 'std::cout << (int)buffer[i] << " ";': '…واطبع كل واحد كرقم.',
 'std::cout << std::endl;': 'انزل سطر.',
 # p6
 'char** ptr = &buffer;': 'نجمتين = «عنوان لعنوان». شايل عنوان <code>buffer</code> نفسه.',
 'std::cout << "ptr      = " << (void*)ptr << std::endl;': 'اطبع اللي جوه <code>ptr</code>…',
 'std::cout << "&buffer  = " << (void*)&buffer << std::endl;': '…وهو هو عنوان <code>buffer</code>.',
 'std::cout << "*ptr     = " << (void*)*ptr << std::endl;': 'روح لـ <code>ptr</code> مرة: تلاقي عنوان البيانات…',
 'std::cout << "buffer   = " << (void*)buffer << std::endl;': '…وهو هو اللي جوه <code>buffer</code>.',
 'std::cout << "(*ptr)[0] = " << (int)(*ptr)[0] << std::endl;': 'روح مرتين: توصل للبيانات نفسها (0).',
 # u1
 'int wrong = glGetUniformLocation(shader, "u_Colour");': 'جرّب اسم فيه غلطة (<code>Colour</code> بدل <code>Color</code>).',
 'std::cout << "u_Colour location = " << wrong << std::endl;': 'اطبعه: هيطلع ‎-1 = «مش لاقيها».',
 'glUniform4f(location, 0.2f, 0.3f, 0.8f, 1.0f);': 'ابعت اللون: أحمر قليل، أخضر قليل، أزرق كتير، مش شفاف = أزرق.',
})

for k in ['static const char* vertexShaderSrc = R"(#version 330 core','layout(location = 0) in vec4 position;','gl_Position = position;',
          'static const char* fragmentShaderSrc = R"(#version 330 core','layout(location = 0) out vec4 color;','uniform vec4 u_Color;','color = u_Color;',
          'layout (location = 0) in vec3 aPos;','layout (location = 1) in vec3 aColor;','uniform mat4 camMatrix;','gl_Position = camMatrix * vec4(aPos, 1.0);',
          'out vec4 FragColor;','FragColor = vec4(color, 1.0);']:
    E[k] = E[k] + ' <span style="color:#2563eb">(شرحه كلمة كلمة فوق)</span>'
