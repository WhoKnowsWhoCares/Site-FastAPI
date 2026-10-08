/** Static Trade4Me (trading automation) content. Images served from /public/trade4me (WebP). */

export const STACK = [
  "Python",
  "LightGBM",
  "Optuna",
  "FastAPI",
  "Docker",
  "Telegram Bot API",
] as const;

export const OVERVIEW = {
  headline: "Trade for me.",
  blurb:
    "Global macro trends provide invaluable insights into the potential future. My objective is to diligently monitor these trends and interpret them with utmost accuracy. The purpose of this project is to develop practical automations that facilitate efficient market observation and enable prompt decision-making — with machine learning for automatic trade execution as the long-term goal.",
};

export const LEVELS = [
  {
    title: "Global Macro level",
    text: "Macroeconomic factors and companies' quarterly reports to predict trends on a high level and for the long term.",
  },
  {
    title: "Company level",
    text: "Open/close statistics on the market for technical analysis and mid-term horizon prediction.",
  },
  {
    title: "Daily-trading level",
    text: "5-minute trading data and news for intraday trading.",
  },
] as const;

export const NEWS_PARSER = {
  title: "News Parser",
  status: "Being reworked — coming back soon",
  text: "Daily news for intraday trading — collected info for fast decision-making. From various sources it gathers text info, stores it, then applies ML-based summarization and sentiment analysis. Based on user preferences it sorts all news and sends only the top of the list as a Telegram notification.",
  diagram: {
    dark: { src: "/trade4me/newsparser-dark.webp", width: 1090, height: 515 },
    light: { src: "/trade4me/newsparser-light.webp", width: 1090, height: 515 },
    caption:
      "News Parser architecture: sources → parsing & storage → ML summarization and sentiment → ranking → Telegram notifications.",
  },
};
