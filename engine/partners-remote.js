// ===== Догрузка партнёров из Supabase =====
// Мержит записи из базы в window.PARTNERS (статический реестр приоритетнее:
// запись из базы с id, который уже есть в partners.js, игнорируется — так
// базовых партнёров нельзя перезаписать через форму).
// Экспортирует window.PARTNERS_READY — promise, после которого список финален.
// Без ключей в config.js или при недоступной базе резолвится сразу/по таймауту —
// сайт продолжает работать на статике.
(function(){
  var cfg = window.SITE_CONFIG || {};
  if (!cfg.supabaseUrl || !cfg.supabaseAnonKey) {
    window.PARTNERS_READY = Promise.resolve();
    return;
  }
  var load = fetch(cfg.supabaseUrl + "/rest/v1/partners_ext?select=id,name,role,facts,tg,photo_b64&order=created_at",
    { headers: { apikey: cfg.supabaseAnonKey, Authorization: "Bearer " + cfg.supabaseAnonKey } })
    .then(function(r){ return r.json(); })
    .then(function(rows){
      if (!Array.isArray(rows)) return;
      var have = {};
      (window.PARTNERS || []).forEach(function(p){ have[p.id] = 1; });
      rows.forEach(function(r){
        if (have[r.id]) return;
        window.PARTNERS.push({
          id: r.id, name: r.name, role: r.role,
          facts: r.facts || [], tg: r.tg || null,
          photo: r.photo_b64 || null
        });
      });
    })
    .catch(function(){ /* база недоступна — работаем на статике */ });
  // страховка: не держать сайт дольше 2.5 с
  window.PARTNERS_READY = Promise.race([load, new Promise(function(res){ setTimeout(res, 2500); })]);
})();
