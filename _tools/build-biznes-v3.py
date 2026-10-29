# -*- coding: utf-8 -*-
# Сборка decks/biznes-v3.html — гибрид направлений B (доказательства) + C (симулятор) + D (экосистема)
# из decks/biznes.html: шапка/стили/движок — оттуда, состав слайдов — новый.
# Экономика — по уточнениям ментора (2026-10-29): Start = пробная Pro на 210 дней для себя,
# клиенты из корзины компании: аренда 45 $/мес партнёру, продажа 400 $. Business+ — свои
# лицензии: аренда 85 $/мес, выкуп 1 500 $ (цифры из старой деки, не подтверждены).
# Запуск: python3 _tools/build-biznes-v3.py

import io, os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, 'decks', 'biznes.html')
DST = os.path.join(BASE, 'decks', 'biznes-v3.html')

src = io.open(SRC, encoding='utf-8').read()
body_start = src.index('<div class="stage">')
body_end = src.index('<div class="nav-zone prev"')
head = src[:body_start]
body = src[body_start:body_end]
tail = src[body_end:]
marks = list(re.finditer(r'<!--\s*(\d+\s*·[^>]*?|Контакты)\s*-->', body))

def orig(prefix, subs=()):
    for k, m in enumerate(marks):
        if m.group(1).strip().startswith(prefix):
            end = marks[k + 1].start() if k + 1 < len(marks) else len(body)
            chunk = body[m.start():end].rstrip() + '\n'
            for old, new in subs:
                rx = re.compile(re.escape(old).replace('\\ ', '[  ]'))
                if not rx.search(chunk):
                    raise SystemExit('замена не нашлась в слайде %r: %r' % (prefix, old))
                chunk = rx.sub(lambda _m: new, chunk, count=1)
            return chunk
    raise SystemExit('нет слайда ' + prefix)

LOGO = '<div class="logo">uds<span>Partner</span></div>'

# ---------- новые слайды ----------

S_TITLE = orig('1 ·', [
    ('Система дохода на IT-продукте,<br>которым пользуются 8 000+ компаний',
     'Карта лояльности Беларуси пока пустая.<br>Я ищу тех, кто заполнит её первыми'),
])

S_MANIFEST = '''<!-- · Манифест: карта пустая -->
<section class="slide">
  %s
  <div class="st-glow"></div>
  <div class="eco-city" data-city></div>
  <div class="eco-txt">
    <div class="eyebrow a" style="--i:0">Беларусь · 2026</div>
    <h1 class="st-h1 a" style="--i:1; text-align:left; font-size:4.6cqw">Карта лояльности страны<br><em class="chrome">пока пустая.</em></h1>
    <div class="eco-sub a" style="--i:2">7 000+ бизнесов в России уже работают на UDS. В Беларуси — первые точки. Каждая новая точка на этой карте — чей-то район, который подключил конкретный человек.</div>
  </div>
</section>
''' % LOGO

S_PAIN = '''<!-- · Боль -->
<section class="slide">
  %s
  <div class="st-glow"></div>
  <div class="st-center">
    <div>
      <h1 class="st-h1 a" style="--i:0">В девяти из десяти кафе, салонов и магазинов рядом с вами <em>нет системы</em> возврата клиентов<small>Проверьте сами: спросите у знакомого владельца, сколько гостей вернулось в этом месяце. Ответа не будет — его негде посмотреть.</small></h1>
    </div>
  </div>
</section>
''' % LOGO

def shot(i, src_, cap):
    return ('<figure class="a" style="--i:%d; margin:0; display:flex; flex-direction:column; align-items:center; gap:1.1cqw">'
            '<img src="../assets/img/pervichka/%s" alt="%s" style="height:31cqw; border-radius:1.4cqw; border:1px solid var(--panel-line)">'
            '<figcaption style="font-size:1.3cqw; color:var(--mut)">%s</figcaption></figure>') % (i, src_, cap, cap)

S_PRODUCT_LIVE = '''<!-- · Продукт в руках клиента -->
<section class="slide">
  %s
  <div class="head"><div class="eyebrow">Как это выглядит</div><div class="h2">Продукт <em>в руках клиента</em></div></div>
  <div style="position:absolute; inset:14.5cqw 12cqw 4.5cqw; display:flex; gap:5cqw; justify-content:center; z-index:2">
    %s
    %s
    %s
  </div>
</section>
''' % (LOGO,
       shot(0, 'app-home.jpg', 'Все компании города — в одном приложении'),
       shot(1, 'app-status.jpg', 'Статусы и кешбэк клиента'),
       shot(2, 'app-referral.jpg', 'Бонусы за рекомендации друзьям'))

