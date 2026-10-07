/** Static About Me content, sourced from CV v2. */

export interface ExperienceEntry {
  period: string;
  org: string;
  role: string;
  points: string[];
}

export const SUMMARY = {
  headline: "Senior Data Scientist",
  blurb:
    "I own ML products end-to-end — from architecture and modeling to production, monitoring and business impact. Fintech, big tech and retail background with a strong academic foundation in mathematics and economics.",
  stats: [
    { label: "Data Science & Analytics", years: "5+ years" },
    { label: "Software Engineering", years: "5 years" },
  ],
};

export const EDUCATION = [
  {
    degree: "MA in Economics",
    place: "European University at St. Petersburg, Dept. of Economics",
    period: "2015–2017",
    note: "Full Fee Waiver Scholarship",
  },
  {
    degree: "Specialist in Mathematics & Computer Science",
    place: "St. Petersburg State University, Dept. of Applied Mathematics",
    period: "2008–2014",
  },
];

export const SKILLS: { group: string; items: string[] }[] = [
  {
    group: "ML / DS",
    items: [
      "Python (PyTorch, scikit-learn, pandas, LightGBM, Optuna)",
      "Forecasting",
      "NLP",
      "LLM integration",
      "A/B testing",
    ],
  },
  {
    group: "Data & Engineering",
    items: [
      "SQL (PostgreSQL, ClickHouse, YQL)",
      "YTsaurus",
      "Workflow orchestration",
      "FastAPI",
      "Docker",
      "Git",
      "Linux",
    ],
  },
  {
    group: "Languages",
    items: ["English — advanced", "Russian — native"],
  },
];

export const INTERESTS = [
  "Analytics and Machine Learning",
  "Global macroeconomics and stock trading",
  "Smart home automation (Home Assistant)",
  "AI art and photo editing with neural networks",
];

export const EXPERIENCE: ExperienceEntry[] = [
  {
    period: "2024–2026",
    org: "Yandex — FinTech, Payment Analytics",
    role: "Analyst-Developer (Data Scientist)",
    points: [
      "Owned the payment incident prediction system for Yandex Bank (100k+ DAU) end-to-end; prevents faulty transaction traffic estimated at ~700M RUB/year",
      "Re-architected the anomaly predictor (Python, Arcadia, Nirvana, YTsaurus): from a fragile single-maintainer setup to a testable, versioned product with CI and monitoring",
      "Cut scoring-to-alert time from ~30 to ~15 min; recall on conversion incidents raised to ~90% via a backtesting framework",
      "Introduced ML and LLMs into production: LLM-based validation of error-code mappings with human-in-the-loop review",
      "Built a Sankey dashboard for cascading payments — managers resolve payment cases without analysts",
    ],
  },
  {
    period: "2022–2024",
    org: "Independent Projects & Trading",
    role: "Founder / Trader",
    points: [
      "ML startup: sports outcome prediction — feature pipeline + LightGBM tuned with Optuna; first production model delivered +3% margin",
      "Personalized news service: Telegram/RSS/web aggregation with LLM summarization and relevance ranking",
      "Smart home automation platform on Raspberry Pi / Home Assistant",
      "Independent securities trading",
    ],
  },
  {
    period: "2017–2022",
    org: "SAS Institute — CI & Retail Department",
    role: "Analytics Consultant / Data Scientist",
    points: [
      "ML implementation, analytical data marts, A/B testing and business consulting for big tech companies (Sber, X5, McDonald's, Mondelez)",
      "Banking, Internal Fraud: fraud detection rules aligned with the bank's business processes",
      "Retail, Promo Optimization: sales analysis, product segmentation, elasticity estimation",
      "Retail, Demand Forecasting: time-series models (ARIMA, ETS) and ML ensembles (RandomForest, GradientBoosting) at scale",
      "Banking, Customer Intelligence: segmentation, NLP categorization of payment descriptions, propensity-to-buy models",
    ],
  },
  {
    period: "2010–2015",
    org: "UbiqMobile / SPSU R&D startup",
    role: "Software Engineer",
    points: [
      "Core backend services in .NET for a mobile services platform; Java client on a custom protocol optimized for low-bandwidth connections",
      "R&D project awarded a Microsoft Seed Fund grant; grew into UbiqMobile, an innovation platform for mobile services",
    ],
  },
];

export const ACHIEVEMENTS = [
  { year: "2013", text: "CRDF grant for product extension" },
  {
    year: "2015",
    text: "Full Fee Waiver Scholarship, European University at St. Petersburg",
  },
];

export const CONTACTS = {
  email: "as.frantsev@gmail.com",
  linkedin: "https://linkedin.com/in/asfrantsev",
  telegram: "https://t.me/as_frantsev",
  github: "https://github.com/WhoKnowsWhoCares",
};

/** Portrait carousel images, served from /public/me. */
export const PORTRAITS = [
  { src: "/me/portrait-1.webp", alt: "Alexander Frantsev — portrait 1" },
  { src: "/me/portrait-3.webp", alt: "Alexander Frantsev — portrait 2" },
];

export const CV_DOWNLOAD_URL = "/cv.pdf";
