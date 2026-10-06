// Generative infographics for the Elevatus brochure.
// Every SVG is drawn in millimetre units so it prints at exactly the size it is laid out at.

const NS = "http://www.w3.org/2000/svg";
const L = (n) => `assets/logos/${n}.svg`;

// deterministic randomness so every export is identical
function rng(seed) {
  let s = seed >>> 0;
  return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296);
}
const rad = (d) => (d * Math.PI) / 180;
const polar = (cx, cy, r, deg) => [cx + r * Math.cos(rad(deg)), cy + r * Math.sin(rad(deg))];
const f = (n) => +n.toFixed(3);

function el(tag, attrs = {}, parent) {
  const n = document.createElementNS(NS, tag);
  for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
  if (parent) parent.appendChild(n);
  return n;
}
function txt(parent, x, y, s, attrs = {}) {
  const t = el("text", { x: f(x), y: f(y), ...attrs }, parent);
  t.textContent = s;
  return t;
}
function svgRoot(host, w, h) {
  const s = el("svg", { viewBox: `0 0 ${w} ${h}`, xmlns: NS });
  host.appendChild(s);
  return s;
}
function arcPath(cx, cy, r, a0, a1) {
  const [x0, y0] = polar(cx, cy, r, a0);
  const [x1, y1] = polar(cx, cy, r, a1);
  const large = a1 - a0 > 180 ? 1 : 0;
  return `M${f(x0)} ${f(y0)} A${r} ${r} 0 ${large} 1 ${f(x1)} ${f(y1)}`;
}
function bandPath(cx, cy, r0, r1, a0, a1) {
  const [ax, ay] = polar(cx, cy, r1, a0), [bx, by] = polar(cx, cy, r1, a1);
  const [cx2, cy2] = polar(cx, cy, r0, a1), [dx, dy] = polar(cx, cy, r0, a0);
  const large = a1 - a0 > 180 ? 1 : 0;
  return `M${f(ax)} ${f(ay)} A${r1} ${r1} 0 ${large} 1 ${f(bx)} ${f(by)} L${f(cx2)} ${f(cy2)} A${r0} ${r0} 0 ${large} 0 ${f(dx)} ${f(dy)}Z`;
}
function gradient(defs, id, stops, x2 = 1, y2 = 0, extra = {}) {
  const g = el("linearGradient", { id, x1: 0, y1: 0, x2, y2, ...extra }, defs);
  stops.forEach(([o, c, op = 1]) => el("stop", { offset: o, "stop-color": c, "stop-opacity": op }, g));
  return g;
}

const BRAND = ["#4d7cff", "#6a63ff", "#7a5cff", "#a46fd8", "#d98d8a", "#f2a45f"];