def case_cover(tag, num, num_unit, who, meta, img, img_pos='50% 50%', extra=''):
    return '''<!-- · Кейс: %s -->
<section class="slide">
  %s
  <div class="bc">
    <div class="bc-pic a" style="--i:0"><img src="%s" alt="%s" style="object-position:%s"></div>
    <div class="bc-txt">
      <div class="eyebrow a" style="--i:1">%s</div>
      <div class="bc-num chrome a" style="--i:2">%s<span>%s</span></div>
      <div class="bc-who a" style="--i:3">%s</div>
      <div class="bc-meta a" style="--i:4">%s</div>
      %s
    </div>
  </div>
</section>
''' % (who, LOGO, img, who, img_pos, tag, num, num_unit, who, meta, extra)

# Кейсы клиентов (Nicecar, SAVVALI) в этой деке не нужны — их рассказывают до Alex в продуктовой
# части. Остаются только партнёрские кейсы из оригинальной деки. Фото Шестаковой — base64 из оригинала.
_m = re.search(r'<img src="(data:image/[a-z]+;base64,[A-Za-z0-9+/=]+)" alt="Екатерина Шестакова"', orig('38 ·'))
if not _m:
    raise SystemExit('не нашёл фото Шестаковой в оригинале')
S_CASE_SHESTAKOVA = case_cover('Партнёр · Россия', '≈ 16 000 $', 'за первый год (1,3 млн ₽)', 'Екатерина Шестакова',
    'Учитель музыки в детском саду, Екатеринбург. До UDS — 35–40 тыс ₽ в месяц, вокруг только учителя и воспитатели, без опыта в бизнесе. Через год — клиенты и партнёры в 20+ регионах России и 7 странах.',
    _m.group(1), '50% 15%')

HV_BARS = '''<div class="bc-bars frag" data-step="1">
        <div style="height:7%"><b>236</b><i>1-й мес</i></div><div style="height:44%"><b>1 591</b><i>2-й</i></div><div style="height:46%"><b>1 667</b><i>3-й</i></div><div style="height:100%"><b>3 621</b><i>4-й</i></div>
      </div>
      <div class="bc-meta frag" data-step="1">К четвёртому месяцу окупил VIP-пакет. 17 партнёров в команде — пока служил.</div>'''
S_CASE_HVISEVICH = case_cover('Партнёр · Беларусь', '3 621 $', ' в 4-й месяц', 'Андрей Хвисевич',
    'Кадровый военный, подполковник. 1–2 часа в день на бизнес, параллельно со службой. Доход по месяцам, $:',
    '../assets/partners/hvisevich.jpg', '50% 15%', HV_BARS)

S_CASE_PARFENOV = case_cover('Партнёр · Беларусь', '8 000 $', ' за первый месяц', 'Евгений Парфёнов',
    'Менеджер по продажам в международной IT-компании — опыт продаж был, опыта в UDS не было. Партнёр с мая 2026: статус «Директор» закрыт в первый же месяц, победитель личного зачёта LevelUP. Лучший старт в команде — не средний, и я это говорю прямо.',
    '../assets/partners/parfenov.jpg', '50% 15%')

S_TWO_CIRCUITS = '''<!-- · Два контура дохода -->
<section class="slide">
  %s
  <div class="head"><div class="eyebrow">Откуда деньги</div><div class="h2">Два контура — <em>честно</em></div></div>
  <div class="cards c2" style="bottom:15cqw">
    <div class="card glass hi frag" data-step="1" data-spot="1">
      <div class="n viol">01</div>
      <div class="k">Продуктовый</div>
      <div class="v">Подключаешь бизнесы, сопровождаешь, получаешь с каждого оплаченного месяца и с каждой продажи. Платит <b style="color:var(--ink)">бизнес</b> — за продукт, которым пользуется каждый день</div>
    </div>
    <div class="card glass frag" data-step="2" data-spot="2">
      <div class="n viol">02</div>
      <div class="k">Партнёрский</div>
      <div class="v">Приглашаешь партнёров, обучаешь, получаешь бонус с их пакетов и долю с их клиентов. Ускоритель — но <b style="color:var(--ink)">не замена</b> первому контуру</div>
    </div>
  </div>
  <div class="card glass frag" data-step="3" style="position:absolute; left:4.4cqw; right:4.4cqw; bottom:5cqw; flex-direction:row; align-items:center; gap:2.6cqw; padding:1.9cqw 2.6cqw; z-index:2">
    <div class="k viol" style="white-space:nowrap">Моя позиция</div>
    <div class="v" style="flex:1">Я зарабатываю на первом контуре и строю команду из тех, кто тоже подключает бизнесы. Так растёт карта, а не список фамилий</div>
  </div>
</section>
''' % LOGO

