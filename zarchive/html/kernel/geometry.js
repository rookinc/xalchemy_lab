export function polarFrom(origin, angleDeg, length) {
  const a = (angleDeg - 90) * Math.PI / 180;
  return {
    x: origin.x + Math.cos(a) * length,
    y: origin.y + Math.sin(a) * length,
  };
}

export function dist(a, b) {
  return Math.hypot(b.x - a.x, b.y - a.y);
}