/* ------------------------------------------------------------------ */
/* P01 — hero orbit behind the Enfinity agent UI                       */
/* ------------------------------------------------------------------ */
function drawHero(host) {
  const px2mm = 25.4 / 96;
  const W = host.clientWidth * px2mm, H = host.clientHeight * px2mm;
  const s = svgRoot(host, f(W), f(H));
  s.classList.add("orbit");
  const defs = el("defs", {}, s);
  const core = el("radialGradient", { id: "core", cx: "50%", cy: "50%", r: "50%" }, defs);
  [["0%", "#ffffff", 1], ["18%", "#dfe6ff", 0.95], ["45%", "#5b7dff", 0.75], ["75%", "#3a2fd0", 0.25], ["100%", "#3a2fd0", 0]]
    .forEach(([o, c, op]) => el("stop", { offset: o, "stop-color": c, "stop-opacity": op }, core));
  const halo = el("radialGradient", { id: "halo", cx: "50%", cy: "50%", r: "50%" }, defs);
  [["0%", "#f2a45f", 0.55], ["60%", "#7a5cff", 0.18], ["100%", "#7a5cff", 0]]
    .forEach(([o, c, op]) => el("stop", { offset: o, "stop-color": c, "stop-opacity": op }, halo));
  gradient(defs, "orbitStroke", [[0, "#ffffff", 0.05], [0.5, "#ffffff", 0.55], [1, "#f2a45f", 0.7]]);

  const cx = W * 0.7, cy = H * 0.5, R = Math.min(W, H) * 0.25;
  el("circle", { cx: f(cx), cy: f(cy), r: f(R * 2.3), fill: "url(#halo)" }, s);

  // tilted orbits
  const orbits = [[R * 1.25, R * 0.62, -18], [R * 1.75, R * 0.9, -18], [R * 2.25, R * 1.18, -18]];
  orbits.forEach(([rx, ry, rot], i) => {
    el("ellipse", {
      cx: f(cx), cy: f(cy), rx: f(rx), ry: f(ry), transform: `rotate(${rot} ${f(cx)} ${f(cy)})`,
      fill: "none", stroke: "url(#orbitStroke)", "stroke-width": i === 1 ? 0.28 : 0.2,
      "stroke-dasharray": i === 2 ? "0.6 1.4" : "none",
    }, s);
  });
  // nodes travelling on the orbits
  const nodes = [[0, 200, 1.1], [0, 20, 0.8], [1, 250, 1.3], [1, 95, 1], [2, 150, 1.2], [2, 320, 0.9]];
  nodes.forEach(([o, deg, r], i) => {
    const [rx, ry, rot] = orbits[o];
    const x0 = rx * Math.cos(rad(deg)), y0 = ry * Math.sin(rad(deg));
    const x = cx + x0 * Math.cos(rad(rot)) - y0 * Math.sin(rad(rot));
    const y = cy + x0 * Math.sin(rad(rot)) + y0 * Math.cos(rad(rot));
    el("circle", { cx: f(x), cy: f(y), r: r * 1.9, fill: BRAND[i % 6], opacity: 0.22, class: "pulse" }, s);
    el("circle", { cx: f(x), cy: f(y), r, fill: i % 2 ? "#ffffff" : "#f2a45f" }, s);
  });
  // core orb
  el("circle", { cx: f(cx), cy: f(cy), r: f(R), fill: "url(#core)" }, s);
  el("circle", { cx: f(cx), cy: f(cy), r: f(R * 0.56), fill: "none", stroke: "#fff", "stroke-opacity": 0.5, "stroke-width": 0.25 }, s);
  txt(s, cx, cy + 0.2, "Enfinity", { "text-anchor": "middle", "font-size": 4.6, "font-weight": 600, fill: "#0a0f2e", "letter-spacing": -0.1 });
  txt(s, cx, cy + 3.8, "AGENTIC AI", { "text-anchor": "middle", "font-size": 1.9, "font-weight": 700, fill: "#2340ff", "letter-spacing": 0.5 });

  // place the floating chips on the orbit geometry
  const chips = host.querySelectorAll(".chip");
  const spots = [[W * 0.66, H * 0.06], [W * 0.88, H * 0.3], [W * 0.84, H * 0.78], [W * 0.46, H * 0.9]];
  chips.forEach((c, i) => {
    const [x, y] = spots[i];
    c.style.left = `${x}mm`; c.style.top = `${y}mm`;
    c.style.transform = "translate(-50%, -50%)";
  });
}

/* ------------------------------------------------------------------ */
/* P02 — awards (laurels) and security seals                           */
/* ------------------------------------------------------------------ */
function laurel(year, lines) {
  const s = el("svg", { viewBox: "0 0 44 32", xmlns: NS });
  const cx = 22, cy = 16.5, r = 14.6;
  [-1, 1].forEach((side) => {
    for (let i = 0; i < 9; i++) {
      const a = 112 + i * 15.5;               // sweep up one side
      const deg = side < 0 ? a : 180 - a;
      const [x, y] = polar(cx, cy, r, deg);
      const tangent = deg + (side < 0 ? 90 : -90) + side * 28;
      const sc = 1 - i * 0.045;
      el("ellipse", {
        cx: f(x), cy: f(y), rx: f(2.25 * sc), ry: f(0.85 * sc), transform: `rotate(${f(tangent)} ${f(x)} ${f(y)})`,
        fill: "#fff", opacity: f(0.95 - i * 0.05),
      }, s);
    }
    el("path", { d: side < 0 ? arcPath(cx, cy, r - 0.2, 108, 236) : arcPath(cx, cy, r - 0.2, -56, 72), fill: "none", stroke: "#fff", "stroke-width": 0.3, opacity: 0.6 }, s);
  });
  el("path", { d: star(cx, 9.6, 1.5), fill: "#f2a45f" }, s);
  txt(s, cx, 19.6, year, { "text-anchor": "middle", "font-size": 7.4, "font-weight": 700, fill: "#fff", "letter-spacing": -0.3 });
  return s;
}