S_PYRAMID = '''<!-- · Это пирамида? -->
<section class="slide">
  %s
  <div class="head"><div class="eyebrow">Честный вопрос</div><div class="h2">«Это <em>пирамида</em>?»</div></div>
  <div class="cards c3" style="bottom:15cqw">
    <div class="card glass frag" data-step="1">
      <div class="k">Есть продукт, за который платят</div>
      <div class="v">7 000+ компаний в России и СНГ платят абонентскую плату за UDS — каждый месяц, 10+ лет подряд</div>
    </div>
    <div class="card glass frag" data-step="2">
      <div class="k">Деньги приходят от клиентов</div>
      <div class="v">Партнёру платят с оплаты бизнеса: 45 $ с каждого оплаченного месяца аренды, 400 $ с продажи. Не со взносов новичков</div>
    </div>
    <div class="card glass frag" data-step="3">
      <div class="k">Порог входа — 850 $</div>
      <div class="v">Это одна пробная Pro-лицензия на 210 дней для себя. Клиентов подключаешь из корзины компании — покупать лицензии не нужно</div>
    </div>
  </div>
  <div class="card glass hi frag" data-step="4" style="position:absolute; left:4.4cqw; right:4.4cqw; bottom:5cqw; flex-direction:row; align-items:center; gap:2.6cqw; padding:1.9cqw 2.6cqw; z-index:2">
    <div class="k viol" style="white-space:nowrap">Разница</div>
    <div class="v" style="flex:1">В пирамиде деньги есть, только пока приходят новые участники. Здесь — пока бизнесы пользуются продуктом. Это проверяется за 10 минут в приложении</div>
  </div>
</section>
''' % LOGO

S_TILES = '''<!-- · Выбери вход -->
<section class="slide">
  %s
  <div class="head"><div class="eyebrow">Вход</div><div class="h2">Выбери <em>вход</em> — и что на нём разрешено</div></div>
  <div class="tiles">
    <div class="tile glass hi frag" data-step="1"><div class="tp">Start</div><div class="tc chrome">850 $</div><div class="td">1 пробная Pro · 210 дней · для себя<br><span class="ok">✓</span> аренда из корзины — <b>45 $/мес</b><br><span class="ok">✓</span> продажа из корзины — <b>400 $</b><br><span class="no">✕</span> своих лицензий нет</div></div>
    <div class="tile glass frag" data-step="2"><div class="tp">Business</div><div class="tc chrome">1 900 $</div><div class="td">2 свои лицензии<br><span class="ok">✓</span> аренда — <b>85 $/мес</b><br><span class="ok">✓</span> выкуп — <b>1 500 $</b></div></div>
    <div class="tile glass frag" data-step="3"><div class="tp">Premium</div><div class="tc chrome">3 950 $</div><div class="td">6 своих лицензий<br><span class="ok">✓</span> аренда — 85 $/мес<br><span class="ok">✓</span> выкуп — 1 500 $</div></div>
    <div class="tile glass frag" data-step="4"><div class="tp">VIP</div><div class="tc chrome">6 350 $</div><div class="td">12 своих лицензий<br><span class="ok">✓</span> аренда · выкуп<br><b>1 000 $</b> за приглашённого партнёра VIP</div></div>
    <div class="tile glass frag" data-step="5"><div class="tp">3 VIP</div><div class="tc chrome">16 450 $</div><div class="td">36 своих лицензий<br><span class="ok">✓</span> всё<br><b>3 600 $</b> командный бонус</div></div>
  </div>
</section>
''' % LOGO

