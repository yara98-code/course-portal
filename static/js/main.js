function subscribeToOffering(offeringId, buttonEl) {
  buttonEl.disabled = true;
  buttonEl.textContent = "Subscribing...";

  let statusEl = buttonEl.parentElement.querySelector(".subscribe-status");
  if (!statusEl) {
    statusEl = document.createElement("span");
    statusEl.className = "subscribe-status";
    buttonEl.parentElement.appendChild(statusEl);
  }

  statusEl.textContent = "";
  statusEl.className = "subscribe-status";

  fetch("/ajax/subscribe", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCSRFToken(),
    },
    body: JSON.stringify({ offering_id: offeringId }),
  })
    .then((response) => {
      return response.json().then((data) => ({ ok: response.ok, data }));
    })
    .then(({ ok, data }) => {
      if (ok && data.success) {
        showStatus(
          statusEl,
          data.message || "Subscribed successfully!",
          "success",
        );
        buttonEl.textContent = "Subscribed";
        buttonEl.classList.add("btn-subscribed");
      } else {
        showStatus(statusEl, data.message || "Something went wrong.", "error");
        resetButton(buttonEl);
      }
    })
    .catch((err) => {
      console.error("Subscribe error: - main.js:41", err);
      showStatus(statusEl, "Network error. Please try again.", "error");
      resetButton(buttonEl);
    });
}

function getCSRFToken() {
  const meta = document.querySelector('meta[name="csrf-token"]');
  return meta ? meta.getAttribute("content") : "";
}

function showStatus(el, msg, type) {
  el.textContent = msg;
  el.className = "subscribe-status " + (type === "success" ? "status-success" : "status-error");
}

function resetButton(btn) {
  btn.disabled = false;
  btn.textContent = "Subscribe Now";
}

document.addEventListener("DOMContentLoaded", () => {
  const savedTheme = getCookie(THEME_COOKIE) || "light";
  applyTheme(savedTheme);

  const toggleBtn = document.getElementById("theme-toggle");
  if (toggleBtn) {
    toggleBtn.addEventListener("click", toggleTheme);
  }

  document.querySelectorAll(".btn-subscribe").forEach((btn) => {
    btn.addEventListener("click", () => {
      const offeringId = btn.dataset.offeringId;
      if (offeringId) {
        subscribeToOffering(offeringId, btn);
      }
    });
  });
});

const THEME_COOKIE = "theme";
const DARK_CLASS = "dark-mode";

function setCookie(name, value, days) {
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  document.cookie =
    name +
    "=" +
    encodeURIComponent(value) +
    "; expires=" +
    expires +
    "; path=/; SameSite=Lax";
}

function getCookie(name) {
  const match = document.cookie.match(
    new RegExp(
      "(?:^|; )" + name.replace(/([.$?*|{}()[\].\\/+^])/g, "\\$1") + "=([^;]*)",
    ),
  );
  return match ? decodeURIComponent(match[1]) : null;
}

function applyTheme(theme) {
  const isDark = theme === "dark";
  document.body.classList.toggle(DARK_CLASS, isDark);

  const toggleBtn = document.getElementById("theme-toggle");
  if (toggleBtn) {
    toggleBtn.textContent = isDark ? "Light Mode" : "Dark Mode";
    toggleBtn.setAttribute("aria-pressed", String(isDark));
  }
}

function toggleTheme() {
  const current = getCookie(THEME_COOKIE) || "light";
  const next = current === "dark" ? "light" : "dark";
  setCookie(THEME_COOKIE, next, 365);
  applyTheme(next);
}