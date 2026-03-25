export function makePetersenGraph() {
  const N = 10;

  const edges = [
    [0, 1], [1, 2], [2, 3], [3, 4], [4, 0],
    [0, 5], [1, 6], [2, 7], [3, 8], [4, 9],
    [5, 7], [7, 9], [9, 6], [6, 8], [8, 5],
  ];

  const cx = window.innerWidth / 2;
  const cy = window.innerHeight / 2;

  const nodes = Array.from({ length: N }, (_, i) => {
    const a = (i / N) * Math.PI * 2;
    const r = i < 5 ? 180 : 90;

    return {
      id: i,
      x: cx + Math.cos(a) * r,
      y: cy + Math.sin(a) * r,
      vx: 0,
      vy: 0,
      fx: 0,
      fy: 0,
    };
  });

  return { nodes, edges };
}
