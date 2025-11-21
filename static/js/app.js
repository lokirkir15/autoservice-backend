(function () {
  const STORAGE_KEY = "theme"; // "light" | "dark"

  const getPreferredTheme = () => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) return stored;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  };

  const applyTheme = (theme) => {
    // ustaw atrybut na <html> (Bootstrap 5.3 bazuje na data-bs-theme)
    document.documentElement.setAttribute("data-bs-theme", theme);

    // zaktualizuj wygląd przycisku
    const btn = document.getElementById("themeToggle");
    if (btn) {
      const icon = btn.querySelector(".theme-icon");
      if (icon) icon.textContent = theme === "dark" ? "☀️" : "🌙";
      const title = theme === "dark" ? "Przełącz na jasny" : "Przełącz na ciemny";
      btn.setAttribute("data-bs-title", title);

      // uaktualnij ewentualną instancję tooltips (jeśli istnieje)
      if (window.bootstrap) {
        const instance = bootstrap.Tooltip.getInstance(btn) || new bootstrap.Tooltip(btn);
        // w BS5.3 można podmienić zawartość tooltips:
        if (instance.setContent) {
          instance.setContent({ ".tooltip-inner": title });
        } else {
          instance.dispose();
          new bootstrap.Tooltip(btn);
        }
      }
    }
  };

  document.addEventListener("DOMContentLoaded", () => {
    // 1) Zastosuj preferowany motyw
    applyTheme(getPreferredTheme());

    // 2) Obsłuż kliknięcie na przycisku
    const btn = document.getElementById("themeToggle");
    if (btn) {
      btn.addEventListener("click", () => {
        const current = document.documentElement.getAttribute("data-bs-theme") || "light";
        const next = current === "dark" ? "light" : "dark";
        localStorage.setItem(STORAGE_KEY, next);
        applyTheme(next);
      });
    }

    // 3) Reaguj na zmianę systemowego motywu, jeśli użytkownik nie wybrał sam
    const mq = window.matchMedia("(prefers-color-scheme: dark)");
    mq.addEventListener("change", (e) => {
      if (!localStorage.getItem(STORAGE_KEY)) {
        applyTheme(e.matches ? "dark" : "light");
      }
    });
  });
})();
