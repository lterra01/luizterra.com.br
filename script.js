const revealElements = document.querySelectorAll(".section-reveal");
const ticker = document.querySelector(".ticker");
const tickerTrack = document.querySelector(".ticker-track");
const navToggle = document.querySelector(".nav-toggle");
const navLinks = document.querySelector(".nav-links");
const emailLink = document.querySelector("#email-link");
const emailText = document.querySelector("#email-text");
const languageButtons = document.querySelectorAll(".language-switcher button");
const protectedShortcutKeys = ["c", "s", "p", "u"];
const protectedInspectorKeys = ["i", "j", "c"];

const insightArticles = [
  {
    slug: "ai-powered-amd-outbound-operations",
    category: "AI & Contact Center",
    title: "Why AI-powered AMD is becoming strategic for outbound operations",
  },
  {
    slug: "future-of-sbcs-cloud-contact-centers",
    category: "Telecom Infrastructure",
    title: "The future of SBCs in cloud contact centers",
  },
  {
    slug: "bpos-evaluate-telecom-infrastructure-partners",
    category: "BPO Technology",
    title: "How BPOs should evaluate telecom infrastructure partners",
  },
  {
    slug: "latam-bridge-us-cx-global-delivery",
    category: "Market Entry",
    title: "LATAM as a bridge between US CX demand and global delivery",
  },
  {
    slug: "european-ccaas-local-telecom-partners",
    category: "CCaaS Expansion",
    title: "What European CCaaS vendors need from local telecom partners",
  },
  {
    slug: "ai-contact-centers-roi",
    category: "AI ROI",
    title: "AI in Contact Centers: where the hype ends and ROI starts",
  },
];

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

window.luizTerraInsights = insightArticles;
