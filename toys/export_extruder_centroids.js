(function () {
  function centroidOfTetra(t) {
    if (!t) return null;

    if (Array.isArray(t.vertices) && t.vertices.length >= 4) {
      const vs = t.vertices.slice(0, 4).map((v) => ({
        x: Number(v.x ?? v[0] ?? 0),
        y: Number(v.y ?? v[1] ?? 0),
        z: Number(v.z ?? v[2] ?? 0),
      }));
      return {
        x: (vs[0].x + vs[1].x + vs[2].x + vs[3].x) / 4,
        y: (vs[0].y + vs[1].y + vs[2].y + vs[3].y) / 4,
        z: (vs[0].z + vs[1].z + vs[2].z + vs[3].z) / 4,
      };
    }

    if (t.centroid && typeof t.centroid === "object") {
      return {
        x: Number(t.centroid.x ?? 0),
        y: Number(t.centroid.y ?? 0),
        z: Number(t.centroid.z ?? 0),
      };
    }

    if ("x" in t && "y" in t && "z" in t) {
      return {
        x: Number(t.x),
        y: Number(t.y),
        z: Number(t.z),
      };
    }

    return null;
  }

  function probeObject(obj, objName, hits) {
    if (!obj || typeof obj !== "object") return;
    for (const [key, value] of Object.entries(obj)) {
      if (!Array.isArray(value) || value.length === 0) continue;
      const sample = value[0];
      if (!sample || typeof sample !== "object") continue;

      const looksLikeTetra =
        Array.isArray(sample.vertices) ||
        !!sample.centroid ||
        ("x" in sample && "y" in sample && "z" in sample);

      if (looksLikeTetra) {
        hits.push({
          owner: objName,
          key,
          size: value.length,
          value,
        });
      }
    }
  }

  const hits = [];
  probeObject(window, "window", hits);
  probeObject(window.__EXTRUDER__, "window.__EXTRUDER__", hits);
  probeObject(window.extruderApp, "window.extruderApp", hits);
  probeObject(window.app, "window.app", hits);
  probeObject(window.state, "window.state", hits);

  if (!hits.length) {
    console.log("No candidate tetra arrays found.");
    console.log("Try inspecting window, window.app, window.state, or your lab boot globals.");
    return;
  }

  hits.sort((a, b) => b.size - a.size);
  const best = hits[0];

  const pts = best.value.map(centroidOfTetra).filter(Boolean);

  console.log("Best source:", `${best.owner}.${best.key}`, "size:", best.size);
  console.log("Extracted centroids:", pts.length);

  const blob = new Blob([JSON.stringify(pts, null, 2)], {
    type: "application/json",
  });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "centroids.json";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);

  window.__lastExportedCentroids = pts;
  console.log("Saved centroids.json");
})();
