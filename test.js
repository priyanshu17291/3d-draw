const loader = new GLTFLoader();
loader.load('sphere.gltf', (gltf) => scene.add(gltf.scene));
