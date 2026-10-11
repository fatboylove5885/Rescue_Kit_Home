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