S_RATES = '''<!-- · Ставки -->
<section class="slide">
  %s
  <div class="head"><div class="eyebrow">Ставки</div><div class="h2">Что платит клиент — <em>что получаешь ты</em></div></div>
  <div class="tbl">
    <div class="thead-note">Корзина компании — для партнёра на Start. Своя лицензия — от Business и выше. Клиент платит одинаково в обоих случаях</div>
    <table>
      <tr><th></th><th>Клиент платит</th><th>Тебе · корзина компании (Start)</th><th>Тебе · своя лицензия</th></tr>
      <tr class="frag" data-step="1"><td><b>Аренда</b></td><td>130 $/мес</td><td class="acc">45 $ за каждый оплаченный месяц</td><td>85 $/мес</td></tr>
      <tr class="frag" data-step="2"><td><b>Продажа</b></td><td>1 500 $ единоразово + 50 $/мес</td><td class="acc">400 $</td><td>1 500 $ + 11 $/мес</td></tr>
      <tr class="hl frag" data-step="3"><td><b>Окупаемость Start</b></td><td class="mut" colspan="3">850 $ возвращаются за две продажи из корзины — или за ~19 оплаченных месяцев аренды: например, 4 клиента × 5 месяцев</td></tr>
    </table>
  </div>
</section>
''' % LOGO

S_CALC = '''<!-- · Калькулятор -->
<section class="slide" id="calcSlide">
  %s
  <div class="head"><div class="eyebrow">Твой расчёт</div><div class="h2">Посчитаем <em>твой год</em></div></div>
  <div class="calc">
    <div class="calc-ctl glass a" style="--i:0">
      <div class="calc-pk" id="pk">
        <button type="button" data-pk="start" class="on">Start</button><button type="button" data-pk="business">Business</button><button type="button" data-pk="premium">Premium</button><button type="button" data-pk="vip">VIP</button><button type="button" data-pk="vip3">3 VIP</button>
      </div>
      <label class="calc-row"><span>Клиентов в аренду, в месяц</span><b id="cR">2</b><input type="range" id="iR" min="0" max="6" step="1" value="2"></label>
      <label class="calc-row"><span>Продаж лицензии, в месяц</span><b id="cB">0</b><input type="range" id="iB" min="0" max="3" step="1" value="0"></label>
      <label class="calc-row"><span>Партнёров VIP приглашаешь, в месяц</span><b id="cP">0</b><input type="range" id="iP" min="0" max="3" step="1" value="0"></label>
      <label class="calc-row"><span>Горизонт, месяцев</span><b id="cM">12</b><input type="range" id="iM" min="1" max="24" step="1" value="12"></label>
      <div class="calc-note" id="calcNote"></div>
    </div>
    <div class="calc-out">
      <div class="calc-tile glass a" style="--i:1"><div class="calc-l">Первый месяц</div><div class="calc-n chrome"><span id="oFirst">0</span> $</div></div>
      <div class="calc-tile glass hi a" style="--i:2"><div class="calc-l">Месяц <span id="oMlbl">12</span> · с накопленной арендой</div><div class="calc-n viol"><span id="oLast">0</span> $</div><div class="calc-sub">из них повторяющихся <b id="oPassive">0</b> $/мес</div></div>
      <div class="calc-tile glass a" style="--i:3"><div class="calc-l">Вход окупается</div><div class="calc-n chrome" id="oPayback">—</div><div class="calc-sub">всего за период: <b id="oTotal">0</b> $</div></div>
    </div>
  </div>
</section>
''' % LOGO

S_ROLE = '''<!-- · Роль: оператор района -->
<section class="slide">
  %s
  <div class="st-glow"></div>
  <div class="eco-city dim" data-city></div>
  <div class="eco-txt">
    <div class="eyebrow a" style="--i:0">Роль</div>
    <h1 class="st-h1 a" style="--i:1; text-align:left; font-size:4.2cqw">Ты не продаёшь лицензии.<br>Ты <em>подключаешь свой район.</em></h1>
    <div class="eco-sub a" style="--i:2">Кафе, где завтракаешь. Барбершоп, куда ходишь. Автосервис друга. Десять точек вокруг дома — это уже бизнес с ежемесячной оплатой.</div>
    <div class="st-chips a" style="--i:3; justify-content:flex-start">
      <div class="chip glass" style="text-decoration:line-through; color:var(--mut2)">продавец</div>
      <div class="chip glass" style="text-decoration:line-through; color:var(--mut2)">сетевик</div>
      <div class="chip glass hi">оператор района</div>
    </div>
  </div>
</section>
''' % LOGO