function seal(id, top, big, small, ringText) {
  const s = el("svg", { viewBox: "0 0 40 40", xmlns: NS });
  const defs = el("defs", {}, s);
  gradient(defs, `sg-${id}`, [[0, "#4d7cff"], [0.6, "#7a5cff"], [1, "#f2a45f"]], 1, 1);
  el("circle", { cx: 20, cy: 20, r: 19, fill: "none", stroke: `url(#sg-${id})`, "stroke-width": 1.2 }, s);
  el("circle", { cx: 20, cy: 20, r: 12.4, fill: "rgba(255,255,255,0.06)", stroke: "#fff", "stroke-opacity": 0.35, "stroke-width": 0.35 }, s);
  el("path", { id: `ring-${id}`, d: "M20 20 m-15.4 0 a15.4 15.4 0 1 1 30.8 0 a15.4 15.4 0 1 1 -30.8 0", fill: "none" }, defs);
  const t = el("text", { "font-size": 2.5, "font-weight": 600, fill: "#fff", "fill-opacity": 0.75, textLength: 94, lengthAdjust: "spacing" }, s);
  const tp = el("textPath", { href: `#ring-${id}`, startOffset: "0" }, t);
  tp.textContent = ringText;
  if (id === "gdpr") {
    for (let i = 0; i < 12; i++) {
      const [x, y] = polar(20, 20, 9.6, i * 30 - 90);
      el("path", { d: star(x, y, 0.95), fill: "#f2c14e" }, s);
    }
    txt(s, 20, 21.6, big, { "text-anchor": "middle", "font-size": 5, "font-weight": 700, fill: "#fff", "letter-spacing": -0.1 });
    return s;
  }
  if (top) txt(s, 20, 16.8, top, { "text-anchor": "middle", "font-size": 2.5, "font-weight": 600, fill: "#fff", "fill-opacity": 0.7, "letter-spacing": 0.4 });
  txt(s, 20, 22.6, big, { "text-anchor": "middle", "font-size": big.length > 4 ? 5.3 : 6.4, "font-weight": 700, fill: "#fff", "letter-spacing": -0.2 });
  if (small) txt(s, 20, 26.4, small, { "text-anchor": "middle", "font-size": 2.6, "font-weight": 600, fill: "#f2a45f", "letter-spacing": 0.4 });
  return s;
}
function star(cx, cy, r) {
  let d = "";
  for (let i = 0; i < 10; i++) {
    const rr = i % 2 ? r * 0.45 : r;
    const [x, y] = polar(cx, cy, rr, i * 36 - 90);
    d += `${i ? "L" : "M"}${f(x)} ${f(y)}`;
  }
  return d + "Z";
}

/* ------------------------------------------------------------------ */
/* P03 — challenges (outer ring) → hiring journey (inner ring)         */
/* ------------------------------------------------------------------ */
const PROBLEMS = [
  ["01", "BUSINESS CONTEXT"], ["02", "FLEXIBILITY"], ["03", "SPEED TO VALUE"],
  ["04", "MANUAL WORKLOAD"], ["05", "VISIBILITY"], ["06", "SCALABILITY"],
];
const STAGES = [
  ["A", "Requisition"], ["B", "Sourcing"], ["C", "Screening"],
  ["D", "Assess & interview"], ["E", "Select & offer"], ["F", "Onboard"],
];
// which journey stages answer each challenge (index into STAGES)
const MAP = [[0], [0, 4], [1, 2], [2, 3], [3, 4], [3, 5]];

