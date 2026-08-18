// ===== Персонализация деки под партнёра =====
// Дека открывается как decks/<тема>.html?p=<id партнёра>.
// Что делает: 1) в секцию [data-partner-slide] вставляет слайд-визитку;
// 2) элементам [data-partner-name] ставит имя; 3) [data-partner-contact] — телеграм;
// 4) без ?p= визитка убирается, имя остаётся дефолтным из разметки.
// Партнёр может прийти из базы (см. partners-remote.js), поэтому применение —
// после window.PARTNERS_READY. Экспортирует window.DECK_READY: движок деки
// (deck.js) стартует после него, чтобы правильно посчитать слайды.
// Подключать ПОСЛЕ config.js, partners.js, partners-remote.js и ДО deck.js.
(function(){
  var id = new URLSearchParams(location.search).get('p');

  function photoSrc(p){
    // из базы фото приходит data:-URI, из статики — путь от корня сайта
    return /^(data:|https?:)/.test(p) ? p : '../' + p;
  }

  function initials(name){
    return name.split(' ').map(function(w){ return (w[0] || '').toUpperCase(); }).slice(0, 2).join('');
  }

  function apply(){
    var P = (window.PARTNERS || []).filter(function(x){ return x.id === id; })[0] || null;
    window.PARTNER = P;

    var slot = document.querySelector('[data-partner-slide]');
    if (slot) {
      if (P) {
        // регалии появляются поочерёдно (пошаговые фрагменты движка).
        // ВАЖНО: без класса .a — правило .slide.cur .a специфичнее .frag и ломает скрытие шагов
        var facts = (P.facts || []).map(function(f, i){
          return '<li class="frag" data-step="' + (i + 1) + '">' + f + '</li>';
        }).join('');
        var photo = P.photo
          ? '<img src="' + photoSrc(P.photo) + '" alt="' + P.name + '">'
          : '<div style="width:100%; height:100%; border-radius:.9cqw; background:var(--acc-dim); display:grid; place-items:center; font-family:\'Unbounded\',sans-serif; font-weight:800; font-size:6cqw; color:var(--mut2)">' + initials(P.name) + '</div>';
        slot.innerHTML =
          '<div class="logo">uds<span>Partner</span></div>' +
          '<div class="sp-content">' +
            '<div class="sp-photo glass a" style="--i:0">' + photo + '</div>' +
            '<div>' +
              '<div class="sp-name chrome a" style="--i:1">' + P.name + '</div>' +
              '<div class="sp-role a" style="--i:2">' + P.role + '</div>' +
              '<ul class="sp-facts">' + facts + '</ul>' +
            '</div>' +
          '</div>';
      } else {
        slot.parentNode.removeChild(slot);
      }
    }

    document.querySelectorAll('[data-partner-name]').forEach(function(el){
      if (P) el.textContent = P.name;
    });

    document.querySelectorAll('[data-partner-contact]').forEach(function(el){
      if (P && P.tg) {
        el.innerHTML = 'Telegram: <span>@' + P.tg + '</span>';
      } else if (P || id) {
        el.style.display = 'none';
      } else if (!el.textContent.trim()) {
        el.style.display = 'none';
      }
    });
  }

  window.DECK_READY = (window.PARTNERS_READY || Promise.resolve()).then(apply);
})();
