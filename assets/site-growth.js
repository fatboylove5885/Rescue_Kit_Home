/* Consent-controlled measurement for the site's existing GA4 property.
   No analytics script or queued event is created before opt-in. */
(function () {
  'use strict';
  const measurementId = 'G-QM26ZNDC24';
  const storageKey = 'wfe_analytics_choice_v1';
  let choice = null;
  let started = false;
  try { choice = localStorage.getItem(storageKey); } catch (_) { /* Session-only choice if storage is unavailable. */ }
  if (choice !== 'granted' && choice !== 'denied') choice = null;
  if (navigator.globalPrivacyControl === true) choice = 'denied';

  function cleanLocation() {
    const url = new URL(location.origin + location.pathname);
    const source = new URLSearchParams(location.search);
    ['utm_source','utm_medium','utm_campaign','utm_content'].forEach(key => {
      const value = source.get(key);
      if (value && /^[a-z0-9_-]{1,80}$/i.test(value)) url.searchParams.set(key, value);
    });
    return url.href;
  }
  function start() {
    if (choice !== 'granted' || started) return;
    started = true;
    window['ga-disable-' + measurementId] = false;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('consent', 'default', {analytics_storage:'granted',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'});
    window.gtag('js', new Date());
    let referrer = '';
    try { if (document.referrer) { const ref = new URL(document.referrer); referrer = ref.origin + ref.pathname; } } catch (_) {}
    window.gtag('config', measurementId, {send_page_view:true, page_location:cleanLocation(), page_referrer:referrer, allow_google_signals:false, allow_ad_personalization_signals:false});
    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + measurementId;
    document.head.appendChild(script);
  }
  function clearCookies() {
    const domains = [location.hostname, '.' + location.hostname];
    document.cookie.split(';').forEach(part => {
      const name = part.split('=')[0].trim();
      if (!name.startsWith('_ga')) return;
      document.cookie = name + '=; Max-Age=0; path=/';
      domains.forEach(domain => { document.cookie = name + '=; Max-Age=0; path=/; domain=' + domain; });
    });
  }
  const banner = document.createElement('aside');
  banner.className = 'wfe-consent';
  banner.setAttribute('aria-label', 'Optional analytics');
  banner.innerHTML = '<p>May we use optional analytics to learn which dinner guides help? You can use everything with analytics off. <a href="/privacy.html">Privacy information</a></p><div><button type="button" data-choice="denied">No thanks</button><button type="button" data-choice="granted">Allow analytics</button></div>';
  banner.hidden = choice !== null;
  document.body.prepend(banner);
  banner.addEventListener('click', event => {
    const button = event.target.closest('button[data-choice]');
    if (!button) return;
    choice = navigator.globalPrivacyControl === true ? 'denied' : button.dataset.choice;
    try { localStorage.setItem(storageKey, choice); } catch (_) {}
    banner.hidden = true;
    if (choice === 'granted') start();
    else {
      window['ga-disable-' + measurementId] = true;
      if (started && window.gtag) window.gtag('consent', 'update', {analytics_storage:'denied'});
      clearCookies();
      if (started) location.reload();
    }
  });
  const settings = document.createElement('button');
  settings.type = 'button';
  settings.className = 'wfe-consent-settings';
  settings.textContent = 'Analytics choices';
  settings.addEventListener('click', () => { banner.hidden = false; banner.querySelector('button').focus(); banner.scrollIntoView({block:'start'}); });
  document.body.appendChild(settings);
  if (choice !== 'granted') { window['ga-disable-' + measurementId] = true; clearCookies(); }
  start();

  window.wfeTrack = function (name, data) {
    if (choice !== 'granted' || !started || typeof window.gtag !== 'function') return;
    window.gtag('event', name, Object.assign({page_location:cleanLocation()}, data || {}));
  };
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href]');
    if (!link) return;
    let url;
    try { url = new URL(link.href, location.href); } catch (_) { return; }
    if (url.hostname === 'whop.com') window.wfeTrack('checkout_click', {destination_host:'whop.com', product:url.pathname.includes('the-5-47-p-m-rescue-kit') ? 'rescue_kit' : 'other_product'});
    else if (url.origin === location.origin && url.pathname === '/5-47-rescue-kit.html') window.wfeTrack('rescue_kit_view_click', {link_location: link.closest('.wfe-discover') ? 'discovery' : 'content'});
    else if (url.hostname === 'www.pinterest.com') window.wfeTrack('share', {method:'pinterest',content_type:'guide'});
    else if (link.closest('.dinner-card')) window.wfeTrack('dinner_recipe_click', {recipe_id:link.closest('.dinner-card').id});
    else if (url.origin === location.origin && (url.pathname.startsWith('/pdfs/') || url.pathname === '/freebies.html')) window.wfeTrack('freebie_click', {resource_path:url.pathname});
  });
  // Open recipe details when arriving from a direct recipe link.
  function revealRecipe() {
    let target;
    try { target = document.getElementById(decodeURIComponent(location.hash.slice(1))); } catch (_) { return; }
    if (target && target.tagName === 'DETAILS') target.open = true;
  }
  revealRecipe();
  window.addEventListener('hashchange', revealRecipe);
})();
