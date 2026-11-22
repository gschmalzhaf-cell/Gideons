(function () {
  "use strict";

  /* Theme Toggle
     ====================================================================== */
  var STORAGE_KEY = "gideons-theme";
  var root = document.documentElement;
  var toggleBtn = document.getElementById("theme-toggle");

  function currentTheme() {
    var explicit = root.getAttribute("data-theme");
    if (explicit === "dark" || explicit === "light") return explicit;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    try {
      localStorage.setItem(STORAGE_KEY, theme);
    } catch (e) {}
    if (toggleBtn) {
      toggleBtn.setAttribute(
        "aria-label",
        theme === "dark" ? "Zum hellen Modus wechseln" : "Zum dunklen Modus wechseln"
      );
    }
  }

  if (toggleBtn) {
    applyTheme(currentTheme());
    toggleBtn.addEventListener("click", function () {
      applyTheme(currentTheme() === "dark" ? "light" : "dark");
    });
  }

  /* Project Filter & Live Search
     ====================================================================== */
  var cards = Array.prototype.slice.call(document.querySelectorAll("[data-project-card]"));
  var filterBtns = Array.prototype.slice.call(document.querySelectorAll("[data-filter]"));
  var searchInput = document.getElementById("project-search");
  var countEl = document.getElementById("project-count");
  var emptyEl = document.getElementById("empty-state");
  var resetBtn = document.getElementById("reset-filters");

  if (cards.length > 0) {
    var activeFilter = "all";

    function updateGrid() {
      var query = searchInput ? searchInput.value.trim().toLowerCase() : "";
      var visible = 0;

      cards.forEach(function (card) {
        var group = (card.getAttribute("data-platform-group") || "").toLowerCase();
        var haystack = (card.getAttribute("data-search") || "").toLowerCase();
        var matchesFilter = activeFilter === "all" || group === activeFilter;
        var matchesQuery = !query || haystack.indexOf(query) !== -1;
        var show = matchesFilter && matchesQuery;

        card.classList.toggle("is-hidden", !show);
        if (show) visible += 1;
      });

      if (countEl) {
        countEl.textContent =
          visible === cards.length
            ? visible + " Werkzeuge"
            : visible + " von " + cards.length + " Werkzeugen";
      }

      if (emptyEl) {
        emptyEl.hidden = visible > 0;
      }
    }

    filterBtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        activeFilter = btn.getAttribute("data-filter") || "all";
        filterBtns.forEach(function (other) {
          other.setAttribute("aria-pressed", other === btn ? "true" : "false");
        });
        updateGrid();
      });
    });

    if (searchInput) {
      searchInput.addEventListener("input", updateGrid);
      document.addEventListener("keydown", function (event) {
        if (
          event.key === "/" &&
          document.activeElement !== searchInput &&
          !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)
        ) {
          event.preventDefault();
          searchInput.focus();
        }
      });
    }

    if (resetBtn) {
      resetBtn.addEventListener("click", function () {
        activeFilter = "all";
        if (searchInput) searchInput.value = "";
        filterBtns.forEach(function (btn) {
          btn.setAttribute(
            "aria-pressed",
            btn.getAttribute("data-filter") === "all" ? "true" : "false"
          );
        });
        updateGrid();
      });
    }
  }

  /* Subtle Scroll Reveal
     ====================================================================== */
  var revealEls = Array.prototype.slice.call(document.querySelectorAll(".reveal"));
  if (revealEls.length > 0 && "IntersectionObserver" in window) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.08, rootMargin: "0px 0px -24px 0px" }
    );
    revealEls.forEach(function (el) {
      observer.observe(el);
    });
  } else {
    revealEls.forEach(function (el) {
      el.classList.add("is-visible");
    });
  }
})();
