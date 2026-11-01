(function () {
  "use strict";

  const selectActions = (checks, ready) => {
    const pending = checks.filter((_, index) => !ready.includes(index));
    return { maintenance: pending.length === 0, actions: (pending.length ? pending : checks).slice(0, 3) };
  };
  const csvCell = (value) => {
    const text = String(value);
    const safe = /^[=+\-@\t\r]/.test(text) ? `'${text}` : text;
    return `"${safe.replaceAll('"', '""')}"`;
  };
  const planCsv = (headers, actions, cadence) => "\uFEFF" + [
    headers,
    ...actions.map((action, index) => [String(index + 1), action[1], action[2], cadence]),
  ].map((row) => row.map(csvCell).join(";")).join("\r\n");

  if (typeof module === "object" && module.exports) module.exports = { selectActions, planCsv, csvCell };
  if (typeof document === "undefined") return;

  const record = (name, placement) => {
    if (!["www.luizterra.com.br", "luizterra.com.br"].includes(window.location.hostname)) return;
    if (typeof window.gtag !== "function") return;
    window.gtag("event", name, { send_to: "G-68E95X4DZT", placement });
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
  const once = (name) => {
    if (emitted.has(name)) return;
    emitted.add(name);
    record(name, "resource");
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
    form.querySelector('button[type="submit"]').disabled = false;
    form.addEventListener("change", () => {
      result.hidden = true;
      currentPlan = null;
      download.disabled = true;
      status.textContent = "";
    });
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const ready = Array.from(form.querySelectorAll('input[type="checkbox"]:checked')).map((input) => Number(input.value));
      currentPlan = selectActions(data.tracks[track.dataset.cxTrack], ready);
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
      download.disabled = false;
      result.focus();
      once("cx_plan_generate");
    });
    download.addEventListener("click", () => {
      if (!currentPlan) return;
      let url;
      let link;
      try {
        const csv = planCsv(data.headers, currentPlan.actions, data.cadence);
        url = URL.createObjectURL(new Blob([csv], { type: "text/csv;charset=utf-8;" }));
        link = document.createElement("a");
        link.href = url;
        link.download = `luiz-terra-cx-${track.dataset.cxTrack}-${data.lang}.csv`;
        document.body.append(link);
        link.click();
        status.textContent = data.downloaded;
        once("cx_plan_download");
      } catch {
        status.textContent = data.download_error;
      } finally {
        link?.remove();
        if (url) window.setTimeout(() => URL.revokeObjectURL(url), 10000);
      }
    });
  });
  once("cx_resource_view");
})();
