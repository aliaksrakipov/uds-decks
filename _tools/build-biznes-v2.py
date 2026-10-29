# -*- coding: utf-8 -*-
# Сборка decks/biznes-v2.html из decks/biznes.html: шапка/стили/движок — из оригинала,
# состав и порядок слайдов — новый (драматургия для будущих партнёров + калькулятор дохода).
# Переиспользуемые слайды берутся из оригинала по маркеру <!-- N · … --> с точечными заменами.
# Запуск: python3 _tools/build-biznes-v2.py

import io, os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, 'decks', 'biznes.html')
DST = os.path.join(BASE, 'decks', 'biznes-v2.html')

src = io.open(SRC, encoding='utf-8').read()
body_start = src.index('<div class="stage">')
body_end = src.index('<div class="nav-zone prev"')
head = src[:body_start]
body = src[body_start:body_end]
tail = src[body_end:]

marks = list(re.finditer(r'<!--\s*(\d+\s*·[^>]*?|Контакты)\s*-->', body))

def orig(prefix, subs=()):
    """Слайд оригинала по началу заголовка маркера, с заменами (старое, новое)."""
    for k, m in enumerate(marks):
        if m.group(1).strip().startswith(prefix):
            end = marks[k + 1].start() if k + 1 < len(marks) else len(body)
            chunk = body[m.start():end].rstrip() + '\n'
            for old, new in subs:
                # в оригинале много неразрывных пробелов — пробел в шаблоне замены ловит оба
                rx = re.compile(re.escape(old).replace('\\ ', '[  ]'))
                if not rx.search(chunk):
                    raise SystemExit('замена не нашлась в слайде %r: %r' % (prefix, old))
                chunk = rx.sub(lambda _m: new, chunk, count=1)
            return chunk
    raise SystemExit('нет слайда ' + prefix)

LOGO = '<div class="logo">uds<span>Partner</span></div>'

# ---------- новые слайды ----------

S_INSIGHT = '''<!-- · Инсайт спикера -->
<section class="slide">
  <svg class="spark sm" style="right:14cqw; top:9cqw;"><use href="#sparkle"/></svg>
  %s
  <div class="st-glow"></div>
  <div class="st-center">
    <div>
      <div class="eyebrow a" style="--i:0">Почему я здесь</div>
      <h1 class="st-h1 a" style="--i:1">10 лет я строю <em>системы</em><br>для чужих бизнесов<small>100+ проектов полного цикла для международной IT-компании. Главный навык — превращать хаос в конвейер, где каждый шаг измерим.</small></h1>
      <div class="st-chips">
        <div class="chip glass a" style="--i:2">Увидел UDS</div>
        <div class="chip glass a" style="--i:3">Узнал ту же логику</div>
        <div class="chip glass hi a" style="--i:4">Система вместо хаоса — для любого магазина, салона, кафе</div>
      </div>
    </div>
  </div>
</section>
''' % LOGO

def shot(i, src_, cap):
    return ('<figure class="a" style="--i:%d; margin:0; display:flex; flex-direction:column; align-items:center; gap:1.1cqw">'
            '<img src="../assets/img/pervichka/%s" alt="%s" style="height:31cqw; border-radius:1.4cqw; border:1px solid var(--panel-line)">'
            '<figcaption style="font-size:1.3cqw; color:var(--mut)">%s</figcaption></figure>') % (i, src_, cap, cap)

