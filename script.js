const revealElements = document.querySelectorAll(".section-reveal");
const ticker = document.querySelector(".ticker");
const tickerTrack = document.querySelector(".ticker-track");
const navToggle = document.querySelector(".nav-toggle");
const navLinks = document.querySelector(".nav-links");
const emailLink = document.querySelector("#email-link");
const emailText = document.querySelector("#email-text");
const languageButtons = document.querySelectorAll(".language-switcher button");
const categoryFilters = document.querySelectorAll(".category-filters button");
const copyLinkButtons = document.querySelectorAll(".copy-link");
const protectedShortcutKeys = ["c", "s", "p", "u"];
const protectedInspectorKeys = ["i", "j", "c"];

const insightArticles = Array.from(document.querySelectorAll("[data-article-slug]")).map((item) => ({
  slug: item.dataset.articleSlug,
  category: item.dataset.category,
  title: item.querySelector("h3")?.textContent?.trim() || "",
}));

if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.18 }
  );

  revealElements.forEach((element) => observer.observe(element));
} else {
  revealElements.forEach((element) => element.classList.add("is-visible"));
}

if (ticker && tickerTrack) {
  ticker.addEventListener("mouseenter", () => tickerTrack.classList.add("is-paused"));
  ticker.addEventListener("mouseleave", () => tickerTrack.classList.remove("is-paused"));
  ticker.addEventListener("focusin", () => tickerTrack.classList.add("is-paused"));
  ticker.addEventListener("focusout", () => tickerTrack.classList.remove("is-paused"));
}

if (navToggle && navLinks) {
  navToggle.addEventListener("click", () => {
    const isOpen = navLinks.classList.toggle("is-open");
    document.body.classList.toggle("nav-open", isOpen);
    navToggle.setAttribute("aria-expanded", String(isOpen));
  });

  navLinks.addEventListener("click", (event) => {
    if (event.target instanceof HTMLAnchorElement) {
      navLinks.classList.remove("is-open");
      document.body.classList.remove("nav-open");
      navToggle.setAttribute("aria-expanded", "false");
    }
  });
}

if (emailLink && emailText) {
  const address = `${emailLink.dataset.user}@${emailLink.dataset.domain}`;
  emailLink.href = `mailto:${address}`;
  emailText.textContent = address;
}

const isEditableTarget = (target) =>
  target instanceof HTMLElement &&
  Boolean(target.closest("input, textarea, select, [contenteditable='true']"));

document.addEventListener("contextmenu", (event) => {
  event.preventDefault();
});

document.addEventListener("copy", (event) => {
  if (!isEditableTarget(event.target)) {
    event.preventDefault();
  }
});

document.addEventListener("cut", (event) => {
  if (!isEditableTarget(event.target)) {
    event.preventDefault();
  }
});

document.addEventListener("dragstart", (event) => {
  if (event.target instanceof HTMLElement && event.target.closest("img")) {
    event.preventDefault();
  }
});

document.addEventListener("keydown", (event) => {
  const key = event.key.toLowerCase();
  const hasModifier = event.ctrlKey || event.metaKey;
  const blocksDocumentAction = hasModifier && protectedShortcutKeys.includes(key);
  const blocksInspectorAction =
    event.key === "F12" || (hasModifier && event.shiftKey && protectedInspectorKeys.includes(key));

  if (!isEditableTarget(event.target) && (blocksDocumentAction || blocksInspectorAction)) {
    event.preventDefault();
  }
});

languageButtons.forEach((button) => {
  button.addEventListener("click", () => {
    if (button.disabled) return;

    languageButtons.forEach((item) => {
      item.classList.toggle("is-active", item === button);
      item.setAttribute("aria-pressed", String(item === button));
    });
  });
});

categoryFilters.forEach((button) => {
  button.addEventListener("click", () => {
    const selected = button.dataset.filter;
    categoryFilters.forEach((item) => item.setAttribute("aria-pressed", String(item === button)));
    document.querySelectorAll(".insight-grid [data-category]").forEach((article) => {
      article.hidden = selected !== "all" && article.dataset.category !== selected;
    });
  });
});

copyLinkButtons.forEach((button) => {
  button.addEventListener("click", async () => {
    const original = button.textContent;
    try {
      await navigator.clipboard.writeText(button.dataset.copyUrl || window.location.href);
      button.textContent = button.dataset.copyLabel || original;
      window.setTimeout(() => {
        button.textContent = original;
      }, 1800);
    } catch {
      button.textContent = button.dataset.copyUrl || window.location.href;
    }
  });
});

window.luizTerraInsights = insightArticles;