S_ZERO = '''<!-- · Старт без окружения -->
<section class="slide">
  %s
  <div class="head"><div class="eyebrow">Если вокруг нет бизнесов</div><div class="h2">Твой список может быть пустым — <em>это нормально</em></div></div>
  <div class="cards c3" style="bottom:15cqw">
    <div class="card glass frag" data-step="1">
      <div class="n viol">01</div>
      <div class="k">Заведения рядом</div>
      <div class="v">Приложение у тебя на телефоне — пробная Pro-лицензия. Демо занимает 5 минут и делается у стойки, а не по телефону</div>
    </div>
    <div class="card glass frag" data-step="2">
      <div class="n viol">02</div>
      <div class="k">Каталог UDS</div>
      <div class="v">Бизнесы, которые уже ищут систему лояльности, и клиенты, которые уже ходят в соседние точки на UDS</div>
    </div>
    <div class="card glass frag" data-step="3">
      <div class="n viol">03</div>
      <div class="k">Первые встречи — с куратором</div>
      <div class="v">На первые 2–3 встречи идём вместе. Дальше ты ведёшь сам — тем же способом</div>
    </div>
  </div>
  <div class="card glass hi frag" data-step="4" style="position:absolute; left:4.4cqw; right:4.4cqw; bottom:5cqw; flex-direction:row; align-items:center; gap:2.6cqw; padding:1.9cqw 2.6cqw; z-index:2">
    <div class="k viol" style="white-space:nowrap">Лицензии</div>
    <div class="v" style="flex:1">Покупать не нужно: клиентов подключаешь из корзины компании — 45 $ с каждого оплаченного месяца аренды, 400 $ с продажи</div>
  </div>
</section>
''' % LOGO

S_90DAYS = '''<!-- · Первые 90 дней -->
<section class="slide">
  %s
  <div class="head"><div class="eyebrow">Что делать завтра</div><div class="h2">Первые <em>90 дней</em></div></div>
  <div class="cards c3" style="bottom:15cqw">
    <div class="card glass frag" data-step="1">
      <div class="n viol">01</div>
      <div class="k">Неделя 1</div>
      <div class="v">Пакет, UDS School, пробная Pro на своём телефоне. Показываешь продукт, а не рассказываешь о нём</div>
    </div>
    <div class="card glass frag" data-step="2">
      <div class="n viol">02</div>
      <div class="k">Месяц 1</div>
      <div class="v">Десять демо в заведениях рядом. Цель — первый клиент в аренде из корзины и понимание, какие возражения повторяются</div>
    </div>
    <div class="card glass frag" data-step="3">
      <div class="n viol">03</div>
      <div class="k">Месяц 3</div>
      <div class="v">4–5 клиентов на сопровождении — вход окупается на 4–5-й месяц. Первый партнёр, которому ты показал то же самое</div>
    </div>
  </div>
  <div class="card glass hi frag" data-step="4" style="position:absolute; left:4.4cqw; right:4.4cqw; bottom:5cqw; flex-direction:row; align-items:center; gap:2.6cqw; padding:1.9cqw 2.6cqw; z-index:2">
    <div class="k viol" style="white-space:nowrap">Старт</div>
    <div class="v" style="flex:1">Следующий шаг — встреча на 30 минут: разберём твою ситуацию и посчитаем твой вариант входа в калькуляторе</div>
  </div>
</section>
''' % LOGO

# ---------- состав ----------

slides = [
    S_TITLE,
    orig('2 ·'),
    S_MANIFEST,
    S_PAIN,
    orig('4 ·'),
    S_PRODUCT_LIVE,
    S_CASE_HVISEVICH,
    S_CASE_PARFENOV,
    S_CASE_SHESTAKOVA,
    orig('8 ·'),
    orig('10 ·'),
    orig('20 ·', [
        ('<!-- 20 · Система сбыта -->', '<!-- 20 · Как устроены продажи -->'),
        ('Система сбыта <em>UDS</em>', 'Как устроены <em>продажи UDS</em>'),
        ('Продают лицензии<br>и строят сети', 'Подключают бизнесы<br>и строят команды'),
    ]),
    S_TWO_CIRCUITS,
    S_PYRAMID,
    S_TILES,
    S_RATES,
    S_CALC,
    orig('31 ·'),
    orig('32 ·', [('в левой и правой команде появляется по партнёру с таким же пакетом',
                   'два партнёра твоей команды берут такой же пакет')]),
    orig('36 ·', [('партнёр твоей структуры', 'партнёр твоей команды')]),
    S_ROLE,
    S_ZERO,
    S_90DAYS,
    orig('15 ·', [('Эффективная партнёрская сеть', 'Живое партнёрское сообщество')]),
    orig('42 ·'),
    orig('Контакты'),
]

