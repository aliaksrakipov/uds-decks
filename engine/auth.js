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

  // письмо со ссылкой на смену пароля. redirectTo — куда попадёт партнёр по ссылке
  // из письма (должен быть в списке Redirect URLs в Supabase Dashboard → Auth →
  // URL Configuration, иначе Supabase откажется редиректить).
  function recover(email, redirectTo){
    var url = cfg.supabaseUrl + '/auth/v1/recover' +
      (redirectTo ? '?redirect_to=' + encodeURIComponent(redirectTo) : '');
    return fetch(url, {
      method: 'POST',
      headers: { apikey: cfg.supabaseAnonKey, 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email })
    }).then(function(r){
      if (r.ok) return true;
      return r.json().then(function(j){ throw new Error(j.error_description || j.msg || 'Ошибка'); });
    });
  }

  // ставит новый пароль по токену из ссылки восстановления и сразу сохраняет
  // сессию (после смены пароля партнёр остаётся залогинен)
  function updatePasswordWithToken(accessToken, newPassword){
    return fetch(cfg.supabaseUrl + '/auth/v1/user', {
      method: 'PUT',
      headers: {
        apikey: cfg.supabaseAnonKey,
        Authorization: 'Bearer ' + accessToken,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ password: newPassword })
    }).then(function(r){
      return r.json().then(function(j){
        if (!r.ok) throw new Error(j.error_description || j.msg || 'Ошибка');
        return j;
      });
    });
  }

  // сохранить сессию напрямую (используется после смены пароля по ссылке из письма,
  // где токен приходит не через signIn/signUp, а прямо в URL)
  function adoptSession(accessToken, refreshToken, user){
    save({ access_token: accessToken, refresh_token: refreshToken, user: user });
  }

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
    recover: recover,
    updatePasswordWithToken: updatePasswordWithToken,
    adoptSession: adoptSession,
    getSession: get,
    isLoggedIn: function(){ return !!get(); },
    authFetch: authFetch
  };
})();
