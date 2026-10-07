/** Static iHome (smart home) content. Images served from /public/ihome (WebP). */

export interface MediaItem {
  src: string;
  alt: string;
  caption: string;
  width: number;
  height: number;
}

export const STACK = [
  "Raspberry Pi 4",
  "Home Assistant",
  "Zigbee / WiFi / ESPHome",
  "Telegram bot",
  "Yandex Alice",
  "Node-RED",
] as const;

export const OVERVIEW = {
  headline: "Smart home on Home Assistant",
  blurb:
    "One of my interests is automating daily routines. My home runs on a Raspberry Pi 4 with Home Assistant in the local network — sensors, automations and dashboards, with no cloud dependency. A battery backup keeps it running for 24 hours even without power.",
  // stats: [
  //   { label: "Server", value: "Raspberry Pi 4" },
  //   { label: "Voice assistants", value: "Alice ×2 (kitchen + living room)" },
  //   { label: "Control", value: "Dashboard, Telegram bot, voice" },
  //   { label: "Power backup", value: "24h on batteries" },
  // ],
};

export const MORNING_ROUTINE = [
  { time: "Alarm", text: "Phone morning alarm triggers the chain" },
  { time: "Step 1", text: "Curtains open" },
  { time: "Step 2", text: "Day schedule from Google Calendar" },
  { time: "Step 3", text: "Weather forecast" },
  { time: "Step 4", text: "Daily news" },
  { time: "Step 5", text: "Podcasts start" },
] as const;

/** Theme-aware architecture diagram (dark/light variants). */
export const ARCHITECTURE = {
  dark: {
    src: "/ihome/architecture-dark.webp",
    width: 892,
    height: 312,
  },
  light: {
    src: "/ihome/architecture-light.webp",
    width: 892,
    height: 312,
  },
  caption:
    "Architecture: Raspberry Pi 4 in the local network, sensors connected via Zigbee, WiFi and ESPHome; control via dashboard, Telegram bot and Yandex Alice.",
};

/** Interface & infrastructure gallery — click to open fullscreen. */
export const MEDIA_ITEMS: MediaItem[] = [
  {
    src: "/ihome/dashboard.webp",
    alt: "Home Assistant dashboard with sensor readings, air quality, light, calendar and music",
    caption: "Main dashboard — sensors, air quality, lights, calendar, music",
    width: 1920,
    height: 1080,
  },
  {
    src: "/ihome/monitoring.webp",
    alt: "System monitoring: load graphs, backups and uptime",
    caption: "System monitoring — load, backups, uptime",
    width: 1920,
    height: 1080,
  },
  {
    src: "/ihome/tile-phone.webp",
    alt: "Home Assistant companion app on a phone — dashboard on the go",
    caption: "Companion app — the same dashboard on a phone",
    width: 1366,
    height: 768,
  },
  {
    src: "/ihome/tile-raspi4.webp",
    alt: "Raspberry Pi 4 single-board computer running the smart home server",
    caption: "Raspberry Pi 4 — the heart of the system",
    width: 1366,
    height: 768,
  },
];