numbered = []
for i, s in enumerate(slides, 1):
    s = re.sub(r'<!--\s*(?:\d+\s*)?·?\s*(.*?)\s*-->', lambda m: '<!-- %d · %s -->' % (i, m.group(1)), s, count=1)
    numbered.append(s)

preamble = body[:marks[0].start()]
new_body = preamble + '\n'.join(numbered) + '\n</div></div>\n\n'

EXTRA_CSS = '''
  /* v3: экосистема (D) */
  .eco-city{ position:absolute; right:-2cqw; top:0; width:58cqw; height:56.25cqw; z-index:1; pointer-events:none; }
  .eco-city i{ position:absolute; width:.7cqw; height:.7cqw; border-radius:50%; background:#C4B5FD; box-shadow:0 0 1cqw rgba(196,181,253,.9); animation:ecoPulse 3s ease-in-out infinite; }
  .eco-city i.d{ background:rgba(196,181,253,.25); box-shadow:none; animation:none; width:.5cqw; height:.5cqw; }
  .eco-city.dim i{ opacity:.45; }
  @keyframes ecoPulse{ 0%,100%{ transform:scale(1); opacity:1; } 50%{ transform:scale(1.6); opacity:.5; } }
  .eco-txt{ position:absolute; left:4.4cqw; top:50%; transform:translateY(-50%); width:60cqw; z-index:2; }
  .eco-txt .eyebrow{ margin-bottom:2.2cqw; }
  .eco-sub{ margin-top:2.4cqw; font-size:1.75cqw; color:var(--mut); line-height:1.5; max-width:50cqw; }
  body.light .eco-city i{ background:#6D28D9; box-shadow:none; }
  /* v3: кейс-обложка (B) */
  .bc{ position:absolute; inset:0; display:grid; grid-template-columns:1.1fr 1fr; z-index:2; }
  .bc-pic{ position:relative; overflow:hidden; }
  .bc-pic img{ width:100%; height:100%; object-fit:cover; display:block; filter:saturate(.9); }
  .bc-pic:after{ content:""; position:absolute; inset:0; background:linear-gradient(90deg, transparent 55%, var(--bg-base) 100%), linear-gradient(0deg, rgba(14,14,21,.55), transparent 40%); }
  .bc-txt{ padding:7cqw 5cqw 5cqw 3cqw; display:flex; flex-direction:column; justify-content:center; gap:1.1cqw; }
  .bc-num{ font-family:"Unbounded",sans-serif; font-weight:800; font-size:5.6cqw; line-height:1; letter-spacing:-.02em; }
  .bc-num span{ display:block; margin-top:.5cqw; font-size:2cqw; color:var(--mut); font-family:"Inter",sans-serif; font-weight:500; letter-spacing:0; line-height:1.2; }
  .bc-who{ font-size:2cqw; font-weight:700; color:var(--ink); }
  .bc-meta{ font-size:1.4cqw; color:var(--mut); line-height:1.5; }
  .bc-bars{ display:flex; gap:1.2cqw; align-items:flex-end; flex:0 0 12cqw; height:12cqw; margin:2.6cqw 0 1.6cqw; }
  .bc-bars div{ flex:1; background:linear-gradient(180deg,var(--acc),var(--acc2)); border-radius:.5cqw .5cqw 0 0; position:relative; }
  .bc-bars div b{ position:absolute; left:0; right:0; top:-2.3cqw; text-align:center; font-size:1.3cqw; font-weight:600; color:var(--ink); }
  .bc-bars div i{ position:absolute; left:0; right:0; bottom:-2.1cqw; text-align:center; font-size:1.05cqw; color:var(--mut2); font-style:normal; }
  /* v3: плитки пакетов (C) */
  .tiles{ position:absolute; inset:14.5cqw 4.4cqw 6cqw; display:grid; grid-template-columns:repeat(5,1fr); gap:1.4cqw; z-index:2; align-content:center; }
  .tile{ padding:1.8cqw 1.5cqw; display:flex; flex-direction:column; gap:.8cqw; min-height:26cqw; }
  .tile .tp{ font-size:1.2cqw; letter-spacing:.14em; text-transform:uppercase; color:var(--mut2); font-weight:600; }
  .tile .tc{ font-family:"Unbounded",sans-serif; font-weight:800; font-size:2.4cqw; }
  .tile .td{ font-size:1.22cqw; color:var(--bar-text); line-height:1.5; margin-top:auto; }
  .tile .td b{ color:var(--acc); font-weight:700; }
  .tile .ok{ color:#9fe0bb; } .tile .no{ color:#f0aab6; }
  /* v3: калькулятор */
  .calc{ position:absolute; inset:14.5cqw 4.4cqw 6cqw; display:grid; grid-template-columns:1.15fr 1fr; gap:2.4cqw; z-index:2; align-items:stretch; }
  .calc-ctl{ padding:2cqw 2.6cqw; display:flex; flex-direction:column; justify-content:center; gap:1.5cqw; }
  .calc-pk{ display:flex; gap:.6cqw; margin-bottom:.4cqw; }
  .calc-pk button{ flex:1; padding:.9cqw .4cqw; border-radius:99cqw; border:1px solid var(--panel-line); background:transparent; color:var(--mut); font:600 1.15cqw/1 "Inter",sans-serif; cursor:pointer; }
  .calc-pk button.on{ background:var(--acc-dim); border-color:rgba(167,139,250,.6); color:var(--ink); }
  .calc-row{ display:grid; grid-template-columns:1fr auto; gap:.3cqw 1.6cqw; align-items:center; font-size:1.38cqw; color:var(--bar-text); }
  .calc-row b{ font-family:"Unbounded",sans-serif; font-weight:800; font-size:1.8cqw; color:var(--acc); font-variant-numeric:tabular-nums; min-width:3cqw; text-align:right; }
  .calc-row input{ grid-column:1/-1; width:100%; accent-color:var(--acc); height:1.2cqw; cursor:pointer; }
  .calc-row.off{ opacity:.35; pointer-events:none; }
  .calc-note{ font-size:1.05cqw; color:var(--mut2); line-height:1.45; border-top:1px solid var(--panel-line); padding-top:1.1cqw; }
  .calc-out{ display:grid; grid-template-rows:1fr 1.3fr 1fr; gap:1.6cqw; }
  .calc-tile{ padding:1.6cqw 2.2cqw; display:flex; flex-direction:column; justify-content:center; gap:.5cqw; }
  .calc-l{ font-size:1.2cqw; letter-spacing:.14em; text-transform:uppercase; color:var(--mut2); font-weight:600; }
  .calc-n{ font-family:"Unbounded",sans-serif; font-weight:800; font-size:3.2cqw; line-height:1.1; font-variant-numeric:tabular-nums; }
  .calc-tile.hi .calc-n{ font-size:4cqw; }
  .calc-sub{ font-size:1.25cqw; color:var(--mut); }
  .calc-sub b{ color:var(--ink); }
  body.calc-mode .nav-zone{ pointer-events:none; }
  @media print{ .calc-row input, .calc-pk{ display:none; } }
  @media (prefers-reduced-motion: reduce){ .frag, .tm-grid20 svg, .tm-dots, [data-spot], .mk-map .frag, .eco-city i{ transition:none!important; animation:none!important; } }
'''
head = head.replace('</style>', EXTRA_CSS + '</style>', 1)
head = head.replace('<title>Бизнес на продукте UDS — Александр Ракипов</title>',
                    '<title>Бизнес на продукте UDS — Александр Ракипов (v3)</title>')

