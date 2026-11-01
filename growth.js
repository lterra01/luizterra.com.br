(function () {
  "use strict";

  const selectActions = (checks, ready) => {
    const pending = checks.filter((_, index) => !ready.includes(index));
    return { maintenance: pending.length === 0, actions: (pending.length ? pending : checks).slice(0, 3) };
  };
  if (typeof module === "object" && module.exports) module.exports = { selectActions };
  if (typeof document === "undefined") return;

  const record = (name, placement, parameters = {}) => {
    if (!["www.luizterra.com.br", "luizterra.com.br"].includes(window.location.hostname)) return;
    if (typeof window.gtag !== "function") return;
    window.gtag("event", name, { send_to: "G-68E95X4DZT", placement, ...parameters });
  };
  document.querySelectorAll("[data-cx-resource-link]").forEach((link) => {
    link.addEventListener("click", () => record("cx_resource_click", link.dataset.cxResourceLink));
  });

  const resource = document.querySelector("[data-cx-resource]");
  if (!resource) return;
  const data = JSON.parse(document.querySelector("#cx-plan-data").textContent);
  const select = document.querySelector("#cx-priority");
  const tracks = Array.from(resource.querySelectorAll("[data-cx-track]"));
  const emitted = new Set();
  const once = (name, parameters = {}) => {
    if (emitted.has(name)) return;
    emitted.add(name);
    record(name, "resource", parameters);
  };
  let libraryPromise;
  const loadPdfLibrary = () => {
    if (window.PDFLib) return Promise.resolve(window.PDFLib);
    if (libraryPromise) return libraryPromise;
    libraryPromise = new Promise((resolve, reject) => {
      const script = document.createElement("script");
      const fail = () => { script.remove(); reject(new Error("PDF library unavailable")); };
      const timer = window.setTimeout(fail, 15000);
      script.src = data.pdf_library;
      script.onload = () => {
        window.clearTimeout(timer);
        if (window.PDFLib) resolve(window.PDFLib);
        else fail();
      };
      script.onerror = () => { window.clearTimeout(timer); fail(); };
      document.head.append(script);
    }).catch((error) => { libraryPromise = null; throw error; });
    return libraryPromise;
  };
  const showTrack = () => {
    tracks.forEach((track) => { track.hidden = track.dataset.cxTrack !== select.value; });
  };
  const requested = new URLSearchParams(window.location.search).get("topic");
  if (Object.hasOwn(data.tracks, requested)) select.value = requested;
  select.addEventListener("change", showTrack);
  showTrack();

  tracks.forEach((track) => {
    const form = track.querySelector("form");
    const result = track.querySelector("[data-cx-result]");
    const list = track.querySelector("[data-cx-actions]");
    const maintenance = track.querySelector("[data-cx-maintenance]");
    const download = track.querySelector("[data-cx-download]");
    const status = track.querySelector("[data-cx-status]");
    let currentPlan = null;
    let planVersion = 0;
    let downloading = false;
    form.querySelector('button[type="submit"]').disabled = false;
    form.addEventListener("change", () => {
      result.hidden = true;
      currentPlan = null;
      planVersion += 1;
      download.disabled = true;
      status.textContent = "";
    });
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const ready = Array.from(form.querySelectorAll('input[type="checkbox"]:checked')).map((input) => Number(input.value));
      currentPlan = selectActions(data.tracks[track.dataset.cxTrack], ready);
      planVersion += 1;
      status.textContent = "";
      list.replaceChildren();
      currentPlan.actions.forEach((action) => {
        const item = document.createElement("li");
        const heading = document.createElement("h4");
        heading.textContent = action[1];
        const evidence = document.createElement("p");
        evidence.textContent = `${data.evidence}: ${action[2]}`;
        item.append(heading, evidence);
        list.append(item);
      });
      maintenance.hidden = !currentPlan.maintenance;
      result.hidden = false;
      download.disabled = downloading;
      result.focus();
      once("cx_plan_generate");
    });
    download.addEventListener("click", async () => {
      if (!currentPlan || downloading) return;
      const snapshot = currentPlan;
      const version = planVersion;
      downloading = true;
      download.disabled = true;
      download.setAttribute("aria-busy", "true");
      status.textContent = data.download_loading;
      let url;
      let link;
      try {
        const PDFLib = await loadPdfLibrary();
        const topic = data.pdf_topics[track.dataset.cxTrack];
        const dateLabel = new Intl.DateTimeFormat(data.lang, { day: "2-digit", month: "long", year: "numeric" }).format(new Date());
        const { bytes } = await window.CxPlanPdf.create(PDFLib, {
          language: document.documentElement.lang, topic: topic.label,
          copy: data.pdf_copy, plan: snapshot, dateLabel,
          relatedTitle: topic.relatedTitle, relatedUrl: topic.relatedUrl,
        });
        if (version !== planVersion || select.value !== track.dataset.cxTrack) {
          if (version === planVersion) status.textContent = "";
          return;
        }
        url = URL.createObjectURL(new Blob([bytes], { type: "application/pdf" }));
        link = document.createElement("a");
        link.href = url;
        link.download = `luiz-terra-cx-${track.dataset.cxTrack}-${data.lang}.pdf`;
        document.body.append(link);
        link.click();
        status.textContent = data.downloaded;
        once("cx_plan_download", { file_format: "pdf" });
      } catch {
        if (version === planVersion) status.textContent = data.download_error;
      } finally {
        downloading = false;
        download.disabled = !currentPlan;
        download.setAttribute("aria-busy", "false");
        link?.remove();
        if (url) window.setTimeout(() => URL.revokeObjectURL(url), 10000);
      }
    });
  });
  once("cx_resource_view");
})();
