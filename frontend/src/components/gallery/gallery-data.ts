/** Static gallery data: images live in /public/sdart, prompts from the original SD generations. */
export interface GalleryItem {
  src: string;
  /** Short caption shown as image alt and overlay title. */
  title: string;
  /** Full generation prompt, revealed on hover with a copy button. */
  prompt: string;
  /** Sampler and checkpoint used for the generation. */
  sampler: string;
  model: string;
  /** Intrinsic aspect ratio (width/height) to reserve layout space. */
  width: number;
  height: number;
}

export const GALLERY_ITEMS: GalleryItem[] = [
  {
    src: "/sdart/home_1.webp",
    title: "Cyberpunk Interior",
    prompt:
      "sofa, interior, cyberpunk room decor, lots of detailes, futuristic decor, window to the city, illustration, comic style, cyberpunk in the background, night city, insane details, intricate details, hyperdetailed, 4k textures sharp details, ornate, beautiful, atmosphere, vibe, technology, concept art illustration, greg rutowski, volumetric lighting, particles, colorful clothes, by Jean-Baptiste Monge, Gilles Beloeil, Tyler Edlin, Marek Okon, Pixar, album art, comic style, golden ratio, perfect composition, a masterpiece, trending on artstation, oversaturated, epic realistic, hdr, intricate details, rutkowski, intricate, cinematic, detailed",
    sampler: "DPM++ 2M Karras",
    model: "deliberate_v2",
    width: 1920,
    height: 1280,
  },
  {
    src: "/sdart/dark.webp",
    title: "Old House in the Storm",
    prompt:
      "night, b&w photo of old house, post apocalypse, forest, storm weather, wind, rocks, 8k uhd, dslr, soft lighting, high quality, film grain, (lora:epiNoiseoffset_v2:1.5)",
    sampler: "Euler a",
    model: "realisticVisionV20",
    width: 1920,
    height: 1440,
  },
  {
    src: "/sdart/landscape_2.webp",
    title: "Cave Hills",
    prompt:
      "(cave, hills, Dichondra, Floratam, The Peach Tree, Hackberry, white oak, maple tree:0.9), (in style of Adriaen van de Venne:1.1), digital art, trending on artstation, detailed, hdr, cinematic, (lora:lowra_v10:0.7)",
    sampler: "DPM++ 2M Karras",
    model: "dreamlike-photoreal-2.0",
    width: 1920,
    height: 1069,
  },
  {
    src: "/sdart/landscape_1.webp",
    title: "Japanese Garden",
    prompt:
      "cascade of arches, red gate, forest with trees in the background, japan garden, bonsai, sharp details, a medieval village in switzerland, mess jungle in background, ornate, beautiful, atmosphere, vibe, flowers, concept art illustration, greg rutowski, volumetric lighting, sunbeams, particles, colorful clothes, by Jean-Baptiste Monge, Gilles Beloeil, Tyler Edlin, Marek Okon, Pixar, album art, comic style, golden ratio, perfect composition, a masterpiece, trending on artstation, oversaturated, epic realistic, hdr, intricate details, rutkowski, intricate, cinematic, detailed",
    sampler: "DPM++ 2M Karras",
    model: "realisticVisionV20",
    width: 1920,
    height: 1280,
  },
];