function drawRings(host) {
  const W = 134, H = 100, cx = 67, cy = 50;
  const s = svgRoot(host, W, H);
  const defs = el("defs", {}, s);
  gradient(defs, "bandFill", [[0, "#ffffff"], [1, "#eef1ff"]], 0, 1);
  gradient(defs, "coreFill", [[0, "#2340ff"], [0.55, "#5a3ee0"], [1, "#f2a45f"]], 1, 1);
  gradient(defs, "spoke", [[0, "#2340ff", 0.0], [1, "#2340ff", 0.75]], 1, 0);
  const glow = el("filter", { id: "softGlow", x: "-50%", y: "-50%", width: "200%", height: "200%" }, defs);
  el("feGaussianBlur", { stdDeviation: 3 }, glow);

  // ambient dot field
  const r = rng(7);
  for (let i = 0; i < 160; i++) {
    const a = r() * 360, d = 30 + r() * 20;
    const [x, y] = polar(cx, cy, d, a);
    el("circle", { cx: f(x), cy: f(y), r: 0.18, fill: "#2340ff", opacity: f(0.08 + r() * 0.2) }, s);
  }

  const R0 = 39, R1 = 48.5, gap = 2.2;
  PROBLEMS.forEach(([n, name], i) => {
    const mid = -90 + i * 60, a0 = mid - 30 + gap, a1 = mid + 30 - gap;
    el("path", {
      d: bandPath(cx, cy, R0, R1, a0, a1), fill: "url(#bandFill)", stroke: "#0a0f2e", "stroke-opacity": 0.14, "stroke-width": 0.25,
    }, s);
    // puzzle "key" notch pointing inward
    const [kx, ky] = polar(cx, cy, R0 - 0.2, mid);
    el("circle", { cx: f(kx), cy: f(ky), r: 1.5, fill: "#ffffff", stroke: "#2340ff", "stroke-width": 0.35 }, s);
    // label along the arc (flip lower half so it reads left→right)
    const lower = mid > 0 && mid < 180;
    const rp = (R0 + R1) / 2;
    const pid = `arc-${i}`;
    el("path", { id: pid, d: lower ? arcPathRev(cx, cy, rp - 1, a1, a0) : arcPath(cx, cy, rp - 1, a0, a1), fill: "none" }, defs);
    const t = el("text", { "font-size": 2.35, "font-weight": 700, "letter-spacing": 0.38, fill: "#0a0f2e" }, s);
    const tp = el("textPath", { href: `#${pid}`, startOffset: "50%", "text-anchor": "middle" }, t);
    const num = el("tspan", { fill: "#2340ff" }, tp); num.textContent = `${n}  `;
    const lab = el("tspan", {}, tp); lab.textContent = name;
  });

  // inner journey ring with direction arrows
  const RJ = 27.5;
  el("circle", { cx, cy, r: RJ, fill: "none", stroke: "#0a0f2e", "stroke-opacity": 0.22, "stroke-width": 0.3, "stroke-dasharray": "0.9 1.1" }, s);
  for (let i = 0; i < 6; i++) {
    const a = -60 + i * 60;
    const [x, y] = polar(cx, cy, RJ, a);
    el("path", { d: "M-0.9 -1 L0.9 0 L-0.9 1Z", fill: "#2340ff", transform: `translate(${f(x)} ${f(y)}) rotate(${a + 90})` }, s);
  }

  // spokes: challenge → the stages that answer it
  MAP.forEach((targets, i) => {
    const mid = -90 + i * 60;
    const [sx, sy] = polar(cx, cy, R0 - 1.8, mid);
    targets.forEach((ti) => {
      const tm = -90 + ti * 60;
      const [tx, ty] = polar(cx, cy, RJ + 3.6, tm);
      const [qx, qy] = polar(cx, cy, (R0 + RJ) / 2 + 1, (mid + tm) / 2);
      el("path", { d: `M${f(sx)} ${f(sy)} Q${f(qx)} ${f(qy)} ${f(tx)} ${f(ty)}`, fill: "none", stroke: "#2340ff", "stroke-opacity": ti === i ? 0.7 : 0.38, "stroke-width": 0.3, class: "flow" }, s);
      el("circle", { cx: f(tx), cy: f(ty), r: 0.45, fill: "#2340ff" }, s);
    });
  });

  // stage nodes
  STAGES.forEach(([l, name], i) => {
    const a = -90 + i * 60;
    const [x, y] = polar(cx, cy, RJ, a);
    el("rect", { x: f(x - 3.3), y: f(y - 3.3), width: 6.6, height: 6.6, rx: 1.8, fill: BRAND[i], stroke: "#fff", "stroke-width": 0.5 }, s);
    txt(s, x, y + 1.15, l, { "text-anchor": "middle", "font-size": 3.3, "font-weight": 700, fill: "#fff" });
    // label towards the centre
    const below = Math.sin(rad(a)) > 0.6 ? -4.6 : 5.9;   // bottom node: label above it
    const w = name.length * 1.25 + 2.4;
    el("rect", { x: f(x - w / 2), y: f(y + below - 2.2), width: f(w), height: 3.1, rx: 1.55, fill: "#fff", stroke: "#0a0f2e", "stroke-opacity": 0.1, "stroke-width": 0.2 }, s);
    txt(s, x, y + below, name, { "text-anchor": "middle", "font-size": 2.05, "font-weight": 600, fill: "#2a3152" });
  });

  // core
  el("circle", { cx, cy, r: 11, fill: "#5a3ee0", opacity: 0.35, filter: "url(#softGlow)" }, s);
  el("circle", { cx, cy, r: 10.4, fill: "url(#coreFill)" }, s);
  el("circle", { cx, cy, r: 12, fill: "none", stroke: "#2340ff", "stroke-opacity": 0.25, "stroke-width": 0.25 }, s);
  el("image", { href: L("elevatus-white"), x: cx - 6.6, y: cy - 2.4, width: 13.2, height: 1.75 }, s);
  txt(s, cx, cy + 1.9, "ENFINITY", { "text-anchor": "middle", "font-size": 1.6, "font-weight": 700, fill: "#fff", "letter-spacing": 0.35 });
  txt(s, cx, cy + 4.1, "AGENTIC AI", { "text-anchor": "middle", "font-size": 1.3, "font-weight": 600, fill: "#fff", "fill-opacity": 0.75, "letter-spacing": 0.3 });

  // legend
  const lg = el("g", { transform: "translate(104 2)" }, s);
  el("rect", { x: 0, y: 0, width: 3, height: 2, rx: 0.5, fill: "#fff", stroke: "#0a0f2e", "stroke-opacity": 0.3, "stroke-width": 0.2 }, lg);
  txt(lg, 4.2, 1.7, "Outer — your challenges", { "font-size": 2.1, fill: "#5b6280", "font-weight": 500 });
  el("rect", { x: 0, y: 3.6, width: 3, height: 2, rx: 0.5, fill: "#4d7cff" }, lg);
  txt(lg, 4.2, 5.3, "Inner — our hiring journey", { "font-size": 2.1, fill: "#5b6280", "font-weight": 500 });
}
function arcPathRev(cx, cy, r, a1, a0) {
  const [x1, y1] = polar(cx, cy, r, a1), [x0, y0] = polar(cx, cy, r, a0);
  return `M${f(x1)} ${f(y1)} A${r} ${r} 0 0 0 ${f(x0)} ${f(y0)}`;
}

