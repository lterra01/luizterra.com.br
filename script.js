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

const ebookIntroduction = document.querySelector("#ebook-introduction");
const ebookSessionKey = ebookIntroduction?.dataset.ebookSessionKey || "luiz-terra-ebook-cx-v1-introduced";
const ebookAdId = ebookIntroduction?.dataset.ebookAdId || "cx_na_operacao_launch_v1";
let ebookIntroductionShown = false;
let ebookDecisionRecorded = false;

const ebookIdentity = (element) => {
  const product = element?.closest("[data-ebook-id]");
  if (!product?.dataset.ebookId) {
    const collection = element?.closest("[data-ebook-collection-id]");
    return collection ? { ebook_collection_id: collection.dataset.ebookCollectionId } : {};
  }
  return {
    ebook_id: product.dataset.ebookId,
    ebook_title: product.dataset.ebookTitle || product.dataset.ebookId,
    item_id: product.dataset.ebookId,
    item_name: product.dataset.ebookTitle || product.dataset.ebookId,
    ...(product.dataset.hotmartProductId ? { hotmart_product_id: product.dataset.hotmartProductId } : {}),
  };
};

const recordEbookEvent = (eventName, placement, parameters = {}, element = ebookIntroduction) => {
  if (typeof window.location.hostname === "string" && !["www.luizterra.com.br", "luizterra.com.br"].includes(window.location.hostname)) return;
  if (typeof window.gtag === "function") {
    window.gtag("event", eventName, {
      send_to: "G-68E95X4DZT",
      ...ebookIdentity(element),
      placement,
      ...parameters,
    });
  }
};

const recordEbookDecision = (choice, method, parameters = {}, element = ebookIntroduction) => {
  if (!ebookIntroductionShown || ebookDecisionRecorded) return;
  ebookDecisionRecorded = true;
  recordEbookEvent(choice === "offer" ? "ebook_offer_continue" : "ebook_site_continue", "introduction", {
    ebook_ad_id: ebookAdId,
    interaction_method: method,
    ...parameters,
  }, element);
};

document.querySelectorAll("[data-ebook-placement]").forEach((link) => {
  link.addEventListener("click", (event) => {
    if (link.dataset.ebookPlacement === "introduction" && ebookIntroduction?.open) {
      const sameTabClick = event.button === 0 && !event.ctrlKey && !event.metaKey &&
        !event.shiftKey && !event.altKey && link.target !== "_blank";
      if (sameTabClick && typeof window.gtag === "function") {
        event.preventDefault();
        let navigated = false;
        const continueToOffer = () => {
          if (navigated) return;
          navigated = true;
          window.location.assign(link.href);
        };
        // Keep navigation working even when Analytics is delayed or blocked.
        window.setTimeout(continueToOffer, 700);
        recordEbookDecision("offer", "offer_button", { event_callback: continueToOffer, event_timeout: 600 }, link);
      } else {
        recordEbookDecision("offer", "offer_button", {}, link);
      }
      ebookIntroduction.close();
    }
    recordEbookEvent("ebook_landing_click", link.dataset.ebookPlacement, {}, link);
  });
});

document.querySelectorAll("[data-ebook-checkout]").forEach((link) => {
  link.addEventListener("click", () => {
    recordEbookEvent("ebook_checkout_click", link.dataset.ebookCheckout, {}, link);
  });
});

const ebookLanding = document.querySelector("body.ebook-landing[data-ebook-id]");
if (ebookLanding) recordEbookEvent("ebook_landing_view", "landing", {}, ebookLanding);
const ebookCatalog = document.querySelector("body.ebook-catalog[data-ebook-collection-id]");
if (ebookCatalog) recordEbookEvent("ebook_catalog_view", "catalog", {}, ebookCatalog);

