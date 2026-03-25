export const state = {
  width: 900,
  height: 560,
  origin: { x: 450, y: 300 },
  T: 0,

  rayLength: 170,
  iRadius: 72,
  zLength: 170,
  rLength: 190,

  tCount: 4,
  tSpacing: 70,

  playing: false,
  timer: null,
  fps: 30,
  step: 1,

  colors: {
    bg: "#000000",
    frame: "#555",
    text: "#eaeaea",
    x: "#58b8ff",
    y: "#84c98a",
    z: "#e8a0a0",
    i: "#f2cc5c",
    t: "#d8d8d8",
    shell: "#6d6d6d",
    tri1: "#58b8ff",
    tri2: "#84c98a",
    tri3: "#f2cc5c",
    tri4: "#b0b0b0",
    r: "#ffffff",
  }
};