S_PRODUCT_LIVE = '''<!-- · Продукт живьём -->
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

S_TWO_CIRCUITS = '''<!-- · Два контура дохода -->
<section class="slide">
  %s
  <div class="head"><div class="eyebrow">Откуда деньги</div><div class="h2">Два контура — <em>честно</em></div></div>
  <div class="cards c2" style="bottom:15cqw">
    <div class="card glass hi frag" data-step="1" data-spot="1">
      <div class="n viol">01</div>
      <div class="k">Продуктовый</div>
      <div class="v">Продаёшь лицензии бизнесам, внедряешь и сопровождаешь, получаешь долю с их абонентской платы. Платит <b style="color:var(--ink)">бизнес</b> — за продукт, которым пользуется каждый день</div>
    </div>
    <div class="card glass frag" data-step="2" data-spot="2">
      <div class="n viol">02</div>
      <div class="k">Партнёрский</div>
      <div class="v">Приглашаешь партнёров, обучаешь, получаешь бонус с их пакетов и продаж. Ускоритель — но <b style="color:var(--ink)">не замена</b> первому контуру</div>
    </div>
  </div>
  <div class="card glass frag" data-step="3" style="position:absolute; left:4.4cqw; right:4.4cqw; bottom:5cqw; flex-direction:row; align-items:center; gap:2.6cqw; padding:1.9cqw 2.6cqw; z-index:2">
    <div class="k viol" style="white-space:nowrap">Моя позиция</div>
    <div class="v" style="flex:1">Я зарабатываю на первом контуре и строю команду из тех, кто тоже продаёт продукт. Так растёт экосистема, а не список фамилий</div>
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
      <div class="k">Деньги идут от клиентов</div>
      <div class="v">Основной доход партнёра — продажа лицензии бизнесу и его абонентская плата. Не взносы новичков</div>
    </div>
    <div class="card glass frag" data-step="3">
      <div class="k">Порог входа — одна продажа</div>
      <div class="v">Стартовый пакет 850 $. Одна проданная лицензия по выкупу приносит 1 500 $ — вложения возвращаются первой же сделкой</div>
    </div>
  </div>
  <div class="card glass hi frag" data-step="4" style="position:absolute; left:4.4cqw; right:4.4cqw; bottom:5cqw; flex-direction:row; align-items:center; gap:2.6cqw; padding:1.9cqw 2.6cqw; z-index:2">
    <div class="k viol" style="white-space:nowrap">Разница</div>
    <div class="v" style="flex:1">В пирамиде деньги есть только пока приходят новые участники. Здесь — пока бизнесы пользуются продуктом. Это проверяется за 10 минут в приложении</div>
  </div>
</section>
''' % LOGO

S_PACKAGE_INCOME = '''<!-- · Доход по пакетам -->
<section class="slide">
  %s
  <div class="head"><div class="eyebrow">Розница</div><div class="h2">Доход <em>по пакетам</em></div></div>
  <div class="tbl">
    <div class="thead-note">Все лицензии пакета сданы в аренду (85 $/мес за каждую) — или проданы по выкупу (1 500 $ за каждую)</div>
    <table>
      <tr><th>Статус</th><th>Вложения</th><th>Лицензий</th><th>Аренда</th><th>Выкуп</th></tr>
      <tr class="hl frag" data-step="1"><td><b>3 VIP</b></td><td>16 450 $</td><td>36</td><td class="acc">3 060 $/мес</td><td class="acc">54 000 $</td></tr>
      <tr class="frag" data-step="2"><td><b>VIP</b></td><td>6 350 $</td><td>12</td><td>1 020 $/мес</td><td>18 000 $</td></tr>
      <tr class="frag" data-step="3"><td><b>Premium</b></td><td>3 950 $</td><td>6</td><td>510 $/мес</td><td>9 000 $</td></tr>
      <tr class="frag" data-step="4"><td><b>Business</b></td><td>1 900 $</td><td>2</td><td>170 $/мес</td><td>3 000 $</td></tr>
    </table>
  </div>