GUARD = "    if(e.target === jump) return;\n    if(/^(INPUT|SELECT|TEXTAREA|BUTTON)$/.test(e.target.tagName)) return;\n"
if "    if(e.target === jump) return;\n" not in tail:
    raise SystemExit('не нашёл guard')
tail = tail.replace("    if(e.target === jump) return;\n", GUARD, 1)
if "    cur = n;\n" not in tail:
    raise SystemExit('не нашёл cur = n')
tail = tail.replace("    cur = n;\n", "    cur = n;\n    document.body.classList.toggle('calc-mode', s.id === 'calcSlide');\n", 1)

V3_JS = '''
<script>
// Калькулятор: пакет -> права и ставки. Корзина компании (Start): аренда 45 $/мес, продажа 400 $.
// Своя лицензия (Business+): аренда 85 $/мес, выкуп 1 500 $ (+11 $/мес) — цифры маркетинг-плана из деки.
(function(){
  var PK = {
    start:    { price: 850,   lic: 0,  rent: 45, sale: 400,  saleSub: 0,  label: 'Start: своих лицензий нет — ставки корзины компании (45 $/мес, 400 $). Продажи тоже из корзины.' },
    business: { price: 1900,  lic: 2,  rent: 85, sale: 1500, saleSub: 11, label: 'Business: 2 свои лицензии — 85 $/мес аренда или 1 500 $ выкуп. Продать больше двух своих нельзя.' },
    premium:  { price: 3950,  lic: 6,  rent: 85, sale: 1500, saleSub: 11, label: 'Premium: 6 своих лицензий — 85 $/мес или 1 500 $.' },
    vip:      { price: 6350,  lic: 12, rent: 85, sale: 1500, saleSub: 11, label: 'VIP: 12 своих лицензий. Бонус 1 000 $ за приглашённого партнёра VIP, 600 $ за каждую пару.' },
    vip3:     { price: 16450, lic: 36, rent: 85, sale: 1500, saleSub: 11, label: '3 VIP: 36 своих лицензий. Командный бонус 3 600 $ за пару партнёров 3 VIP.' }
  };
  var PARTNER_BONUS = 1000, TEAM_BONUS = 600, PARTNER_SUB = 3;
  var pk = 'start';
  var ids = ['R','B','P','M'];
  function val(k){ return +document.getElementById('i'+k).value; }
  function fmt(n){ return Math.round(n).toLocaleString('ru-RU'); }
  function calc(){
    var p = PK[pk], R = val('R'), B = val('B'), P = val('P'), M = val('M');
    ids.forEach(function(k){ document.getElementById('c'+k).textContent = val(k); });
    var total = 0, first = 0, last = 0, passive = 0, payback = null, sold = 0;
    for(var t = 1; t <= M; t++){
      var salesNow = B;
      if(p.lic > 0){ salesNow = Math.max(0, Math.min(B, p.lic - sold)); } // своих лицензий конечное число
      sold += salesNow;
      var pairs = Math.floor(P*t/2) - Math.floor(P*(t-1)/2);
      var recurring = p.rent*R*t + p.saleSub*sold + PARTNER_SUB*P*t;
      var income = p.sale*salesNow + PARTNER_BONUS*P + TEAM_BONUS*pairs + recurring;
      total += income;
      if(t === 1) first = income;
      if(t === M){ last = income; passive = recurring; }
      if(payback === null && total >= p.price) payback = t;
    }
    document.getElementById('oFirst').textContent = fmt(first);
    document.getElementById('oLast').textContent = fmt(last);
    document.getElementById('oPassive').textContent = fmt(passive);
    document.getElementById('oTotal').textContent = fmt(total);
    document.getElementById('oMlbl').textContent = M;
    document.getElementById('oPayback').textContent = payback === null ? 'позже ' + M + ' мес' : (payback === 1 ? 'в 1-й месяц' : 'на ' + payback + '-й месяц');
    document.getElementById('calcNote').textContent = p.label;
  }
  ids.forEach(function(k){
    var el = document.getElementById('i'+k);
    el.addEventListener('input', calc);
    el.addEventListener('keydown', function(e){ e.stopPropagation(); });
  });
  Array.prototype.forEach.call(document.querySelectorAll('#pk button'), function(b){
    b.addEventListener('click', function(){
      pk = b.dataset.pk;
      Array.prototype.forEach.call(document.querySelectorAll('#pk button'), function(x){ x.classList.toggle('on', x === b); });
      calc();
    });
  });
  calc();
})();
// Точки «карты» на слайдах экосистемы
(function(){
  Array.prototype.forEach.call(document.querySelectorAll('[data-city]'), function(c){
    for(var k = 0; k < 140; k++){
      var i = document.createElement('i');
      var r = Math.pow(Math.random(), .6) * 46, a = Math.random() * 6.283;
      i.style.left = (50 + Math.cos(a) * r) + '%'; i.style.top = (50 + Math.sin(a) * r * .8) + '%';
      if(k % 9) i.className = 'd'; else i.style.animationDelay = (Math.random() * 3) + 's';
      c.appendChild(i);
    }
  });
})();
</script>
'''
for anchor in ('</body>', '</html>'):
    if anchor in tail:
        tail = tail.replace(anchor, V3_JS + anchor, 1); break
else:
    tail = tail + V3_JS

io.open(DST, 'w', encoding='utf-8').write(head + new_body + tail)
print('ok ->', DST, '| слайдов:', len(numbered))
