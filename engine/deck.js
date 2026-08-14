// ===== Движок деки UDS · общий для всех тем =====
// HUD (навигация, прогресс, тема) вставляется сюда, чтобы не дублировать в каждой деке
(function(){
  var frag = document.createElement('div');
  frag.innerHTML =
    '<div class="nav-zone prev" aria-label="Назад"></div>' +
    '<div class="nav-zone next" aria-label="Вперёд"></div>' +
    '<div class="hud-top">' +
      '<input class="jump" id="jump" type="number" min="1" inputmode="numeric" placeholder="№ →">' +
      '<button class="theme-btn" id="themeBtn">T · тема: тёмная</button>' +
    '</div>' +
    '<div class="hud-line"><i id="prog"></i></div>' +
    '<div class="count" id="count"></div>' +
    '<div class="hint" id="hint">→ ← / PgUp PgDn (презентор) / клик по краям · F — фулскрин · T — тема · цифры+Enter — прыжок на слайд</div>';
  while(frag.firstChild) document.body.appendChild(frag.firstChild);
  var sym = document.createElementNS('http://www.w3.org/2000/svg','svg');
  sym.setAttribute('style','display:none'); sym.setAttribute('aria-hidden','true');
  sym.innerHTML = '<symbol id="sparkle" viewBox="0 0 100 100"><path fill="currentColor" d="M50 0 C54 33 67 46 100 50 C67 54 54 67 50 100 C46 67 33 54 0 50 C33 46 46 33 50 0 Z"/></symbol>';
  document.body.appendChild(sym);

  // Клик по логотипу «uds» (слева сверху) — возврат в каталог с сохранением партнёра.
  // Лого живёт внутри .deck, а .deck из-за container-type — свой stacking context,
  // и подняться над fixed нав-зонами изнутри нельзя. Поэтому ссылка вешается на body
  // как fixed поверх всего, а позиция лого пересчитывается от прямоугольника деки.
  var deckEl = document.getElementById('deck');
  if (deckEl && document.querySelector('.logo')) {
    var p = new URLSearchParams(location.search).get('p');
    var home = document.createElement('a');
    home.href = '../index.html' + (p ? '?p=' + p : '');
    home.title = 'В каталог презентаций';
    home.setAttribute('aria-label', 'В каталог презентаций');
    home.style.cssText = 'position:fixed; z-index:12; cursor:pointer;';
    document.body.appendChild(home);
    var place = function(){
      var r = deckEl.getBoundingClientRect(), u = r.width / 100; // 1cqw в px
      home.style.left  = (r.left + 3.6 * u) + 'px';
      home.style.top   = (r.top  + 3.2 * u) + 'px';
      home.style.width  = (15 * u) + 'px';
      home.style.height = (3.6 * u) + 'px';
    };
    place();
    window.addEventListener('resize', place);
    document.addEventListener('fullscreenchange', place);
  }
})();
// Основной движок стартует после DECK_READY (partner.js): партнёр может
// догружаться из базы, и слайды надо считать после вставки/удаления визитки.
function __deckInit(){
  var slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
  var cur = Math.min(Math.max((parseInt(location.hash.slice(1),10)||1)-1,0), slides.length-1);
  var prog = document.getElementById('prog'), count = document.getElementById('count'),
      hint = document.getElementById('hint'), themeBtn = document.getElementById('themeBtn');

  var steps = {}; // индекс слайда -> открыто шагов

  function fragRange(f){
    var from = f.hasAttribute('data-step') ? +f.dataset.step : 1;
    var until = f.hasAttribute('data-until') ? +f.dataset.until : Infinity;
    return [from, until];
  }
  function maxStep(s){
    var m = 0;
    s.querySelectorAll('.frag').forEach(function(f){
      var r = fragRange(f);
      m = Math.max(m, r[0], isFinite(r[1]) ? r[1] : 0);
    });
    var sp = s.querySelectorAll('[data-spot]').length;
    if(sp) m = Math.max(m, sp + 1);
    return m;
  }
  function animateCnt(el){
    var to = +el.dataset.to, dur = 900, t0 = null;
    if(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches){
      el.textContent = to.toLocaleString('ru-RU'); return;
    }
    function tick(t){
      if(t0 === null) t0 = t;
      var k = Math.min(1, (t - t0) / dur);
      k = 1 - Math.pow(1 - k, 3);
      el.textContent = Math.round(to * k).toLocaleString('ru-RU');
      if(k < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }
  function applySteps(s, st){
    s.querySelectorAll('.frag').forEach(function(f){
      var r = fragRange(f);
      var vis = st >= r[0] && st < r[1];
      var was = f.classList.contains('in');
      f.classList.toggle('in', vis);
      if(vis && !was) f.querySelectorAll('.cnt').forEach(animateCnt);
    });
    // спотлайт: узел рождается уже в фокусе, следующий клик ставит его на место
    var spots = s.querySelectorAll('[data-spot]');
    spots.forEach(function(el){
      var n = +el.dataset.spot;
      var appeared = !el.classList.contains('frag') || el.classList.contains('in');
      el.classList.toggle('focus', appeared && st === n);
      el.classList.toggle('dim', appeared && st > 0 && st <= spots.length && st !== n);
    });
  }

  function show(n, dir){
    n = Math.min(Math.max(n,0), slides.length-1);
    slides.forEach(function(s,i){
      s.classList.toggle('cur', i===n);
      if(i!==n) s.classList.remove('go');
    });
    var s = slides[n];
    // при входе вперёд — фрагменты закрыты, при входе назад — открыты
    // ?qa=1 — режим проверки: все пошаговые фрагменты сразу раскрыты (для скриншотов)
    steps[n] = (dir === -1 || /[?&]qa=1/.test(location.search)) ? maxStep(s) : 0;
    applySteps(s, steps[n]);
    s.querySelectorAll('.cnt-auto').forEach(animateCnt);
    requestAnimationFrame(function(){ requestAnimationFrame(function(){ s.classList.add('go'); }); });
    cur = n;
    prog.style.width = ((n+1)/slides.length*100) + '%';
    count.textContent = (n+1) + ' / ' + slides.length;
    history.replaceState(null,'','#'+(n+1));
  }
  function next(){
    var s = slides[cur], st = steps[cur] || 0;
    if(st < maxStep(s)){ steps[cur] = ++st; applySteps(s, st); }
    else show(cur+1, 1);
  }
  function prev(){
    var st = steps[cur] || 0;
    if(st > 0){ steps[cur] = --st; applySteps(slides[cur], st); }
    else show(cur-1, -1);
  }
  function toggleTheme(){
    document.body.classList.toggle('light');
    themeBtn.textContent = 'T · тема: ' + (document.body.classList.contains('light') ? 'светлая' : 'тёмная');
  }
  function toggleFS(){
    if(document.fullscreenElement){ document.exitFullscreen(); return; }
    var p = document.documentElement.requestFullscreen && document.documentElement.requestFullscreen();
    if(p && p.catch) p.catch(function(){
      hint.textContent = 'Фулскрин заблокирован во вьювере артефактов — открой deck.html локально (там F работает) или сверни панели браузера';
      hint.classList.remove('hide');
      setTimeout(function(){ hint.classList.add('hide'); }, 6000);
    });
  }

  // прыжок на слайд: поле № или набор цифр + Enter
  var jump = document.getElementById('jump');
  var buf = '', bufTimer = null;
  function goTo(v){
    var n = parseInt(v,10);
    if(n >= 1 && n <= slides.length) show(n-1, -1); // -1: фрагменты раскрыты — удобно проверять правки
  }
  jump.addEventListener('keydown', function(e){
    e.stopPropagation();
    if(e.key==='Enter'){ goTo(jump.value); jump.value=''; jump.blur(); }
    else if(e.key==='Escape'){ jump.value=''; jump.blur(); }
  });

  document.addEventListener('keydown', function(e){
    if(e.target === jump) return;
    if(/^[0-9]$/.test(e.key)){
      buf += e.key;
      count.textContent = '→ ' + buf;
      clearTimeout(bufTimer);
      bufTimer = setTimeout(function(){ buf=''; count.textContent = (cur+1)+' / '+slides.length; }, 3000);
      return;
    }
    if(e.key==='Enter' && buf){ goTo(buf); buf=''; return; }
    if(e.key==='Escape'){ buf=''; count.textContent = (cur+1)+' / '+slides.length; return; }
    if(e.key==='ArrowRight'||e.key==='PageDown'||e.key===' '||e.key==='Enter'){ e.preventDefault(); next(); }
    else if(e.key==='ArrowLeft'||e.key==='PageUp'||e.key==='Backspace'){ e.preventDefault(); prev(); }
    else if(e.key==='f'||e.key==='F'||e.key==='а'||e.key==='А'){ toggleFS(); }
    else if(e.key==='t'||e.key==='T'||e.key==='е'||e.key==='Е'){ toggleTheme(); }
    else if(e.key==='Home'){ show(0,1); } else if(e.key==='End'){ show(slides.length-1,-1); }
    if(e.key!=='f'&&e.key!=='F') hint.classList.add('hide');
  });
  document.querySelector('.nav-zone.next').addEventListener('click', next);
  document.querySelector('.nav-zone.prev').addEventListener('click', prev);
  themeBtn.addEventListener('click', toggleTheme);
  setTimeout(function(){ hint.classList.add('hide'); }, 7000);

  show(cur);

  // точечный глобус (canvas): фибоначчи-сфера, медленное вращение, глоу
  (function(){
    var cv = document.getElementById('globe');
    if(!cv) return;
    var ctx = cv.getContext('2d');
    var N = 700, pts = [];
    for(var i = 0; i < N; i++){
      var y = 1 - 2 * (i + .5) / N;
      var r = Math.sqrt(1 - y * y);
      var phi = i * 2.399963229728653;
      pts.push([Math.cos(phi) * r, y, Math.sin(phi) * r]);
    }
    var rot = 0, last = 0;
    var reduced = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    function draw(t){
      requestAnimationFrame(draw);
      if(!cv.parentElement.classList.contains('in')) return;
      if(t - last < 33) return;
      last = t;
      var w = cv.width, h = cv.height, R = Math.min(w, h) * .42, cx = w / 2, cy = h / 2;
      ctx.clearRect(0, 0, w, h);
      var g = ctx.createRadialGradient(cx, cy, R * .1, cx, cy, R * 1.3);
      g.addColorStop(0, 'rgba(124,58,237,.22)');
      g.addColorStop(1, 'rgba(124,58,237,0)');
      ctx.fillStyle = g;
      ctx.fillRect(0, 0, w, h);
      if(!reduced) rot += .0035;
      var s = Math.sin(rot), c = Math.cos(rot);
      for(var i = 0; i < N; i++){
        var p = pts[i];
        var x = p[0] * c + p[2] * s;
        var z = -p[0] * s + p[2] * c;
        var k = (z + 1) / 2; // 0 сзади, 1 спереди
        ctx.fillStyle = 'rgba(196,181,253,' + (.08 + .6 * k).toFixed(2) + ')';
        ctx.beginPath();
        ctx.arc(cx + x * R, cy + p[1] * R, 1 + 2.2 * k, 0, 6.2832);
        ctx.fill();
      }
      ctx.strokeStyle = 'rgba(167,139,250,.3)';
      ctx.lineWidth = 1.4;
      ctx.beginPath();
      ctx.arc(cx, cy, R, 0, 6.2832);
      ctx.stroke();
    }
    requestAnimationFrame(draw);
  })();
}
(window.DECK_READY || Promise.resolve()).then(__deckInit);