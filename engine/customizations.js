// ===== Применение личных правок партнёра к деке =====
// Пока умеет только порядок слайдов (order), поля и добавленные слайды — позже.
// Дека открыта как decks/<тема>.html?p=<id> — читаем deck_customizations по
// этому id ПУБЛИЧНО, без логина (иначе не работает «отправил ссылку клиенту»).
// Подключать ПОСЛЕ partner.js (нужен window.DECK_READY), ДО deck.js (он же
// на DECK_READY и стартует, и должен увидеть уже переставленные слайды).
(function(){
  var cfg = window.SITE_CONFIG || {};
  var id = new URLSearchParams(location.search).get('p');
  var deckName = location.pathname.split('/').pop().replace(/\.html$/, '');

  function applyOrder(){
    if (!id || !cfg.supabaseUrl || !cfg.supabaseAnonKey) return;
    return fetch(
      cfg.supabaseUrl + '/rest/v1/deck_customizations?select=data&partner_id=eq.' +
      encodeURIComponent(id) + '&deck=eq.' + encodeURIComponent(deckName),
      { headers: { apikey: cfg.supabaseAnonKey, Authorization: 'Bearer ' + cfg.supabaseAnonKey } }
    ).then(function(r){ return r.json(); })
      .then(function(rows){
        var order = rows && rows[0] && rows[0].data && rows[0].data.order;
        if (!Array.isArray(order) || !order.length) return;
        var deck = document.getElementById('deck');
        if (!deck) return;
        var bySlug = {};
        Array.prototype.forEach.call(deck.querySelectorAll('.slide[data-slide-id]'), function(el){
          bySlug[el.getAttribute('data-slide-id')] = el;
        });
        // appendChild переносит существующий узел в конец — прогоняя id по порядку,
        // слайды выстраиваются в нужную последовательность. Титул и визитку мы
        // никогда не трогаем (их нет в order), поэтому они остаются первыми как есть.
        // Слайд, которого партнёр никогда не переставлял (или который появился в базовой
        // деке позже его последнего сохранения), просто остаётся на исходном месте —
        // может оказаться перед переставленным блоком, а не в идеальной позиции; для
        // редкого случая устройства базовой деки после сохранения правок это ок.
        order.forEach(function(sid){
          var el = bySlug[sid];
          if (el) deck.appendChild(el);
        });
      })
      .catch(function(){ /* база недоступна или правок нет — дека остаётся как есть */ });
  }

  var prev = window.DECK_READY || Promise.resolve();
  window.DECK_READY = prev.then(applyOrder);
})();
