import { tetraEdgePairs } from "./d4_spec.js";

function armColorFromChirality(chirality, alpha = 0.82) {
  if (chirality === "left") {
    return `rgba(255, 196, 230, ${alpha})`;
  }
  return `rgba(186, 239, 255, ${alpha})`;
}

function compositeColor(alpha = 0.45) {
  return `rgba(208, 248, 219, ${alpha})`;
}

function faceKey(vertexIds) {
  return [...vertexIds].sort((a, b) => a - b).join("|");
}

function tetraFaces(vertexIds) {
  return [
    { label: 1, ids: [vertexIds[1], vertexIds[2], vertexIds[3]] },
    { label: 2, ids: [vertexIds[0], vertexIds[2], vertexIds[3]] },
    { label: 3, ids: [vertexIds[0], vertexIds[1], vertexIds[3]] },
    { label: 4, ids: [vertexIds[0], vertexIds[1], vertexIds[2]] },
  ];
}

export function renderPrimeScene(ctx, scene, project3D, options = {}) {
  const {
    showFaces = true,
    showLabels = false,
    highlightActive = true,
  } = options;

  if (!scene || !scene.tetrahedra || !scene.tetrahedra.length) return;

  const projectedVertices = new Map();
  for (const v of scene.vertices) {
    projectedVertices.set(v.id, project3D(v));
  }

  const openFaceKeys = new Set(scene.openFaces.map((f) => f.faceKey));

  const tetraItems = scene.tetrahedra.map((tetra) => {
    const pts = tetra.vertexIds.map((id) => projectedVertices.get(id));
    const depth = pts.reduce((sum, p) => sum + p.depth, 0) / pts.length;
    return { tetra, depth };
  });

  tetraItems.sort((a, b) => b.depth - a.depth);

  ctx.save();

  for (const item of tetraItems) {
    const tetra = item.tetra;
    const isActive = highlightActive && tetra.id === scene.activeTetraId;

    if (showFaces) {
      const faces = tetraFaces(tetra.vertexIds).map((face) => {
        const pts = face.ids.map((id) => projectedVertices.get(id));
        const depth = pts.reduce((sum, p) => sum + p.depth, 0) / pts.length;
        return {
          label: face.label,
          ids: face.ids,
          pts,
          depth,
          key: faceKey(face.ids),
        };
      });

      faces.sort((a, b) => b.depth - a.depth);

      for (const face of faces) {
        const isComposite = face.label === 4;
        const isOpen = !isComposite && openFaceKeys.has(face.key);
        const isActiveFace = isActive && face.label === scene.activeFaceLabel;

        ctx.beginPath();
        ctx.moveTo(face.pts[0].x, face.pts[0].y);
        ctx.lineTo(face.pts[1].x, face.pts[1].y);
        ctx.lineTo(face.pts[2].x, face.pts[2].y);
        ctx.closePath();

        if (isComposite) {
          ctx.fillStyle = compositeColor(isActiveFace ? 0.22 : 0.14);
          ctx.strokeStyle = compositeColor(isActiveFace ? 0.95 : 0.62);
          ctx.lineWidth = isActiveFace ? 2.0 : 1.0;
        } else if (isActiveFace) {
          ctx.fillStyle = armColorFromChirality(tetra.chirality, 0.20);
          ctx.strokeStyle = armColorFromChirality(tetra.chirality, 1.0);
          ctx.lineWidth = 2.2;
        } else if (isOpen) {
          ctx.fillStyle = armColorFromChirality(tetra.chirality, 0.12);
          ctx.strokeStyle = armColorFromChirality(tetra.chirality, 0.86);
          ctx.lineWidth = 1.2;
        } else {
          ctx.fillStyle = armColorFromChirality(tetra.chirality, 0.08);
          ctx.strokeStyle = armColorFromChirality(tetra.chirality, 0.52);
          ctx.lineWidth = 1.0;
        }

        ctx.fill();
        ctx.stroke();

        if (showLabels && isComposite) {
          const cx = (face.pts[0].x + face.pts[1].x + face.pts[2].x) / 3;
          const cy = (face.pts[0].y + face.pts[1].y + face.pts[2].y) / 3;
          ctx.fillStyle = "rgba(232,240,248,0.85)";
          ctx.font = "11px sans-serif";
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          ctx.fillText(`T${tetra.id}`, cx, cy);
        }
      }
    } else {
      for (const [a, b] of tetraEdgePairs(tetra.vertexIds)) {
        const pa = projectedVertices.get(a);
        const pb = projectedVertices.get(b);
        ctx.beginPath();
        ctx.moveTo(pa.x, pa.y);
        ctx.lineTo(pb.x, pb.y);
        ctx.strokeStyle = armColorFromChirality(
          tetra.chirality,
          isActive ? 1.0 : 0.78
        );
        ctx.lineWidth = isActive ? 2.0 : 1.0;
        ctx.stroke();
      }
    }
  }

  ctx.restore();
}
