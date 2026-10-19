/* 极简 service worker：让 App 可"添加到主屏幕"并在网络抖动时保留外壳。
   注意：实时数据(/api/state)始终走网络，不缓存，避免看到过期状态。 */
const CACHE = "life-shell-v2";
const SHELL = ["/", "/manifest.json"];

self.addEventListener("install", (e) => {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)).catch(() => {}));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  // API 实时数据永远走网络
  if (url.pathname.startsWith("/api/")) return;
  // 其余：网络优先，失败回退缓存(离线时仍能打开外壳)
  e.respondWith(
    fetch(e.request)
      .then((resp) => {
        const copy = resp.clone();
        caches.open(CACHE).then((c) => c.put(e.request, copy)).catch(() => {});
        return resp;
      })
      .catch(() => caches.match(e.request))
  );
});