</section>
''' % LOGO

S_CALC = '''<!-- · Калькулятор дохода -->
<section class="slide" id="calcSlide">
  %s
  <div class="head"><div class="eyebrow">Твой расчёт</div><div class="h2">Посчитаем <em>твой месяц</em></div></div>
  <div class="calc">
    <div class="calc-ctl glass a" style="--i:0">
      <label class="calc-row"><span>Лицензий в аренду, в месяц</span><b id="cR">1</b><input type="range" id="iR" min="0" max="6" step="1" value="1"></label>
      <label class="calc-row"><span>Лицензий по выкупу, в месяц</span><b id="cB">1</b><input type="range" id="iB" min="0" max="4" step="1" value="1"></label>
      <label class="calc-row"><span>Партнёров VIP приглашаешь, в месяц</span><b id="cP">1</b><input type="range" id="iP" min="0" max="4" step="1" value="1"></label>
      <label class="calc-row"><span>Горизонт, месяцев</span><b id="cM">12</b><input type="range" id="iM" min="1" max="24" step="1" value="12"></label>
      <div class="calc-note">Ставки из маркетинг-плана: аренда 85 $/мес, выкуп 1 500 $ + 11 $/мес, бонус за партнёра VIP 1 000 $, командный бонус 600 $ за каждую пару, абонплата 3 $/мес с партнёра</div>
    </div>
    <div class="calc-out">
      <div class="calc-tile glass a" style="--i:1"><div class="calc-l">Первый месяц</div><div class="calc-n chrome"><span id="oFirst">0</span> $</div></div>
      <div class="calc-tile glass hi a" style="--i:2"><div class="calc-l">Месяц <span id="oMlbl">12</span> — с накопленным пассивом</div><div class="calc-n viol"><span id="oLast">0</span> $</div><div class="calc-sub">из них пассив <b id="oPassive">0</b> $/мес</div></div>
      <div class="calc-tile glass a" style="--i:3"><div class="calc-l">Всего за <span id="oMlbl2">12</span> мес</div><div class="calc-n chrome"><span id="oTotal">0</span> $</div></div>
    </div>
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
      <div class="v">Выбираешь пакет, проходишь UDS School, со мной собираем список из 20 бизнесов, которым продукт нужен уже сейчас</div>
    </div>
    <div class="card glass frag" data-step="2">
      <div class="n viol">02</div>
      <div class="k">Месяц 1</div>
      <div class="v">Первые встречи — вместе. Цель: первая подключённая компания и первый партнёр, который увидел, как это работает</div>
    </div>
    <div class="card glass frag" data-step="3">
      <div class="n viol">03</div>
      <div class="k">Месяц 3</div>
      <div class="v">Свои 3–5 клиентов на сопровождении, первые абонентские платы, команда из 2–3 партнёров — и ты сам ведёшь такие встречи</div>
    </div>
  </div>
  <div class="card glass hi frag" data-step="4" style="position:absolute; left:4.4cqw; right:4.4cqw; bottom:5cqw; flex-direction:row; align-items:center; gap:2.6cqw; padding:1.9cqw 2.6cqw; z-index:2">
    <div class="k viol" style="white-space:nowrap">Старт</div>
    <div class="v" style="flex:1">Следующий шаг — встреча на 30 минут: разберём твою ситуацию, посчитаем твой вариант входа и первых клиентов</div>
  </div>
