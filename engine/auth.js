// ===== Сессия Supabase Auth (без SDK, чистый fetch — как и весь остальной сайт) =====
// Хранит access_token/refresh_token в localStorage браузера партнёра.
// Токен живёт ~1 час (дефолт Supabase) — по истечении просто просим войти заново;
// обновление по refresh_token можно добавить позже, если это станет мешать.
// Подключать после config.js, до любой страницы, которой нужен логин (login.html,
// в будущем — dashboard/edit).
window.UdsAuth = (function(){
  var KEY = 'uds_auth_session';
  var cfg = window.SITE_CONFIG || {};

  function save(session){
    localStorage.setItem(KEY, JSON.stringify({
      access_token: session.access_token,
      refresh_token: session.refresh_token,
      user: session.user,
      saved_at: Date.now()
    }));
  }

  function get(){
    try { return JSON.parse(localStorage.getItem(KEY) || 'null'); }
    catch (e) { return null; }
  }

  function clear(){ localStorage.removeItem(KEY); }

  function parseAuthResponse(r){
    return r.json().then(function(j){
      if (!r.ok) throw new Error(j.error_description || j.msg || j.error || 'Ошибка авторизации');
      if (j.access_token) save(j);
      return j;
    });
  }

  function signUp(email, password){
    return fetch(cfg.supabaseUrl + '/auth/v1/signup', {
      method: 'POST',
      headers: { apikey: cfg.supabaseAnonKey, 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email, password: password })
    }).then(parseAuthResponse);
  }

  function signIn(email, password){
    return fetch(cfg.supabaseUrl + '/auth/v1/token?grant_type=password', {
      method: 'POST',
      headers: { apikey: cfg.supabaseAnonKey, 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email, password: password })
    }).then(parseAuthResponse);
  }

  function signOut(){ clear(); }

  // fetch от имени залогиненного партнёра (Authorization = его access_token,
  // а не общий anon key) — нужен для всего, что проверяет auth.uid() на сервере:
  // link_partner_account, запись в deck_customizations.
  // Без сессии тихо откатывается на anon key — подходит для публичного чтения.
  function authFetch(path, opts){
    opts = opts || {};
    var session = get();
    var headers = { apikey: cfg.supabaseAnonKey, 'Content-Type': 'application/json' };
    if (opts.headers) { for (var k in opts.headers) headers[k] = opts.headers[k]; }
    headers.Authorization = 'Bearer ' + (session ? session.access_token : cfg.supabaseAnonKey);
    return fetch(cfg.supabaseUrl + path, { method: opts.method, headers: headers, body: opts.body });
  }

  return {
    signUp: signUp,
    signIn: signIn,
    signOut: signOut,
    getSession: get,
    isLoggedIn: function(){ return !!get(); },
    authFetch: authFetch
  };
})();