/* ------------------------------------------------------------------ */
/* P04 — connected ecosystem with real integration logos               */
/* ------------------------------------------------------------------ */
const CLUSTERS = [
  { name: "HR & enterprise systems", stages: "A · F", at: [-105, -75], logos: ["sap", "oracle"], label: [70, 3.2, "middle"] },
  { name: "Sourcing & job boards", stages: "B", at: [-45, -15], logos: ["linkedin", "indeed"], label: [139, 14, "end"] },
  { name: "Candidate communication", stages: "C", at: [15, 45], logos: ["whatsapp", "gmail"], label: [139, 101.5, "end"] },
  { name: "Interviews & collaboration", stages: "D", at: [75, 105, 135], logos: ["teams", "zoom", "meet"], label: [70, 112, "middle"] },
  { name: "Offers, signing & learning", stages: "E · F", at: [165, 195, 225], logos: ["docusign", "slack", "udemy"], label: [1, 14, "start"] },
];

function drawEcosystem(host) {
  const W = 140, H = 118, cx = 70, cy = 57;
  const s = svgRoot(host, W, H);
  const defs = el("defs", {}, s);
  gradient(defs, "wire", [[0, "#4d7cff", 0.9], [0.55, "#7a5cff", 0.7], [1, "#f2a45f", 0.9]], 1, 1);
  const hub = el("radialGradient", { id: "hubGlow", cx: "50%", cy: "50%", r: "50%" }, defs);
  [["0%", "#7a5cff", 0.35], ["55%", "#4d7cff", 0.12], ["100%", "#4d7cff", 0]].forEach(([o, c, op]) => el("stop", { offset: o, "stop-color": c, "stop-opacity": op }, hub));
  gradient(defs, "hubRing", [[0, "#4d7cff"], [0.5, "#7a5cff"], [1, "#f2a45f"]], 1, 1);
  const sh = el("filter", { id: "nodeShadow", x: "-60%", y: "-60%", width: "220%", height: "220%" }, defs);
  el("feDropShadow", { dx: 0, dy: 0.8, stdDeviation: 1.1, "flood-color": "#0a0f2e", "flood-opacity": 0.16 }, sh);

  // concentric guides + dot lattice
  [22, 34, 46].forEach((rr, i) => el("circle", { cx, cy, r: rr, fill: "none", stroke: "#0a0f2e", "stroke-opacity": 0.07 + i * 0.01, "stroke-width": 0.25, "stroke-dasharray": i === 1 ? "0.6 1.2" : "none" }, s));
  for (let x = 4; x < W; x += 3.2) for (let y = 4; y < H; y += 3.2) {
    const d = Math.hypot(x - cx, y - cy);
    if (d > 20 && d < 58) el("circle", { cx: f(x), cy: f(y), r: 0.16, fill: "#0a0f2e", opacity: f(0.16 * (1 - (d - 20) / 38)) }, s);
  }
  el("circle", { cx, cy, r: 34, fill: "url(#hubGlow)" }, s);

  const r = rng(42);
  const wires = el("g", {}, s);
  const nodes = el("g", {}, s);
  const labels = el("g", {}, s);
  const RX = 52, RY = 43, hubR = 15.5;

  CLUSTERS.forEach((c, ci) => {
    const pts = c.at.map((a) => [cx + RX * Math.cos(rad(a)), cy + RY * Math.sin(rad(a)), a]);
    pts.forEach(([x, y, a], li) => {
      // 3 generative strands per integration: hub edge → node
      for (let k = 0; k < 3; k++) {
        const ha = a + (r() - 0.5) * 26;
        const [hx, hy] = polar(cx, cy, hubR + 0.4, ha);
        const bend = (r() - 0.5) * 18;
        const [c1x, c1y] = polar(cx, cy, hubR + 12, ha + bend);
        const [c2x, c2y] = [x + (cx - x) * 0.28 + (r() - 0.5) * 6, y + (cy - y) * 0.28 + (r() - 0.5) * 6];
        const d = `M${f(hx)} ${f(hy)} C${f(c1x)} ${f(c1y)} ${f(c2x)} ${f(c2y)} ${f(x)} ${f(y)}`;
        el("path", { d, fill: "none", stroke: "url(#wire)", "stroke-width": k === 0 ? 0.42 : 0.2, opacity: k === 0 ? 0.85 : 0.35 }, wires);
        if (k === 0) {
          el("path", { d, fill: "none", stroke: "#ffffff", "stroke-width": 0.32, class: "flow", opacity: 0.9 }, wires);
          // data packet
          const t = 0.35 + r() * 0.3;
          const bx = bez(hx, c1x, c2x, x, t), by = bez(hy, c1y, c2y, y, t);
          el("circle", { cx: f(bx), cy: f(by), r: 0.7, fill: BRAND[(ci + li) % 6] }, wires);
          el("circle", { cx: f(bx), cy: f(by), r: 1.5, fill: BRAND[(ci + li) % 6], opacity: 0.2, class: "pulse" }, wires);
        }
      }
      const g = el("g", { filter: "url(#nodeShadow)" }, nodes);
      el("circle", { cx: f(x), cy: f(y), r: 6, fill: "#ffffff" }, g);
      el("circle", { cx: f(x), cy: f(y), r: 6, fill: "none", stroke: "#0a0f2e", "stroke-opacity": 0.1, "stroke-width": 0.25 }, nodes);
      const wide = ["sap", "oracle", "indeed", "docusign"].includes(c.logos[li]);
      const iw = wide ? 8.4 : 6, ih = wide ? 4 : 6;
      el("image", { href: L(c.logos[li]), x: f(x - iw / 2), y: f(y - ih / 2), width: iw, height: ih, preserveAspectRatio: "xMidYMid meet" }, nodes);
    });

    const [ax, ay, anchor] = c.label;
    txt(labels, ax, ay, c.name, { "text-anchor": anchor, "font-size": 2.35, "font-weight": 700, fill: "#0a0f2e" });
    txt(labels, ax, ay + 3, `Plugs into stage ${c.stages}`, { "text-anchor": anchor, "font-size": 2.05, "font-weight": 500, fill: "#2340ff" });
  });

  // hub
  el("circle", { cx, cy, r: hubR + 2.6, fill: "none", stroke: "url(#hubRing)", "stroke-width": 0.5, "stroke-dasharray": "0.5 0.9", class: "flow" }, s);
  el("circle", { cx, cy, r: hubR, fill: "#ffffff", filter: "url(#nodeShadow)" }, s);
  el("circle", { cx, cy, r: hubR, fill: "none", stroke: "url(#hubRing)", "stroke-width": 0.9 }, s);
  el("image", { href: L("elevatus-ink"), x: cx - 10.5, y: cy - 2.1, width: 21, height: 2.75 }, s);
  txt(s, cx, cy + 4.3, "AGENTIC AI SYSTEM", { "text-anchor": "middle", "font-size": 1.7, "font-weight": 700, fill: "#2340ff", "letter-spacing": 0.32 });
}
function bez(p0, p1, p2, p3, t) {
  const u = 1 - t;
  return u * u * u * p0 + 3 * u * u * t * p1 + 3 * u * t * t * p2 + t * t * t * p3;
}

