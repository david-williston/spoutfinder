/* SpoutFinder runner: the program's method, run live over the traced prototype pockets.
   Parameters are fixed on purpose. */
(function () {
  var root = document.getElementById("runner");
  if (!root) return;
  var $ = function (id) { return document.getElementById(id); };
  var R = 9, PITCH = 23, INC = 23, ACC = 0.02, X0 = 30, Y0 = 30;
  var cv = $("rn-canvas"), ctx = cv.getContext("2d");
  var data, pockets, W, H, dpr = Math.min(window.devicePixelRatio || 1, 2);
  var state, gen, timer = 0, running = false;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- geometry ---------- */
  function inside(poly, x, y) {
    var c = false;
    for (var i = 0, j = poly.length - 1; i < poly.length; j = i++) {
      var a = poly[i], b = poly[j];
      if ((a[1] > y) !== (b[1] > y) && x < (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]) + a[0]) c = !c;
    }
    return c;
  }
  /* sample points spread evenly over a spout circle: 6k points on ring k */
  var DISC = (function () {
    var pts = [];
    for (var k = 1; k <= 8; k++) for (var n = 0; n < 6 * k; n++) {
      var a = 2 * Math.PI * n / (6 * k) + k, r = R * (k - 0.5) / 8;
      pts.push([r * Math.cos(a), r * Math.sin(a)]);
    }
    return pts;
  })();
  function overlap(poly, cx, cy) {   /* fraction of the circle inside the pocket (SOLINT + SOLAREA) */
    var n = 0;
    for (var i = 0; i < DISC.length; i++) if (inside(poly, cx + DISC[i][0], cy + DISC[i][1])) n++;
    return n / DISC.length;
  }
  function bbox(poly) {
    var x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    poly.forEach(function (p) { x0 = Math.min(x0, p[0]); y0 = Math.min(y0, p[1]); x1 = Math.max(x1, p[0]); y1 = Math.max(y1, p[1]); });
    return { x0: x0, y0: y0, x1: x1, y1: y1 };
  }
  function pathOf(poly) {
    var p = new Path2D(); poly.forEach(function (q, i) { i ? p.lineTo(q[0], q[1]) : p.moveTo(q[0], q[1]); }); p.closePath(); return p;
  }

  /* ---------- drawing ---------- */
  var base, marks, mctx;
  function offscreen() { var c = document.createElement("canvas"); c.width = W * dpr; c.height = H * dpr; var x = c.getContext("2d"); x.scale(dpr, dpr); return [c, x]; }
  function drawBase() {
    var b = offscreen(); base = b[0]; var x = b[1];
    x.fillStyle = "#000"; x.fillRect(0, 0, W, H);
    x.fillStyle = "#303030";
    for (var gx = 20; gx < W; gx += 20) for (var gy = 20; gy < H - 30; gy += 20) x.fillRect(gx, gy, 1, 1);
    x.strokeStyle = "#f0f0f0"; x.lineWidth = 1.8;
    data.outline.forEach(function (p) { x.stroke(pathOf(p)); });
    pockets.forEach(function (k) { x.strokeStyle = k.color; x.lineWidth = 1.5; x.stroke(k.path); });
  }
  function resetMarks() { var m = offscreen(); marks = m[0]; mctx = m[1]; }
  function frame(active) {
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.drawImage(base, 0, 0); ctx.drawImage(marks, 0, 0);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    if (state.cur) {   /* highlight the pocket being worked on */
      ctx.strokeStyle = "#fff"; ctx.lineWidth = 3; ctx.stroke(state.cur.path);
    }
    if (active) {      /* the circle under test: overlap region filled */
      ctx.save(); ctx.clip(active.p.path);
      ctx.fillStyle = "rgba(245,228,0,.45)"; ctx.beginPath(); ctx.arc(active.x, active.y, R, 0, 7); ctx.fill(); ctx.restore();
      ctx.strokeStyle = "#f5e400"; ctx.lineWidth = 1.6; ctx.beginPath(); ctx.arc(active.x, active.y, R, 0, 7); ctx.stroke();
    }
  }
  function markResult(x, y, frac, ok) {
    mctx.lineWidth = 1.4;
    if (ok) {
      mctx.strokeStyle = "#00e000"; mctx.beginPath(); mctx.arc(x, y, R, 0, 7); mctx.stroke();
      mctx.beginPath(); mctx.moveTo(x - 3, y); mctx.lineTo(x + 3, y); mctx.moveTo(x, y - 3); mctx.lineTo(x, y + 3); mctx.lineWidth = 1; mctx.stroke();
    } else if (frac > 0) {
      mctx.strokeStyle = "#ff3030"; mctx.setLineDash([3, 3]); mctx.lineWidth = 1; mctx.beginPath(); mctx.arc(x, y, R, 0, 7); mctx.stroke(); mctx.setLineDash([]);
    }
  }

  /* ---------- the algorithm, as a generator: one yield per spout position ---------- */
  function* program() {
    var order = pockets.slice().sort(function (a, b) { return a.cx - b.cx; });
    for (var pi = 0; pi < order.length; pi++) {
      var p = order[pi]; p.n = pi + 1;
      state.cur = p; state.pocketNo = pi + 1;
      var b = p.box, xs = [], total = 0;
      /* the grid (NEXTROW / NEXTSPOUT), gated by the bounding box (SEEIFLOCAL) */
      for (var gx = X0; gx < W; gx += INC) for (var gy = Y0; gy < H - 30; gy += PITCH) {
        total++;
        if (gx > b.x0 - R && gx < b.x1 + R && gy > b.y0 - R && gy < b.y1 + R) xs.push([gx, gy]);
      }
      state.skipped += total - xs.length;
      log("(pocketsurf)   pocket " + (pi + 1) + " of " + order.length + "  [" + p.layer + "]");
      log("(seeiflocal)   " + xs.length + " of " + total + " positions fall inside its bounding box");
      yield { pocket: p };
      for (var i = 0; i < xs.length; i++) {
        var x = xs[i][0], y = xs[i][1];
        var frac = overlap(p.poly, x, y);               /* DOINT: circle ∩ surface; SOLAREA */
        var ok = frac > 0 && (1 - frac) < ACC;          /* CHECK: shortfall under the tolerance */
        state.tested++;
        if (ok) { state.valid++; p.found++; } else if (frac > 0) state.bad++;
        var gi = Math.round((x - X0) / INC), gj = Math.round((y - Y0) / PITCH);
        if (ok) state.grid[gi][gj] = p.n;
        markResult(x, y, frac, ok);
        state.line = "(doint) circle at (" + Math.round(x) + "," + Math.round(y) + ")   (check) overlap " + (frac * 100).toFixed(1) +
          "%  shortfall " + ((1 - frac) * 100).toFixed(1) + "%  " + (frac === 0 ? "-> OUTSIDE, erased" : ok ? "< 2.0% -> VALID" : ">= 2.0% -> rejected");
        yield { test: { p: p, x: x, y: y, frac: frac } };
      }
      log("(buildlist)    pocket " + (pi + 1) + ": " + p.found + " valid location" + (p.found === 1 ? "" : "s"));
      log("(combine)      merged into the running list");
    }
    state.cur = null;
  }

  /* ---------- UI plumbing ---------- */
  var logEl = $("rn-log");
  function log(t) { state.log.push(t); logEl.textContent = state.log.slice(-14).join("\n"); logEl.scrollTop = logEl.scrollHeight; }
  function stats() {
    $("rn-pocket").textContent = state.pocketNo + " / " + pockets.length;
    $("rn-skip").textContent = state.skipped; $("rn-tested").textContent = state.tested;
    $("rn-valid").textContent = state.valid; $("rn-bad").textContent = state.bad;
  }
  function init() {
    state = { cur: null, pocketNo: 0, skipped: 0, tested: 0, valid: 0, bad: 0, log: [], line: "", grid: [] };
    var cols = Math.ceil((W - X0) / INC), rows = Math.ceil((H - 30 - Y0) / PITCH);
    for (var i = 0; i < cols + 1; i++) { state.grid.push([]); for (var j = 0; j < rows + 1; j++) state.grid[i].push(0); }
    pockets.forEach(function (p) { p.found = 0; });
    resetMarks(); gen = program();
    logEl.textContent = "Command: GO\n(setdefaults)  spout diameter 18, pitch 23, increment 23, accuracy 2%"; state.log = ["Command: GO", "(setdefaults)  spout diameter 18, pitch 23, increment 23, accuracy 2%"];
    $("rn-sdf").hidden = true; $("rn-sdf").textContent = "";
    $("rn-status").textContent = "Press RUN to start the program.";
    stats(); frame(null); setButtons("idle");
  }
  function setButtons(mode) {
    $("rn-run").disabled = mode !== "idle" && mode !== "paused"; $("rn-run").textContent = mode === "paused" ? "RESUME" : "RUN";
    $("rn-pause").disabled = mode !== "running"; $("rn-reset").disabled = mode === "idle";
  }
  function finish() {
    running = false; cancelAnimationFrame(timer);
    frame(null); stats();
    log("(output)       writing OUTPUT.SDF ...  Program Complete");
    $("rn-status").textContent = "Program complete: " + state.valid + " valid spout locations in " + pockets.length + " pockets.";
    renderSdf(); setButtons("done");
  }
  function renderSdf() {
    var lines = ["SpoutFinder V0.1 beta DATA FILE", ""], palette = {};
    pockets.forEach(function (p) { palette[p.n] = p.color; });
    var html = ["SpoutFinder V0.1 beta DATA FILE", ""];
    for (var i = 0; i < state.grid.length; i++) {
      var row = state.grid[i], cells = [];
      for (var j = 0; j < row.length; j++) {
        var v = row[j];
        cells.push(v ? '<span style="color:' + palette[v] + '">' + v.toString(36) + "</span>" : '<span class="z">0</span>');
      }
      html.push(cells.join(" "));
    }
    html.push("", "End of File");
    var el = $("rn-sdf"); el.innerHTML = html.join("\n"); el.hidden = false;
  }
  /* Pace: 6 visible tests per second (ten times slower than the first version). Positions with no
     overlap at all leave no mark, so they are processed without waiting. */
  var RATE = 6, last = 0, budget = 0, curTest = null;
  function tick(now) {
    if (!running) return;
    budget += Math.min(100, now - (last || now)) * RATE / 1000; last = now;
    var shown = null;
    while (budget >= 1) {
      var r = gen.next();
      if (r.done) { finish(); return; }
      var cost = r.value.pocket ? 4 : (r.value.test && r.value.test.frac === 0 ? 0 : 1);
      budget -= cost;
      if (cost && r.value.test) shown = r.value.test;
    }
    if (shown) { curTest = shown; $("rn-status").textContent = state.line; }
    frame(curTest); stats();
    timer = requestAnimationFrame(tick);
  }
  function runAll() { var r; while (!(r = gen.next()).done) {} finish(); }
  $("rn-run").addEventListener("click", function () {
    running = true; setButtons("running");
    if (reduce) return runAll();
    last = 0; curTest = null; timer = requestAnimationFrame(tick);
  });
  $("rn-pause").addEventListener("click", function () { running = false; cancelAnimationFrame(timer); setButtons("paused"); });
  $("rn-reset").addEventListener("click", function () { running = false; cancelAnimationFrame(timer); init(); });

  fetch(root.getAttribute("data-src")).then(function (r) { return r.json(); }).then(function (d) {
    data = d; W = d.w; H = d.h;
    cv.width = W * dpr; cv.height = H * dpr; cv.style.aspectRatio = W + " / " + H;
    pockets = [];
    d.layers.forEach(function (l) { l.polys.forEach(function (poly) {
      var b = bbox(poly), c = poly.reduce(function (s, q) { return s + q[0]; }, 0) / poly.length;
      pockets.push({ layer: l.name, color: l.color, poly: poly, path: pathOf(poly), box: b, cx: c, n: 0, found: 0 });
    }); });
    drawBase(); init();
  });
})();
