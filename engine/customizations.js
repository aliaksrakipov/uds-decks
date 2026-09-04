// ===== Применение личных правок партнёра к деке =====
// Умеет: порядок слайдов (order) и какие слайды скрыть (hidden). Поля и
// добавленные слайды-шаблоны — позже.
// Дека открыта как decks/<тема>.html?p=<id> — читаем deck_customizations по
// этому id ПУБЛИЧНО, без логина (иначе не работает «отправил ссылку клиенту»).
// Подключать ПОСЛЕ partner.js (нужен window.DECK_READY), ДО deck.js (он же
// на DECK_READY и стартует, и должен увидеть уже применённые правки).
(function(){
  var cfg = window.SITE_CONFIG || {};
  var id = new URLSearchParams(location.search).get('p');
  var deckName = location.pathname.split('/').pop().replace(/\.html$/, '');

  function applyCustomizations(){
    if (!id || !cfg.supabaseUrl || !cfg.supabaseAnonKey) return;
    return fetch(
      cfg.supabaseUrl + '/rest/v1/deck_customizations?select=data&partner_id=eq.' +
      encodeURIComponent(id) + '&deck=eq.' + encodeURIComponent(deckName),
      { headers: { apikey: cfg.supabaseAnonKey, Authorization: 'Bearer ' + cfg.supabaseAnonKey } }
    ).then(function(r){ return r.json(); })
      .then(function(rows){
        var data = rows && rows[0] && rows[0].data;
        if (!data) return;
        var deck = document.getElementById('deck');
        if (!deck) return;

        // скрытые слайды удаляем из DOM целиком (не CSS-прячем) — тогда
        // deck.js, который считает .slide уже ПОСЛЕ нас, сам всё посчитает
        // правильно, без специального кода на «пропускать скрытые»
        var hidden = Array.isArray(data.hidden) ? data.hidden : [];
        hidden.forEach(function(sid){
          var el = deck.querySelector('.slide[data-slide-id="' + sid + '"]');
          if (el) el.remove();
        });

        // appendChild переносит существующий узел в конец — прогоняя id по порядку,
        // слайды выстраиваются в нужную последовательность. Титул и визитку мы
        // никогда не трогаем (их нет в order), поэтому они остаются первыми как есть.
        // Слайд, которого партнёр никогда не переставлял (или который появился в базовой
        // деке позже его последнего сохранения), просто остаётся на исходном месте —
        // может оказаться перед переставленным блоком, а не в идеальной позиции; для
        // редкого случая устройства базовой деки после сохранения правок это ок.
        var order = Array.isArray(data.order) ? data.order : [];
        if (order.length) {
          var bySlug = {};
          Array.prototype.forEach.call(deck.querySelectorAll('.slide[data-slide-id]'), function(el){
            bySlug[el.getAttribute('data-slide-id')] = el;
          });
          order.forEach(function(sid){
            var el = bySlug[sid];
            if (el) deck.appendChild(el);
          });
        }
      })
      .catch(function(){ /* база недоступна, правок нет или в них опечатка — дека остаётся как есть */ });
  }

  var prev = window.DECK_READY || Promise.resolve();
  window.DECK_READY = prev.then(applyCustomizations);
})();