/* ------------------------------------------------------------------ */
/* P05 — product micro-visuals                                         */
/* ------------------------------------------------------------------ */
const GLYPHS = {
  rec(s) { // pipeline board
    [0, 9, 18].forEach((x, c) => {
      el("rect", { x, y: 0, width: 8, height: 18, rx: 1.4, fill: "#2340ff", opacity: 0.06 }, s);
      for (let i = 0; i < 3 - c; i++) el("rect", { x: x + 1, y: 1.4 + i * 4.4, width: 6, height: 3.4, rx: 0.8, fill: "#fff", stroke: "#2340ff", "stroke-opacity": 0.35, "stroke-width": 0.3 }, s);
    });
    el("rect", { x: 19, y: 1.4, width: 6, height: 3.4, rx: 0.8, fill: "#2340ff" }, s);
  },
  ssess(s) { // video tile + waveform
    el("rect", { x: 0, y: 0, width: 26, height: 18, rx: 2, fill: "#0a0f2e" }, s);
    el("circle", { cx: 9, cy: 7.4, r: 3, fill: "#4d7cff" }, s);
    el("path", { d: "M8 5.9 L10.6 7.4 L8 8.9Z", fill: "#fff" }, s);
    [3, 5, 2.4, 6, 3.6, 5, 2.2, 4.4, 3, 1.8].forEach((h, i) => el("rect", { x: 14.4 + i * 1.05, y: 7.4 - h / 2, width: 0.55, height: h, rx: 0.27, fill: i < 6 ? "#f2a45f" : "#7a5cff" }, s));
    el("rect", { x: 2, y: 13.6, width: 22, height: 1.2, rx: 0.6, fill: "#fff", opacity: 0.18 }, s);
    el("rect", { x: 2, y: 13.6, width: 13, height: 1.2, rx: 0.6, fill: "#4d7cff" }, s);
  },
  test(s) { // bar scores
    [11, 15, 8, 13, 16].forEach((h, i) => el("rect", { x: 1 + i * 5, y: 17 - h, width: 3.4, height: h, rx: 0.8, fill: BRAND[i], opacity: 0.9 }, s));
    el("path", { d: "M0 17.5 H26", stroke: "#0a0f2e", "stroke-opacity": 0.25, "stroke-width": 0.3 }, s);
  },
  board(s) { // checklist
    [0, 1, 2].forEach((i) => {
      const y = 1.5 + i * 5.6;
      el("rect", { x: 0, y, width: 4, height: 4, rx: 1.1, fill: i < 2 ? "#2340ff" : "#fff", stroke: "#2340ff", "stroke-width": 0.35 }, s);
      if (i < 2) el("path", { d: `M0.9 ${y + 2} l1 1 l1.4 -1.8`, fill: "none", stroke: "#fff", "stroke-width": 0.5, "stroke-linecap": "round" }, s);
      el("rect", { x: 6, y: y + 0.8, width: i === 1 ? 14 : 18, height: 1.1, rx: 0.55, fill: "#0a0f2e", opacity: 0.55 }, s);
      el("rect", { x: 6, y: y + 2.5, width: 10, height: 0.9, rx: 0.45, fill: "#0a0f2e", opacity: 0.18 }, s);
    });
  },
  brand(s) { // career page
    el("rect", { x: 0, y: 0, width: 26, height: 18, rx: 2, fill: "#fff", stroke: "#0a0f2e", "stroke-opacity": 0.2, "stroke-width": 0.3 }, s);
    el("rect", { x: 0, y: 0, width: 26, height: 7, rx: 2, fill: "url(#gb-brand)" }, s);
    el("rect", { x: 0, y: 5, width: 26, height: 2, fill: "url(#gb-brand)" }, s);
    [0, 1, 2].forEach((i) => el("circle", { cx: 1.8 + i * 1.4, cy: 1.6, r: 0.45, fill: "#fff", opacity: 0.8 }, s));
    el("rect", { x: 2.4, y: 3.4, width: 11, height: 1.3, rx: 0.65, fill: "#fff" }, s);
    [0, 1].forEach((i) => {
      el("rect", { x: 2.4 + i * 11, y: 9.4, width: 10, height: 6.6, rx: 1.1, fill: "#2340ff", opacity: 0.07 }, s);
      el("rect", { x: 3.6 + i * 11, y: 10.8, width: 6, height: 1, rx: 0.5, fill: "#0a0f2e", opacity: 0.55 }, s);
      el("rect", { x: 3.6 + i * 11, y: 13, width: 4, height: 1.6, rx: 0.8, fill: "#2340ff" }, s);
    });
  },
  ops(s) { // analytics line
    [4.5, 9, 13.5].forEach((y) => el("path", { d: `M0 ${y} H26`, stroke: "#0a0f2e", "stroke-opacity": 0.1, "stroke-width": 0.25 }, s));
    el("path", { d: "M0 15 C4 14 5 10 8.5 11 S13 6 16 7.5 S21 3 26 2 V18 H0Z", fill: "url(#gb-area)" }, s);
    el("path", { d: "M0 15 C4 14 5 10 8.5 11 S13 6 16 7.5 S21 3 26 2", fill: "none", stroke: "#2340ff", "stroke-width": 0.55 }, s);
    el("circle", { cx: 26 - 0.1, cy: 2, r: 1, fill: "#f2a45f", stroke: "#fff", "stroke-width": 0.4 }, s);
  },
};
function drawGlyph(host, kind) {
  const s = el("svg", { viewBox: "-0.5 -0.5 27 19", xmlns: NS });
  const defs = el("defs", {}, s);
  gradient(defs, "gb-brand", [[0, "#4d7cff"], [0.6, "#7a5cff"], [1, "#f2a45f"]]);
  gradient(defs, "gb-area", [[0, "#4d7cff", 0.3], [1, "#4d7cff", 0]], 0, 1);
  GLYPHS[kind](s);
  host.appendChild(s);
}

/* ------------------------------------------------------------------ */
function init() {
  const q = new URLSearchParams(location.search);
  if (q.has("bleed")) {
    document.body.classList.add("bleed");
    const st = document.createElement("style");
    st.textContent = "@page { size: 448mm 216mm; margin: 0; }";
    document.head.appendChild(st);
  }
  if (q.has("guides")) document.body.classList.add("guides");
  document.querySelectorAll("[data-laurel]").forEach((n) => {
    const [year, ...lines] = n.dataset.laurel.split("|");
    n.appendChild(laurel(year, lines));
    const cap = document.createElement("span");
    cap.innerHTML = lines.join("<br>");
    n.appendChild(cap);
  });
  document.querySelectorAll("[data-seal]").forEach((n) => {
    const [id, top, big, small, ring] = n.dataset.seal.split("|");
    n.prepend(seal(id, top, big, small, ring));
  });
  document.querySelectorAll("[data-glyph]").forEach((n) => drawGlyph(n, n.dataset.glyph));
  drawHero(document.querySelector(".hero"));
  drawRings(document.querySelector(".rings-wrap"));
  drawEcosystem(document.querySelector(".eco-wrap"));

  document.body.dataset.ready = "1";
}
document.fonts.ready.then(init);
