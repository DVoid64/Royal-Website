(function () {
  "use strict";

  // Royal seal: guilloche rings, crown and founding year, built as stacked
  // SVG layers so the hero version can tilt with real depth.

  var NS = "http://www.w3.org/2000/svg";
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var uid = 0;

  function el(name, attrs, parent) {
    var node = document.createElementNS(NS, name);
    for (var k in attrs) node.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(node);
    return node;
  }

  // One closed curve: r(t) = base + amp * sin(n * t + phase)
  function wave(base, amp, n, phase) {
    var steps = n * 10;
    var d = "";
    for (var i = 0; i <= steps; i++) {
      var t = (i / steps) * Math.PI * 2;
      var r = base + amp * Math.sin(n * t + phase);
      d += (i ? "L" : "M") + (r * Math.cos(t)).toFixed(1) + " " + (r * Math.sin(t)).toFixed(1);
    }
    return d + "Z";
  }

  function band(svg, base, amp, n, strands, width) {
    var g = el("g", { "class": "seal-band" }, svg);
    for (var k = 0; k < strands; k++) {
      el("path", {
        d: wave(base, amp, n, (k / strands) * Math.PI * 2),
        "stroke-width": width,
        pathLength: 1
      }, g);
    }
    return g;
  }

  function ring(svg, r, width) {
    return el("circle", { cx: 0, cy: 0, r: r, "stroke-width": width, pathLength: 1 }, svg);
  }

  function layer(seal, depth) {
    var svg = el("svg", { viewBox: "-300 -300 600 600", "class": "seal-layer", "aria-hidden": "true", focusable: "false" });
    svg.dataset.depth = depth;
    seal.appendChild(svg);
    return svg;
  }

  function build(seal) {
    var id = "seal-text-" + (++uid);

    // Outer rings and the engraved name
    var outer = layer(seal, 0);
    ring(outer, 292, 1.2);
    ring(outer, 286, .6);
    ring(outer, 244, .6);
    ring(outer, 238, 1.2);
    el("path", { id: id, d: "M0,-264 a264,264 0 1,1 -0.1,0", fill: "none", stroke: "none" }, outer);
    var text = el("text", { "class": "seal-text" }, outer);
    var tp = el("textPath", { href: "#" + id, textLength: 1650, lengthAdjust: "spacing" }, text);
    tp.textContent = "ROYAL CLEAN SERVICES AY ✦ GEBÄUDEREINIGUNG ✦ OBERHAUSEN ✦ GEGRÜNDET 2025 ✦";

    // Two woven guilloche bands
    var a = layer(seal, 18);
    band(a, 214, 14, 30, 7, .55);
    ring(a, 192, .5);

    var b = layer(seal, 36);
    band(b, 152, 26, 15, 9, .55);
    ring(b, 118, .6);

    // Rosette, crown and year
    var c = layer(seal, 60);
    band(c, 82, 28, 8, 12, .5);
    ring(c, 112, .5);
    el("circle", { cx: 0, cy: 0, r: 66, "class": "seal-disc" }, c);
    ring(c, 66, .8);
    var crown = el("g", { "class": "seal-crown", transform: "translate(0 -8) scale(.82)" }, c);
    el("path", { d: "M-36 14 L-42 -20 L-21 0 L0 -32 L21 0 L42 -20 L36 14 Z", "stroke-width": 1.4, pathLength: 1 }, crown);
    el("path", { d: "M-36 14 H36 M-34 22 H34", "stroke-width": 1.4, pathLength: 1 }, crown);
    el("circle", { cx: -42, cy: -25, r: 3.5, "stroke-width": 1.2, pathLength: 1 }, crown);
    el("circle", { cx: 0, cy: -37, r: 4, "stroke-width": 1.2, pathLength: 1 }, crown);
    el("circle", { cx: 42, cy: -25, r: 3.5, "stroke-width": 1.2, pathLength: 1 }, crown);
    var year = el("text", { "class": "seal-year", x: 2, y: 46, "text-anchor": "middle" }, c);
    year.textContent = "MMXXV";

    seal.classList.add("is-built");
  }

  function draw(seal) {
    if (reduceMotion) {
      seal.classList.add("is-drawn");
      return;
    }
    var strokes = seal.querySelectorAll("path[pathLength], circle[pathLength]");
    strokes.forEach(function (p, i) {
      var depth = Number(p.ownerSVGElement.dataset.depth);
      p.animate(
        [{ strokeDashoffset: 1 }, { strokeDashoffset: 0 }],
        {
          duration: 1800,
          delay: 150 + depth * 14 + (i % 10) * 40,
          easing: "cubic-bezier(0.77, 0, 0.175, 1)",
          fill: "backwards"
        }
      );
    });
    seal.classList.add("is-drawn");
  }

  // Hero seal: tilts toward the pointer with spring-like easing, rings turn on scroll
  function animateHero(seal) {
    var layers = Array.prototype.slice.call(seal.querySelectorAll(".seal-layer"));
    var target = { x: 0, y: 0 };
    var current = { x: 0, y: 0 };
    var visible = true;
    var running = false;

    function frame() {
      current.x += (target.x - current.x) * 0.08;
      current.y += (target.y - current.y) * 0.08;
      var spin = window.scrollY * 0.04;
      seal.style.transform = "rotateX(" + current.y.toFixed(2) + "deg) rotateY(" + current.x.toFixed(2) + "deg)";
      layers.forEach(function (l, i) {
        var dir = i % 2 ? -1 : 1;
        l.style.transform = "translateZ(" + l.dataset.depth + "px) rotate(" + (spin * dir * (i ? 1 : .4)).toFixed(2) + "deg)";
      });
      var settling = Math.abs(target.x - current.x) + Math.abs(target.y - current.y) > 0.01;
      if (visible && settling) {
        requestAnimationFrame(frame);
      } else {
        running = false;
      }
    }

    function kick() {
      if (!running && visible) {
        running = true;
        requestAnimationFrame(frame);
      }
    }

    if (finePointer) {
      seal.closest(".hero").addEventListener("pointermove", function (e) {
        var r = seal.getBoundingClientRect();
        target.x = ((e.clientX - (r.left + r.width / 2)) / window.innerWidth) * 16;
        target.y = -((e.clientY - (r.top + r.height / 2)) / window.innerHeight) * 16;
        kick();
      });
      seal.closest(".hero").addEventListener("pointerleave", function () {
        target.x = 0;
        target.y = 0;
        kick();
      });
    }

    window.addEventListener("scroll", kick, { passive: true });

    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        visible = entries[0].isIntersecting;
        if (visible) kick();
      }).observe(seal);
    }
    kick();
  }

  var seals = document.querySelectorAll("[data-seal]");
  seals.forEach(function (seal) {
    build(seal);
    var mode = seal.getAttribute("data-seal");

    if (mode === "hero") {
      draw(seal);
      if (!reduceMotion) animateHero(seal);
    } else if (mode === "reveal" && "IntersectionObserver" in window && !reduceMotion) {
      var io = new IntersectionObserver(function (entries) {
        if (entries[0].isIntersecting) {
          draw(seal);
          io.disconnect();
        }
      }, { rootMargin: "0px 0px -15% 0px" });
      io.observe(seal);
    } else {
      seal.classList.add("is-drawn");
    }
  });
})();
