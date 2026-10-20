(function () {
  "use strict";

  var WHATSAPP_NUMBER = "4917676275792";
  var EMAIL = "info@royalclean-ay.de";

  // Header background once the page scrolls
  var header = document.querySelector("[data-header]");
  if (header && !document.body.classList.contains("page-legal")) {
    var onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 24);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  // Thin gold reading-progress line under the header
  var progress = document.querySelector("[data-progress]");
  if (progress) {
    var ticking = false;
    var updateProgress = function () {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.transform = "scaleX(" + (max > 0 ? Math.min(1, window.scrollY / max) : 0).toFixed(4) + ")";
      ticking = false;
    };
    updateProgress();
    window.addEventListener("scroll", function () {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(updateProgress);
      }
    }, { passive: true });
  }

  // Mobile menu
  var toggle = document.querySelector("[data-menu-toggle]");
  var nav = document.querySelector("[data-nav]");
  if (toggle && nav) {
    var setMenu = function (open) {
      toggle.setAttribute("aria-expanded", String(open));
      nav.classList.toggle("is-open", open);
      header.classList.toggle("is-open", open);
    };
    toggle.addEventListener("click", function () {
      setMenu(toggle.getAttribute("aria-expanded") !== "true");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) setMenu(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) {
        setMenu(false);
        toggle.focus();
      }
    });
  }

  // Footer year
  var year = document.querySelector("[data-year]");
  if (year) year.textContent = String(new Date().getFullYear());

  // Quote form
  var form = document.querySelector("[data-quote-form]");
  if (!form) return;

  var status = form.querySelector("[data-form-status]");
  var serviceSelect = form.querySelector("#f-leistung");
  var businessFields = form.querySelectorAll("[data-business-only]");

  // "Anfragen" links in the service list preselect the service
  document.querySelectorAll("[data-service]").forEach(function (link) {
    link.addEventListener("click", function () {
      serviceSelect.value = link.getAttribute("data-service");
      if (link.getAttribute("data-service") === "Privathaushalt") {
        form.querySelector('input[name="kunde"][value="Privat"]').checked = true;
        updateCustomerType();
      }
    });
  });

  // Service pages link to /?leistung=...#anfrage to preselect the service
  var requested = new URLSearchParams(window.location.search).get("leistung");
  if (requested) {
    var match = Array.prototype.some.call(serviceSelect.options, function (o) { return o.value === requested; });
    if (match) {
      serviceSelect.value = requested;
      if (requested === "Privathaushalt") {
        form.querySelector('input[name="kunde"][value="Privat"]').checked = true;
      }
    }
  }

  function updateCustomerType() {
    var isPrivate = form.querySelector('input[name="kunde"]:checked').value === "Privat";
    businessFields.forEach(function (el) {
      el.hidden = isPrivate;
    });
  }
  form.querySelectorAll('input[name="kunde"]').forEach(function (radio) {
    radio.addEventListener("change", updateCustomerType);
  });
  updateCustomerType();

  var rules = [
    { id: "f-name", test: function (v) { return v.trim().length > 1; }, msg: "Bitte geben Sie Ihren Namen an." },
    { id: "f-telefon", test: function (v) { return v.replace(/[^\d]/g, "").length >= 6; }, msg: "Bitte geben Sie eine Telefonnummer an, unter der wir Sie erreichen." },
    { id: "f-email", test: function (v) { return v.trim() === "" || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()); }, msg: "Diese E-Mail-Adresse ist unvollständig. Beispiel: name@firma.de" },
    { id: "f-leistung", test: function (v) { return v !== ""; }, msg: "Bitte wählen Sie eine Leistung aus." },
    { id: "f-ort", test: function (v) { return v.trim().length > 1; }, msg: "Bitte geben Sie an, wo sich das Objekt befindet." }
  ];

  function setError(input, message) {
    var error = document.getElementById(input.id + "-error");
    if (message) {
      input.setAttribute("aria-invalid", "true");
      input.setAttribute("aria-describedby", input.id + "-error");
    } else {
      input.removeAttribute("aria-invalid");
      input.removeAttribute("aria-describedby");
    }
    if (error) error.textContent = message || "";
  }

  function validate() {
    var firstInvalid = null;
    rules.forEach(function (rule) {
      var input = document.getElementById(rule.id);
      var ok = rule.test(input.value);
      setError(input, ok ? "" : rule.msg);
      if (!ok && !firstInvalid) firstInvalid = input;
    });
    var consent = document.getElementById("f-datenschutz");
    setError(consent, consent.checked ? "" : "Bitte bestätigen Sie, dass Sie die Datenschutzerklärung gelesen haben.");
    if (!consent.checked && !firstInvalid) firstInvalid = consent;
    return firstInvalid;
  }

  // Clear an error as soon as the field is fixed
  form.addEventListener("input", function (e) {
    var t = e.target;
    if (t.getAttribute("aria-invalid") !== "true") return;
    var rule = rules.filter(function (r) { return r.id === t.id; })[0];
    if ((rule && rule.test(t.value)) || (t.type === "checkbox" && t.checked)) setError(t, "");
  });

  function buildMessage() {
    var data = new FormData(form);
    var isPrivate = data.get("kunde") === "Privat";
    var lines = [
      "Angebotsanfrage über royalclean-ay.de",
      "",
      "Kunde: " + data.get("kunde"),
      "Name: " + data.get("name").trim()
    ];
    if (!isPrivate && data.get("firma").trim()) lines.push("Firma: " + data.get("firma").trim());
    lines.push("Telefon: " + data.get("telefon").trim());
    if (data.get("email").trim()) lines.push("E-Mail: " + data.get("email").trim());
    lines.push("Leistung: " + data.get("leistung"));
    lines.push("Ort: " + data.get("ort").trim());
    lines.push("Turnus: " + data.get("turnus"));
    if (data.get("flaeche").trim()) lines.push("Fläche: ca. " + data.get("flaeche").trim() + " m²");
    if (data.get("nachricht").trim()) {
      lines.push("", "Nachricht:", data.get("nachricht").trim());
    }
    return lines.join("\n");
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var invalid = validate();
    if (invalid) {
      status.textContent = "";
      invalid.focus();
      return;
    }

    var via = e.submitter ? e.submitter.value : "whatsapp";
    var text = buildMessage();

    if (via === "email") {
      var subject = "Angebotsanfrage: " + serviceSelect.value;
      window.location.href = "mailto:" + EMAIL +
        "?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(text);
      status.textContent = "Ihr E-Mail-Programm wurde mit der fertigen Anfrage geöffnet. Bitte senden Sie die E-Mail dort ab.";
    } else {
      window.open("https://wa.me/" + WHATSAPP_NUMBER + "?text=" + encodeURIComponent(text), "_blank", "noopener");
      status.textContent = "WhatsApp wurde mit der fertigen Anfrage geöffnet. Bitte senden Sie die Nachricht dort ab.";
    }
  });
})();
