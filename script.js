const revealElements = document.querySelectorAll(".section-reveal");
const ticker = document.querySelector(".ticker");
const tickerTrack = document.querySelector(".ticker-track");
const navToggle = document.querySelector(".nav-toggle");
const navLinks = document.querySelector(".nav-links");
const emailLink = document.querySelector("#email-link");
const emailText = document.querySelector("#email-text");

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