</section>
''' % LOGO

# ---------- состав деки ----------

slides = [
    orig('1 ·', [('8 000+ компаний', '7 000+ компаний')]),
    orig('2 ·'),
    S_INSIGHT,
    orig('3 ·'),
    orig('4 ·'),
    S_PRODUCT_LIVE,
    orig('5 ·'),
    orig('8 ·'),
    orig('9 ·', [
        ('Рынок предпринимателей — <em>неограничен</em>', 'Рынок — <em>больше, чем кажется</em>'),
        ('<span class="cnt" data-to="500">0</span> млн</div>\n        <div class="mk-l">предпринимателей · весь мир</div>',
         '<span class="cnt" data-to="44">0</span> млн</div>\n        <div class="mk-l">загрузок приложения UDS · по данным компании</div>'),
    ]),
    orig('10 ·'),
    orig('13 ·'),
    orig('14 ·', [
        ('растёт вместе с твоей сетью', 'растёт вместе с твоей командой'),
        ('<div class="k">Рынок сбыта — весь мир</div><div class="v">Продукт работает на 29 языках в десятках стран</div>',
         '<div class="k">Рынок только открывается</div><div class="v">В России продукт работает 10+ лет, в Беларуси — первые партнёры. Лучшее время заходить — пока конкуренция нулевая</div>'),
        ('в твоей структуре', 'в твоей команде'),
    ]),
    orig('17 ·', [('Система сбыта', 'Система продаж')]),
    orig('20 ·', [
        ('<!-- 20 · Система сбыта -->', '<!-- 20 · Система продаж -->'),
        ('Система сбыта <em>UDS</em>', 'Как устроены <em>продажи UDS</em>'),
        ('Продают лицензии<br>и строят сети', 'Продают лицензии<br>и строят команды'),
    ]),
    S_TWO_CIRCUITS,
    S_PYRAMID,
    orig('16 ·', [('Готовая модель сбыта', 'Готовая модель продаж')]),
    orig('21 ·'),
    orig('22 ·'),
    orig('23 ·', [('Оптовые продажи', 'Партнёрские продажи')]),
    orig('24 ·'),
    S_PACKAGE_INCOME,
    orig('27 ·'),
    orig('28 ·', [('партнёров строят их сети', 'партнёров строят свои команды')]),
    orig('31 ·'),
    orig('32 ·', [('в левой и правой команде появляется по партнёру с таким же пакетом',
                   'два партнёра твоей команды берут такой же пакет')]),
    orig('36 ·', [('партнёр твоей структуры', 'партнёр твоей команды')]),
    S_CALC,
    orig('15 ·', [('Эффективная партнёрская сеть', 'Живое партнёрское сообщество')]),
    orig('39 ·'),
    orig('40 ·', [('<!-- 40 · Кейс-заглушка 2 -->', '<!-- 40 · Кейс: Евгений Парфёнов -->')]),
    orig('38 ·'),
    S_90DAYS,
    orig('42 ·'),
    orig('Контакты'),
]

# перенумеровать маркеры подряд
numbered = []
for i, s in enumerate(slides, 1):
    s = re.sub(r'<!--\s*(?:\d+\s*)?·?\s*(.*?)\s*-->', lambda m: '<!-- %d · %s -->' % (i, m.group(1)), s, count=1)
    numbered.append(s)

preamble = body[:marks[0].start()]  # <div class="stage">… + svg symbol sparkle
new_body = preamble + '\n'.join(numbered) + '\n</div></div>\n\n'

# ---------- дополнительные стили ----------

EXTRA_CSS = '''
  /* v2: калькулятор */
  .calc{ position:absolute; inset:14.5cqw 4.4cqw 6cqw; display:grid; grid-template-columns:1.15fr 1fr; gap:2.4cqw; z-index:2; align-items:stretch; }
  .calc-ctl{ padding:2.4cqw 2.6cqw; display:flex; flex-direction:column; justify-content:center; gap:1.9cqw; }
  .calc-row{ display:grid; grid-template-columns:1fr auto; gap:.4cqw 1.6cqw; align-items:center; font-size:1.45cqw; color:var(--bar-text); }
  .calc-row b{ font-family:"Unbounded",sans-serif; font-weight:800; font-size:1.9cqw; color:var(--acc); font-variant-numeric:tabular-nums; min-width:3cqw; text-align:right; }
  .calc-row input{ grid-column:1/-1; width:100%; accent-color:var(--acc); height:1.2cqw; cursor:pointer; }
  .calc-note{ font-size:1.1cqw; color:var(--mut2); line-height:1.45; border-top:1px solid var(--panel-line); padding-top:1.3cqw; }
  .calc-out{ display:grid; grid-template-rows:1fr 1.3fr 1fr; gap:1.6cqw; }
  .calc-tile{ padding:1.8cqw 2.2cqw; display:flex; flex-direction:column; justify-content:center; gap:.5cqw; }
  .calc-l{ font-size:1.25cqw; letter-spacing:.14em; text-transform:uppercase; color:var(--mut2); font-weight:600; }
  .calc-n{ font-family:"Unbounded",sans-serif; font-weight:800; font-size:3.4cqw; line-height:1.1; font-variant-numeric:tabular-nums; }
  .calc-tile.hi .calc-n{ font-size:4.2cqw; }
  .calc-sub{ font-size:1.3cqw; color:var(--mut); }
  .calc-sub b{ color:var(--ink); }
  body.calc-mode .nav-zone{ pointer-events:none; }
  @media print{ .calc-row input{ display:none; } }
  @media (prefers-reduced-motion: reduce){ .frag, .tm-grid20 svg, .tm-dots, [data-spot], .mk-map .frag{ transition:none!important; } }
