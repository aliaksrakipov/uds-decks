# -*- coding: utf-8 -*-
# ===== Генератор стабильных id слайдов + манифеста для редактора порядка =====
# Запускать заново, если в produkt/marketing/pervichka добавили, убрали или
# переставили слайды — иначе манифест (для edit.html) разойдётся с реальной
# декой. biznes.html НЕ трогает — у неё свой вшитый движок, отдельная история.
#
# Что делает для каждой деки:
#   1) вписывает data-slide-id="<deck>-<slug>" в каждую <section class="slide"...>
#      (slug — из заголовка в HTML-комментарии, не из позиции: переживает
#      переносы слайдов местами, в отличие от порядкового номера);
#   2) пишет decks/<deck>.slides.json — [{id, title, locked}], locked=true
#      у титула и визитки-спикера (их порядок редактор не даёт менять).
#
# Комментарий <!-- N · Заголовок --> и следующая за ним <section class="slide"...>
# сопоставляются СТРОГО ПО ПОРЯДКУ (i-й комментарий -> i-я секция), а не поиском
# конкретного варианта тега — у слайда-визитки, например, тег отличается
# (<section class="slide" data-partner-slide></section>), и точный поиск
# по литералу '<section class="slide">' на нём проваливается и уводит
# сопоставление вбок на весь остаток файла.
#
# Использование: python3 _tools/gen-slide-manifest.py

import io, re, json, os

DECKS = ['produkt', 'marketing', 'pervichka']
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TR = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e','ж':'zh','з':'z','и':'i',
      'й':'i','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r','с':'s','т':'t',
      'у':'u','ф':'f','х':'h','ц':'c','ч':'ch','ш':'sh','щ':'sch','ъ':'','ы':'y','ь':'',
      'э':'e','ю':'yu','я':'ya'}

def slugify(text):
    out = []
    for ch in text.lower():
        if ch.isascii() and ch.isalnum():
            out.append(ch)
        elif ch in TR:
            out.append(TR[ch])
        else:
            out.append('-')
    s = re.sub(r'-+', '-', ''.join(out)).strip('-')
    return s[:40]

def clean_title(raw):
    t = re.sub(r'\(src\s*\d+\)', '', raw)
    t = t.split(' · ВАЖНО')[0]
    return t.strip(' —-')

COMMENT_RE = re.compile(r'<!--\s*(\d+)\s*·\s*(.*?)-->', re.S)
SECTION_RE = re.compile(r'<section class="slide"[^>]*>')

for deck in DECKS:
    path = os.path.join(BASE, 'decks', deck + '.html')
    s = io.open(path, encoding='utf-8').read()
    s = re.sub(r' data-slide-id="[^"]*"', '', s)  # идемпотентность: снимаем старые id перед перегенерацией

    comments = list(COMMENT_RE.finditer(s))
    sections = list(SECTION_RE.finditer(s))

    if len(comments) != len(sections):
        print('MISMATCH', deck, 'comments:', len(comments), 'sections:', len(sections), '- ПРОПУСКАЮ, проверь руками')
        continue

    slides = []
    used = {}
    out = s
    offset = 0

    for i in range(len(comments)):
        num = comments[i].group(1)
        title = clean_title(comments[i].group(2))
        slug = slugify(title) or ('slide-' + num)
        base_slug = slug
        n = 2
        while slug in used:
            slug = base_slug + '-' + str(n)
            n += 1
        used[slug] = True
        full_id = deck + '-' + slug

        sec = sections[i]
        insert_at = sec.end() - len('>') + offset  # прямо перед закрывающим '>' тега
        attr = ' data-slide-id="' + full_id + '"'
        out = out[:insert_at] + attr + out[insert_at:]
        offset += len(attr)

        locked = (i == 0) or ('визитка' in title.lower())
        slides.append({'id': full_id, 'title': title, 'locked': locked})

    io.open(path, 'w', encoding='utf-8').write(out)
    manifest_path = os.path.join(BASE, 'decks', deck + '.slides.json')
    io.open(manifest_path, 'w', encoding='utf-8').write(json.dumps(slides, ensure_ascii=False, indent=2))
    print(deck, '-', len(slides), 'slides ->', manifest_path)
