async function loadJSON(url) {
  const resp = await fetch(url, { credentials: "same-origin" });
  if (!resp.ok) throw new Error("Request failed");
  return await resp.json();
}

async function init() {
  const meEl = document.getElementById("me");
  const evEl = document.getElementById("events");
  if (!meEl || !evEl) return;

  try {
    const me = await loadJSON("/api/me");
    meEl.textContent = JSON.stringify(me, null, 2);
  } catch (e) {
    meEl.textContent = "Not authenticated or error fetching /me.";
  }

  try {
    const events = await loadJSON("/api/events");
    evEl.textContent = JSON.stringify(events, null, 2);
  } catch (e) {
    evEl.textContent = "Not authenticated or error fetching /me/events.";
  }
}

document.addEventListener("DOMContentLoaded", init);
