/* Shared, defensive navigation behavior for What's for Eats. */
(function () {
  if (window.__whatsForEatsNavInstalled) return;
  window.__whatsForEatsNavInstalled = true;

  document.addEventListener("click", function (event) {
    var target = event.target;
    if (!target || !target.closest) return;

    var menuButton = target.closest(".site-nav .menu-toggle");
    if (menuButton) {
      event.preventDefault();
      event.stopImmediatePropagation();
      var menuId = menuButton.getAttribute("aria-controls") || "primary-menu";
      var menu = document.getElementById(menuId);
      if (!menu) return;
      var isOpen = menuButton.getAttribute("aria-expanded") === "true";
      menuButton.setAttribute("aria-expanded", String(!isOpen));
      menu.classList.toggle("open", !isOpen);
      menuButton.textContent = isOpen ? "☰ Menu" : "✕ Close";
      return;
    }

    var summary = target.closest(".site-nav .nav-dropdown > summary");
    if (summary) {
      event.preventDefault();
      event.stopImmediatePropagation();
      var dropdown = summary.parentElement;
      var shouldOpen = !dropdown.open;
      document.querySelectorAll(".site-nav .nav-dropdown[open]").forEach(function (item) {
        item.open = false;
      });
      dropdown.open = shouldOpen;
      return;
    }

    if (!target.closest(".site-nav .nav-dropdown")) {
      document.querySelectorAll(".site-nav .nav-dropdown[open]").forEach(function (item) {
        item.open = false;
      });
    }
  }, true);

  document.addEventListener("keydown", function (event) {
    if (event.key !== "Escape") return;
    document.querySelectorAll(".site-nav .nav-dropdown[open]").forEach(function (item) {
      item.open = false;
    });
    document.querySelectorAll(".site-nav .menu-toggle[aria-expanded='true']").forEach(function (button) {
      button.setAttribute("aria-expanded", "false");
      var menu = document.getElementById(button.getAttribute("aria-controls") || "primary-menu");
      if (menu) menu.classList.remove("open");
      button.textContent = "☰ Menu";
      button.focus();
    });
  });
})();

/* Site-wide iOS/Safari scrolling integrity: prevent background scroll bleed
   for true dialogs, without locking normal articles or page navigation. */
(function () {
  'use strict';
  if (window.__wfeScrollIntegrityInstalled) return;
  window.__wfeScrollIntegrityInstalled = true;

  var sheet = document.createElement('style');
  sheet.id = 'wfe-scroll-integrity';
  sheet.textContent =
    'dialog[open], [role="dialog"][aria-modal="true"], [data-wfe-scroll-lock="true"] {' +
      'overscroll-behavior-y:contain; -webkit-overflow-scrolling:touch; }' +
    '@supports (-webkit-touch-callout: none) {' +
      '.cozy-recipe {content-visibility:visible !important;contain-intrinsic-size:none !important;}' +
    '}';
  document.head.appendChild(sheet);

  var locked = false;
  var savedY = 0;
  var original = null;
  var scheduled = false;
  var selector = 'dialog[open], [role="dialog"][aria-modal="true"], [data-wfe-scroll-lock="true"]';

  function hasVisibleDialog() {
    var nodes = document.querySelectorAll(selector);
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      if (el.getAttribute('aria-hidden') === 'true') continue;
      if (!el.getClientRects().length) continue;
      var css = window.getComputedStyle(el);
      if (css.visibility !== 'hidden' && css.display !== 'none') return true;
    }
    return false;
  }
  function sync() {
    scheduled = false;
    if (!document.body) return;
    var body = document.body;
    if (hasVisibleDialog() && !locked) {
      savedY = window.scrollY || window.pageYOffset || 0;
      original = {
        position: body.style.position,
        top: body.style.top,
        left: body.style.left,
        right: body.style.right,
        width: body.style.width,
        overflow: body.style.overflow
      };
      locked = true;
      body.style.position = 'fixed';
      body.style.top = '-' + savedY + 'px';
      body.style.left = '0';
      body.style.right = '0';
      body.style.width = '100%';
      body.style.overflow = 'hidden';
    } else if (!hasVisibleDialog() && locked) {
      body.style.position = original.position;
      body.style.top = original.top;
      body.style.left = original.left;
      body.style.right = original.right;
      body.style.width = original.width;
      body.style.overflow = original.overflow;
      locked = false;
      original = null;
      window.scrollTo(0, savedY);
    }
  }
  function queueSync() {
    if (scheduled) return;
    scheduled = true;
    window.requestAnimationFrame(sync);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', queueSync, { once: true });
  } else {
    queueSync();
  }
  if (typeof MutationObserver !== 'undefined') {
    var watcher = new MutationObserver(queueSync);
    watcher.observe(document.documentElement, {
      subtree: true, childList: true, attributes: true,
      attributeFilter: ['open', 'aria-modal', 'aria-hidden', 'hidden', 'class', 'style', 'data-wfe-scroll-lock']
    });
  }
  document.addEventListener('close', queueSync, true);
  document.addEventListener('toggle', queueSync, true);
  window.addEventListener('pageshow', queueSync);
})();