const recordMiniExpertEvent = (name, placement, element) => {
  if (!["www.luizterra.com.br", "luizterra.com.br"].includes(window.location.hostname)) return;
  const product = element?.closest("[data-mini-expert-id]");
  if (!product?.dataset.miniExpertId || typeof window.gtag !== "function") return;
  window.gtag("event", name, {
    send_to: "G-68E95X4DZT",
    product_id: product.dataset.miniExpertId,
    item_id: product.dataset.miniExpertId,
    item_name: product.dataset.miniExpertTitle,
    hotmart_product_id: product.dataset.hotmartProductId,
    item_category: "AI assistant",
    billing_period: "monthly",
    placement,
  });
};

document.querySelectorAll("[data-mini-expert-link]").forEach((link) => {
  link.addEventListener("click", () => recordMiniExpertEvent("mini_expert_landing_click", link.dataset.miniExpertLink, link));
});
document.querySelectorAll("[data-mini-expert-checkout]").forEach((link) => {
  link.addEventListener("click", () => recordMiniExpertEvent("mini_expert_checkout_click", link.dataset.miniExpertCheckout, link));
});
const miniExpertLanding = document.querySelector("body.mini-expert-landing");
if (miniExpertLanding) recordMiniExpertEvent("mini_expert_landing_view", "landing", miniExpertLanding);
const miniExpertProducts = document.querySelectorAll("[data-mini-expert-product]");
if (miniExpertProducts.length && "IntersectionObserver" in window) {
  const seen = new WeakSet();
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting || entry.intersectionRatio < 0.5 || seen.has(entry.target)) return;
      seen.add(entry.target);
      recordMiniExpertEvent("mini_expert_product_view", entry.target.dataset.productPlacement, entry.target);
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.5 });
  miniExpertProducts.forEach((product) => observer.observe(product));
}

if ("IntersectionObserver" in window) {
  const viewedProducts = new WeakSet();
  const productObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting || entry.intersectionRatio < 0.5 || viewedProducts.has(entry.target)) return;
      viewedProducts.add(entry.target);
      recordEbookEvent("ebook_product_view", ebookCatalog ? "catalog" : "related", {}, entry.target);
      productObserver.unobserve(entry.target);
    });
  }, { threshold: 0.5 });
  document.querySelectorAll("[data-ebook-product]").forEach((product) => productObserver.observe(product));
}

if (typeof HTMLDialogElement !== "undefined" && ebookIntroduction instanceof HTMLDialogElement) {
  const rememberIntroduction = () => {
    try {
      sessionStorage.setItem(ebookSessionKey, "1");
    } catch {
      // The announcement remains available when session storage is blocked.
    }
  };

  ebookIntroduction.querySelectorAll("[data-ebook-close]").forEach((button) => {
    button.addEventListener("click", () => {
      recordEbookDecision("site", button.dataset.ebookClose);
      ebookIntroduction.close();
    });
  });

  ebookIntroduction.addEventListener("cancel", () => recordEbookDecision("site", "escape"));
  ebookIntroduction.addEventListener("click", (event) => {
    const bounds = ebookIntroduction.getBoundingClientRect();
    if (event.target === ebookIntroduction &&
        (event.clientX < bounds.left || event.clientX > bounds.right ||
         event.clientY < bounds.top || event.clientY > bounds.bottom)) {
      recordEbookDecision("site", "backdrop");
      ebookIntroduction.close();
    }
  });
  ebookIntroduction.addEventListener("close", () => {
    recordEbookDecision("site", "other_close");
    rememberIntroduction();
  });

  let alreadyIntroduced = false;
  try {
    alreadyIntroduced = sessionStorage.getItem(ebookSessionKey) === "1";
  } catch {
    alreadyIntroduced = true;
  }

  if (!alreadyIntroduced && typeof ebookIntroduction.showModal === "function") {
    window.setTimeout(() => {
      if (document.visibilityState === "visible" && !document.querySelector("dialog[open]") &&
          !document.body.classList.contains("nav-open") && !isEditableTarget(document.activeElement)) {
        ebookIntroduction.showModal();
        ebookIntroductionShown = true;
        rememberIntroduction();
        recordEbookEvent("ebook_introduction_view", "first_session_entry", { ebook_ad_id: ebookAdId });
      }
    }, 1800);
  }
}