'''
head = head.replace('</style>', EXTRA_CSS + '</style>', 1)
head = head.replace('<title>Бизнес на продукте UDS — Александр Ракипов</title>',
                    '<title>Бизнес на продукте UDS — Александр Ракипов (v2)</title>')

# ---------- движок: стрелки на ползунках не листают слайды + калькулятор ----------

GUARD = "    if(e.target === jump) return;\n    if(/^(INPUT|SELECT|TEXTAREA)$/.test(e.target.tagName)) return;\n"
if "    if(e.target === jump) return;\n" not in tail:
    raise SystemExit('не нашёл место для guard в движке')
tail = tail.replace("    if(e.target === jump) return;\n", GUARD, 1)
# на слайде калькулятора боковые зоны клика не должны перехватывать ползунки
if "    cur = n;\n" not in tail:
    raise SystemExit('не нашёл cur = n в движке')
tail = tail.replace("    cur = n;\n", "    cur = n;\n    document.body.classList.toggle('calc-mode', s.id === 'calcSlide');\n", 1)

CALC_JS = '''
<script>
// Калькулятор дохода: ставки — из слайдов маркетинг-плана этой же деки.
(function(){
  var RENT = 85, BUYOUT = 1500, BUYOUT_SUB = 11, PARTNER_BONUS = 1000, TEAM_BONUS = 600, PARTNER_SUB = 3;
  var ids = ['R','B','P','M'];
  function val(k){ return +document.getElementById('i'+k).value; }
  function fmt(n){ return Math.round(n).toLocaleString('ru-RU'); }
  function calc(){
    var R = val('R'), B = val('B'), P = val('P'), M = val('M');
    ids.forEach(function(k){ document.getElementById('c'+k).textContent = val(k); });
    var total = 0, first = 0, last = 0, passive = 0;
    for(var t = 1; t <= M; t++){
      var pairs = Math.floor(P*t/2) - Math.floor(P*(t-1)/2);
      var recurring = RENT*R*t + BUYOUT_SUB*B*t + PARTNER_SUB*P*t;
      var income = BUYOUT*B + PARTNER_BONUS*P + TEAM_BONUS*pairs + recurring;
      total += income;
      if(t === 1) first = income;
      if(t === M){ last = income; passive = recurring; }
    }
    document.getElementById('oFirst').textContent = fmt(first);
    document.getElementById('oLast').textContent = fmt(last);
    document.getElementById('oPassive').textContent = fmt(passive);
    document.getElementById('oTotal').textContent = fmt(total);
    document.getElementById('oMlbl').textContent = M;
    document.getElementById('oMlbl2').textContent = M;
  }
  ids.forEach(function(k){
    var el = document.getElementById('i'+k);
    el.addEventListener('input', calc);
    el.addEventListener('keydown', function(e){ e.stopPropagation(); });
  });
  calc();
})();
</script>
'''
for anchor in ('</body>', '</html>'):
    if anchor in tail:
        tail = tail.replace(anchor, CALC_JS + anchor, 1)
        break
else:
    tail = tail + CALC_JS
if 'Калькулятор дохода: ставки' not in tail:
    raise SystemExit('скрипт калькулятора не вставился')

io.open(DST, 'w', encoding='utf-8').write(head + new_body + tail)
print('ok ->', DST, '| слайдов:', len(numbered))
