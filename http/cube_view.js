import React from "https://esm.sh/react@18.3.1";
import { createRoot } from "https://esm.sh/react-dom@18.3.1/client";
import * as THREE from "https://esm.sh/three@0.161.0";

const h = React.createElement;
let cubeRoot = null;
let teardownThree = null;

function CubeViewApp() {
  return h("div", { className: "cube-react-shell" }, [
    h("div", { className: "cube-react-head", key: "head" }, [
      h("h2", { key: "title" }, "Cube View"),
      h("p", { key: "copy" }, "Drag on the canvas to rotate the cube."),
    ]),
    h("div", {
      className: "cube-canvas-shell",
      id: "cube-canvas-shell",
      key: "canvas",
    }),
  ]);
}

function setupThreeCanvas(host) {
  if (!host) return () => {};

  host.innerHTML = "";

  const width = host.clientWidth || 800;
  const height = host.clientHeight || 520;

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x11161d);

  const camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 100);
  camera.position.set(3.2, 2.6, 3.8);
  camera.lookAt(0, 0, 0);

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setSize(width, height);
  host.appendChild(renderer.domElement);

  const ambient = new THREE.AmbientLight(0xffffff, 1.2);
  scene.add(ambient);

  const dir1 = new THREE.DirectionalLight(0xffffff, 1.2);
  dir1.position.set(3, 4, 5);
  scene.add(dir1);

  const dir2 = new THREE.DirectionalLight(0xffffff, 0.45);
  dir2.position.set(-3, -2, -4);
  scene.add(dir2);

  const floorGeo = new THREE.PlaneGeometry(12, 12);
  const floorMat = new THREE.MeshStandardMaterial({
    color: 0x1a2230,
    roughness: 0.92,
    metalness: 0.05,
  });
  const floor = new THREE.Mesh(floorGeo, floorMat);
  floor.rotation.x = -Math.PI / 2;
  floor.position.y = -1.8;
  scene.add(floor);

  const cubeGeo = new THREE.BoxGeometry(1.6, 1.6, 1.6);
  const cubeMat = new THREE.MeshStandardMaterial({
    color: 0x4da3ff,
    roughness: 0.3,
    metalness: 0.2,
  });
  const cube = new THREE.Mesh(cubeGeo, cubeMat);
  cube.rotation.set(0.45, 0.65, 0);
  scene.add(cube);

  let isDragging = false;

  function onPointerDown() {
    isDragging = true;
    cube.material.color.set(0x8ec5ff);
  }

  function onPointerUp() {
    isDragging = false;
    cube.material.color.set(0x4da3ff);
  }

  function onPointerLeave() {
    isDragging = false;
    cube.material.color.set(0x4da3ff);
  }

  function onPointerMove(event) {
    if (!isDragging) return;
    cube.rotation.x += (event.movementY || 0) * 0.01;
    cube.rotation.y += (event.movementX || 0) * 0.01;
  }

  function onResize() {
    const newWidth = host.clientWidth || width;
    const newHeight = host.clientHeight || height;
    camera.aspect = newWidth / newHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(newWidth, newHeight);
  }

  renderer.domElement.addEventListener("pointerdown", onPointerDown);
  renderer.domElement.addEventListener("pointerleave", onPointerLeave);
  renderer.domElement.addEventListener("pointermove", onPointerMove);
  window.addEventListener("pointerup", onPointerUp);
  window.addEventListener("resize", onResize);

  let frameId = null;

  function animate() {
    frameId = requestAnimationFrame(animate);
    renderer.render(scene, camera);
  }

  animate();

  return () => {
    if (frameId) cancelAnimationFrame(frameId);

    renderer.domElement.removeEventListener("pointerdown", onPointerDown);
    renderer.domElement.removeEventListener("pointerleave", onPointerLeave);
    renderer.domElement.removeEventListener("pointermove", onPointerMove);
    window.removeEventListener("pointerup", onPointerUp);
    window.removeEventListener("resize", onResize);

    cubeGeo.dispose();
    cubeMat.dispose();
    floorGeo.dispose();
    floorMat.dispose();
    renderer.dispose();
    host.innerHTML = "";
  };
}

export function mountCubeView(target) {
  if (!target) return;

  if (!cubeRoot) {
    cubeRoot = createRoot(target);
  }

  cubeRoot.render(h(CubeViewApp));

  const host = document.getElementById("cube-canvas-shell");
  teardownThree = setupThreeCanvas(host);
}

export function unmountCubeView() {
  if (teardownThree) {
    teardownThree();
    teardownThree = null;
  }

  if (cubeRoot) {
    cubeRoot.unmount();
    cubeRoot = null;
  }
}
